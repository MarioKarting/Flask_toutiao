import time

from flask import current_app, g
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser

from cache import article as cache_article  # 起别名

from rpc import reco_pb2, reco_pb2_grpc
from toutiao.resources.news import constants
from utils import parser


class ArticleListResource(Resource):
    """
    获取推荐文章列表数据
    """

    def _feed_articles(self, channel_id, timestamp, feed_count):
        """
        获取推荐文章
        :param channel_id: 频道id
        :param feed_count: 推荐数量
        :param timestamp: 时间戳
        :return: [{article_id, trace_params}, ...], timestamp
        """
        #构建辅助调用工具
        stub = reco_pb2_grpc.UserRecommendStub(current_app.rpc_reco)

        #进行rpc调用
        user_request = reco_pb2.UserRequest()
        # userid用字符串的原因，有匿名用户，不登录的
        user_request.user_id = g.user_id or 'annoy'
        user_request.channel_id = channel_id  # 频道
        user_request.article_num = feed_count  # 文章数量
        user_request.time_stamp = round(time.time() * 1000)  # 时间戳

        #feeds = user_request.recommend
        #pre_timwstamp =  user_request.time_stamp
        ret = stub.user_recommend(user_request)
        # ret->ArticleResponse 对象
        return ret.recommends, ret.time_stamp

    def get(self):
        """
        获取文章列表
        """
        qs_parser = RequestParser()
        qs_parser.add_argument('channel_id', type=parser.channel_id, required=True, location='args')
        qs_parser.add_argument('timestamp', type=inputs.positive, required=True, location='args')
        args = qs_parser.parse_args()
        channel_id = args.channel_id
        timestamp = args.timestamp
        per_page = constants.DEFAULT_ARTICLE_PER_PAGE_MIN
        try:
            feed_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        except Exception:
            return {'message': 'timestamp param error'}, 400

        results = []

        # 获取推荐文章列表
        feeds, pre_timestamp = self._feed_articles(channel_id, timestamp, per_page)

        # 查询文章
        for feed in feeds:
            article = cache_article.ArticleInfoCache(feed.article_id).get()
            if article:
                article['pubdate'] = feed_time
                article['trace'] = {
                    'click': feed.track.click,
                    'collect': feed.track.collect,
                    'share': feed.track.share,
                    'read': feed.track.read
                }
                results.append(article)

        return {'pre_timestamp': pre_timestamp, 'results': results}


# /users/123
# /users/<int(min=1):user_id>

class ArticleResourceDD(Resource):
    """
    文章信息
    """

    def get(self, article_id):

        # 检验参数
        # 创建工具对象
        cache_tool = cache_article.ArticleMessageCache(article_id)
        if not cache_tool.exists():
            # 文章不存在
            return {'message': 'Article does not exists.'}, 404
        else:
            # 查询文章数据
            article_dict = cache_tool.get()
            article_dict['article_id'] = article_id
            return article_dict

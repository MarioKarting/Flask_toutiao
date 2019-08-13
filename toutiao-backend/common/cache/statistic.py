# redis 持久化保存
# 用户发表文章    zset       number    sore
#   count:user:arts       [{user_id,count}]
#                              1      4
#
#                              2      2
from redis.exceptions import RedisError
from sqlalchemy.exc import DatabaseError

from flask import current_app
from flask import current_app
from redis.exceptions import RedisError
from sqlalchemy import func

from models import db
from models.news import Article, Attitude, CommentLiking, Collection, Comment
from models.user import Relation





class CountStorageBase(object):
    # 类属性，全部函数都共享这个属性，无论查询哪个文章都是公用的在这个redis中查询
    key = " "

    # 查询数据
    @classmethod
    def get(cls, member_id):
        # zscore
        # ZRANGE salary 0 -1 WITHSCORES 查询所有成员和分数
        # zscore key member -> score
        # 异常捕获
        try:
            count = current_app.redis_master.zscore(cls.key, member_id)
        except RedisError as e:
            current_app.logger.error(e)
            # 如果主机出现故障，不等哨兵了，直接连接从机
            count = current_app.redis_slave.zscore(cls.key, member_id)
            # 取出的redis是byte类型，需要进行转换成int
        return 0 if count is None else int(count)

    # 累计数据  参数需要一个增值 incrment 默认等于1
    @classmethod
    def increase(cls, member_id, increment=1):
        try:
            # zincre key,increment,user_id
            current_app.redis_master.zincrby(cls.key, increment, member_id)
        except RedisError as e:
            current_app.logger.error(e)
            raise e

    @classmethod
    def reset(cls, db_query_results):
        """
        重置redis记录，在定时任务中使用
        :return:
        """
        # 删除redis记录
        r = current_app.redis_master
        r.delete(cls.key)

        # 保存最新的正确数据
        # zadd key score member

        # 方式一：
        # pl = r.pipeline()
        #
        # for user_id, count in ret:
        #     pl.zadd(key, count, user_id)
        #
        # pl.execute()

        # 方式二：
        # zadd key score1 member1 score2 member2 ...
        redis_data = []
        for user_id, count in db_query_results:
            redis_data.append(count)
            redis_data.append(user_id)

        # redis_data -> [count1, user_id1, count2, user_id2, ...]
        r.zadd(cls.key, *redis_data)
        # r.zadd(key, count1, user_id1, count2, user_id2, ...)

    @staticmethod
    def db_query():
        """
        跟这个统计指标相关的数据库查询
        :return:
        """
        pass

class UserArtuclesCountStorage(CountStorageBase):
    key = 'count:user:arts'

    @staticmethod
    def db_query():
        ret = db.session.query(Article.user_id, func.count(Article.id)).filter(
            Article.status == Article.STATUS.APPROVED) \
            .group_by(Article.user_id).all()
        return ret

class UserFollowsCountStorage(CountStorageBase):
    key = 'count:user:follows'

    @staticmethod
    def db_query():
        # select user_id, count(target_user_id) from user_relation where relation=1 group by user_id;
        return db.session.query(Relation.user_id, func.count(Relation.target_user_id)) \
            .filter(Relation.relation == Relation.RELATION.FOLLOW).group_by(Relation.user_id).all()


class UserFansCountStorage(CountStorageBase):
    key = 'count:user:fans'

class UserLikingCountStorage(CountStorageBase):
    key = 'count:user:liking'


class ArticleLikingCountStorage(CountStorageBase):
    """
    文章点赞数据
    """
    key = 'count:art:liking'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Attitude.article_id, func.count(Collection.article_id)) \
            .filter(Attitude.attitude == Attitude.ATTITUDE.LIKING).group_by(Collection.article_id).all()
        return ret


class CommentLikingCountStorage(CountStorageBase):
    """
    评论点赞数据
    """
    key = 'count:comm:liking'

    @classmethod
    def db_query(cls):
        ret = db.session.query(CommentLiking.comment_id, func.count(CommentLiking.comment_id)) \
            .filter(CommentLiking.is_deleted == 0).group_by(CommentLiking.comment_id).all()
        return ret


class ArticleCollectingCountStorage(CountStorageBase):
    """
    文章收藏数量
    """
    key = 'count:art:collecting'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Collection.article_id, func.count(Collection.article_id)) \
            .filter(Collection.is_deleted == 0).group_by(Collection.article_id).all()
        return ret




class ArticleCommentCountStorage(CountStorageBase):
    """
    文章评论数量
    """
    key = 'count:art:comm'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Comment.article_id, func.count(Comment.id)) \
            .filter(Comment.status == Comment.STATUS.APPROVED).group_by(Comment.article_id).all()
        return ret




# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 定义类


# class UserArticleStatistic(object):
#     # 类属性，全部函数都共享这个属性，无论查询哪个文章都是公用的在这个redis中查询
#     key = "count:user:arts"
#
#     # 查询数据
#     @classmethod
#     def get(cls, user_id):
#         # zscore
#         # ZRANGE salary 0 -1 WITHSCORES 查询所有成员和分数
#         # zscore key member -> score
#         # 异常捕获
#         try:
#             count = current_app.redis_master.zscore(cls.key, user_id)
#         except RedisError as e:
#             current_app.logger.error(e)
#             #如果主机出现故障，不等哨兵了，直接连接从机
#             count = current_app.redis_master.zscore(cls.key, user_id)
#             #取出的redis是byte类型，需要进行转换成int
#         return 0 if count is None else int(count)
#
#     # 累计数据  参数需要一个增值 incrment 默认等于1
#     @classmethod
#     def increase(cls, user_id,increment=1):
#         try:
#         #zincre key,increment,user_id
#             current_app.redis_master.zincrby(cls.key,increment, user_id)
#         except RedisError as e:
#             current_app.logger.error(e)
#             raise e
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

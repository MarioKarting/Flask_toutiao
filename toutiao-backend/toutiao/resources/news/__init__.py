from flask import Blueprint
from flask_restful import Api

# from . import article, collection, liking, dislike, report, comment, channel, reading
from toutiao.resources.news import article
from utils.output import output_json


news_bp = Blueprint('news', __name__)
news_api = Api(news_bp, catch_all_404s=True)
news_api.representation('application/json')(output_json)

#
# news_api.add_resource(article.ArticleResource, '/v1_0/articles/<int(min=1):.>',
#                       endpoint='Article')
#
news_api.add_resource(article.ArticleListResource, '/v1_0/articles',
                      endpoint='Articles')
#
# news_api.add_resource(article.ArticleListResourceV1D1, '/v1_1/articles',
#                       endpoint='ArticlesV1_1')
#
# news_api.add_resource(article.UserArticleListResource, '/v1_0/users/<int(min=1):user_id>/articles',
#                       endpoint='UserArticles')
#
# news_api.add_resource(article.CurrentUserArticleListResource, '/v1_0/user/articles',
#                       endpoint='CurrentUserArticles')
#
# news_api.add_resource(collection.CollectionListResource, '/v1_0/article/collections',
#                       endpoint='ArticleCollections')
#
# news_api.add_resource(collection.CollectionResource, '/v1_0/article/collections/<int(min=1):target>',
#                       endpoint='ArticleCollection')
#
# news_api.add_resource(liking.ArticleLikingListResource, '/v1_0/article/likings',
#                       endpoint='ArticleLikings')
#
# news_api.add_resource(liking.ArticleLikingResource, '/v1_0/article/likings/<int(min=1):target>',
#                       endpoint='ArticleLiking')
#
# news_api.add_resource(dislike.DislikeListResource, '/v1_0/article/dislikes',
#                       endpoint='ArticleDislikes')
#
# news_api.add_resource(dislike.DislikeResource, '/v1_0/article/dislikes/<int(min=1):target>',
#                       endpoint='ArticleDislike')
#
# news_api.add_resource(report.ReportListResource, '/v1_0/article/reports',
#                       endpoint='ArticleReports')
#
# news_api.add_resource(comment.CommentListResource, '/v1_0/comments',
#                       endpoint='Comments')
#
# news_api.add_resource(liking.CommentLikingListResource, '/v1_0/comment/likings',
#                       endpoint='CommentLikings')
#
# news_api.add_resource(liking.CommentLikingResource, '/v1_0/comment/likings/<int(min=1):target>',
#                       endpoint='CommentLiking')
#
# news_api.add_resource(channel.ChannelListResource, '/v1_0/channels',
#                       endpoint='Channels')
#
# news_api.add_resource(reading.ReadingHistoryListResource, '/v1_0/user/histories',
#                       endpoint='UserReadingHistories')
#
# news_api.add_resource(reading.ReadingDurationResource, '/v1_0/reading/durations',
#                       endpoint='UserReadingDurations')


from cache import statistic as cache_statistic

# def fix_statistics(flask_app):
#     """
#     修正redis中保存的统计数据
#     :return:
#     """
#     # 这个函数是apscheduler在一个单独的线程中执行，与flask视图执行流程无关，
#     # 所以此处用到的current_app 离不开手动创建上下文环境
#     with flask_app.app_context():
#
#         # 用户的文章数量
#         # 查询数据库 MySQL
#         # 查询所有用户 每个人的文章数量
#         # select user_id, count(article_id) from news_article_basic where status=2 group by user_id;
#
#         ret = db.session.query(Article.user_id, func.count(Article.id)).filter(Article.status == Article.STATUS.APPROVED)\
#             .group_by(Article.user_id).all()
#
#         # +---------+-------------------+
#         # | user_id | count(article_id) |
#         # +---------+-------------------+
#         # |       1 |             46141 |
#         # |       2 |             46357 |
#         # |       3 |             46187 |
#         # |       5 |                25 |
#         # +---------+-------------------+
#
#         # ret -> [(1, 46141), (2, 46357), (3, 46187), (5, 25)]
#
#         # 删除redis记录
#         key = 'count:user:arts'
#         r = current_app.redis_master
#         r.delete(key)
#
#         # 保存最新的正确数据
#         # zadd key score member
#
#         # 方式一：
#         # pl = r.pipeline()
#         #
#         # for user_id, count in ret:
#         #     pl.zadd(key, count, user_id)
#         #
#         # pl.execute()
#
#         # 方式二：
#         # zadd key score1 member1 score2 member2 ...
#         redis_data = []
#         for user_id, count in ret:
#             redis_data.append(count)
#             redis_data.append(user_id)
#
#         # redis_data -> [count1, user_id1, count2, user_id2, ...]
#         r.zadd(key, *redis_data)
#         # r.zadd(key, count1, user_id1, count2, user_id2, ...)


################# 考虑到每一个统计指标 都是按照相同的处理逻辑 处理，所以复用代码，进行拆分######################


def __fix_process(storage_class):
    ret = storage_class.db_query()
    storage_class.reset(ret)


def fix_statistics(flask_app):
    """
    修正redis中保存的统计数据
    :return:
    """
    # 这个函数是apscheduler在一个单独的线程中执行，与flask视图执行流程无关，
    # 所以此处用到的current_app 离不开手动创建上下文环境
    with flask_app.app_context():

        # ret = cache_statistic.UserArticlesCountStorage.db_query()
        # cache_statistic.UserArticlesCountStorage.reset(ret)
        #
        # ret = cache_statistic.UserFollowsCountStorage.db_query()
        # cache_statistic.UserFollowsCountStorage.reset(ret)

        __fix_process(cache_statistic.UserArtuclesCountStorage)
        __fix_process(cache_statistic.UserFollowsCountStorage)
        # __fix_process(cache_statistic.UserFansCountStorage)








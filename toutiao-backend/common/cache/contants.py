import random


class CacheTTLBase(object):
    """
    有效期工具类
    """
    # 缓存有效期 ，单位秒
    TTL = 2 * 60 * 60

    # 最大的偏差上限
    MAX_DELTA = 10 * 60

    @classmethod
    def get_val(cls):
        return cls.TTL + random.randint(0, cls.MAX_DELTA)


class UserProfileCacheTTL(CacheTTLBase):
    """
    用户资料缓存有效期
    """
    pass


class UserProfileNotExistsCacheTTL(CacheTTLBase):
    """
    用户资料缓存有效期
    """
    TTL = 5 * 60
    MAX_DELTA = 60


class ArticleNotExistsCacheTTL(CacheTTLBase):
    """
    用户资料缓存有效期
    """
    TTL = 5 * 60
    MAX_DELTA = 60


class ArticleInfoCacheTTL(CacheTTLBase):
    """
    文章缓存有效期
    """
    TTL = 1 * 60 * 60
    MAX_DELTA = 5 * 60

# UserProfileCacheTTL.get_val()
import random


class CacheTTLBase(object):
    """
    有效期工具类
    """
    # 缓存有效期 ，单位秒
    TTL = 2 * 60 * 60

    # 最大的偏差上限
    MAX_DELTA = 10 * 60

    @classmethod
    def get_val(cls):
        return cls.TTL + random.randint(0, cls.MAX_DELTA)


class UserProfileCacheTTL(CacheTTLBase):
    """
    用户资料缓存有效期
    """
    pass


class UserProfileNotExistsCacheTTL(CacheTTLBase):
    """
    用户资料缓存有效期
    """
    TTL = 5 * 60
    MAX_DELTA = 60


class ArticleInfoCacheTTL(CacheTTLBase):
    """
    文章缓存有效期
    """
    TTL = 1 * 60 * 60
    MAX_DELTA = 5 * 60


# UserProfileCacheTTL.get_val()


class UserStatusCacheTTL(CacheTTLBase):
    """
    用户状态缓存时间，秒
    """
    TTL = 60 * 60



class UserFollowingsCacheTTL(CacheTTLBase):
    """
    用户关注列表缓存时间，秒
    """
    TTL = 30 * 60


class UserRelationshipCacheTTL(CacheTTLBase):
    """
    用户关系缓存时间，秒
    """
    TTL = 30 * 60


class UserRelationshipNotExistsCacheTTL(CacheTTLBase):
    """
    用户关系不存在数据缓存时间，秒
    """
    TTL = 5 * 60
    MAX_DELTA = 60


class UserAdditionalProfileCacheTTL(CacheTTLBase):
    """
    用户详细资料缓存时间，秒
    """
    TTL = 10 * 60
    MAX_DELTA = 2 * 60


class UserFansCacheTTL(CacheTTLBase):
    """
    用户粉丝列表缓存时间，秒
    """
    TTL = 30 * 60


class UserChannelsCacheTTL(CacheTTLBase):
    """
    用户频道缓存时间，秒
    """
    TTL = 60 * 60


class UserArticleAttitudeCacheTTL(CacheTTLBase):
    """
    用户文章态度缓存时间，秒
    """
    TTL = 30 * 60


class UserArticleAttitudeNotExistsCacheTTL(CacheTTLBase):
    """
    用户文章态度不存在数据缓存时间，秒
    """
    TTL = 5 * 60
    MAX_DELTA = 60


class UserCommentLikingCacheTTL(CacheTTLBase):
    """
    用户文章评论点赞缓存时间，秒
    """
    TTL = 10 * 60
    MAX_DELTA = 2 * 60


class UserCommentLikingNotExistsCacheTTL(CacheTTLBase):
    """
    用户文章评论点赞不存在数据缓存时间，秒
    """
    TTL = 3 * 60
    MAX_DELTA = 60


class ArticleNotExistsCacheTTL(CacheTTLBase):
    """
    文章不存在结果缓存
    为解决缓存击穿，有效期不宜过长
    """
    TTL = 5 * 60
    MAX_DELTA = 60


class ArticleDetailCacheTTL(CacheTTLBase):
    """
    文章详细内容缓存时间，秒
    """
    TTL = 60 * 60


class ArticleUserNoAttitudeCacheTTL(CacheTTLBase):
    """
    用户对文章无态度缓存
    为解决缓存击穿，有效期不宜过长
    """
    TTL = 3 * 60
    MAX_DELTA = 30


class UserArticlesCacheTTL(CacheTTLBase):
    """
    用户文章作品缓存时间，秒
    """
    TTL = 10 * 60
    MAX_DELTA = 2 * 60


class UserArticleCollectionsCacheTTL(CacheTTLBase):
    """
    用户文章收藏缓存时间，秒
    """
    TTL = 10 * 60
    MAX_DELTA = 2 * 60


class ArticleCommentsCacheTTL(CacheTTLBase):
    """
    文章评论列表缓存时间，秒
    """
    TTL = 30 * 60


class CommentRepliesCacheTTL(CacheTTLBase):
    """
    评论回复列表缓存时间，秒
    """
    TTL = 30 * 60


class CommentCacheTTL(CacheTTLBase):
    """
    评论信息缓存时间，秒
    """
    TTL = 30 * 60


class CommentNotExistsCacheTTL(CacheTTLBase):
    """
    评论不存在结果缓存
    为解决缓存击穿，有效期不宜过长
    """
    TTL = 5 * 60
    MAX_DELTA = 60


class AnnouncementDetailCacheTTL(CacheTTLBase):
    """
    系统公告详细信息缓存时间，秒
    """
    TTL = 2 * 60 * 60


class AnnouncementNotExistsCacheTTL(CacheTTLBase):
    """
    公告不存在结果缓存
    为解决缓存击穿，有效期不宜过长
    """
    TTL = 5 * 60
    MAX_DELTA = 60


# 缓存评论最大SCORE
COMMENTS_CACHE_MAX_SCORE = 2e19

# 默认用户头像
DEFAULT_USER_PROFILE_PHOTO = 'Fkj6tQi3xJwVXi1u2swCElotfdCi'  # 程序猿

# 阅读历史每人保存数目
READING_HISTORY_COUNT_PER_USER = 100

# 用户搜索历史每人保存数目
SEARCHING_HISTORY_COUNT_PER_USER = 4

# 允许用户资料数据缓存更新的TTL限制，秒
# ALLOW_UPDATE_USER_PROFILE_CACHE_TTL_LIMIT = 5

# 允许用户资料数据缓存中统计数据更新的TTL限制，秒
# ALLOW_UPDATE_USER_PROFILE_STATISTIC_CACHE_TTL_LIMIT = 5 + ALLOW_UPDATE_USER_PROFILE_CACHE_TTL_LIMIT

# 允许更新关注缓存的TTL限制，秒
ALLOW_UPDATE_FOLLOW_CACHE_TTL_LIMIT = 5

# 默认用户频道缓存有效期，秒
DEFAULT_USER_CHANNELS_CACHE_TTL = 24 * 60 * 60

# 全部频道缓存有效期，秒
ALL_CHANNELS_CACHE_TTL = 24 * 60 * 60

# 允许更新文章评论列表缓存的TTL限制，秒
ALLOW_UPDATE_ARTICLE_COMMENTS_CACHE_TTL_LIMIT = 5

# 系统公告缓存时间，秒
ANNOUNCEMENTS_CACHE_TTL = 48 * 60 * 60

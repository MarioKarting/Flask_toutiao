from datetime import datetime

from . import db


class Channel(db.Model):
    """
    新闻频道
    """
    __tablename__ = 'news_channel'

    id = db.Column('channel_id', db.Integer, primary_key=True, doc='频道ID')
    name = db.Column('channel_name', db.String, doc='频道名称')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    sequence = db.Column(db.Integer, default=0, doc='序号')
    is_visible = db.Column(db.Boolean, default=False, doc='是否可见')
    is_default = db.Column(db.Boolean, default=False, doc='是否默认')


class UserChannel(db.Model):
    """
    用户关注频道表
    """
    __tablename__ = 'news_user_channel'

    id = db.Column('user_channel_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    channel_id = db.Column(db.Integer, db.ForeignKey('news_channel.channel_id'), doc='频道ID')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    is_deleted = db.Column(db.Boolean, default=False, doc='是否删除')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    sequence = db.Column(db.Integer, default=0, doc='序号')

    channel = db.relationship('Channel', uselist=False)


class Article(db.Model):
    """
    文章基本信息表
    """
    __tablename__ = 'news_article_basic'

    class STATUS:
        DRAFT = 0  # 草稿
        UNREVIEWED = 1  # 待审核
        APPROVED = 2  # 审核通过
        FAILED = 3  # 审核失败
        DELETED = 4  # 已删除
        BANNED = 5  # 封禁

    STATUS_ENUM = [0, 1, 2, 3]

    id = db.Column('article_id', db.Integer, primary_key=True,  doc='文章ID')
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.user_id'), doc='用户ID')
    channel_id = db.Column(db.Integer, db.ForeignKey('news_channel.channel_id'), doc='频道ID')
    title = db.Column(db.String, doc='标题')
    cover = db.Column(db.JSON, doc='封面')
    is_advertising = db.Column(db.Boolean, default=False, doc='是否投放广告')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    status = db.Column(db.Integer, default=0, doc='帖文状态')
    reviewer_id = db.Column(db.Integer, doc='审核人员ID')
    review_time = db.Column(db.DateTime, doc='审核时间')
    delete_time = db.Column(db.DateTime, doc='删除时间')
    comment_count = db.Column(db.Integer, default=0, doc='评论数')
    allow_comment = db.Column(db.Boolean, default=True, doc='是否允许评论')
    reject_reason = db.Column(db.String, doc='驳回原因')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, doc='更新时间')

    content = db.relationship('ArticleContent', uselist=False)
    user = db.relationship('User', uselist=False)
    statistic = db.relationship('ArticleStatistic', uselist=False)
    channel = db.relationship('Channel', uselist=False)


class ArticleContent(db.Model):
    """
    文章内容表
    """
    __tablename__ = 'news_article_content'

    id = db.Column('article_id', db.Integer, db.ForeignKey('news_article_basic.article_id'), primary_key=True, doc='文章ID')
    content = db.Column(db.Text, doc='帖文内容')


class ArticleStatistic(db.Model):
    """
    文章统计表
    ******************已废弃****************
    """
    __tablename__ = 'news_article_statistic'

    id = db.Column('article_id', db.Integer, db.ForeignKey('news_article_basic.article_id'), primary_key=True, doc='文章ID')
    read_count = db.Column(db.Integer, default=0, doc='阅读量')
    like_count = db.Column(db.Integer, default=0, doc='点赞量')
    dislike_count = db.Column(db.Integer, default=0, doc='不喜欢数')
    repost_count = db.Column(db.Integer, default=0, doc='转发数')
    collect_count = db.Column(db.Integer, default=0, doc='收藏数')
    fans_comment_count = db.Column(db.Integer, default=0, doc='粉丝评论数')


class Collection(db.Model):
    """
    用户收藏表
    """
    __tablename__ = 'news_collection'

    id = db.Column('collection_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    article_id = db.Column(db.Integer, doc='文章ID')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    is_deleted = db.Column(db.Boolean, default=False, doc='是否删除')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')


class Read(db.Model):
    """
    用户阅读历史表
    ******************已废弃****************
    """
    __tablename__ = 'news_read'

    id = db.Column('read_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    article_id = db.Column(db.Integer, doc='文章ID')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, doc='更新时间')


class Attitude(db.Model):
    """
    用户文章态度表
    """
    __tablename__ = 'news_attitude'

    class ATTITUDE:
        DISLIKE = 0  # 不喜欢
        LIKING = 1  # 点赞

    id = db.Column('attitude_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    article_id = db.Column(db.Integer, db.ForeignKey('news_article_basic.article_id'), doc='文章ID')
    attitude = db.Column(db.Boolean, doc='态度')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')

    article = db.relationship('Article', uselist=False)


class Report(db.Model):
    """
    文章举报
    """
    __tablename__ = 'news_report'

    TYPE_LIST = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    class TYPE:
        OTHER = 0

    id = db.Column('report_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    article_id = db.Column(db.Integer, doc='文章ID')
    type = db.Column(db.Integer, doc='问题类型')
    remark = db.Column(db.String, doc='备注问题')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')


class Comment(db.Model):
    """
    文章评论
    """
    __tablename__ = 'news_comment'

    class STATUS:
        UNREVIEWED = 0  # 待审核
        APPROVED = 1  # 审核通过
        FAILED = 2  # 审核失败
        DELETED = 3  # 已删除

    id = db.Column('comment_id', db.Integer, primary_key=True, doc='评论ID')
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.user_id'), doc='用户ID')
    article_id = db.Column(db.Integer, db.ForeignKey('news_article_basic.article_id'), doc='文章ID')
    parent_id = db.Column(db.Integer, doc='被评论的评论id')
    like_count = db.Column(db.Integer, default=0, doc='点赞数')
    reply_count = db.Column(db.Integer, default=0, doc='回复数')
    content = db.Column(db.String, doc='评论内容')
    is_top = db.Column(db.Boolean, default=False, doc='是否置顶')
    status = db.Column(db.Integer, default=1, doc='评论状态')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')

    user = db.relationship('User', uselist=False)
    article = db.relationship('Article', uselist=False)


class CommentLiking(db.Model):
    """
    评论点赞
    """
    __tablename__ = 'news_comment_liking'

    id = db.Column('liking_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    comment_id = db.Column(db.Integer, doc='评论ID')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    is_deleted = db.Column(db.Boolean, default=False, doc='是否删除')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')

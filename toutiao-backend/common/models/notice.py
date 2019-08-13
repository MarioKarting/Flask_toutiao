from datetime import datetime

from . import db


class Announcement(db.Model):
    """
    系统公告表
    """
    __tablename__ = 'global_announcement'

    class STATUS:
        UNPUBLISHED = 0  # 待发布
        PUBLISHED = 1  # 已发布
        OBSELETE = 2  # 已撤下

    id = db.Column('announcement_id', db.Integer, primary_key=True, doc='公告ID')
    title = db.Column(db.String, doc='标题')
    content = db.Column(db.Text, doc='正文')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    status = db.Column(db.Integer, default=0, doc='状态')
    pubtime = db.Column('publish_time', db.DateTime, doc='发布时间')
    utime = db.Column('update_time', db.DateTime, doc='更新时间')

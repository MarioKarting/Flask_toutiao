from . import db
from datetime import datetime


class SensitiveWord(db.Model):
    """
    敏感词
    """
    __tablename__ = 'recommend_sensitive_word'

    id = db.Column(db.Integer, primary_key=True, doc='敏感词id')
    word = db.Column(db.String, doc='敏感词')
    weights = db.Column(db.Integer, doc='权重')
    hold_count = db.Column(db.Integer, doc='拦截次数')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now(), doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now(), doc='修改时间')


class Word(db.Model):
    """
    单词
    """
    __tablename__ = 'word'

    id = db.Column(db.Integer, primary_key=True, doc='id')
    word = db.Column(db.String, doc='英文')
    fanyi = db.Column(db.Integer, doc='翻译')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now(), doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now(), doc='修改时间')


from datetime import datetime

from . import db


class LegalizeLog(db.Model):
    """
    用户认证申请记录
    """
    __tablename__ = 'user_legalize_log'

    class TYPE:
        REAL_NAME = 1  # 实名认证
        QUALIFICATION = 2  # 资质认证

    class STATUS:
        PROCESSING = 1  # 处理中
        APPROVED = 2 # 通过审核
        REJECT = 3 # 驳回

    id = db.Column('legalize_id', db.Integer, primary_key=True, doc='认证申请ID')
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.user_id'), doc='用户ID')
    user = db.relationship('User', uselist=False)
    type = db.Column(db.Integer, doc='认证类型')
    status = db.Column(db.Integer, doc='申请状态')
    reject_reason = db.Column(db.String, doc='驳回原因')
    qualification_id = db.Column(db.Integer, db.ForeignKey('user_qualification.qualification_id'), doc='资质认证材料ID')
    qualification = db.relationship('Qualification', uselist=False)
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, doc='更新时间')


class Qualification(db.Model):
    """
    用户资质认证材料
    """
    __tablename__ = 'user_qualification'

    id = db.Column('qualification_id', db.Integer, primary_key=True, doc='资质认证材料ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    name = db.Column(db.String, doc='姓名')
    id_number = db.Column(db.String, doc='身份证号')
    industry = db.Column(db.String, doc='行业')
    company = db.Column(db.String, doc='公司')
    position = db.Column(db.String, doc='职位')
    add_info = db.Column(db.String, doc='补充信息')
    id_card_front = db.Column(db.String, doc='身份证正面')
    id_card_back = db.Column(db.String, doc='身份证背面')
    id_card_handheld = db.Column(db.String, doc='手持身份证')
    qualification_img = db.Column(db.String, doc='证明资料')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, doc='更新时间')


class User(db.Model):
    """
    用户基本信息
    """
    __tablename__ = 'user_basic'

    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    mobile = db.Column(db.String, doc='手机号')
    password = db.Column(db.String, doc='密码')
    name = db.Column('user_name', db.String, doc='昵称')
    profile_photo = db.Column(db.String, doc='头像')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    is_media = db.Column(db.Boolean, default=False, doc='是否是自媒体')
    is_verified = db.Column(db.Boolean, default=False, doc='是否实名认证')
    introduction = db.Column(db.String, doc='简介')
    certificate = db.Column(db.String, doc='认证')
    article_count = db.Column(db.Integer, default=0, doc='发帖数')
    following_count = db.Column(db.Integer, default=0, doc='关注的人数')
    fans_count = db.Column(db.Integer, default=0, doc='被关注的人数（粉丝数）')
    like_count = db.Column(db.Integer, default=0, doc='累计点赞人数')
    read_count = db.Column(db.Integer, default=0, doc='累计阅读人数')

    account = db.Column(db.String, doc='账号')
    email = db.Column(db.String, doc='邮箱')
    status = db.Column(db.Integer, default=1, doc='状态，是否可用')

    # 两种方法都可以
    # followings = db.relationship('Relation', primaryjoin='User.id==Relation.user_id')
    followings = db.relationship('Relation', foreign_keys='Relation.user_id')


class UserProfile(db.Model):
    """
    用户资料表
    """
    __tablename__ = 'user_profile'

    class GENDER:
        MALE = 0
        FEMALE = 1

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    gender = db.Column(db.Integer, default=0, doc='性别')
    birthday = db.Column(db.Date, doc='生日')
    real_name = db.Column(db.String, doc='真实姓名')
    id_number = db.Column(db.String, doc='身份证号')
    id_card_front = db.Column(db.String, doc='身份证正面')
    id_card_back = db.Column(db.String, doc='身份证背面')
    id_card_handheld = db.Column(db.String, doc='手持身份证')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    register_media_time = db.Column(db.DateTime, doc='注册自媒体时间')

    area = db.Column(db.String, doc='地区')
    company = db.Column(db.String, doc='公司')
    career = db.Column(db.String, doc='职业')

    followings = db.relationship('Relation', foreign_keys='Relation.user_id')


class Relation(db.Model):
    """
    用户关系表
    """
    __tablename__ = 'user_relation'

    class RELATION:
        DELETE = 0
        FOLLOW = 1
        BLACKLIST = 2

    id = db.Column('relation_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.user_id'), db.ForeignKey('user_profile.user_id'), doc='用户ID')
    target_user_id = db.Column(db.Integer, db.ForeignKey('user_basic.user_id'), doc='目标用户ID')
    relation = db.Column(db.Integer, doc='关系')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')


class Search(db.Model):
    """
    用户搜索记录表
    ******************已废弃****************
    """
    __tablename__ = 'user_search'

    id = db.Column('search_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    keyword = db.Column(db.String, doc='关键词')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    is_deleted = db.Column(db.Boolean, default=False, doc='是否删除')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')


class Material(db.Model):
    """
    素材表
    """
    __tablename__ = 'user_material'

    class TYPE:
        IMAGE = 0
        VIDEO = 1
        AUDIO = 2

    class STATUS:
        UNREVIEWED = 0  # 待审核
        APPROVED = 1  # 审核通过
        FAILED = 2  # 审核失败
        DELETED = 3  # 已删除

    id = db.Column('material_id', db.Integer, primary_key=True, doc='素材ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    type = db.Column(db.Integer, default=0, doc='素材类型')
    hash = db.Column(db.String, doc='素材指纹')
    url = db.Column(db.String, doc='素材链接地址')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    status = db.Column(db.Integer, default=0, doc='状态')
    reviewer_id = db.Column(db.Integer, doc='审核人员ID')
    review_time = db.Column(db.DateTime, doc='审核时间')
    is_collected = db.Column(db.Boolean, default=False, doc='是否收藏')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')







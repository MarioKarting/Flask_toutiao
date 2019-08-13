from datetime import datetime

from . import db


class MisAdministrator(db.Model):
    """
    管理员基本信息
    """
    __tablename__ = 'mis_administrator'

    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = db.Column('administrator_id', db.Integer, primary_key=True, doc='管理员ID')
    account = db.Column(db.String, doc='账号')
    password = db.Column(db.String, doc='密码')
    name = db.Column(db.String, doc='管理员名称')
    email = db.Column(db.String, doc='电子邮箱')
    mobile = db.Column(db.String, doc='手机号')
    access_count = db.Column(db.Integer, default=0, doc='访问次数')
    status = db.Column(db.Integer, default=1, doc='状态')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    group_id = db.Column(db.Integer, db.ForeignKey('mis_administrator_group.group_id'), doc='管理员角色/组ID')
    group = db.relationship('MisAdministratorGroup', uselist=False)


class MisAdministratorGroup(db.Model):
    """
    管理员组/角色
    """
    __tablename__ = 'mis_administrator_group'
    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = db.Column('group_id', db.Integer, primary_key=True, doc='管理员角色/组ID')
    name = db.Column(db.String, doc='角色/组')
    status = db.Column(db.Integer, default=1, doc='状态')
    remark = db.Column(db.String, doc='备注')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    group_permission = db.relationship('MisGroupPermission')


class MisPermission(db.Model):
    """
    权限表
    """
    __tablename__ = 'mis_permission'
    class TYPE:
        # 菜单
        MENU = 0
        # 接口
        API = 1

    id = db.Column('permission_id', db.Integer, primary_key=True, doc='权限ID')
    name = db.Column(db.Integer, doc='权限名称')
    type = db.Column(db.Integer, default=1, doc='权限类型')
    parent_id = db.Column(db.Integer, default=0, doc='父权限的ID')
    code = db.Column(db.String, doc='权限点代码')
    sequence = db.Column(db.Integer, default=0, doc='序列')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')


class MisGroupPermission(db.Model):
    """
    组权限表
    """
    __tablename__ = 'mis_group_permission'

    id = db.Column('group_permission_id', db.Integer, primary_key=True, doc='组权限ID')
    group_id = db.Column(db.Integer, db.ForeignKey('mis_administrator_group.group_id'), doc='角色/组ID')
    group = db.relationship('MisAdministratorGroup', uselist=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('mis_permission.permission_id'), doc='权限ID')
    permission = db.relationship('MisPermission', uselist=False)
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')


class MisOperationLog(db.Model):
    """
    运营日志
    """
    __tablename__ = 'mis_operation_log'

    id = db.Column('operation_log_id', db.Integer, primary_key=True, doc='日志id')
    administrator_id = db.Column(db.Integer, db.ForeignKey('mis_administrator.administrator_id'), doc='管理员ID')
    administrator = db.relationship("MisAdministrator", uselist=False)
    ip = db.Column(db.String, doc='ip地址')
    operation = db.Column(db.String, doc='操作')
    description = db.Column(db.String, doc='描述')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')



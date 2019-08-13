from  flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

#数据库设置
class DefaultConfig(object):
    '''
    默认配置
    '''
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/toutiao'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

app.config.from_object(DefaultConfig)

#定义模型类
#创建模型类对象
db = SQLAlchemy(app) #这个方式直接就知道数据库在哪里 ,创建初就知道

#方式二需要上下文环境  with app.app_context();这里后补充的app， 相当于用current_app去配置config的属性
# db = SQLAlchemy()
# db.init_app(app)
'''
操作需要在上下文环境中完成 
with app.app_context():
    db.xxx
    User.xxx
'''

# class User(db.Model):
#     #映射哪个表
#     __tablename__ = 'user_basic'
#     #有些属性给自己看的 primary_Key = TUre doc
#     id = db.Column('user_id',db.BigInteger)
#     #对于约束条件直接用db.integer ,因为我们只为了生成sql语句
#     #如果你的模型类是为创建表的话，就必须很详细，什么为空，不为空，主键等约束
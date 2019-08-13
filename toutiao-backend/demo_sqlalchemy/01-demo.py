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


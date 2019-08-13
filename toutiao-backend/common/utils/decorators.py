from flask import g, current_app
from functools import wraps
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError

from models import db


def set_db_to_read(func):
    """
    设置使用读数据库
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_read()
        return func(*args, **kwargs)

    return wrapper


def set_db_to_write(func):
    """
    设置使用写数据库
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_write()
        return func(*args, **kwargs)

    return wrapper


# 进入视图函数的装饰器
def login_required(func):
    def wrapper(*args, **kwargs):
        if g.user_id is not None and g.use_refersh_token is False:
            return func(*args, **kwargs)
        else:
            return {'message': 'Invalid token'}, 401

    return wrapper

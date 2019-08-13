from flask import current_app
import json
from sqlalchemy.orm import load_only
import random
from redis.exceptions import RedisError
from sqlalchemy.exc import DatabaseError

from models.user import User
from . import contants

# key              value
# user:{user_id}:info
# user:123:info
# user:124:info  ->  str
# 				json.dumps(user_data)

# 用户基本资料的缓存

# 分析工具的使用场景：
# 1. 需要查询用户的资料数据
# 2. 需要清除缓存
# 3. 需要判读用户是否存在

# 考虑：
# 1. 这三个方法应该是一条redis记录所支持的操作，可以封装到一起
# 2. 三个方法操作相同的数据， 采用类封装

# 类的定义方法：
#   需要明确类中的内容：
#       1. 数据 -> 属性
#       2. 函数 -> 方法
#
#  确定 使用哪个属性保存数据
#     区别：数据是每个对象独有还是所有对象共享
#      类属性： 类的所有对象 共享的数据，数据相同
#      实例属性（对象属性）： 类的每个对象 独有的数据，数据不同

# 确定 使用哪种方法保存函数
#      区别： 能够使用的数据(属性）范围不同

#       对象方法（实例方法） -> 直接能够读写对象属性， 能够读取类属性
#       def obj_func(self, ...)
#           self.xxx

#       类方法
#       @classmethod  -> 直接能够读写类属性
#       def class_func(cls, ...)
#           cls.xxx

#       静态方法
#       @staticmethod -> 也可以读写类属性
#       def static_func(..)
#           类名.xxx
#
# 选择： 如果函数需要直接操作对象属性，定义对象方法
#       如果函数仅需要操作类属性， 定义类方法
#       如果函数中不需要任何类的属性，仅仅从逻辑的角度 封装的角度，认为是类的一种方法，定义静态方法


class UserProfileCache(object):
    """
    用户资料数据缓存辅助工具
    """
    def __init__(self, user_id):
        # 要操作的redis key
        self.key = 'user:{}:info'.format(user_id)
        self.user_id = user_id

    def save(self):
        """
        查询mysql数据库，形成保存redis缓存数据
        :return:
        """
        r = current_app.redis_cluster

        try:
            # 查询数据库MySQL
            user = User.query.options(load_only(
                User.mobile,
                User.profile_photo,
                User.name,
                User.introduction,
                User.certificate
            )).filter_by(id=self.user_id).first()
        except DatabaseError as e:
            current_app.logger.error(e)
            raise e

        if user is not None:
            # 如果数据库有数据，保存redis缓存，返回
            # user_dict = {
            #     "mobile": user.mobile,
            #     "photo": user.profile_photo,
            #     "name": user.name,
            #     "intro": user.introduction,
            #     "certi": user.certificate
            # }
            user_dict = dict(
                mobile=user.mobile,
                photo=user.profile_photo,
                name=user.name,
                intro=user.introduction,
                certi=user.certificate
            )
            user_json_str = json.dumps(user_dict)
            try:
                # r.setex(key, 有效期, 数据)
                r.setex(self.key, contants.UserProfileCacheTTL.get_val(), user_json_str)
            except RedisError as e:
                current_app.logger.error(e)

            return user_dict
        else:
            try:
                # 如果数据库没有数据， 保存redis 记录-1， 返回
                r.setex(self.key, contants.UserProfileNotExistsCacheTTL.get_val(), -1)
            except RedisError as e:
                current_app.logger.error(e)

            return None

    def get(self):
        """
        查询
        :return:
        """
        r = current_app.redis_cluster

        # 查询redis记录
        try:
            ret = r.get(self.key)
            # redis 有数据，未过期 返回数据
            # redis 没有数据， 返回None
            # redis 有数据，但是过期，返回None
            # 从redis 中取出的 字符串数据 到python3中是bytes类型
        except RedisError as e:
            # flask中的日志
            current_app.logger.error(e)
            # redis不能查出，但是mysql还是有可能查询数据
            ret = None

        if ret is not None:
            # 如果redis有数据 ，返回
            if ret == b'-1':  # -> 声明bytes类型的数据 b'-1' -> bytes类型
                # 表示用户不存在
                return None
            else:
                # 表示用户存在，存放的是json的缓存数据
                # json.loads 接收bytes类型
                user_dict = json.loads(ret)
                return user_dict
        else:
            # 如果redis没有数据，
            return self.save()

    def clear(self):
        """
        清除缓存
        :return:
        """
        r = current_app.redis_cluster

        try:
            r.delete(self.key)
        except RedisError as e:
            current_app.logger.error(e)

    def exists(self):
        """
        判断用户是否存在
        :return: Boolean  True or False
        """
        r = current_app.redis_cluster

        # 查询redis
        try:
            ret = r.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            ret = None

        if ret is not None:
            # 如果redis有数据，返回
            if ret == b'-1':
                return False
            else:
                return True
        else:
            # 如果redis没有数据
            # 查询数据库，判断用户是否存在
            result = self.save()
            return False if result is None else True

#
# user1   UserProfileCache(1)  -> redis key   user:1:info
# user2   UserProfileCache(2)  -> redis key   user:2:info


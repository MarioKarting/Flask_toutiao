import json
from sqlalchemy.orm import load_only, contains_eager
from flask import current_app
from redis.exceptions import RedisError

from models.news import Channel, UserChannel
from . import contants


class AllChannelsCache(object):
    """
    全部频道缓存
    """
    key = 'ch:all'

    @classmethod
    def get(cls):
        """
        获取
        :return: [{'name': 'python', 'id': '123'}, {}]
        """
        rc = current_app.redis_cluster

        # 缓存取数据
        ret = rc.get(cls.key)
        if ret:
            results = json.loads(ret)
            return results

        # 数据库查询
        results = []

        channels = Channel.query.options(load_only(Channel.id, Channel.name)) \
            .filter(Channel.is_visible == True).order_by(Channel.sequence, Channel.id).all()

        if not channels:
            return results

        for channel in channels:
            results.append({
                'id': channel.id,
                'name': channel.name
            })

        # 设置缓存
        try:
            rc.setex(cls.key, contants.ALL_CHANNELS_CACHE_TTL, json.dumps(results))
        except RedisError as e:
            current_app.logger.error(e)

        return results

    @classmethod
    def exists(cls, channel_id):
        """
        判断channel_id是否存在
        :param channel_id: 频道id
        :return: bool
        """
        # 此处不直接用redis判断是否存在键值
        # 先从redis中判断是否存在键，再从键判断值是否存在，redis集群中无法保证事务
        chs = cls.get()
        for ch in chs:
            if channel_id == ch['id']:
                return True
        return False


class UserDefaultChannelsCache(object):
    """
    用户默认频道
    """
    key = 'ch:user:default'

    @classmethod
    def get(cls):
        """
        获取用户默认频道数据
        :return: [{'name': 'python', 'id': '123'}, {}]
        """
        rc = current_app.redis_cluster

        # 缓存取数据
        try:
            ret = rc.get(cls.key)
        except RedisError as e:
            current_app.logger.error(e)
            ret = None

        if ret:
            results = json.loads(ret)
            return results

        # 数据库查询
        results = []

        channels = Channel.query.options(load_only(Channel.id, Channel.name))\
            .filter(Channel.is_default == True, Channel.is_visible == True).order_by(Channel.sequence, Channel.id).all()

        if not channels:
            return results

        for ch in channels:
            results.append({
                'id': ch.id,
                'name': ch.name
            })

        # 设置缓存
        try:
            rc.setex(cls.key, contants.DEFAULT_USER_CHANNELS_CACHE_TTL, json.dumps(results))
        except RedisError as e:
            current_app.logger.error(e)

        return results

    @classmethod
    def clear(cls):
        """
        清除缓存
        """
        rc = current_app.redis_cluster

        try:
            rc.delete(cls.key)
        except RedisError as e:
            current_app.logger.error(e)


class UserChannelsCache(object):
    """
    用户频道缓存
    """
    def __init__(self, user_id):
        self.key = 'user:{}:ch'.format(user_id)
        self.user_id = user_id

    def get(self):
        """
        获取
        :return:
        """
        rc = current_app.redis_cluster
        try:
            ret = rc.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            ret = None

        if ret:
            return json.loads(ret)

        # error
        # user_channels = UserChannel.query.options(load_only(UserChannel.channel_id),
        #                                           joinedload(UserChannel.channel, innerjoin=True)
        #                                           .load_only(Channel.name))\
        #     .filter(UserChannel.user_id == user_id, UserChannel.is_deleted == False, Channel.is_visible == True)\
        #     .order_by(UserChannel.sequence).all()

        user_channels = UserChannel.query.join(UserChannel.channel).options(load_only(UserChannel.channel_id),
                                                                            contains_eager(UserChannel.channel)
                                                                            .load_only(Channel.name)) \
            .filter(UserChannel.user_id == self.user_id, UserChannel.is_deleted == False, Channel.is_visible == True) \
            .order_by(UserChannel.sequence).all()

        results = []
        for ch in user_channels:
            results.append({
                'id': ch.channel_id,
                'name': ch.channel.name
            })

        try:
            rc.setex(self.key, contants.UserChannelsCacheTTL.get_val(), json.dumps(results))
        except RedisError as e:
            current_app.logger.error(e)

        return results

    def clear(self):
        """
        清除
        """
        try:
            current_app.redis_cluster.delete(self.key)
        except RedisError as e:
            current_app.logger.error(e)

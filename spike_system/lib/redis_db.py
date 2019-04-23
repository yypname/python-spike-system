# -*- coding: utf-8 -*-

import redis
from config import REDISINFO
class RedisBase(object):
    def __init__(self):
        if not hasattr(OPRedis, 'pool'):
            RedisBase.GetRedisCoon()  #创建redis连接
        self.coon = redis.Redis(connection_pool=OPRedis.pool)

    @staticmethod
    def GetRedisCoon():
        OPRedis.pool = redis.ConnectionPool(host=REDISINFO['host'], port=REDISINFO['port'], db=REDISINFO['db'])


class OPRedis(RedisBase):

    """
    string类型 {'key':'value'} redis操作
    """

    def set_redis(self, key, value, time=None):
        # 非空即真非0即真
        if time:
            res = self.coon.setex(key, value, time)
        else:
            res = self.coon.set(key, value)
        return res

    def get_redis(self, key):
        res = self.coon.get(key).decode()
        return res

    def del_redis(self, key):
        res = self.coon.delete(key)
        return res

    """
    hash类型，{'name':{'key':'value'}} redis操作
    """
    def set_hash_redis(self, name, key, value):
        res = self.coon.hset(name, key, value)
        return res

    def get_hash_redis(self, name, key=None):
        # 判断key是否我为空，不为空，获取指定name内的某个key的value; 为空则获取name对应的所有value
        if key:
            res = self.coon.hget(name, key)
        else:
            res = self.coon.hgetall(name)
        return res

    def del_hash_redis(self, name, key=None):
        if key:
            res = self.coon.hdel(name, key)
        else:
            res = self.coon.delete(name)
        return res


class RedisQueue(RedisBase):
    def __init__(self, name, namespace='queue', **redis_kwargs):
        # super(RedisBase, self).__init__()
        RedisBase.__init__(self)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        return self.coon.llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, item):
        self.coon.rpush(self.key, item)  # 添加新元素到队列最右方

    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.coon.blpop(self.key, timeout=timeout)
        # if item:
        #     item = item[1]  # 返回值为一个tuple
        return item

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.coon.lpop(self.key)
        return item


redis_cache = OPRedis()
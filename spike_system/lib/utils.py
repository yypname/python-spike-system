# -*- coding: utf-8 -*-
from spike_system.lib.redis_db import redis_cache


def limit_handler(amount_limit, key_name, incr_amount):
    """
    :param amount_limit: # 限制数量
    :param keyn_ame: # redis key name
    :param incr_amount: # 每次增加数量
    :return: True: 允许; False: 拒绝
    """
    # 判断key是否存在
    if not redis_cache.coon.exists(key_name):
        # 为了方便测试，这里设置默认初始值为95
        # setnx可以防止并发时多次设置key
        redis_cache.coon.setnx(key_name, 0)

    # 数据插入后再判断是否大于限制数
    if redis_cache.coon.incrby(key_name, incr_amount) <= amount_limit:
        return True
    return False
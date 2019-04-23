# -*- coding: utf-8 -*-

from flask import render_template, jsonify, request, redirect
from flask.views import MethodView

from spike_system.lib.redis_db import redis_cache, RedisQueue
from spike_system.model.goods import Product
# from manage import url_cache
import logging
from . import api
import json

GOODS_DETAIL_REDIS_EXPIRE_SECOND = 7200

OUTPUT_MARK = True

queue = RedisQueue('rq')


class GetGoods(MethodView):
   # @url_cache.cached(timeout=300, key_prefix='view_%s', unless=None)
    def get(self):
        # 获取redis信息
        pid = 'd3c43528529311e9b7c0720020e93501'

        try:
            total = redis_cache.get_hash_redis('goods_info_%s' % pid, "Total")
            ret = redis_cache.get_hash_redis('goods_info_%s' % pid, "Booked")
        except Exception as e:
            logging.info(e)
            total = 0
            ret = 0

        if ret:
            logging.info("hit product info redis")

            return render_template("index.html", p_count=(int(total)-int(ret)))

        # 查询数据库
        try:
            item = Product.query.get(pid)
        except Exception as e:
            logging.error(e)
            return "查询数据失败"

        if not item:
            return "产品不存在"

        try:
            item_counts = item.counts
        except Exception as e:
            logging.error(e)
            return "数据出错"

        try:
            redis_cache.set_hash_redis("goods_info_%s" % pid, "Total", item_counts)
            redis_cache.set_hash_redis("goods_info_%s" % pid, "Booked", 0)
        except Exception as e:
            logging.error(e)
        return render_template("index.html", p_count=item_counts)

    def post(self):
        # product = Product.query.get(1)
        # 检验秒杀是否开始
        start_mark = redis_cache.get_redis('start')
        if start_mark == '0':
            return redirect('/')

        # 接收参数
        uid = request.form.get('uid')
        if not uid:
            return '用户未登录'
        # pid = request.form.get('pid')
        pid = 'd3c43528529311e9b7c0720020e93501'
        count = request.form.get('count')
        print(count)
        if not all([pid, count]):
            return "参数不完整"
        # 校验商品的数量
        try:
            count = int(count)
        except Exception as e:
            return '商品数目非法'
        if count <= 0:
            return '商品数目非法'

        try:
            sha1 = redis_cache.get_redis('sha1')
            ret = redis_cache.coon.evalsha(sha1, 1, 'goods_info_%s' % pid, count)
        except Exception as e:
            logging.info(e)
            return "redis error : %s" % e

        if ret:
            logging.info("抢购成功")
            print("抢购成功")
            print(ret)
            order = {"pid": pid, "count": ret, "uid": uid}
            queue.put(order)

        else:
            logging.info("库存不足")
            print("库存不足")
            return "库存不足"

        return "抢购成功"


# import random
# class GetGoodss(MethodView):
#     def post(self):
#         uid = random.randint(1, 10)
#         if REDIS.lpop('goods_list'):
#             if REDIS.hset('user_list', uid, 1):
#                 print(f'Success,{uid}')
#                 return f'Success,{uid}'
#             else:
#                 # 不可重复抢（每人限领一个）
#                 print(f'push ,{uid}')
#                 REDIS.lpush('goods_list', 1)
#                 return f'create a user {uid}'
#         else:
#             # 已抢完
#             print('Finsh!')
#             return 'Finsh!'
#
#     def get(self):
#         user_list = REDIS.hgetall('user_list')
#         user_list_len = REDIS.hlen('user_list')
#         goods_list = REDIS.llen('goods_list')
#         result_dict = {"user_list": user_list, "user_list_len": user_list_len, 'goods_list': goods_list}
#         print(result_dict)
#         return 'success!'

# @api.route("/goods", methods=["GET"])
# # def spike_goods():
# #
# 用户抢购接口
api.add_url_rule('/goods', view_func=GetGoods.as_view('goods'), methods=['POST'])
# 获取秒杀商品详情
api.add_url_rule('/', view_func=GetGoods.as_view('get_goods'), methods=['GET'])
# api.add_url_rule('/', view_func=GetGoods.as_view('get_goods'), methods=['GET'])
# api.add_resource(GetGoods, "goods")
# add_resource(CustomFilterApi, "/info")
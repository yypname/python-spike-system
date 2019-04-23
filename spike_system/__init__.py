# -*- coding:utf-8 -*-

# 进行app的创建


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_cache import Cache
from config import REDISINFO


def create_app():
    app = Flask(__name__)
    # cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    # url_cache = Cache(app, config={'CACHE_TYPE': 'redis',  # Use Redis
    #                                'CACHE_REDIS_HOST': REDISINFO['host'],  # Host, default 'localhost'
    #                                'CACHE_REDIS_PORT': REDISINFO['port'],  # Port, default 6379
    #                                # 'CACHE_REDIS_PASSWORD': '111',  # Password
    #                                'CACHE_REDIS_DB': REDISINFO['db']})
    db = SQLAlchemy()

    app.config.from_object('config')

    db.init_app(app)

    from spike_system.view.apis import api
    # url_cache.init_app(app)

    app.register_blueprint(api)

    return app#, url_cache

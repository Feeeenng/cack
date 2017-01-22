# -*- coding: utf8 -*-
from __future__ import unicode_literals


class Config(object):
    SECRET_KEY = 'h!a@n#n$e%n^g&f*a(n)g_i+n.k'

    # 加密salt
    SALT = '*^)h#a&n@#$;.'

    # mongodb 链接信息
    DATABASE_NAME = 'cack'
    DATABASE_HOST = '127.0.0.1'
    DATABASE_PORT = 27017
    DATABASE_USERNAME = 'root'
    DATABASE_PASSWORD = 'haner27'
    DATABASE_URL = 'mongodb://{0}:{1}@{2}:{3}'.format(DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

    # 缓存 相关信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 0
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = '{0}://{1}:{2}/{3}'.format(CACHE_TYPE, REDIS_HOST, REDIS_PORT, REDIS_DB)

    # 七牛
    QINIU_BUCKET_NAME = 'cack'
    QINIU_BUCKET_DOMAIN = 'http://ojysw795f.bkt.clouddn.com'
    QINIU_ACCESS_KEY = 'Q_2wWA9VY0rtEUwo1z2Va2cGeFygTYO8UH2i1TR8'
    QINIU_SECRET_KEY = 'xraDccwOWajsCO-FRH6agGcTuPilVBdTeavh_-MA'


class DevelopmentConfig(Config):
    DEBUG = True

    # 邮箱配置
    EMAIL_SMTP_SERVER = 'smtp.126.com'
    EMAIL_USERNAME = 'haner27'
    EMAIL_PASSWORD = 'mqhaner27'
    EMAIL_SENDER = 'haner27@126.com'


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

conf = config['development']
# -*- coding: utf8 -*-
from __future__ import unicode_literals
from functools import wraps
from datetime import timedelta

from flask import jsonify, session
from flask_login import current_user

from errors import Errors
# from utils.datetime_utils import now_lambda
from datetime import datetime
from app import cache

# 缓存方法
memoize = cache.memoize  # 用于缓存费视图函数，以函数名以及参数进行缓存
cached = cache.cached  # 用户缓存视图函数，以request.path进行缓存


def res(code=Errors.SUCCESS, data=None, error=None, extra_msg=None):
    result = {
        'code': code,
    }
    if Errors.is_succeed(code):
        result['success'] = True
        result['detail'] = data
    else:
        result['success'] = False
        if error:
            result['error'] = error
        else:
            result['error'] = Errors.error_msg(code, extra_msg)
    return jsonify(**result)


def access_condition(times=10, limit=3):
    def decorate(func):
        @wraps(func)
        def _decorate(*args, **kwargs):
            now = datetime.now()
            if not session.get('logins'):
                session['logins'] = []
            session['logins'].append(now)
            dt = now - timedelta(seconds=times)
            over_list = filter(lambda a: a >= dt, session['logins'])
            session['logins'] = over_list
            if len(over_list) - 1 >= limit:
                return res(Errors.LIMITATION_EXCEED, extra_msg=['同一个账号任意{0}秒钟内请求不能大于{1}次！'.format(times, limit)])
            return func(*args, **kwargs)
        return _decorate
    return decorate


def pagination_list(page, total):
    if page > total:
        return []

    start_page_data = [1, 2, 3]
    end_page_data = [i for i in xrange(total - 2, total + 1)]

    if page < 10:
        data = [i for i in xrange(1, page+1)]
    else:
        data = start_page_data + ['...'] + [i for i in xrange(page - 5, page + 1)]

    if page > total - 8:
        data += [i for i in xrange(page + 1, total + 1)]
    else:
        data +=  [i for i in xrange(page + 1, page + 6)] + ['...'] + end_page_data

    return data
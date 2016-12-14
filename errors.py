# -*- coding: utf8 -*-
from __future__ import unicode_literals


class Errors(object):
    SUCCESS = 0  # 成功
    PRIVILEGE_REQUIRED = 100
    LIMITATION_EXCEED = 101
    UPLOAD_FORMAT_LIMITATION = 200
    UPLOAD_SIZE_LIMITATION = 201
    PARAMS_REQUIRED = 300
    AUTH_LOGIN_INFO_ERROR = 400

    # error map
    error_map = {
        SUCCESS: '操作成功',
        LIMITATION_EXCEED: '超出限制，{0}',
        UPLOAD_FORMAT_LIMITATION: '上传文件格式受限',
        UPLOAD_SIZE_LIMITATION: '上传文件大小受限',
        PARAMS_REQUIRED: '参数缺失',
        AUTH_LOGIN_INFO_ERROR: '用户名或密码错误'
    }

    # checked_success
    @classmethod
    def is_succeed(cls, code):
        return True if code == cls.SUCCESS else False

    @classmethod
    def error_msg(cls, code, extra_msg):
        msg = cls.error_map.get(code, '')
        if extra_msg:
            msg = msg.format(*extra_msg)
        return msg
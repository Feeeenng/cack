# -*- coding: utf8 -*-
from __future__ import unicode_literals
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def generate_confirmation_token(secret_key, key, data, expiration=86400):
    s = Serializer(secret_key, expires_in=expiration)
    return s.dumps({key: data})


def confirm_token(secret_key, key, data, token):
    s = Serializer(secret_key)
    try:
        d = s.loads(token)
    except:
        return False
    if d.get(key) != data:
        return False
    return True
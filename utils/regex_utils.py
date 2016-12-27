# -*- coding: utf8 -*-
from __future__ import unicode_literals
import re


# 邮箱验证
def regex_email(email):
    regex = ur"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    match = re.search(regex, email)
    if not match:
        return False
    else:
        return True


# 账号的正则
def regex_username(username):
    code = False
    if re.match('^[A-Za-z][A-Za-z0-9]{7,19}$', username):
        if re.search('[0-9]+', username):
            code = True
    return code


# 密码的正则
def regex_password(password):
    code = False
    if re.match('^[A-Z][A-Za-z0-9]{5,19}$', password):
        if re.search('[0-9]+', password):
            code = True
    return code

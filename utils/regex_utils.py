# -*- coding: utf8 -*-
from __future__ import unicode_literals
import re


# 邮箱验证
def check_email_format(subject):
    regex = ur"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    match = re.search(regex, subject)
    if not match:
        return False
    else:
        return True

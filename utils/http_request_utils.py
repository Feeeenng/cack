# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

import requests


def new_request(url, method, data=None, headers=None, **kwargs):
    if not headers:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    res = requests.request(method=method, url=url, data=data, headers=headers, **kwargs)

    code = res.status_code
    if code == 200:
        results = json.loads(res.text)
        return True, results
    else:
        return False, None


# code, results = request('http://dev.api.uxiang.uroaming.cn/notify_test', 'POST', data={'name': 'han', 'age': 23})
# code, results = request('http://www.baidu.com', 'GET')

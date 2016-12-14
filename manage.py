# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask_script import Manager, Server

from app import create_app


# manager配置
cack = create_app()
manager = Manager(cack)
manager.add_command("runserver", Server(threaded=True))


@cack.before_request
def before_request():
    """每个请求前都执行"""
    pass


@cack.teardown_request
def teardown_request(exception):
    """每个请求结束时都执行"""
    pass


if __name__ == '__main__':
    manager.run(default_command='runserver')

# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask.ext.principal import identity_loaded
from flask_script import Manager, Server
from flask_login import current_user
from flask_principal import UserNeed, RoleNeed

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


# 当用户登陆的时候，对用户的identity进行判断
@identity_loaded.connect_via(cack)
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role))


if __name__ == '__main__':
    manager.run(default_command='runserver')

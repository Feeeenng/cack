# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask_principal import RoleNeed, Permission


# 角色
MEMBER = 'MEMBER'
ADMIN = 'ADMIN'
ROLES = [
    (MEMBER, '用户'),
    (ADMIN, '系统管理员')
]

member_permission = Permission(RoleNeed(MEMBER))
admin_permission = Permission(RoleNeed(ADMIN))

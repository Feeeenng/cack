# -*- coding: utf8 -*-
from __future__ import unicode_literals
from collections import namedtuple
from functools import partial

from flask_principal import ActionNeed, RoleNeed, Permission


# 角色
MEMBER = 'MEMBER'
ADMIN = 'ADMIN'
SELLER = 'SELLER'
ROLES = [
    (MEMBER, '用户'),
    (SELLER, '卖家'),
    (ADMIN, '系统管理员')
]

member_permission = Permission(RoleNeed(MEMBER))
seller_permission = Permission(RoleNeed(SELLER))
admin_permission = Permission(RoleNeed(ADMIN))
# edit = Permission(ActionNeed())


# 粗粒度的权限保护
# BlogPostNeed = namedtuple('blog_post', ['method', 'value'])
# EditBlogPostNeed = partial(BlogPostNeed, 'edit')
#
#
# class EditBlogPostPermission(Permission):
#     def __init__(self, post_id):
#         need = EditBlogPostNeed(unicode(post_id))
#         super(EditBlogPostPermission, self).__init__(need)
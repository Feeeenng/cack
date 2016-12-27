# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import current_app
from flask_login import UserMixin, login_user, logout_user
from mongoengine import StringField, ListField, IntField, DateTimeField, EmailField, BooleanField

from . import BaseDocument, register_pre_save
from configs import conf
from constants import GENDERS, SECRET
from permissions import ROLES, MEMBER
from utils.datetime_utils import now_lambda
from utils.regex_utils import regex_username, regex_password, regex_email
from utils.md5_utils import MD5


@register_pre_save()
class User(UserMixin, BaseDocument):
    username = StringField(required=True)  # 用户名
    password = StringField(required=True)  # 密码
    nickname = StringField(required=True)  # 昵称
    email = EmailField(default=None, unique=True)  # 联系邮箱
    gender = IntField(choices=GENDERS, default=SECRET)  # 性别
    avatar = StringField()  # 头像
    is_confirmed = BooleanField(default=False)  # 是否邮箱验证过
    privileges = ListField(IntField(), default=None)  # 权限
    sign_in_ip = StringField(default=None)  # 登录IP
    sign_in_at = DateTimeField(default=None)  # 登录时间
    sign_out_at = DateTimeField(default=None)  # 注销时间
    roles = ListField(StringField(choices=ROLES, default=MEMBER), default=[])

    meta = {
        'collection': 'user',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    def login(self, remember_me):
        login_user(self, remember=remember_me)
        self.sign_in_at = now_lambda()

    def logout(self):
        self.sign_out_at = now_lambda()
        self.save()
        logout_user()

    def verify_password(self, password):
        md5 = MD5(password)
        return self.password == md5.add_salt(current_app.config.get('SALT'))

    @classmethod
    def register(cls, username, password, confirm, email):
        if not regex_username(username):
            return False, '用户名必须是8-20位字母和数字的组合, 第一位必须为字母'

        user = cls.objects(username=username).first()
        if user:
            return False, '用户名已经存在'

        if password != confirm:
            return False, '密码不一致'

        if not regex_password(password):
            return False, '密码必须是6-20位字母和数字的组合, 第一位必须为大字母'

        if not regex_email(email):
            return False, '邮箱格式错误'

        user = cls()
        user.username = username.lower()
        md5 = MD5(password)
        user.password = md5.add_salt(current_app.config.get('SALT'))
        user.email = email
        user.save()
        return True, None

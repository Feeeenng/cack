# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import render_template
from flask import url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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
from utils.mail_utils import Email


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
    roles = ListField(StringField(choices=ROLES, default=MEMBER), default=[])  # 角色

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
        msgs = []
        if not username:
            msgs.append('用户名不能为空')
        else:
            if not regex_username(username):
                msgs.append('用户名必须是8-20位字母和数字的组合, 第一位必须为字母')
            else:
                user = cls.objects(username=username).first()
                if user:
                    msgs.append('用户名已经存在')

        if not password:
            msgs.append('密码不能为空')
            if not confirm:
                msgs.append('重复密码不能为空')
        else:
            if not regex_password(password):
                msgs.append('密码必须是6-20位字母和数字的组合, 第一位必须为大字母')
            else:
                if not confirm:
                    msgs.append('重复密码不能为空')
                else:
                    if password != confirm:
                        msgs.append('密码不一致')

        if not email:
            msgs.append('邮箱不能为空')
        else:
            if not regex_email(email):
                msgs.append('邮箱格式错误')
            else:
                user = cls.objects(email=email).first()
                if user:
                    msgs.append('邮箱已经存在')

        if msgs:
            return msgs

        user = cls()
        user.username = username.lower()
        md5 = MD5(password)
        user.password = md5.add_salt(current_app.config.get('SALT'))
        user.email = email
        user.nickname = username
        user.save()

        # generate confirm token
        token = user.generate_confirmation_token()

        # get confirm url
        confirm_url = url_for('auth.confirm', token=token, _external=True)
        html = render_template('email/email_activate.html', confirm_url=confirm_url)

        email = Email(smtp_sever='smtp.126.com', username='haner27', password='mqhaner27', sender='haner27@126.com',
                      receivers=[user.email], subject='账户邮件确认', html=html)
        email.build_email()
        email.send_email()

        return msgs

    def generate_confirmation_token(self, expiration=86400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False

        self.is_confirmed = 1
        self.save()
        return True

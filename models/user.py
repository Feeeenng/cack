# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import url_for, current_app, render_template
from flask_login import UserMixin, login_user, logout_user
from mongoengine import StringField, ListField, IntField, DateTimeField, EmailField, EmbeddedDocument, EmbeddedDocumentField

from . import BaseDocument, register_pre_save, conf
from constants import GENDERS, SECRET, GENDERS_DICT
from permissions import ROLES, MEMBER
from utils.datetime_utils import now_lambda
from utils.regex_utils import regex_password, regex_email, regex_nickname
from utils.md5_utils import MD5
from utils.mail_utils import Email
from utils.token_utils import generate_confirmation_token, confirm_token
from utils.datetime_utils import format_datetime


@register_pre_save()
class User(UserMixin, BaseDocument):
    email = EmailField(default=None, unique=True)  # 联系邮箱
    password = StringField(required=True)  # 密码
    nickname = StringField(required=True)  # 昵称
    gender = StringField(choices=GENDERS, default=SECRET)  # 性别
    avatar = StringField()  # 头像
    privileges = ListField(IntField(), default=None)  # 权限
    sign_in_ip = StringField(default=None)  # 登录IP
    sign_in_at = DateTimeField(default=None)  # 登录时间
    sign_out_at = DateTimeField(default=None)  # 注销时间
    roles = ListField(StringField(choices=ROLES, default=MEMBER), default=[])  # 角色
    motto = StringField()  # 座右铭
    birthday = DateTimeField()  # 生日

    meta = {
        'collection': 'user',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    @property
    def gender_text(self):
        return GENDERS_DICT.get(self.gender)

    @classmethod
    def login_check(cls, email, password, login_captcha):
        if not email:
            return 'email', 'Email required'

        if not regex_email(email):
            return 'email', 'Email format error'

        if not password:
            return 'password', 'Password required'

        if login_captcha == None or login_captcha == '':
            return 'captcha', 'Captcha required'

        return None, None

    def login(self, remember_me, sign_in_ip):
        login_user(self, remember=remember_me)
        self.sign_in_ip = sign_in_ip
        self.sign_in_at = now_lambda()
        self.save()

    def logout(self):
        self.sign_out_at = now_lambda()
        self.save()
        logout_user()

    def verify_password(self, password):
        md5 = MD5(password)
        return self.password == md5.add_salt(current_app.config.get('SALT'))

    @classmethod
    def find_password_check(cls, email):
        if not email:
            return 'find_password_email', 'Email required'
        else:
            if not regex_email(email):
                return 'find_password_email', 'Email format error'
        return None, None

    @classmethod
    def signup_check(cls, email, password, confirm, nickname):
        if not email:
            return 'email', 'Email required'
        else:
            if not regex_email(email):
                return 'email', 'Email format error'
            else:
                user = cls.objects(email=email).first()
                if user:
                    return 'email', 'Email is existed'

        if not password:
            return 'password', 'Password required'
        else:
            if not regex_password(password):
                return 'password', 'Password must be 6 to 20 of the combination of letters and Numbers, the first must be big letter'
            else:
                if not confirm:
                    return 'confirm', 'Password required'
                else:
                    if password != confirm:
                        return 'confirm', 'Passwords don\'t match'

        if not nickname:
            return 'nickname', 'Nickname required'
        else:
            if not regex_nickname(nickname):
                return 'nickname', 'Nickname can\'t contain illegal characters(chinese, english letters and numbers only)'
            else:
                user = cls.objects(nickname=nickname).first()
                if user:
                    return 'nickname', 'Nickname is existed'
        return None, None

    @classmethod
    def signup(cls, email, password, nickname):
        user = cls()
        md5 = MD5(password)
        user.password = md5.add_salt(current_app.config.get('SALT'))
        user.email = email
        user.nickname = nickname
        user.save()

    def generate_confirmation_token(self, expiration=86400):
        return generate_confirmation_token(current_app.config['SECRET_KEY'], 'confirm', self.id, expiration)

    def confirm(self, token):
        return confirm_token(current_app.config['SECRET_KEY'], 'confirm', self.id, token)

    def reset_password(self, password):
        md5 = MD5(password)
        self.password = md5.add_salt(current_app.config.get('SALT'))
        self.save()

    def send_email_find_password(self):
        # generate confirm token
        token = generate_confirmation_token(current_app.config['SECRET_KEY'], 'reset', self.email, 60 * 15)

        # get confirm url
        find_password_url = url_for('auth.reset_password', token=token, email=self.email, _external=True)
        html = render_template('email/email_find_password.html', find_password_url=find_password_url)

        EMAIL_SMTP_SERVER = current_app.config['EMAIL_SMTP_SERVER']
        EMAIL_USERNAME = current_app.config['EMAIL_USERNAME']
        EMAIL_PASSWORD = current_app.config['EMAIL_PASSWORD']
        EMAIL_SENDER = current_app.config['EMAIL_SENDER']
        email = Email(smtp_sever=EMAIL_SMTP_SERVER, username=EMAIL_USERNAME, password=EMAIL_PASSWORD, sender=EMAIL_SENDER,
                      receivers=[self.email], subject='密码找回', html=html)
        email.build_email()
        email.send_email()

    @property
    def sign_in_at_str(self):
        return format_datetime(self.sign_in_at)

    @property
    def birthday_str(self):
        return format_datetime(self.birthday, '%Y-%m-%d')

    def as_dict(self):
        dic = dict(self.to_mongo())
        if self.password:
            del dic['password']

        if self.sign_in_ip:
            del dic['sign_in_ip']

        if self.sign_in_at:
            dic['sign_in_at'] = self.sign_in_at_str

        if self.created_at:
            del dic['created_at']

        if self.updated_at:
            del dic['updated_at']

        if self.deleted_at:
            del dic['deleted_at']

        if self.birthday:
            dic['birthday'] = self.birthday_str

        dic['gender_text'] = self.gender_text
        return dic

    @classmethod
    def get_user_by_uid(cls, uid):
        return cls.objects(id=uid, deleted_at=None).first()

    @classmethod
    def get_user_name(cls, uid):
        nickname = ''
        u = cls.get_user_by_uid(uid)
        if u:
            nickname = u.nickname
        return nickname


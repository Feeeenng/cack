# -*- coding: utf8 -*-
from __future__ import unicode_literals

from mongoengine import StringField, ListField, IntField, EmbeddedDocumentField, EmbeddedDocument, DateTimeField, BooleanField

from . import BaseDocument, register_pre_save
from configs import conf
from utils.datetime_utils import format_datetime, now_lambda
from models.user import User


class EmbeddedVoter(EmbeddedDocument):
    uid = StringField()  # 投票人ID
    voted_at = DateTimeField()  # 投票时间

    def as_dict(self):
        dic = dict(self.to_mongo())

        if 'voted_at' in dic:
            dic['voted_at'] = format_datetime(self.voted_at)

        user = User.get_user_by_uid(self.uid)
        dic['username'] = user.nickname if user else ''
        return dic


class EmbeddedOption(EmbeddedDocument):
    content = StringField()  # 选项内容
    voters_info = ListField(EmbeddedDocumentField(EmbeddedVoter), default=[])

    def is_voted(self, uid):
        voters = map(lambda a: a.uid, self.voters_info)
        return uid in voters

    @property
    def voters_count(self):
        return len(self.voters_info)

    def as_dict(self, uid=None):
        dic = {
            'content': self.content,
            'voters_info': map(lambda a: a.as_dict(), self.voters_info),
            'is_voted': self.is_voted(uid)
        }
        return dic


@register_pre_save()
class Vote(BaseDocument):
    T_NORMAL = 'NORMAL'
    T_SPECIAL = 'SPECIAL'

    title = StringField(required=True)  # 投票标题
    cover = StringField()  # 封面url
    description = StringField()  # 描述
    options = ListField(EmbeddedDocumentField(EmbeddedOption), default=[])  # 选项
    v_limit = BooleanField(default=False)  # 限制投票人
    v_category = StringField()  # 分类
    specific_voters = ListField(StringField, default=[])  # 指定投票人， 类型为T_SPECIAL的时候用
    limitation = IntField(default=0)  # 限制投票人数
    expired_at = DateTimeField()  # 过期时间
    creator_id = StringField()  # 投票发起人

    meta = {
        'collection': 'vote',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    def as_dict(self, uid):
        dic = {
            'id': self.id,
            'title': self.title,
            'cover': self.cover,
            'description': self.description,
            'options': map(lambda a: a.as_dict(uid), self.options),
            'v_limit': self.v_limit,
            'v_category': self.v_category,
            'v_category_text': '',
            'specific_voters': [],
            'limitation': self.limitation,
            'creator_id': self.creator_id,
            'creator_name': User.get_user_name(self.creator_id),
            'voters_count': self.voters_count,
            'created_at': format_datetime(self.created_at, '%Y-%m-%d'),
            'expired_at': format_datetime(self.expired_at, '%Y-%m-%d'),
            'is_voted': self.is_voted(uid),
            'is_closed': self.is_closed,
            'could_edit': self.could_edit(uid)
        }

        return dic

    def is_voted(self, uid):
        return any(map(lambda a: a.is_voted(uid), self.options))

    def could_edit(self, uid):
        return self.creator_id == uid

    @property
    def voters_count(self):
        return sum(map(lambda a: a.voters_count, self.options))

    @property
    def is_closed(self):
        now = now_lambda()
        # 超时或者人数超过限制
        if self.expired_at < now or self.voters_count >= self.limitation:
            return True
        return False


@register_pre_save()
class VoteCategory(BaseDocument):
    RED = 'red'
    ORANGE = 'orange'
    YELLOW = 'yellow'
    OLIVE = 'olive'
    GREEN = 'green'
    TEAL = 'teal'
    BLUE = 'blue'
    VIOLET = 'violet'
    PURPLE = 'purple'
    PINK = 'pink'
    BROWN = 'brown'
    GREY = 'grey'
    BLACK = 'black'
    COLORS = [
        (RED, '红色'),
        (ORANGE, '橙色'),
        (YELLOW, '黄色'),
        (OLIVE, '橄榄色'),
        (GREEN, '绿色'),
        (TEAL, '青色'),
        (BLUE, '蓝色'),
        (VIOLET, '淡紫色'),
        (PURPLE, '紫色'),
        (PINK, '粉色'),
        (BROWN, '棕色'),
        (GREY, '灰色'),
        (BLACK, '黑色')
    ]
    COLORS_DICT = dict(COLORS)

    name = StringField()  # 分类为名
    color = StringField(choices=COLORS, required=True)  # 分类颜色

    meta = {
        'collection': 'vote_category',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    def as_dict(self):
        dic = {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }
        return dic

    @classmethod
    def new_category(cls, name, color):
        c = cls.objects(name=name, deleted_at=None).first()
        if c:
            return False

        c = cls()
        c.name = name
        c.color = color
        c.save()
        return True

# -*- coding: utf8 -*-
from __future__ import unicode_literals

from mongoengine import StringField, FloatField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, \
    DateTimeField, BooleanField

from . import BaseDocument, register_pre_save, conf
from utils.datetime_utils import datetime_op, now_lambda


@register_pre_save()
class Trend(BaseDocument):
    uid = StringField(required=True)  # 发表人
    content = StringField()  # 内容
    top = BooleanField(default=False)  # 置顶
    # todo: 添加点赞、评论和回复

    meta = {
        'collection': 'trend',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    def as_dict(self):
        dic = dict(self.to_mongo())
        dic['created_at'] = datetime_op(dic['created_at'])
        if 'updated_at' in dic:
            del dic['updated_at']
        if 'deleted_at' in dic:
            del dic['deleted_at']
        return dic

    @classmethod
    def get_the_top_one(cls):
        return cls.objects(top=True, deleted_at=None).first()

    def set_the_top_one(self):
        the_top_one = self.__class__.get_the_top_one()
        if the_top_one:
            the_top_one.top = False
            the_top_one.save()

        self.top = True
        self.save()

    def cancel_top_display(self):
        self.top = False
        self.save()

    def delete(self):
        now = now_lambda()
        self.deleted_at = now
        self.save()
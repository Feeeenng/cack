# -*- coding: utf8 -*-
from __future__ import unicode_literals

from mongoengine import StringField, FloatField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, \
    DateTimeField, BooleanField

from . import BaseDocument, register_pre_save, conf
from utils.datetime_utils import datetime_op


@register_pre_save()
class Trend(BaseDocument):
    uid = StringField(required=True)  # 发表人
    content = StringField()  # 内容
    # todo: 添加点赞、评论和回复

    meta = {
        'collection': 'trend',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    def as_dict(self):
        dic = dict(self.to_mongo())
        dic['created_at'] = datetime_op(dic['created_at'])
        del dic['updated_at']
        del dic['deleted_at']
        return dic
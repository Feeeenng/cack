# -*- coding: utf8 -*-
from __future__ import unicode_literals

from mongoengine import StringField, FloatField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, \
    DateTimeField, BooleanField

from utils.datetime_utils import now_lambda
from . import BaseDocument, register_pre_save, conf, uploader


@register_pre_save()
class FileManage(BaseDocument):
    name = StringField(required=True)  # 文件名称
    key = StringField()
    hash = StringField()
    md5 = StringField(required=True)   # 文件内容md5
    content_type = StringField()  # 文件类型
    size = IntField()  # 文件大小

    meta = {
        'collection': 'file_manage',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    @property
    def file_url(self):
        return conf.QINIU_BUCKET_DOMAIN + '/' + self.key + '?' + \
               'watermark/2/text/Y2Fjaw==/font/Y29taWMgc2FucyBtcw==/fontsize/800/fill/IzAwMDAwMA==/dissolve/80/gravity/SouthEast/dx/10/dy/10'

    @property
    def avatar(self):
        return conf.QINIU_BUCKET_DOMAIN + '/' + self.key + '?' + 'imageMogr2/auto-orient/thumbnail/300x256!/format/png/blur/1x0/quality/75|imageslim'

    @property
    def file_size(self):
        if self.size / 1024.0 ** 2 >= 1:
            return '%2.2f MB' % (self.size / 1024.0 ** 2)
        return '%2.2f KB' % (self.size / 1024.0)

    def as_dict(self):
        dic = dict(self.to_mongo())
        dic['file_size'] = self.file_size
        return dic

    def delete(self, key):
        now = now_lambda()
        self.deleted_at = now
        self.save()
        code, msg = uploader.delete(key)
        return code, msg
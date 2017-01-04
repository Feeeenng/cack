# -*- coding: utf8 -*-
from __future__ import unicode_literals

from mongoengine import StringField, FloatField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField

from . import BaseDocument, register_pre_save
from models.coupon import Coupon


class EmbeddedContact(EmbeddedDocument):
    phone = StringField()
    mobile_phone = StringField()
    email = StringField()

    def as_dict(self):
        return dict(self.to_mongo())


@register_pre_save()
class Shop(BaseDocument):
    name = StringField(required=True)
    description = StringField()
    owner_id = StringField(required=True)
    contact = EmbeddedDocumentField(EmbeddedContact)

    def as_dict(self):
        dic = dict(self.to_mongo())
        if self.contact:
            dic['contact'] = self.contact.as_dict()
        return dic

    @property
    def coupons(self):
        return Coupon.objects(shop_id=self.id)
# -*- coding: utf8 -*-
from __future__ import unicode_literals

from mongoengine import StringField, FloatField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, \
    DateTimeField, BooleanField

from . import BaseDocument, register_pre_save


class EmbeddedRule(EmbeddedDocument):
    start_at = DateTimeField(default=None)  # 开始时间
    end_at = DateTimeField(default=None)  # 结束时间

    # 抵债券才有的字段
    baseline_price = FloatField()  # 启用最低面额
    price = FloatField()  # 抵债券的面额

    # 打折卡才有的字段
    discount = FloatField()  # 折扣, 例如: 8.8为8.8折

    def as_dict(self):
        return dict(self.to_mongo())


@register_pre_save()
class Coupon(BaseDocument):
    DISCOUNT_CARD = 'DISCOUNT_CARD'
    BOND = 'BOND'
    CATEGORIES = [
        (DISCOUNT_CARD, '打折卡'),
        (BOND, '抵债券')
    ]
    CATEGORIES_DICT = dict(CATEGORIES)

    name = StringField(required=True)  # 店铺名称
    description = StringField()  # 店铺描述
    shop_id = StringField(required=True)  # 所属商店
    category = StringField(choices=CATEGORIES, default=BOND)  # 债券类型
    rule = EmbeddedDocumentField(EmbeddedRule)  # 规则
    usage = BooleanField(default=False)  # 是否使用过
    owner_id = StringField()  # 所属用户

    def as_dict(self):
        dic = dict(self.to_mongo())
        if self.contact:
            dic['contact'] = self.as_dict()
        return dic
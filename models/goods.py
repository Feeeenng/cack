# -*- coding: utf8 -*-
from __future__ import unicode_literals

from mongoengine import StringField, FloatField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField

from . import BaseDocument, register_pre_save


@register_pre_save()
class GoodsCategory(BaseDocument):
    # 商品分类树
    name = StringField(required=True)  # 分类名
    level = IntField()  # 分类等级， 1级是最大
    parent_id = StringField(default='')  # 父分类ID
    ancestors_ids = ListField(StringField(), default=[])  # 祖先ID

    @classmethod
    def get_root_node(cls):
        return cls.objects(parent_id='')

    @property
    def has_child(self):
        return self.__class__.objects(parent_id=self.id, deleted_at=None).count() > 0

    @property
    def children(self):
        return self.__class__.objects(parent_id=self.id, deleted_at=None)

    @property
    def parent(self):
        return self.__class__.objects(id=self.parent_id, deleted_at=None).first()

    def ancestors(self):
        return self.__class__.objects(id__in=self.ancestors_ids)

    @property
    def full_name(self):
        ancestors = self.ancestors() + [self]
        ancestors = sorted(ancestors, key=lambda a: a.level)
        return '-'.join(map(lambda a: a.name, ancestors))


class EmbeddedSpecification(EmbeddedDocument):
    name = StringField()  # 规格名
    value = StringField()  # 规格值


@register_pre_save()
class Goods(BaseDocument):
    ST_NEW = 0  # 新建
    ST_UP_SHELVES = 1  # 上架
    ST_ADJUST = 2  # 商品调整
    ST_DOWN_SHELVES = 3  # 下架
    ST_SELL_OUT = 4  # 告罄
    STATUS = [
        (ST_NEW, '新建商品'),
        (ST_UP_SHELVES, '商品上架'),
        (ST_ADJUST, '商品调整中'),
        (ST_DOWN_SHELVES, '商品下架'),
        (ST_SELL_OUT, '商品告罄')
    ]
    STATUS_DICT = dict(STATUS)

    name = StringField(required=True)  # 商品名
    description = StringField(required=True)  # 商品描述
    category_id = StringField(required=True)  # 商品分类ID
    keywords = ListField(StringField(), default=[])  # 关键词数组
    price = FloatField(required=True)  # 单价
    stock = IntField(default=0)  # 库存
    status = IntField(choices=STATUS, default=ST_NEW)  # 商品状态
    discount = FloatField(default=10.0)  # 折扣, 例如: 8.8为8.8折
    shop_id = StringField(required=True)  # 商店ID
    specifications = ListField(EmbeddedDocumentField(EmbeddedSpecification), default=[])  # 商品规格(如：大小, 颜色, 形状，型号, 品牌等)

    @property
    def real_price(self):
        return self.price * self.discount / 10

    @property
    def category(self):
        return GoodsCategory.objects(id=self.category_id).first()

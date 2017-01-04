# -*- coding: utf8 -*-
from __future__ import unicode_literals

from mongoengine import StringField, DateTimeField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField, \
    FloatField

from . import BaseDocument, register_pre_save


class EmbeddedOrderHistory(EmbeddedDocument):
    operator_id = StringField()  # 操作者
    old_status = IntField()  # 订单旧状态
    new_status = IntField()  # 订单
    operated_at = DateTimeField(default=None)  # 操作时间


class EmbeddedOrderProduct(EmbeddedDocument):
    goods_id = StringField()  # 商品ID
    count = IntField(default=1)  # 购买数量
    coupons = ListField(StringField(), default=[])  # 用户的使用的打折、抵债卡券
    price = FloatField()  # 原价
    real_price = FloatField()  # 实价


@register_pre_save()
class Order(BaseDocument):
    ST_NEW = 1
    ST_PREPAY = 2
    ST_PAY = 3
    ST_DELIVERED = 4
    ST_FINISHED = 5
    ST_REFUNDING = 6
    ST_REFUNDED = 7
    ST_CANCELED = 8
    ST_EXPIRED = 9
    ST_CLOSED = 10
    STATUS = [
        (ST_NEW, '订单新建'),
        (ST_PREPAY, '买家未支付'),
        (ST_PAY, '买家已支付'),
        (ST_DELIVERED, '卖家已发货'),
        (ST_FINISHED, '交易完成'),
        (ST_REFUNDING, '退款中'),
        (ST_REFUNDED, '已退款'),
        (ST_CANCELED, '交易取消'),
        (ST_EXPIRED, '订单已过期'),
        (ST_CLOSED, '交易关闭')
    ]
    STATUS_DICT = dict(STATUS)

    status = IntField(choices=STATUS, default=ST_NEW)  # 订单状态
    owner_id = StringField()  # 订单所属者ID
    histories = ListField(EmbeddedDocumentField(EmbeddedOrderHistory), default=[])  # 订单变更历史
    products = ListField(EmbeddedDocumentField(EmbeddedOrderProduct), default=[])  # 产品
    total_price = FloatField()  # 原总价
    real_total_price = FloatField()  # 真实总价
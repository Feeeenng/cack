# -*- coding: utf8 -*-
from __future__ import unicode_literals

from mongoengine import StringField, FloatField, IntField

from . import BaseDocument, register_pre_save
from configs import conf

JOB_COMMIT = 'COMMIT'
JOB_PROCESSING = 'PROCESSING'
JOB_EXCEPTION = 'EXCEPTION'
JOB_FINISH = 'FINISH'
JOB_STATUS = [
    (JOB_COMMIT, '任务提交'),
    (JOB_PROCESSING, '任务处理中'),
    (JOB_EXCEPTION, '任务异常'),
    (JOB_FINISH, '任务完成')
]

QUEUE_TYPES = [
    ('queue', 3),  # 通用并行队列
    ('queue-s-1', 1),  # 串行队列1
    ('queue-s-2', 1),  # 串行队列2
    ('queue-s-3', 1),  # 串行队列3
]


@register_pre_save()
class Job(BaseDocument):
    module_name = StringField()  # 被调用的模块名
    function_name = StringField()  # 被调用的函数名
    arguments = StringField()  # 参数
    queue_type = StringField(choices=QUEUE_TYPES, default='queue')  # 队列类型
    status = StringField(choices=JOB_STATUS, default=JOB_COMMIT)  # 任务状态
    duration = FloatField()  # 执行时间（单位：s）
    results = StringField()  # 执行结果
    exceptions = StringField()  # 异常
    process_id = IntField()  # 进程ID

    meta = {
        'collection': 'job',
        'db_alias': conf.DATABASE_NAME,
        'strict': False
    }

    def processing(self):
        self.status = JOB_PROCESSING

    def exception(self):
        self.status = JOB_EXCEPTION

    def finish(self):
        self.status = JOB_FINISH



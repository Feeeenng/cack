# -*- coding: utf8 -*-
from __future__ import unicode_literals


# 性别
MALE = 1
FEMALE = 2
GENDERS = (
    (MALE, '男'),
    (FEMALE, '女')
)
GENDERS_DICT = dict(GENDERS)

# 上传文件格式设置
ALLOWED_FORMATS = ['jpg', 'png', 'jpeg', 'gif']

# 上传文件大小上线
ALLOWED_MAX_SIZE = 10 * 1024 ** 2  # 10M


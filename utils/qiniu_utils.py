# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bson import ObjectId
from cStringIO import StringIO

import requests
from qiniu import Auth, put_data, BucketManager

from utils.md5_utils import MD5


class UploaderUtils(object):
    def __init__(self, access_key, secret_key, bucket_name, bucket_domain):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.q = Auth(self.access_key, self.secret_key)
        self.policy = None
        self.bucket_domain = bucket_domain

    def is_existed(self, io, content_md5):
        content = io.getvalue()
        return MD5(content).get_md5_content() == content_md5

    def upload(self, io):  # 传入buff

        # 上传到七牛后保存的文件名
        key = unicode(ObjectId())

        # 生成上传 Token，可以指定过期时间等
        token = self.q.upload_token(self.bucket_name, key, 3600, policy=self.policy)
        content = io.getvalue()
        ret, info = put_data(token, key, content)
        if info.status_code != 200:
            return False, info.exception, None

        io.seek(0)
        key = ret['key']
        hash = ret['hash']

        code, msg, r = self.get_file_info(key)
        if not code:
            return False, msg, None

        size = r.get('fsize')
        content_type = r.get('mimeType')
        return True, None, dict(key=key, hash=hash, size=size, content_type=content_type)

    def get_url(self, key):
        return '{0}/{1}'.format(self.bucket_domain, key)

    def download(self, key, watermark=False):  # 输出buff
        base_url = self.get_url(key)
        private_url = self.q.private_download_url(base_url, expires=3600)
        r = requests.get(private_url)
        if r.status_code != 200:
            return False, '下载图片失败', None

        content = r.content
        io = StringIO()
        io.write(content)
        io.seek(0)
        return True, None, io

    def get_file_info(self, key):
        # 初始化BucketManager
        bucket = BucketManager(self.q)

        # 获取文件的状态信息
        ret, info = bucket.stat(self.bucket_name, key)
        if info.status_code != 200:
            return False, info.exception, None

        return True, None, ret

    def delete(self, key):
        # 初始化BucketManager
        bucket = BucketManager(self.q)

        # 删除文件
        ret, info = bucket.delete(self.bucket_name, key)
        if info.status_code != 200:
            return False, info.exception

        return True, None


# if __name__ == '__main__':
#     from cStringIO import StringIO
#     access_key = 'Q_2wWA9VY0rtEUwo1z2Va2cGeFygTYO8UH2i1TR8'
#     secret_key = 'xraDccwOWajsCO-FRH6agGcTuPilVBdTeavh_-MA'
#     bucket_name = 'cack'
#     bucket_domain = 'ojysw795f.bkt.clouddn.com'
#     u = UploaderUtils(access_key, secret_key, bucket_name, bucket_domain)
#     io = StringIO()
#     # with open('2.jpg', 'rb') as f:
#     #     io.write(f.read())
#     #     io.seek(0)
#     #     print u.upload(io, '2.jpg')
#     # code, msg, io = u.download('2.jpg')
#     # with open('3.jpg', 'wb') as f:
#     #     f.write(io.getvalue())
#     print u.get_file_info('2.jpg')
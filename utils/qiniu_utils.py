# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from qiniu import BucketManager

from utils.md5_utils import MD5
from bson import ObjectId
from qiniu import Auth, put_data


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

    def upload(self, io, key):  # 传入buff

        # 上传到七牛后保存的文件名
        if not key:
            key = '{0}.png'.format(unicode(ObjectId()))

        # 生成上传 Token，可以指定过期时间等
        token = self.q.upload_token(self.bucket_name, key, 3600, policy=self.policy)
        content = io.getvalue()
        ret, info = put_data(token, key, content)
        if info.status_code != 200:
            return False, info.status_code, info.exception, None

        io.seek(0)
        key = ret['key']
        hash = ret['hash']
        return True, info.status_code, None, dict(key=key, hash=hash)

    def get_file_url(self, key, watermark=False):  # 输出buff
        base_url = 'http://{0}/{1}'.format(self.bucket_domain, key)
        if watermark:
            base_url += '?watermark/2/text/Y2Fjaw==/font/Y29taWMgc2FucyBtcw==/fontsize/800/fill/IzAwMDAwMA==/dissolve/50/gravity/SouthEast/dx/10/dy/10'
        return base_url

    def get_file_info(self, key):
        # 初始化BucketManager
        bucket = BucketManager(self.q)

        # 获取文件的状态信息
        ret, info = bucket.stat(self.bucket_name, key)
        if info.status_code != 200:
            return False, info.status_code, info.exception, None

        return True, info.status_code, None, ret


# if __name__ == '__main__':
#     from cStringIO import StringIO
#     access_key = 'Q_2wWA9VY0rtEUwo1z2Va2cGeFygTYO8UH2i1TR8'
#     secret_key = 'xraDccwOWajsCO-FRH6agGcTuPilVBdTeavh_-MA'
#     bucket_name = 'cack'
#     bucket_domain = 'ojysw795f.bkt.clouddn.com'
#     u = UploaderUtils(access_key, secret_key, bucket_name, bucket_domain)
#     io = StringIO()
#     with open('2.jpg') as f:
#         io.write(f.read())
#         io.seek(0)
#         print u.upload(io, '2.jpg')
#     print u.get_file_url('2.jpg', True)
#     print u.get_file_info('2.jpg')
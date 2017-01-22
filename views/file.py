# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os
from cStringIO import StringIO
from bson import ObjectId

from flask import Blueprint, send_file, request, flash, url_for
from flask_login import login_required

from . import res
from errors import Errors
from constants import ALLOWED_FORMATS, ALLOWED_MAX_SIZE
from utils.md5_utils import MD5
from models import uploader
from models.file import FileManage

instance = Blueprint('file', __name__)


@instance.before_request
def before_request():
    pass


@instance.route('/file/upload', methods=['POST'])
@login_required
def upload():
    f = request.files.get('file')
    if not is_allowed_format(f.filename):
        return res(code=Errors.UPLOAD_FORMAT_LIMITATION)

    if not is_allowed_size(f):
        return res(code=Errors.UPLOAD_SIZE_LIMITATION)

    data = f.stream.read()
    io = StringIO()
    io.write(data)
    io.seek(0)
    md5 = MD5(data).md5_content
    fm = FileManage.objects(md5=md5, deleted_at=None).first()
    if not fm:
        code, msg, d = uploader.upload(io)
        if not code:
            return res(code=Errors.QINIU_ERROR, extra_msg=[msg])

        key = d.get('key', '')
        hash = d.get('hash', '')
        size = d.get('size')
        content_type = d.get('content_type')

        fm = FileManage()
        fm.name = f.filename
        fm.hash = hash
        fm.md5 = md5
        fm.key = key
        fm.size = size
        fm.content_type = content_type
        fm.save()
    return res(data={'url': fm.file_url})


@instance.route('/file/delete/<regex("[0-9a-z]{24}"):key>', methods=['GET'])
@login_required
def delete(key):
    fm = FileManage.objects(key=key, deleted_at=None).first()
    if not fm:
        return res(code=Errors.NOT_FOUND)

    code, msg = fm.delete(key)
    if not code:
        return res(code=Errors.QINIU_ERROR, extra_msg=[msg])
    return res()


@instance.route('/file/download/<regex("[0-9a-z]{24}"):key>', methods=['GET'])
def download(key):
    fm = FileManage.objects(key=key, deleted_at=None).first()
    if not fm:
        return res(code=Errors.NOT_FOUND)

    code, msg, io = uploader.download(key)
    if not code:
        return res(code=Errors.QINIU_ERROR, extra_msg=[msg])

    return send_file(io,
                     fm.content_type,
                     as_attachment=True,
                     attachment_filename=fm.name
                     )


def is_allowed_format(file_name):
    ext = os.path.splitext(file_name)[-1].strip('.')
    if ext.lower() not in ALLOWED_FORMATS:
        flash('上传失败，格式文件受限！')
        return False
    return True


def is_allowed_size(f):
    f.stream.seek(0, 2)
    content_length = f.tell()
    f.stream.seek(0)
    if content_length > ALLOWED_MAX_SIZE:
        flash('上传失败，格式文件大小受限！')
        return False
    return True


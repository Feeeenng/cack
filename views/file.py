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
    md5 = MD5(data).md5_content
    return res()


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


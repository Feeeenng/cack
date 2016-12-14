# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os
from cStringIO import StringIO
from bson import ObjectId
from random import randint
from datetime import datetime

from flask import Blueprint, send_file, request, flash, url_for
from flask_login import login_required

from . import res
from models import gfs
from errors import Errors
from constants import ALLOWED_FORMATS, ALLOWED_MAX_SIZE
from utils.md5_utils import MD5
from utils.zip_utils import Zip

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
    exists = gfs.find_one({'md5': md5})
    if not exists:
        original_filename = f.filename
        content_type = f.content_type
        ext = os.path.splitext(f.filename)[-1].strip('.')
        filename = get_unique_name(ext)
        file_id = gfs.put(data, filename=filename, original_filename=original_filename, content_type=content_type)
    else:
        file_id = exists._id
        filename = exists.filename

    url = url_for('file.show', file_id=file_id)
    return res(data=dict(id=unicode(file_id), name=filename, url=url))


@instance.route('/file/download/<regex("[0-9a-z]{24}"):file_id>', methods=['GET'])
def download(file_id):
    f = gfs.get(ObjectId(file_id))
    imz = Zip()
    io = StringIO(f.read())
    imz.add_file(io, f.filename)
    output_io = imz.output()
    return send_file(output_io, as_attachment=True, attachment_filename='{0}.zip'.format(os.path.splitext(f.filename)[0]))


@instance.route('/file/show/<regex("[0-9a-z]{24}"):file_id>', methods=['GET'])
def show(file_id):
    f = gfs.get(ObjectId(file_id))
    io = StringIO(f.read())
    io.seek(0)
    return send_file(io, mimetype=f.content_type)  # 指定相关mimetype


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


def get_unique_name(ext):
    now = datetime.now()
    return '{0}{1}.{2}'.format(now.strftime('%Y%m%d%H%M%S'), randint(100, 999), ext)

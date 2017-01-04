# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

from views import res

instance = Blueprint('test', __name__)


@instance.before_request
def before_request():
    pass


@instance.route('/test', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('test.html')

    data = [{'id': i, 'content': i} for i in xrange(1, 200)]
    per_page = 60
    r = request.get_json(force=True)
    page = r.get('page', 1)
    d = data[(page - 1) * per_page: page * per_page]
    return res(data=d)
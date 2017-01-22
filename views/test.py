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
    return res()
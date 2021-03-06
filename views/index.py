# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user

from . import access_condition, memoize
from views import res

instance = Blueprint('index', __name__)


@instance.before_request
def before_request():
    pass


@instance.route('/', methods=['GET'])
@access_condition(10, 3)
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('/index/index.html', category='home')


# from permissions import member_permission
# @instance.route('/test')
# @member_permission.require(http_exception=403)
# def test():
#     return res(data='test')
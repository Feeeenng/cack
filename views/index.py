# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

from . import access_condition, memoize

instance = Blueprint('index', __name__)


@instance.before_request
def before_request():
    pass


@instance.route('/', methods=['GET'])
@instance.route('/home', methods=['GET'])
@access_condition(10, 3)
def index():
    return render_template('index.html', category='home')
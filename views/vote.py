# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

from views import res

instance = Blueprint('vote', __name__)


@instance.before_request
@login_required
def before_request():
    pass


@instance.route('/vote', methods=['GET'])
def index():
    return render_template('/vote/index.html', category='vote')
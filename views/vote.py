# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from models.vote import VoteCategory, Vote
from views import res
from utils.datetime_utils import now_lambda, format_datetime, datetime

instance = Blueprint('vote', __name__)


def get_calendar_today():
    now = now_lambda()
    dt = now - datetime.timedelta(days=1)
    dt_str = '[{0},{1},{2}]'.format(dt.year, dt.month, dt.day)
    return dt_str


@instance.before_request
@login_required
def before_request():
    pass


@instance.route('/vote', methods=['GET'])
def index():
    today = get_calendar_today()
    return render_template('/vote/index.html', category='vote', today=today)
# -*- coding: utf8 -*-
from __future__ import unicode_literals
import re

from flask import Blueprint, request, render_template, session, current_app, redirect, url_for, abort
from flask import flash
from flask_login import login_required, current_user
from flask_principal import identity_changed, AnonymousIdentity, Identity, RoleNeed, UserNeed, ActionNeed

from models.trend import Trend
from models.user import User
from views import res
from errors import Errors


instance = Blueprint('friends', __name__)


@instance.before_request
@login_required
def before_request():
    pass


@instance.route('/friends')
def index():
    return render_template('/friends/index.html', category='users')


@instance.route('/trends/send_trend', methods=['POST'])
def send_trend():
    r = request.get_json(True)
    content = r.get('content')
    if not content:
        return res(code=Errors.PARAMS_REQUIRED)

    if calculate_words(content) > 140:
        return res(code=Errors.WORDS_COUNT_LIMITATION)

    t = Trend()
    t.content = content
    t.uid = current_user.id
    t.save()
    return res()


def calculate_words(content):
    count1 = len(re.findall('<img', content))
    content = re.sub('&nbsp', '', content)
    count2 = len(re.sub('<[^>]+>', '', content))
    return count1 + count2


@instance.route('/trends/get_my_trends', methods=['POST'])
def get_trends():
    per_page = 10
    page = request.form.get('page', 1, int)
    ts = Trend.objects(uid=current_user.id, deleted_at=None).order_by('-top', '-created_at')
    total = ts.count()
    ts = ts[(page - 1) * per_page: page * per_page]
    items = [t.as_dict() for t in ts]
    data = {
        'page': page,
        'per_page': per_page,
        'items': items,
        'total': total
    }
    return res(data=data)


@instance.route('/trends/set_top', methods=['POST'])
def set_top():
    tid = request.form.get('tid')
    if not tid:
        return res(code=Errors.PARAMS_REQUIRED)

    t = Trend.objects(id=tid, uid=current_user.id, deleted_at=None).first()
    if not t:
        return res(code=Errors.NOT_FOUND)

    t.set_the_top_one()
    return res()


@instance.route('/trends/delete', methods=['POST'])
def delete():
    tid = request.form.get('tid')
    if not tid:
        return res(code=Errors.PARAMS_REQUIRED)

    t = Trend.objects(id=tid, uid=current_user.id, deleted_at=None).first()
    if not t:
        return res(code=Errors.NOT_FOUND)

    t.delete()
    return res()


@instance.route('/trends/cancel_top', methods=['POST'])
def cancel_top():
    tid = request.form.get('tid')
    if not tid:
        return res(code=Errors.PARAMS_REQUIRED)

    t = Trend.objects(id=tid, uid=current_user.id, deleted_at=None).first()
    if not t:
        return res(code=Errors.NOT_FOUND)

    t.cancel_top_display()
    return res()
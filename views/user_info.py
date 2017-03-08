# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

from models.user import User
from utils.datetime_utils import to_datetime
from constants import SECRET

instance = Blueprint('user_info', __name__)


@instance.before_request
@login_required
def before_request():
    pass


@instance.route('/edit_user_info', methods=['GET', 'POST'])
def edit_user_info():
    # 编辑用户信息
    user_id = request.args.get('user_id') or request.form.get('user_id')
    if not user_id:
        return jsonify(success=False, error='User id required')

    user = User.objects(id=user_id, deleted_at=None).first()
    if not user:
        return jsonify(success=False, error='找不到该用户')

    if request.method == 'GET':
        return jsonify(success=True, data=user.as_dict())

    nickname = request.form.get('nickname')
    if not nickname:
        return jsonify(success=False, error='Nickname required')

    if user.nickname != nickname:
        u = User.objects(nickname=nickname, deleted_at=None).first()
        if u:
            return jsonify(success=False, error='Nickname is existed')

    avatar = request.form.get('avatar')
    if not avatar:
        return jsonify(success=False, error='Avatar is required')

    motto = request.form.get('motto')
    birthday = request.form.get('birthday')
    gender = request.form.get('gender', default=SECRET)

    user.nickname = nickname
    user.motto = motto
    user.birthday = to_datetime(birthday, '%Y-%m-%d')
    user.gender = gender
    user.avatar = avatar
    user.save()

    return jsonify(success=True, data=user.as_dict())
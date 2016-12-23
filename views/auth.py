# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, request, render_template, session, current_app, redirect, url_for, abort
from flask_login import login_required, current_user
from flask_principal import identity_changed, AnonymousIdentity, Identity, RoleNeed, UserNeed, ActionNeed

from models.user import User
from views import res
from errors import Errors


instance = Blueprint('auth', __name__)


@instance.before_request
def before_request():
    if request.method == 'POST':
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


@instance.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/auth/login.html')

    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('remember')

    if not username or not password:
        return res(code=Errors.PARAMS_REQUIRED)

    user = User.objects(username=username).first()
    if not user or not user.verify_password(password):
        return res(code=Errors.AUTH_LOGIN_INFO_ERROR)

    user.sign_in_ip = request.remote_addr
    user.login(remember)
    user.save()

    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    return redirect(request.args.get('next') or url_for('index.index'))


@instance.route('/auth/logout')
@login_required
def logout():
    for key in ['identity.id', 'identity.auth_type']:
        session.pop(key, None)

    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    current_user.logout()
    return redirect(url_for('index.index'))
# -*- coding: utf8 -*-
from __future__ import unicode_literals

from flask import Blueprint, request, render_template, session, current_app, redirect, url_for, abort
from flask import flash
from flask_login import login_required, current_user
from flask_principal import identity_changed, AnonymousIdentity, Identity, RoleNeed, UserNeed, ActionNeed

from models.user import User
from views import res
from errors import Errors
from utils.regex_utils import regex_username, regex_password, regex_email
from utils.token_utils import confirm_token


instance = Blueprint('auth', __name__)


@instance.before_request
def before_request():
    pass


@instance.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/auth/login.html', category='sign in')

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
    flash('你好, {0}'.format(user.nickname), 'info')
    return res(data={'url': request.args.get('next') or url_for('index.index')})


@instance.route('/auth/logout')
@login_required
def logout():
    for key in ['identity.id', 'identity.auth_type']:
        session.pop(key, None)

    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    current_user.logout()
    return redirect(url_for('index.index'))


@instance.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('/auth/register.html', category='edit')

    token = session.pop('_csrf_token', None)
    if not token or token != request.form.get('_csrf_token'):
        abort(403)

    username = request.form.get('username', '')
    password = request.form.get('password', '')
    confirm = request.form.get('confirm', '')
    email = request.form.get('email', '')

    params = {
        'username': username,
        'password': password,
        'confirm': confirm,
        'email': email
    }

    msgs = User.register(**params)
    if msgs:
        return res(code=Errors.AUTH_REGISTER_INFO_ERROR, extra_msg=[' | '.join(msgs)])

    flash('恭喜您注册成功', 'info')
    return redirect(url_for('auth.login'))


@instance.route('/auth/email_confirm/<token>', methods=['GET'])
@login_required
def confirm(token):
    if current_user.is_confirmed:
        return redirect(url_for('index.index'))

    if current_user.confirm(token):
        flash('您的账户邮箱验证成功', 'info')
    else:
        flash('邮箱验证链接无效或是已经过期', 'info')
    return redirect(url_for('index.index'))


@instance.route('/auth/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'GET':
        return render_template('/auth/forget_password.html')

    username = request.form.get('username')
    email = request.form.get('email')

    if not username or not email:
        return res(code=Errors.PARAMS_REQUIRED)

    user = User.objects(username=username, email=email).first()
    if not user:
        return res(code=Errors.AUTH_FORGET_PASSWORD_ERROR)

    user.send_email_find_password()
    flash('重置密码邮件已发送, 请查收')
    return res(data={'url': request.args.get('next') or url_for('index.index')})


@instance.route('/auth/reset_password/<token>/<email>', methods=['GET', 'POST'])
def reset_password(token, email):
    if request.method == 'GET':
        return render_template('/auth/reset_password.html')

    password = request.form.get('password')
    confirm = request.form.get('confirm')
    if not password:
        return res(code=Errors.COMMON_ERROR, extra_msg=['密码不能为空'])

    if not regex_password(password):
        return res(code=Errors.COMMON_ERROR, extra_msg=['密码必须是6-20位字母和数字的组合, 第一位必须为大字母'])

    if not confirm:
        return res(code=Errors.COMMON_ERROR, extra_msg=['重复密码不能为空'])

    if password != confirm:
        return res(code=Errors.COMMON_ERROR, extra_msg=['密码不一致'])

    if confirm_token(current_app.config['SECRET_KEY'], 'reset', email, token):
        user = User.objects(email=email).first()
        if user:
            user.reset_password(password)
            flash('密码重置成功', 'info')
        else:
            flash('邮箱验证链接无效或是已经过期', 'warning')
    else:
        flash('邮箱验证链接无效或是已经过期', 'warning')

    return res(data={'url': request.args.get('next') or url_for('auth.login')})


# ################# ajax请求 ################# #
@instance.route('/auth/username_regex', methods=['POST'])
def username_regex():
    # 检查username格式
    r = request.get_json(force=True)
    username = r.get('username')
    return res(data=regex_username(username))


@instance.route('/auth/password_regex', methods=['POST'])
def password_regex():
    # 检查password格式
    r = request.get_json(force=True)
    password = r.get('password')
    return res(data=regex_password(password))


@instance.route('/auth/email_regex', methods=['POST'])
def email_regex():
    # 检查email格式
    r = request.get_json(force=True)
    email = r.get('email')
    return res(data=regex_email(email))


@instance.route('/auth/check_username', methods=['POST'])
def check_username():
    # 检查username是否存在
    r = request.get_json(force=True)
    username = r.get('username')
    if username:
        user = User.objects(username=username).first()
        if user:
            return res(data=True)
    return res(data=False)


@instance.route('/auth/check_email', methods=['POST'])
def check_email():
    # 检查email是否存在
    r = request.get_json(force=True)
    email = r.get('email')
    if email:
        user = User.objects(email=email).first()
        if user:
            return res(data=True)
    return res(data=False)
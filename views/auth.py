# -*- coding: utf8 -*-
from __future__ import unicode_literals

from datetime import timedelta
from flask import Blueprint, request, render_template, session, current_app, redirect, url_for, abort, jsonify
from flask import flash
from flask_login import login_required, current_user
from flask_principal import identity_changed, AnonymousIdentity, Identity, RoleNeed, UserNeed, ActionNeed

from models.user import User
from utils.captcha import generate_verify_code
from views import res
from errors import Errors
from utils.regex_utils import regex_password, regex_email
from utils.token_utils import confirm_token, generate_confirmation_token, generate_captcha
from utils.mail_utils import Email

instance = Blueprint('auth', __name__)


@instance.before_request
def before_request():
    pass


@instance.route('/logout')
@login_required
def logout():
    for key in ['identity.id', 'identity.auth_type']:
        session.pop(key, None)

    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    current_user.logout()
    return redirect(url_for('index.index'))


@instance.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('/auth/signup.html')

    # token = session.pop('_csrf_token', None)
    # if not token or token != request.form.get('_csrf_token'):
    #     abort(403)

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    confirm = request.form.get('confirm', '').strip()
    nickname = request.form.get('nickname', '').strip()
    captcha = request.form.get('captcha', '').strip()

    params = {
        'email': email,
        'password': password,
        'confirm': confirm,
        'nickname': nickname
    }

    filed_name, msg = User.signup_check(**params)
    if msg:
        return jsonify(success=False, filed_name=filed_name, error=msg)

    if not captcha:
        return jsonify(success=False, filed_name='captcha', error='Captcha required')

    if email != session.get('email') or captcha != session.get('captcha'):
        return jsonify(success=False, filed_name='captcha', error='Wrong captcha')

    User.signup(email, password, nickname)
    del session['email']
    del session['captcha']
    flash('恭喜您注册成功', 'info')
    return jsonify(success=True, url=url_for('index.index'))


@instance.route('/email_confirm/<token>', methods=['GET'])
@login_required
def confirm(token):
    if current_user.is_confirmed:
        return redirect(url_for('index.index'))

    if current_user.confirm(token):
        flash('您的账户邮箱验证成功', 'info')
    else:
        flash('邮箱验证链接无效或是已经过期', 'info')
    return redirect(url_for('index.index'))


@instance.route('/forget_password', methods=['GET', 'POST'])
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


@instance.route('/reset_password/<token>/<email>', methods=['GET', 'POST'])
def reset_password(token, email):
    if request.method == 'GET':
        return render_template('/reset_password.html')

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


@instance.route('/send_captcha', methods=['POST'])
def send_captcha():
    # 注册给邮件发送验证码
    result = request.get_json(force=True)
    email = result.get('email').strip()
    if not email:
        return jsonify(success=False, error='Email required')

    if not regex_email(email):
        return jsonify(success=False, error='Email format error')

    user = User.objects(email=email).first()
    if user:
        return jsonify(success=False, error='Email is existed')

    # generate confirm token
    captcha = generate_captcha()
    __send_captcha_with_email(email, captcha)

    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(minutes=10)
    session['email'] = email
    session['captcha'] = captcha
    return jsonify(success=True)


def __send_captcha_with_email(email, captcha):
    # get confirm url
    html = render_template('email/email_send_captcha.html', captcha=captcha)

    email = Email(smtp_sever=current_app.config['EMAIL_SMTP_SERVER'],
                  username=current_app.config['EMAIL_USERNAME'],
                  password=current_app.config['EMAIL_PASSWORD'],
                  sender=current_app.config['EMAIL_SENDER'],
                  receivers=[email], subject='注册验证码', html=html)
    email.build_email()
    email.send_email()


@instance.route('/get_login_captcha', methods=['GET'])
def get_login_captcha():
    # 获取登录验证码
    result, img_base64 = generate_verify_code()
    session['login_captcha'] = result
    return jsonify(success=True, data='data:image/jpg;base64,{0}'.format(img_base64), result=result)


@instance.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')
    login_captcha = request.form.get('captcha', type=int)

    filed_name, msg = User.login_check(email, password, login_captcha)
    if msg:
        return jsonify(success=False, filed_name=filed_name, error=msg)

    if login_captcha != session.get('login_captcha'):
        return jsonify(success=False, filed_name='captcha', error='Wrong captcha')

    user = User.objects(email=email).first()
    if not user or not user.verify_password(password):
        return 'email', 'Email and Password do not match', None

    user.login(remember, request.remote_addr)
    del session['login_captcha']

    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    flash('你好, {0}'.format(user.nickname), 'info')
    return jsonify(success=True, url=request.args.get('next') or url_for('index.index'))
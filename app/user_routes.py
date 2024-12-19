from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .forms import RegisterForm, LoginForm, VerificationForm
from .models import User
from . import db, mail
import random
import string
from .email_utils import send_email

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        if not email.endswith('@cuc.edu.cn'):
            flash('必须使用@cuc.edu.cn邮箱注册', 'danger')
            return redirect(url_for('user.register'))
        if User.query.filter_by(email=email).first():
            flash('该邮箱已注册', 'danger')
            return redirect(url_for('user.register'))
        user = User(email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # 发送验证码
        code = ''.join(random.choices(string.digits, k=6))
        session['verification_code'] = code
        session['verifying_user'] = user.id
        send_email('验证码', [email], f'您的验证码是: {code}', mail)

        return redirect(url_for('user.verify'))
    return render_template('register.html', form=form)

@user_bp.route('/verify', methods=['GET','POST'])
def verify():
    form = VerificationForm()
    if form.validate_on_submit():
        code = form.code.data
        if code == session.get('verification_code'):
            user_id = session.get('verifying_user')
            user = User.query.get(user_id)
            if user:
                user.verified = True
                db.session.commit()
            session.pop('verification_code', None)
            session.pop('verifying_user', None)
            flash('验证成功，请登录', 'success')
            return redirect(url_for('user.login'))
        else:
            flash('验证码错误', 'danger')
    return render_template('verify.html', form=form)

@user_bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.verified and not user.is_banned:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('course.index'))
        else:
            flash('登录失败，请检查信息或账号状态', 'danger')
    return render_template('login.html', form=form)

@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect(url_for('course.index'))

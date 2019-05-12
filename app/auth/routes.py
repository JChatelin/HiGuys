from app.auth import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegisterForm, ChangePasswordForm, RequestNewPasswordForm
from app.models import User, db
from app.auth.email import send_reset_password_email


@bp.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username and/or password.")
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next = request.args.get('next')
        if next is None or url_parse(next).decode_netloc() != '':
            next = url_for('core.index')
        return redirect(next)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been registered.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Sign Up', form=form)


@bp.route('/request_new_password', methods=['POST', 'GET'])
def request_new_password():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = RequestNewPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            send_reset_password_email(user)
        flash('Reset email sent, Check you email for instructions.')
        return redirect(url_for('auth.login'))
    return render_template('auth/request_new_password.html', form=form)


@bp.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    user = User.verify_reset_password_token(token)
    if user is None:
        return redirect(url_for('auth.login'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

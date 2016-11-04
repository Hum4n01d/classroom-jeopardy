from flask import Blueprint, render_template, flash, redirect, url_for, g, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

import models
import forms

accounts = Blueprint('accounts', __name__, url_prefix='/accounts')

@accounts.route('/')
def index():
    return 'accounts index'

@accounts.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = forms.LoginForm()

    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)

            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Welcome {}!'.format(user.username))

                return redirect(url_for('index'))
            else:
                flash('Incorrect username or password')

        except models.DoesNotExist:
            flash('Incorrect username or password')

    return render_template('simple_form.pug', heading='Log in', form=form)

@accounts.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = forms.SignupForm()

    if form.validate_on_submit():
        try:
            user = models.User.create(
                username=form.username.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data)
            )
            login_user(user)
            flash('Welcome to Jeopardy, {}! You are now logged in'.format(form.username.data))

            return redirect(url_for('index'))

        except models.IntegrityError:
            flash('That username or email is already registered')

    return render_template('simple_form.pug', heading='Sign up', form=form)

@accounts.route('/log_out')
@login_required
def log_out():
    logout_user()

    flash('You\'ve been logged out!')

    return redirect(url_for('accounts.log_in'))

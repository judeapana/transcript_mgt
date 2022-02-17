from datetime import timedelta

from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user

from transcript.auth.forms import LoginForm
from transcript.auth.models import User
from transcript.auth.utils import InvalidAuthentication
from transcript.auth.views import auth


@auth.route('/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data.strip()
        user = User.query.filter(
            (User.username == username) | (User.email_address == username)).first()
        try:
            if not user:
                raise InvalidAuthentication('Incorrect Username or Password')
            else:
                if user.password != password:
                    raise InvalidAuthentication('Incorrect Username or Password')
                else:
                    if user.role:
                        if user.role == 'ADMIN':
                            login_user(user, remember=form.remember_me.data, duration=timedelta(hours=5))
                            return redirect(url_for('admin.dashboard'))
                        elif user.role == 'SECRETARY':
                            login_user(user, remember=form.remember_me.data, duration=timedelta(hours=5))
                            return redirect(url_for('secretary.dashboard'))
                        else:
                            raise InvalidAuthentication('Login failed')
                    else:
                        raise InvalidAuthentication('Your authentication was unsuccessful')
        except InvalidAuthentication as e:
            flash(str(e), 'error')
            return redirect(request.url)
    return render_template('auth/pages/login.html', form=form, title='TTU Transcript Manager')

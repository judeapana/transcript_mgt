import datetime

from flask import redirect, url_for, flash
from flask_login import logout_user, current_user

from . import auth


@auth.route('/lg', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        current_user.last_logged_in = datetime.datetime.utcnow()
        current_user.save()
        logout_user()
        flash('You have successfully logged out. Goodbye', 'info')
    return redirect(url_for('auth.login'))

from flask import render_template, flash, redirect, url_for

from transcript.auth.forms import RequestRestForm
from transcript.auth.models import User
from transcript.auth.views import auth


@auth.route('/rr/<token>', methods=['POST', 'GET'])
def request_reset(token):
    try:
        user = User.query.filter_by(id=User.authenticate_token(token)['pid']).first()
        if not user:
            flash('Reset link expired or invalid', 'error')
            return redirect(url_for('auth.forgot_password'))
    except Exception as e:
        flash('Reset link expired or invalid', 'error')
        return redirect(url_for('auth.forgot_password'))

    form = RequestRestForm()
    if form.validate_on_submit():
        user.password = form.password.data
        user.save()
        flash('Password Changed', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/pages/request-reset.html', form=form, title='TTU Transcript Manager', token=token)

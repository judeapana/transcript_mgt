from flask import render_template, flash, redirect, request, url_for

from transcript.auth.forms import ForgotPasswordForm
from transcript.auth.tasks import send_email
from transcript.auth.views import auth
from transcript.auth.models import User


@auth.route('/fp', methods=['POST', 'GET'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user:
            token = user.create_token()
            url = url_for('auth.request_reset', token=token, _external=True)
            message = f"""
                Use Link <a href='{url}'>{url}</a> to reset password
                """
            send_email.queue([user.email_address], message, subject="Reset Password")
            flash('Please check your mail', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email address not found', 'error')
            return redirect(request.url)
    return render_template('auth/pages/forgot-password.html', form=form, title='TTU Transcript Manager')

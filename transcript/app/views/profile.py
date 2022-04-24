from flask import render_template, request, redirect, url_for
from flask_login import current_user, logout_user

from transcript.app.forms import UserAccForm, UserAccChangePassword
from transcript.app.views import app
from transcript.utils import file_upload


@app.route('/pf', methods=['GET', 'POST'])
def profile():
    form = UserAccForm(prefix='acc', obj=current_user)
    pwd_form = UserAccChangePassword(prefix='pwd')
    option = request.args.get('option', type=str)
    filename = current_user.img
    if option == 'acc':
        if form.validate_on_submit():
            form.populate_obj(current_user)

            if form.img.data and not isinstance(form.img.data, str):
                file_data = file_upload(form.img, dir='users')
                current_user.img = file_data.get('filename')
                file_data.get('upload').save(file_data.get('full_path'))
            else:
                current_user.img = filename
            current_user.save(message='Account has been successfully updated')
            return redirect(request.url)
    if option == 'pwd':
        if pwd_form.validate_on_submit():
            current_user.password = pwd_form.new_password.data
            current_user.save(message='Password  has been successfully changed')
            logout_user()
            return redirect(url_for('auth.logout'))
    return render_template('app/profile.html', title='Profile', form=form, pwd_form=pwd_form)

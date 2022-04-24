import secrets
from collections import namedtuple

from flask import render_template, request, redirect, flash, jsonify, url_for

from transcript.app.forms import UploadForm
from transcript.app.views import app
from transcript.auth.forms import CreateUserForm
from transcript.auth.models import User
from transcript.auth.schema import UserSchema
from transcript.ext import db


@app.route('/act', methods=['GET', 'POST', 'DELETE'])
def accounts():
    columns = [
        {'title': '', 'data': '_'},
        {'title': 'Action', 'data': 'id'},
        {'title': 'Username', 'data': 'username'},
        {'title': 'Email Address', 'data': 'email_address'},
        {'title': 'Phone Number', 'data': 'phone_number'},
        {'title': 'Role', 'data': 'role'},
        {'title': 'created At', 'data': 'created'},
    ]
    form = CreateUserForm()
    update = request.args.get('update')
    context = {'form': form, 'columns': columns}
    if update:
        obj = User.query.get(update)
        if not obj:
            return redirect(url_for('app.accounts'))
        form = CreateUserForm(obj=obj)
        context.update({'form': form})
        if form.validate_on_submit():
            form.populate_obj(obj)
            obj.save()
            flash('User Updated', 'info')
            return redirect(url_for('app.accounts'))
        return render_template('app/accounts.html', title='Update Accounts', **context)

    if form.validate_on_submit():
        new = User()
        form.populate_obj(new)
        new.save()
        flash('New user has been created', 'info')
        return redirect(request.url)

    if request.method == 'DELETE':
        ids = request.args.get('ids')
        try:
            User.query.filter(User.id.in_(ids.split(','))).delete(synchronize_session='fetch')
            db.session.commit()
            return "Delete Complete"
        except Exception as e:
            return "An Error Occurred"
    if request.method == 'GET' and request.args.get('draw'):
        schema = UserSchema(many=True)
        search = request.args.get('search[value]')
        if search:
            data = User.query.filter(User.username.like(f'%{search}%'))
        else:
            data = User.query
        total_records = User.query.count()
        return jsonify(data=schema.dump(obj=data), draw=request.args.get('draw', type=int),
                       recordsFiltered=total_records, recordsTotal=data.count())

    return render_template('app/accounts.html', title='Create Accounts', **context)


@app.route('/account/upload', methods=['POST', 'GET'])
def upload_account():
    form = UploadForm()
    if request.method == 'POST':
        try:
            errors = []
            dataset = request.get_array(field_name='file')
            prepare = namedtuple('accounts', [col.strip().replace(" ", "_").lower() for col in dataset[0]])
            dataset.pop(0)  # remove header
            skipped = 0
            success = 0
            for item in dataset:
                try:
                    schema = prepare._make(item)
                    _user = User()
                    _user.username = str(schema.username)
                    _user.password = str(schema.password)
                    _user.email_address = str(schema.email_address)
                    _user.phone_number = str(schema.phone_number)
                    _user.role = str(schema.role)
                    _user.save()
                    success += 1
                except Exception as e:
                    db.session.rollback()
                    errors.append(dict(data=item, error=str(e)))
            if errors:
                return jsonify(key=secrets.token_hex(4), records=len(dataset), skipped=skipped, total=success,
                               errors=len(errors), detail=errors)
        except Exception as e:
            return jsonify(message=e.__str__()), 400
    return render_template('app/accounts-upload.html', form=form, title="Upload Accounts")

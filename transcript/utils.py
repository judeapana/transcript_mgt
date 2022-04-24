import json
import os
import secrets
from functools import wraps

from PIL import Image
from flask import flash, current_app, abort
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import Timestamp
from werkzeug.utils import secure_filename

from transcript.ext import db


class UniqueValidator:
    @classmethod
    def exists(cls, **kwargs):
        query = cls.query.filter_by(**kwargs).first()
        if query:
            return {'message': 'Already exist'}


class ActiveRecord(Timestamp, UniqueValidator):
    def save(self, **kwargs):
        try:
            db.session.add(self)
            db.session.commit()
            if kwargs.get('message'):
                flash(kwargs.get('message'), 'success')
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error Occurred', 'error')
            print(e)
            exit()
            return False

    def delete(self, **kwargs):
        try:
            db.session.delete(self)
            db.session.commit()
            if kwargs.get('message'):
                flash(kwargs.get('message'), 'success')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error Occurred', 'error')


def file_upload(form, resize=(150, 150), dir='docs', static='static'):
    filename = secure_filename(form.data.filename)
    ext = filename.split('.')[-1]
    uploader_name = f'{secrets.token_hex(20)}.{ext}'
    path = os.path.join(current_app.root_path, static, f'private/{dir}/{uploader_name}')
    ret = {'filename': uploader_name, 'upload': form.data, 'full_path': path}
    if ext in ['jpg', 'png', 'jpeg']:
        image = Image.open(form.data)
        image.thumbnail(resize)
        ret['upload'] = image
    return ret


def roles_required(roles):
    def wrapper(func):
        @wraps(func)
        def decorate(*args, **kwargs):
            if not (current_user.role in roles):
                return abort(401)
            return func(*args, **kwargs)

        return decorate

    return wrapper

def read_config_json(path):
    with open(os.path.join(path,), 'r') as f:
        return json.load(f)


def write_config_json(path, data):
    with open(os.path.join(path), '+w') as f:
        f.write(data)
    with open(os.path.join(path), 'r') as f:
        return json.load(f)



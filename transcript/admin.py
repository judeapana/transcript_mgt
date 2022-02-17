import os

from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import Email, Length

from transcript.app.models import Semester, Programme, Student, Department, Course, GradingSystem, StudentResult
from transcript.auth.models import User
from transcript.ext import admin, db


class UserModeView(ModelView):
    can_delete = True
    column_filters = ['username', 'email_address', 'last_logged_in', 'phone_number']
    column_editable_list = ['username', 'email_address', 'phone_number','role']
    can_view_details = True
    column_searchable_list = ['username']
    create_modal = True
    edit_modal = True
    column_exclude_list = ['updated']
    form_excluded_columns = ['updated', 'created', 'last_logged_in']
    form_args = {
        'email_address': {
            'validators': [Email()]
        }, 'username': {
            'validators': [Length(min=5, max=40)]
        }, 'phone_number': {
            'validators': [Length(max=10, min=10)]
        }
    }
    page_size = 50
    can_export = True


path = os.path.join(os.path.dirname(__file__), 'static', 'private')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

admin.add_view(UserModeView(User, db.session))
admin.add_view(ModelView(Semester, db.session))
admin.add_view(ModelView(Programme, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Department, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(GradingSystem, db.session))
admin.add_view(ModelView(StudentResult, db.session))

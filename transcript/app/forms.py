from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import HiddenField, PasswordField
from wtforms.validators import InputRequired, ValidationError, Optional, EqualTo
from wtforms_alchemy import ModelForm, QuerySelectField

from transcript.app.models import StudentResult, Course, Department, Student, Programme, Semester, GradingSystem
from transcript.auth.models import User


class SemesterForm(ModelForm, FlaskForm):
    class Meta:
        model = Semester


class ProgrammeForm(ModelForm, FlaskForm):
    class Meta:
        model = Programme

    department = QuerySelectField('Department', validators=[InputRequired()], query_factory=lambda: Department.query,
                                  get_label='name_of_department')


class StudentForm(ModelForm, FlaskForm):
    class Meta:
        model = Student

    programme = QuerySelectField('Programme', validators=[InputRequired()], query_factory=lambda: Programme.query,
                                 get_label='name')


class DepartmentForm(ModelForm, FlaskForm):
    class Meta:
        model = Department


class CourseForm(ModelForm, FlaskForm):
    class Meta:
        model = Course

    programme = QuerySelectField('Programme', validators=[InputRequired()], query_factory=lambda: Programme.query,
                                 get_label='name')
    semester = QuerySelectField('Semester', validators=[InputRequired()], query_factory=lambda: Semester.query,
                                get_label='name_of_semester')


class StudentResultForm(ModelForm, FlaskForm):
    class Meta:
        model = StudentResult

    student = QuerySelectField('Student', validators=[InputRequired()], query_factory=lambda: Student.query,
                               get_label='matric_no')
    course = QuerySelectField('Course', validators=[InputRequired()], query_factory=lambda: Course.query,
                              get_label=lambda x: f'{x.title}({x.code})')

    def validate_mid_sem(self, value):
        if value.data > 20:
            raise ValidationError('value must not exceed 20')

    def validate_prac_test1(self, value):
        if value.data > 20:
            raise ValidationError('value must not exceed 20')

    def validate_prac_test2(self, value):
        if value.data > 20:
            raise ValidationError('value must not exceed 20')

    def validate_end_of_sem(self, value):
        if value.data > 40:
            raise ValidationError('value must not exceed 40')

    def validate_course(self, value):
        if not value.data.programme == self.student.data.programme:
            raise ValidationError('Please student doesnt offer this course')


class GradingSystemForm(ModelForm, FlaskForm):
    class Meta:
        model = GradingSystem

    option = HiddenField('option')


class TranscriptForm(FlaskForm):
    student = QuerySelectField('Student', validators=[InputRequired()], query_factory=lambda: Student.query,
                               get_label='matric_no')

    from_semester = QuerySelectField('From Semester', validators=[InputRequired()],
                                     query_factory=lambda: Semester.query,
                                     get_label='name_of_semester')
    to_semester = QuerySelectField('To Semester',
                                   query_factory=lambda: Semester.query,
                                   get_label='name_of_semester')


class UserAccForm(ModelForm, FlaskForm):
    class Meta:
        model = User
        only = ['phone_number', 'img', 'username', 'email_address']

    img = FileField('Profile Image', validators=[Optional(), FileAllowed(['png', 'jpg', 'jpeg'])])


class UserAccChangePassword(FlaskForm):
    old_password = PasswordField('Old Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[
        EqualTo('new_password', 'New password doesnt match confirmed password')])

    def validate_old_password(self, old_password):
        if current_user.password != old_password.data:
            raise ValidationError('Please you have entered a wrong old password / mismatch')


class UploadForm(FlaskForm):
    file = FileField('File', validators=[FileRequired(), FileAllowed(['csv'])])

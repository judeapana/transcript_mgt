from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Regexp
from wtforms_alchemy import ModelForm

from transcript.auth.models import User

MESSAGE = 'Password must have a minimum of eight characters, at least one letter and one number'
PASSWORD_RE = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'


class SubmitMixin(FlaskForm):
    submit = SubmitField('Submit')


class LoginForm(SubmitMixin):
    username = StringField('Username', validators=[InputRequired()],
                           render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')


class ForgotPasswordForm(FlaskForm):
    email_address = EmailField('Email Address', validators=[InputRequired(), Email()])


class RequestRestForm(SubmitMixin):
    password = StringField('New Password', validators=[InputRequired(), Regexp(PASSWORD_RE, message=MESSAGE)])


class CreateUserForm(ModelForm, FlaskForm):
    class Meta:
        model = User
        only = ['username', 'email_address', 'role', 'password',
                'phone_number']

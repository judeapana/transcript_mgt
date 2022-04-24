from flask import Blueprint

from transcript.auth.models import User

auth = Blueprint('auth', __name__, template_folder='templates', url_prefix='/')

from transcript.auth.views import login, forgot_password, request_reset, logout


@auth.before_request
def init_user():
    u = User.query.filter(User.username == 'admin').first()
    if not u:
        new_user = User(
            username='admin',
            password='admin',
            email_address='support@ngsapp.com',
            phone_number='0554138989',
            role='ADMIN'
        )
        new_user.save()

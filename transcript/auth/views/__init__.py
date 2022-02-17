from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates', url_prefix='/')

from transcript.auth.views import login, forgot_password, request_reset, logout

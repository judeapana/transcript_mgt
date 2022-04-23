from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer, URLSafeSerializer, BadSignature
from sqlalchemy.ext.hybrid import hybrid_property

from transcript.ext import db, login_manager
from transcript.utils import ActiveRecord


@login_manager.user_loader
def load_user(pk):
    return User.query.get(pk)


class User(db.Model, ActiveRecord, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False, info={'label': 'Username'}, unique=True, )
    password = db.Column(db.String(200), nullable=False)
    email_address = db.Column(db.String(50), nullable=True, info={'label': 'Email Address'}, )
    phone_number = db.Column(db.String(100), info={'label': 'Primary Phone Number'}, nullable=True)
    img = db.Column(db.String(100), default='default-avatar.png')
    last_logged_in = db.Column(db.DateTime)
    role = db.Column(db.Enum('ADMIN', 'EXAMINATION OFFICER', 'SECRETARY',name='role'), nullable=False)

    def create_token(self, expires=3600):
        jst = TimedJSONWebSignatureSerializer(secret_key=current_app.secret_key, expires_in=expires)
        return jst.dumps({'pid': str(self.id)})

    def qrcode_token(self):
        jws = URLSafeSerializer(secret_key=current_app.secret_key)
        return jws.dumps({'pid': self.id})

    @staticmethod
    def qrcode_decode(token):
        try:
            jst = URLSafeSerializer(secret_key=current_app.secret_key)
            return jst.loads(token)
        except BadSignature:
            return None

    @hybrid_property
    def pwd_create_token(self, expires=3600):
        jst = TimedJSONWebSignatureSerializer(secret_key=current_app.secret_key, expires_in=expires)
        return jst.dumps({'pid': str(self.id)}).decode('utf-8')

    @staticmethod
    def authenticate_token(token):
        try:
            jst = TimedJSONWebSignatureSerializer(secret_key=current_app.secret_key)
            return jst.loads(token)
        except BadSignature:
            return None

import os

from flask import current_app


class LocalConfig:
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:apana1jude1@localhost/ttu_tran_mgt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '67ad41191a14125b92a988d6f1a8112a8b9f20a4'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'niftytester@gmail.com'
    MAIL_PASSWORD = '----'
    MAIL_DEFAULT_SENDER = 'niftytester@gmail.com'
    MAIL_ASCII_ATTACHMENTS = True
    FLASK_APP = 'app.py'
    RQ_REDIS_URL = 'redis://localhost:6379/1'
    RQ_QUEUES = ['ttu_default']
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    APP_MAX_LENGTH = 3
    APP_NAME = 'Tamale Technical University'
    PAGINATE_RESOURCE_LINKS_ENABLED = True
    FLASK_ADMIN_SWATCH = 'cerulean'
    TOASTR_POSITION_CLASS = 'toast-bottom-right'
    SETTING_PATH = os.path.join(os.getcwd(), 'setting.conf.json')
    GOOGLE_FONT_KEY = "AIzaSyC08N9GP2kyNMeIxS_x1VZ_GfqX1weuWtg"


class ServerConfig(LocalConfig):
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_POOL_TIMEOUT = 20
    MAIL_SERVER = 'localhost'
    MAIL_USERNAME = 'transcript@ngsapp.com'
    MAIL_PASSWORD = ''
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = ''
    SQLALCHEMY_DATABASE_URI = 'postgresql://ngs:Ngsappdb123$@localhost/ttu_tran_mgt'
    ENV = 'production'
    DEBUG = False

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
    MAIL_PASSWORD = 'apana1jude1$$'
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


class ServerConfig(LocalConfig):
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_POOL_TIMEOUT = 20
    MAIL_SERVER = ''
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ''
    SQLALCHEMY_DATABASE_URI = 'postgresql://ngs:Ngsappdb123$@localhost/ttu_tran_mgt'
    ENV = 'production'
    DEBUG = False

import flask_excel
from flask import Flask, render_template

from transcript.app.models import db
from transcript.auth.models import db
from transcript.config import LocalConfig
from transcript.ext import migrate, mail, ma, login_manager, rq, toastr, maintenance, menu, qrcode, alchemydumps, hz, \
    pagination, csrf
from .admin import admin


def create_app(config=LocalConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    # csrf.init_app(app)
    admin.init_app(app)
    menu.init_app(app)
    pagination.init_app(app)
    maintenance.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'
    mail.init_app(app)
    alchemydumps.init_app(app, db)
    ma.init_app(app)
    rq.init_app(app)
    hz.init_app(app)
    qrcode.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    app.register_blueprint(application)
    app.register_blueprint(auth)
    toastr.init_app(app)
    flask_excel.init_excel(app)

    @app.errorhandler(503)
    def under_maintenance(e):
        return render_template('503.html', title='Maintenance', code=503, e=e), 503

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html', title='Unavailable', code=500, e=e), 500

    @app.errorhandler(404)
    def not_found(e):
        return render_template('400.html', title='Not Found', code=404, e=e)

    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('401.html', title='Unauthorized', code=401, e=e)

    @app.context_processor
    def f():
        return dict(dir=dir)

    return app


from transcript.app.views import app as application
from transcript.auth.views import auth

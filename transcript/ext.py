from flask_admin import Admin
from flask_alchemydumps import AlchemyDumps
from flask_autocrud import AutoCrud
from flask_humanize import Humanize
from flask_login import LoginManager
from flask_mail import Mail
from flask_maintenance import Maintenance
from flask_marshmallow import Marshmallow
from flask_menu import Menu
from flask_migrate import Migrate
from flask_qrcode import QRcode
from flask_rest_paginate import Pagination
from flask_rq2 import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr
from flask_wtf import CSRFProtect


csrf = CSRFProtect()

admin = Admin()
auto = AutoCrud()
login_manager = LoginManager()
pagination = Pagination()
mail = Mail()
migrate = Migrate()
db = SQLAlchemy()
ma = Marshmallow()
menu = Menu()
alchemydumps = AlchemyDumps()
hz = Humanize()
rq = RQ()
CURRENCY = 'GHS'
maintenance = Maintenance()
toastr = Toastr()
qrcode = QRcode()

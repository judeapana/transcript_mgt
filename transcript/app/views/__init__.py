import os

from flask import Blueprint, send_from_directory, current_app
from flask_login import login_required

app = Blueprint('app', __name__, template_folder='templates', url_prefix='/app')
from transcript.app.views import account, course, dashboard, department, grading_system, profile, reporting, semester, \
    student, student_results, settings, upload_templates, programme


@app.route('protected/<path:filename>')
@login_required
def protected(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'private'), filename=filename)


@app.before_request
@login_required
def route_protected():
    pass

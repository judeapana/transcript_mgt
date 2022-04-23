from flask import Blueprint

app = Blueprint('app', __name__, template_folder='templates', url_prefix='/app')
from transcript.app.views import account, course, dashboard, department, grading_system, profile, reporting, semester, \
    student, student_results, settings

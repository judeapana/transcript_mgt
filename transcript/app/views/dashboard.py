from flask import render_template

from transcript.app.models import Student, Course
from transcript.app.schema import StatisticsSchema
from transcript.app.views import app
from transcript.auth.models import User


@app.route('/')
def dashboard():
    return render_template('app/dashboard.html', title='Dashboard')


@app.route('/statistics')
def statistics():
    schema = StatisticsSchema()
    return schema.dumps(obj=dict(students=Student.query.count(),
                        courses=Course.query.count(),
                        users=User.query.count(),
                        transcripts=0))

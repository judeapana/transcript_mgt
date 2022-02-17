from flask import render_template

from transcript.app.views import app


@app.route('/')
def dashboard():
    return render_template('app/dashboard.html', title='Dashboard')

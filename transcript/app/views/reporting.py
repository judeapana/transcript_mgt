from flask import render_template

from transcript.app.views import app


@app.route('/rp')
def reporting():
    return render_template('app/reporting.html', title='Reporting')

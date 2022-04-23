from flask import render_template, request, flash

from transcript.app.forms import TranscriptForm
from transcript.app.views import app


@app.route('/rp')
def reporting():
    form = TranscriptForm(request.args)
    results = None
    if request.args.get('student'):
        results = form.student.data.student_results.all()
        if results:
            flash('Transcript Generated', 'info')
        else:
            flash('No Data Generated', 'info')
    return render_template('app/reporting.html', title='Reporting', form=form, results=results)

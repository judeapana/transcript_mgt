from flask import render_template

from transcript.app.views import app


@app.route('/pf', methods=['GET', 'POST'])
def profile():
    return render_template('app/profile.html', title='Profile')


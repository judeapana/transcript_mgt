from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import or_

from transcript.app.forms import GradingSystemForm
from transcript.app.models import GradingSystem
from transcript.app.schema import GradingSystemSchema
from transcript.app.views import app
from transcript.ext import db


@app.route('/gs', methods=['GET', 'POST', 'DELETE'])
def grading_system():
    columns = [
        {'title': '', 'data': '_'},
        {'title': 'Action', 'data': 'id'},
        {'title': 'created At', 'data': 'created'},
    ]
    form = GradingSystemForm()
    update = request.args.get('update')
    context = {'form': form, 'columns': columns}
    if update:
        obj = GradingSystem.query.get(update)
        if not obj:
            return redirect(url_for('app.student_results'))
        form = GradingSystemForm(obj=obj)
        context.update({'form': form})
        if form.validate_on_submit():
            form.populate_obj(obj)
            obj.save()
            flash('Results,transcript Updated', 'info')
            return redirect(url_for('app.student_results'))
        return render_template('app/student-results.html', title='Update Student Results Archive', **context)

    if form.validate_on_submit():
        new = GradingSystem()
        form.populate_obj(new)
        new.save()
        flash('Grading System has been created', 'info')
        return redirect(request.url)

    if request.method == 'DELETE':
        ids = request.args.get('ids')
        try:
            GradingSystem.query.filter(GradingSystem.id.in_(ids.split(','))).delete(synchronize_session='fetch')
            db.session.commit()
            return "Delete Complete"
        except Exception as e:
            return "An Error Occurred"
    if request.method == 'GET' and request.args.get('draw'):
        schema = GradingSystemSchema(many=True)
        search = request.args.get('search[value]')
        if search:
            data = GradingSystem.query.filter(or_(GradingSystem.name_of_schema.like(f'%{search}%')))
        else:
            data = GradingSystem.query
        total_records = GradingSystem.query.count()
        return jsonify(data=schema.dump(obj=data), draw=request.args.get('draw', type=int),
                       recordsFiltered=total_records, recordsTotal=data.count())

    return render_template('app/grading-system.html', title='Grading Scheme', **context)

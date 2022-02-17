from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import or_

from transcript.app.forms import SemesterForm
from transcript.app.models import Semester
from transcript.app.schema import SemesterSchema
from transcript.app.views import app
from transcript.ext import db


@app.route('/sm', methods=['GET', 'POST', 'DELETE'])
def semesters():
    columns = [
        {'title': '', 'data': '_'},
        {'title': 'Action', 'data': 'id'},
        {'title': 'Academic Year', 'data': 'name_of_academic_year'},
        {'title': 'Semester', 'data': 'name_of_semester'},
        {'title': 'created At', 'data': 'created'},

    ]
    form = SemesterForm()
    update = request.args.get('update')
    context = {'form': form, 'columns': columns}
    if update:
        obj = Semester.query.get(update)
        if not obj:
            return redirect(url_for('app.semesters'))
        form = SemesterForm(obj=obj)
        context.update({'form': form})
        if form.validate_on_submit():
            form.populate_obj(obj)
            obj.save()
            flash('Semester Updated', 'info')
            return redirect(url_for('app.semesters'))
        return render_template('app/semester.html', title='Update Semester', **context)

    if form.validate_on_submit():
        new = Semester()
        form.populate_obj(new)
        new.save()
        flash('Department has been created', 'info')
        return redirect(request.url)

    if request.method == 'DELETE':
        ids = request.args.get('ids')
        try:
            Semester.query.filter(Semester.id.in_(ids.split(','))).delete(synchronize_session='fetch')
            db.session.commit()
            return "Delete Complete"
        except Exception as e:
            return "An Error Occurred"
    if request.method == 'GET' and request.args.get('draw'):
        schema = SemesterSchema(many=True)
        search = request.args.get('search[value]')
        if search:
            data = Semester.query.filter(
                or_(Semester.name_of_semester.like(f'%{search}%'), Semester.name_of_academic_year.like(f'%{search}%')))
        else:
            data = Semester.query
        total_records = Semester.query.count()
        return jsonify(data=schema.dump(obj=data), draw=request.args.get('draw', type=int),
                       recordsFiltered=total_records, recordsTotal=data.count())

    return render_template('app/semester.html', title='Create Semester', **context)

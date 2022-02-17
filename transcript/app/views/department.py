from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import or_

from transcript.app.forms import DepartmentForm
from transcript.app.models import Department
from transcript.app.schema import DepartmentSchema
from transcript.app.views import app
from transcript.ext import db


@app.route('/dp', methods=['GET', 'POST', 'DELETE'])
def departments():
    columns = [
        {'title': '', 'data': '_'},
        {'title': 'Action', 'data': 'id'},
        {'title': 'Department', 'data': 'name_of_department'},
        {'title': 'Faculty', 'data': 'name_of_faculty'},
        {'title': 'Code', 'data': 'code'},
        {'title': 'created At', 'data': 'created'},
    ]
    form = DepartmentForm()
    update = request.args.get('update')
    context = {'form': form, 'columns': columns}
    if update:
        obj = Department.query.get(update)
        if not obj:
            return redirect(url_for('app.departments'))
        form = DepartmentForm(obj=obj)
        context.update({'form': form})
        if form.validate_on_submit():
            form.populate_obj(obj)
            obj.save()
            flash('Department Updated', 'info')
            return redirect(url_for('app.departments'))
        return render_template('app/departments.html', title='Update Departments', **context)

    if form.validate_on_submit():
        new = Department()
        form.populate_obj(new)
        new.save()
        flash('Department has been created', 'info')
        return redirect(request.url)

    if request.method == 'DELETE':
        ids = request.args.get('ids')
        try:
            Department.query.filter(Department.id.in_(ids.split(','))).delete(synchronize_session='fetch')
            db.session.commit()
            return "Delete Complete"
        except Exception as e:
            return "An Error Occurred"
    if request.method == 'GET' and request.args.get('draw'):
        schema = DepartmentSchema(many=True)
        search = request.args.get('search[value]')
        if search:
            data = Department.query.filter(
                or_(Department.name_of_department.like(f'%{search}%'), Department.name_of_faculty.like(f'%{search}%')))
        else:
            data = Department.query
        total_records = Department.query.count()
        return jsonify(data=schema.dump(obj=data), draw=request.args.get('draw', type=int),
                       recordsFiltered=total_records, recordsTotal=data.count())

    return render_template('app/departments.html', title='Create Departments', **context)

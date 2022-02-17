from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import or_

from transcript.app.forms import StudentForm
from transcript.app.models import Student
from transcript.app.schema import StudentSchema
from transcript.app.views import app
from transcript.ext import db


@app.route('/std', methods=['GET', 'POST', 'DELETE'])
def students():
    columns = [
        {'title': '', 'data': '_'},
        {'title': 'Action', 'data': 'id'},
        {'title': 'Matric No', 'data': 'matric_no'},
        {'title': 'First Name', 'data': 'first_name'},
        {'title': 'Last Name', 'data': 'last_name'},
        {'title': 'Middle Name', 'data': 'middle_name'},
        {'title': 'Gender', 'data': 'gender'},
        {'title': 'created At', 'data': 'created'},
    ]
    form = StudentForm()
    update = request.args.get('update')
    context = {'form': form, 'columns': columns}
    if update:
        obj = Student.query.get(update)
        if not obj:
            return redirect(url_for('app.students'))
        form = StudentForm(obj=obj)
        context.update({'form': form})
        if form.validate_on_submit():
            form.populate_obj(obj)
            obj.save()
            flash('Student Updated', 'info')
            return redirect(url_for('app.students'))
        return render_template('app/students.html', title='Update Students', **context)

    if form.validate_on_submit():
        new = Student()
        form.populate_obj(new)
        new.save()
        flash('Student has been created', 'info')
        return redirect(request.url)

    if request.method == 'DELETE':
        ids = request.args.get('ids')
        try:
            Student.query.filter(Student.id.in_(ids.split(','))).delete(synchronize_session='fetch')
            db.session.commit()
            return "Delete Complete"
        except Exception as e:
            return "An Error Occurred"
    if request.method == 'GET' and request.args.get('draw'):
        schema = StudentSchema(many=True)
        search = request.args.get('search[value]')
        if search:
            data = Student.query.filter(
                or_(Student.matric_no.like(f'%{search}%'), Student.gender.like(f'%{search}%')))
        else:
            data = Student.query
        total_records = Student.query.count()
        return jsonify(data=schema.dump(obj=data), draw=request.args.get('draw', type=int),
                       recordsFiltered=total_records, recordsTotal=data.count())

    return render_template('app/students.html', title='Create Students', **context)

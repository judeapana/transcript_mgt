from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import or_

from transcript.app.forms import StudentResultForm, StudentForm
from transcript.app.models import StudentResult, Student
from transcript.app.schema import StudentResultSchema
from transcript.app.views import app
from transcript.ext import db


@app.route('/std-res', methods=['GET', 'POST', 'DELETE'])
def student_results():
    columns = [
        {'title': '', 'data': '_'},
        {'title': 'Action', 'data': 'id'},
        # {'title': 'Student', 'data': 'student'},
        {'title': 'Option', 'data': 'option'},
        # {'title': 'Course', 'data': ' course'},
        {'title': 'Mid Sem', 'data': 'mid_sem'},
        {'title': 'Prac T1', 'data': 'prac_test1'},
        {'title': 'Prac T2', 'data': 'prac_test2'},
        {'title': 'End of Sem', 'data': 'end_of_sem'},
        {'title': 'created At', 'data': 'created'},
    ]
    form = StudentResultForm()
    update = request.args.get('update')
    context = {'form': form, 'columns': columns}
    if update:
        obj = StudentResult.query.get(update)
        if not obj:
            return redirect(url_for('app.student_results'))
        form = StudentResultForm(obj=obj)
        context.update({'form': form})
        if form.validate_on_submit():
            form.populate_obj(obj)
            obj.save()
            flash('Results,transcript Updated', 'info')
            return redirect(url_for('app.student_results'))
        return render_template('app/student-results.html', title='Update Student Results Archive', **context)

    if form.validate_on_submit():
        new = StudentResult()
        form.populate_obj(new)
        new.save()
        flash('Student has been created', 'info')
        return redirect(request.url)

    if request.method == 'DELETE':
        ids = request.args.get('ids')
        try:
            StudentResult.query.filter(StudentResult.id.in_(ids.split(','))).delete(synchronize_session='fetch')
            db.session.commit()
            return "Delete Complete"
        except Exception as e:
            return "An Error Occurred"
    if request.method == 'GET' and request.args.get('draw'):
        schema = StudentResultSchema(many=True)
        search = request.args.get('search[value]')
        if search:
            data = StudentResult.query.join(Student, StudentResult.student_id == Student.id).filter(
                or_(Student.matric_no.like(f'%{search}%'), Student.gender.like(f'%{search}%')))
        else:
            data = StudentResult.query
        total_records = StudentResult.query.count()
        return jsonify(data=schema.dump(obj=data), draw=request.args.get('draw', type=int),
                       recordsFiltered=total_records, recordsTotal=data.count())

    return render_template('app/student-results.html', title='Create Student Results Archive', **context)

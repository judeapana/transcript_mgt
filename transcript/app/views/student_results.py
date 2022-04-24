import secrets
from collections import namedtuple

from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import or_

from transcript.app.forms import StudentResultForm, UploadForm
from transcript.app.models import StudentResult, Student, Course
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
        {'title': 'Total C.A', 'data': 'total_continuous_assem'},
        {'title': 'Total', 'data': 'total'},
        {'title': 'Remark', 'data': 'grade'},
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


@app.route('/results/upload', methods=['POST', 'GET'])
def upload_results():
    form = UploadForm()
    if request.method == 'POST':
        try:
            errors = []
            dataset = request.get_array(field_name='file')
            prepare = namedtuple('results', [col.strip().replace(" ", "_").lower() for col in dataset[0]])
            dataset.pop(0)  # remove header
            skipped = 0
            success = 0
            for item in dataset:
                try:
                    schema = prepare._make(item)
                    item = StudentResult()
                    item.matric_no = str(schema.matric_no)
                    item.first_name = str(schema.first_name)
                    item.last_name = str(schema.last_name)
                    item.middle_name = str(schema.middle_name)
                    item.gender = str(schema.gender)
                    item.credit_hours = str(schema.credit_hours)
                    student = Student.query.filter(Student.matric_no == str(schema.matric_no)).first()
                    if not student:
                        skipped += 1
                        continue
                    course = Course.query.filter(
                        or_(Course.title == str(schema.course), Course.code == str(schema.code))).first()
                    if not course:
                        skipped += 1
                        continue
                    if not course.programme_id == student.programme_id:
                        skipped += 1
                        continue
                    item.student = student
                    item.course = course
                    item.save()
                    success += 1
                except Exception as e:
                    db.session.rollback()
                    errors.append(dict(data=item, error=str(e)))
            if errors:
                return jsonify(key=secrets.token_hex(4), records=len(dataset), skipped=skipped, total=success,
                               errors=len(errors), detail=errors)
        except Exception as e:
            return jsonify(message=e.__str__()), 400
    return render_template('app/results-upload.html', form=form, title="Upload Student Results")

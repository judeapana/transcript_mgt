import secrets
from collections import namedtuple

from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import or_

from transcript.app.forms import StudentForm, UploadForm
from transcript.app.models import Student, Programme
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


@app.route('/students/upload', methods=['POST', 'GET'])
def upload_students():
    form = UploadForm()
    if request.method == 'POST':
        try:
            errors = []
            dataset = request.get_array(field_name='file')
            prepare = namedtuple('student', [col.strip().replace(" ", "_").lower() for col in dataset[0]])
            dataset.pop(0)  # remove header
            skipped = 0
            success = 0
            for item in dataset:
                try:
                    schema = prepare._make(item)
                    item = Student()
                    item.matric_no = str(schema.matric_no)
                    item.first_name = str(schema.first_name)
                    item.last_name = str(schema.last_name)
                    item.middle_name = str(schema.middle_name)
                    item.gender = str(schema.gender)
                    item.credit_hours = str(schema.credit_hours)
                    programme = Programme.query.filter(Programme.name == str(schema.programme)).first()
                    if not programme:
                        skipped += 1
                        continue

                    item.programme = programme
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
    return render_template('app/student-upload.html', form=form, title="Upload Students")

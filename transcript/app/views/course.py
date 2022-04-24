import secrets
from collections import namedtuple

from flask import render_template, jsonify, request, redirect, url_for, flash
from sqlalchemy import or_

from transcript.app.forms import CourseForm, UploadForm
from transcript.app.models import Course, Programme, Semester
from transcript.app.schema import CourseSchema
from transcript.app.views import app
from transcript.ext import db


@app.route('/cs', methods=['GET', 'POST', 'DELETE'])
def courses():
    columns = [
        {'title': '', 'data': '_'},
        {'title': 'Action', 'data': 'id'},
        {'title': 'Title', 'data': 'title'},
        {'title': 'Abbreviation', 'data': 'abbr'},
        {'title': 'Code', 'data': 'code'},
        {'title': 'Type', 'data': 'course_type'},
        {'title': 'Credits', 'data': 'credit_hours'},
        {'title': 'created At', 'data': 'created'},
    ]
    form = CourseForm()
    update = request.args.get('update')
    context = {'form': form, 'columns': columns}
    if update:
        obj = Course.query.get(update)
        if not obj:
            return redirect(url_for('app.courses'))
        form = CourseForm(obj=obj)
        context.update({'form': form})
        if form.validate_on_submit():
            form.populate_obj(obj)
            obj.save()
            flash('Course Updated', 'info')
            return redirect(url_for('app.courses'))
        return render_template('app/courses.html', title='Update Course', **context)

    if form.validate_on_submit():
        new = Course()
        form.populate_obj(new)
        new.save()
        flash('Course has been created', 'info')
        return redirect(request.url)

    if request.method == 'DELETE':
        ids = request.args.get('ids')
        try:
            Course.query.filter(Course.id.in_(ids.split(','))).delete(synchronize_session='fetch')
            db.session.commit()
            return "Delete Complete"
        except Exception as e:
            return "An Error Occurred"
    if request.method == 'GET' and request.args.get('draw'):
        schema = CourseSchema(many=True)
        search = request.args.get('search[value]')
        if search:
            data = Course.query.filter(or_(Course.title.like(f'%{search}%'), Course.code.like(f'%{search}%')))
        else:
            data = Course.query
        total_records = Course.query.count()
        return jsonify(data=schema.dump(obj=data), draw=request.args.get('draw', type=int),
                       recordsFiltered=total_records, recordsTotal=data.count())

    return render_template('app/courses.html', title='Create Courses', **context)


@app.route('/course/upload', methods=['POST', 'GET'])
def upload_course():
    form = UploadForm()
    if request.method == 'POST':
        try:
            errors = []
            dataset = request.get_array(field_name='file')
            prepare = namedtuple('course', [col.strip().replace(" ", "_").lower() for col in dataset[0]])
            dataset.pop(0)  # remove header
            skipped = 0
            success = 0
            for item in dataset:
                try:
                    schema = prepare._make(item)
                    item = Course()
                    item.title = str(schema.title).strip()
                    item.abbr = str(schema.abbr).strip()
                    item.code = str(schema.code).strip()
                    item.course_type = str(schema.course_type)
                    item.credit_hours = int(schema.credit_hours)
                    programme = Programme.query.filter(Programme.name == str(schema.programme).strip()).first()
                    if not programme:
                        skipped += 1
                        errors.append({'error': 'Programme doesnt exist check name', 'data': item})
                        continue
                    semester = Semester.query.filter(Semester.name_of_semester == str(schema.semester).strip()).first()

                    if not semester:
                        skipped += 1
                        errors.append({'error': 'Semester doesnt exist check name of semester', 'data': item})
                        continue

                    item.programme = programme
                    item.semester = semester
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
    return render_template('app/course-upload.html', form=form, title="Upload Accounts")

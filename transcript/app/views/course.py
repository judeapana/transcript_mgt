from flask import render_template, jsonify, request, redirect, url_for, flash
from sqlalchemy import or_

from transcript.app.forms import CourseForm
from transcript.app.models import Course
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

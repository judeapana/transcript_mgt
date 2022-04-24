from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import or_

from transcript.app.forms import ProgrammeForm
from transcript.app.models import Programme
from transcript.app.schema import ProgrammeSchema
from transcript.app.views import app
from transcript.ext import db


@app.route('/pg', methods=['GET', 'POST', 'DELETE'])
def programme():
    columns = [
        {'title': '', 'data': '_'},
        {'title': 'Action', 'data': 'id'},
        {'title': 'Name', 'data': 'name'},
        {'title': 'Category', 'data': 'category'},
        {'title': 'Duration', 'data': 'duration'},
        # {'title': 'Department', 'data': 'department.name_of_department'},
        {'title': 'created At', 'data': 'created'},
    ]
    form = ProgrammeForm()
    update = request.args.get('update')
    context = {'form': form, 'columns': columns}
    if update:
        obj = Programme.query.get(update)
        if not obj:
            return redirect(url_for('app.programme'))
        form = ProgrammeForm(obj=obj)
        context.update({'form': form})
        if form.validate_on_submit():
            form.populate_obj(obj)
            obj.save()
            flash('Programme Updated', 'info')
            return redirect(url_for('app.programme'))
        return render_template('app/programme.html', title='Update Programme', **context)

    if form.validate_on_submit():
        new = Programme()
        form.populate_obj(new)
        new.save()
        flash('Programme has been created', 'info')
        return redirect(request.url)

    if request.method == 'DELETE':
        ids = request.args.get('ids')
        try:
            Programme.query.filter(Programme.id.in_(ids.split(','))).delete(synchronize_session='fetch')
            db.session.commit()
            return "Delete Complete"
        except Exception as e:
            return "An Error Occurred"
    if request.method == 'GET' and request.args.get('draw'):
        schema = ProgrammeSchema(many=True)
        search = request.args.get('search[value]')
        if search:
            data = Programme.query.filter(
                or_(Programme.name.like(f'%{search}%'), Programme.category.like(f'%{search}%')))
        else:
            data = Programme.query
        total_records = Programme.query.count()
        return jsonify(data=schema.dump(obj=data), draw=request.args.get('draw', type=int),
                       recordsFiltered=total_records, recordsTotal=data.count())

    return render_template('app/programme.html', title='Create Programme', **context)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms_alchemy import ModelForm, QuerySelectField

from transcript.app.models import StudentResult, Course, Department, Student, Programme, Semester, GradingSystem


class SemesterForm(ModelForm, FlaskForm):
    class Meta:
        model = Semester


class ProgrammeForm(ModelForm, FlaskForm):
    class Meta:
        model = Programme

    department = QuerySelectField('Department', validators=[InputRequired()], query_factory=lambda: Department.query,
                                  get_label='name')


class StudentForm(ModelForm, FlaskForm):
    class Meta:
        model = Student

    programme = QuerySelectField('Programme', validators=[InputRequired()], query_factory=lambda: Programme.query,
                                 get_label='name')


class DepartmentForm(ModelForm, FlaskForm):
    class Meta:
        model = Department


class CourseForm(ModelForm, FlaskForm):
    class Meta:
        model = Course

    programme = QuerySelectField('Programme', validators=[InputRequired()], query_factory=lambda: Programme.query,
                                 get_label='name')
    semester = QuerySelectField('Semester', validators=[InputRequired()], query_factory=lambda: Semester.query,
                                get_label='name_of_semester')


class StudentResultForm(ModelForm, FlaskForm):
    class Meta:
        model = StudentResult

    student = QuerySelectField('Student', validators=[InputRequired()], query_factory=lambda: Student.query,
                               get_label='matric_no')
    course = QuerySelectField('Course', validators=[InputRequired()], query_factory=lambda: Course.query,
                              get_label=lambda x: f'{x.title}({x.code})')


class GradingSystemForm(ModelForm, FlaskForm):
    class Meta:
        model = GradingSystem

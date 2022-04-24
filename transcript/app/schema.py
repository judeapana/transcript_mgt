from marshmallow import fields

from transcript.app.models import GradingSystem, Course, Department, Student, Programme, Semester, StudentResult
from transcript.ext import ma


class SemesterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Semester
        include_fk = True
        load_instance = True
        include_relationships = True


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        include_fk = True
        load_instance = True
        include_relationships = True


class ProgrammeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Programme
        include_fk = True
        load_instance = True
        include_relationships = True

    department = fields.Nested(DepartmentSchema)


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        include_fk = True
        load_instance = True
        include_relationships = True


class StudentResultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentResult
        include_fk = True
        load_instance = True
        include_relationships = True

    total_continuous_assem = fields.Function(lambda x: x.total_continuous_assem)
    total = fields.Function(lambda x: x.total)
    grade = fields.Function(lambda x: x.grade)


class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        include_fk = True
        load_instance = True
        include_relationships = True


class GradingSystemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GradingSystem
        include_fk = True
        load_instance = True
        include_relationships = True


class StatisticsSchema(ma.Schema):
    students = fields.Integer(required=True)
    courses = fields.Integer(required=True)
    users = fields.Integer(required=True)
    transcripts = fields.Integer()

from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy_utils import ChoiceType

from transcript.ext import db
from transcript.utils import ActiveRecord


class Semester(db.Model, ActiveRecord):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name_of_academic_year = db.Column(db.String(100), nullable=False)
    name_of_semester = db.Column(db.String(100), nullable=False)
    courses = db.relationship('Course', backref=db.backref('semester'), cascade='all,delete,delete-orphan',
                              lazy='dynamic')

    def __repr__(self):
        return f"{self.name_of_semester} ({self.name_of_academic_year})"


class Programme(db.Model, ActiveRecord):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.Enum('DIPLOMA', 'MASTERS', 'PHD', 'DEGREE', name='category'), nullable=False)
    duration = db.Column(db.Integer, default=True, info={'label': 'Duration(Years)'})
    department_id = db.Column(db.Integer, db.ForeignKey('department.id', ondelete='cascade'), nullable=True)
    students = db.relationship('Student', backref=db.backref('programme'),
                               lazy='dynamic')
    courses = db.relationship('Course', backref=db.backref('programme'),
                              lazy='dynamic')


class Student(db.Model, ActiveRecord):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    matric_no = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    middle_name = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.Enum('Male', 'Female', 'Others', name='gender'), nullable=False)
    programme_id = db.Column(db.Integer, db.ForeignKey('programme.id', ondelete='cascade'), nullable=False)
    student_results = db.relationship('StudentResult', backref=db.backref('student'), lazy='dynamic')


class Department(db.Model, ActiveRecord):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name_of_department = db.Column(db.String(100), nullable=False)
    name_of_faculty = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    programmes = db.relationship('Programme', backref=db.backref('department'), cascade='all,delete,delete-orphan',
                                 lazy='dynamic')


class Course(db.Model, ActiveRecord):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    abbr = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=False)
    course_type = db.Column(db.Enum('Elective', 'Core', name='course_type'), nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)
    programme_id = db.Column(db.Integer, db.ForeignKey('programme.id', ondelete='cascade'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id', ondelete='cascade'), nullable=False)
    results = db.relationship('StudentResult', backref=db.backref('course'), cascade='all,delete,delete-orphan',
                              lazy='dynamic')


class GradingSystem(db.Model, ActiveRecord):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name_of_schema = db.Column(db.String(100), nullable=False)
    option = db.Column(ChoiceType([('PT', 'Practical Test'), ('EX', 'Examination'), ('TT', 'Total')]),
                       nullable=False)
    total_marks = db.Column(db.Float(), nullable=False)
    criteria = db.Column(
        ChoiceType([('<=', 'Less Than Or Equal To'), ('>=', 'Greater Than Or Equal To'), ('>', 'Greater Than'),
                    ('<', 'Less Than'), ('==', 'Equal To')]), nullable=True)
    percentage = db.Column(db.Float(), nullable=True)
    from_score = db.Column(db.Float, nullable=True)
    to_score = db.Column(db.Float, nullable=True)
    grade_point = db.Column(db.Float, nullable=True)
    grade = db.Column(ChoiceType([('NC', 'Not Competent'), ('CD', 'Competent With Distinction'), ('C', 'Competent'),
                                  ('CM', 'Competent With Merit')]))

    # grade = db.Column(db.String(100), nullable=False)

    @hybrid_property
    def strike_score(self):
        return (self.percentage / 100) * self.total_marks


class StudentResult(db.Model, ActiveRecord):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='cascade'), nullable=False, )
    option = db.Column(db.Enum('MAIN', 'RESIT', 'RETAKE', name='option'), default='MAIN', nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='cascade'), nullable=False, )
    mid_sem = db.Column(db.Float(), default=0, nullable=False, info={'label': 'Mid Sem 20%'})
    prac_test1 = db.Column(db.Float(), default=0, nullable=False, info={'label': 'Practical Test 1 20%'})
    prac_test2 = db.Column(db.Float(), default=0, nullable=False, info={'label': 'Practical Test 2 20%'})
    end_of_sem = db.Column(db.Float(), default=0, nullable=False, info={'label': 'End Of Sem 40%'})

    @hybrid_property
    def total_continuous_assem(self):
        """
        (60%)
        :return:
        """
        return self.mid_sem + self.prac_test1 + self.prac_test2

    @hybrid_property
    def total(self):
        return self.total_continuous_assem + self.end_of_sem

    @hybrid_property
    def grade(self):
        rmrks = [self.schema_grading('EX'), self.schema_grading('PT')]
        if "N" in rmrks:
            return {"NC": "Not Competent"}
        else:
            return self.schema_grading('TT')

    @hybrid_method
    def schema_grading(self, option):
        gss = GradingSystem.query.order_by(GradingSystem.percentage).filter(
            GradingSystem.option == option).all()
        if option == 'TT':
            for grade in gss:
                if self.total <= grade.to_score:
                    return grade
        elif option == 'EX' or option == 'PT':
            for gs in gss:
                if gs.criteria == "<":
                    if self.total_continuous_assem < gs.strike_score and option == "PT":
                        return gs.grade
                    if self.end_of_sem < gs.strike_score and option == "EX":
                        return gs.grade
                if gs.criteria == "<=":
                    if self.total_continuous_assem <= gs.strike_score and option == "PT":
                        return gs.grade
                    if self.end_of_sem <= gs.strike_score and option == "EX":
                        return gs.grade
                if gs.criteria == ">":
                    if self.total_continuous_assem > gs.strike_score and option == "PT":
                        return gs.grade
                    if self.end_of_sem > gs.strike_score and option == "EX":
                        return gs.grade
                if gs.criteria == ">=":
                    if self.total_continuous_assem >= gs.strike_score and option == "PT":
                        return gs.grade
                    if self.end_of_sem >= gs.strike_score and option == "EX":
                        return gs.grade
                if gs.criteria == "==":
                    if self.total_continuous_assem == gs.strike_score and option == "PT":
                        return gs.grade
                    if self.end_of_sem == gs.strike_score and option == "EX":
                        return gs.grade
        return 'Not Found'

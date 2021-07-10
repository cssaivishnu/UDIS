from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_of_birth = db.Column(db.String(10), default='01/01/2001')
    contact_number = db.Column(db.String(12), default='123456789')
    address = db.Column(db.String(120), default='Kharagpur')
    sex = db.Column(db.String(10), default='M')
    course_registered = db.Column(db.String(120), default='Computer Science')
    course_taught = db.Column(db.String(120), default='Computer Science')
    user_type = db.Column(db.String(10), default='student')
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    OfferedCourses = db.Column(db.String(20), nullable=False)
    CourseName = db.Column(db.String(20), nullable=False)
    CourseDetails = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return f"Courses('{self.OfferedCourses}', '{self.CourseName}', '{self.CourseDetails}')"

class AcademicDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    Marks = db.Column(db.String(20), nullable=False)
    CGPA = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"AcademicDetails('{self.Marks}', '{self.CGPA}')"


class DepartmentDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    Inventory = db.Column(db.String(20), nullable=False)
    OngoingResearchProjects = db.Column(db.String(20), nullable=False)
    FacultyPublication = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"DepartmentDetails('{self.Inventory}', '{self.OngoingResearchProjects}', '{self.FacultyPublication}')"


class DepartmentAccountDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Deposits = db.Column(db.String(20), nullable=False)
    Expenditure = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f"DepartmentAccountDetails('{self.Deposits}', '{self.Expenditure}')"

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User, Courses, DepartmentDetails, DepartmentAccountDetails


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    date_of_birth = StringField('Date of birth')
    contact_number = StringField('Contact number')
    address = StringField('Address')
    sex = StringField('Sex')
    course_registered = StringField('Course registered')
    course_taught = StringField('Course taught')
    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    date_of_birth = StringField('Date of birth')
    contact_number = StringField('Contact number')
    address = StringField('Address')
    sex = StringField('Sex')
    course_registered = StringField('Course registered')
    course_taught = StringField('Course taught')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class CreateCourseForm(FlaskForm):
    name = StringField('name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    OfferedCourses = StringField('OfferedCourses')
    CourseName = StringField('CourseName', validators=[DataRequired()])
    CourseDetails = StringField('CourseDetails')
    submit = SubmitField('Add')

    def validate_name(self, name):
        course = Courses.query.filter_by(name=name.data).first()
        if course:
            raise ValidationError('That name is taken. Please choose a different one.')

    def validate_email(self, CourseName):
        course = Courses.query.filter_by(CourseName=CourseName.data).first()
        if course:
            raise ValidationError('That Course name is taken. Please choose a different one.')

class UpdateDepartmentDetailsForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired()])
    Inventory = StringField('Inventory',
                        validators=[DataRequired()])
    OngoingResearchProjects = StringField('OngoingResearchProjects')
    FacultyPublication = StringField('FacultyPublication')
    submit = SubmitField('Update')

class UpdateCourseForm(FlaskForm):
    OfferedCourses = StringField('Offered Courses',
                        validators=[DataRequired()])
    CourseName = StringField('Course Name',
                        validators=[DataRequired()])
    CourseDetails = StringField('Course Details',
                        validators=[DataRequired()])
    submit = SubmitField('Update')

class UpdateStudentsGradeForm(FlaskForm):
    Marks = StringField('Marks',
                        validators=[DataRequired()])
    CGPA = StringField('CGPA',
                        validators=[DataRequired()])
    submit = SubmitField('Update')

class UpdateDepartmentAccountDetailsForm(FlaskForm):
    Deposits = StringField('Deposits',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Expenditure = StringField('Expenditure',
                        validators=[DataRequired()])
    submit = SubmitField('Update')

class AcademicDetailsForm(FlaskForm):
    Marks = StringField('Marks',
                           validators=[DataRequired()])
    CGPA = StringField('CGPA',
                        validators=[DataRequired()])
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

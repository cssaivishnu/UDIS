from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Courses, DepartmentDetails, DepartmentAccountDetails, AcademicDetails
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, CreateCourseForm, UpdateDepartmentDetailsForm, UpdateDepartmentAccountDetailsForm, UpdateCourseForm, AcademicDetailsForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, image_file='default.jpg', date_of_birth=form.date_of_birth.data, contact_number=form.contact_number.data, address=form.address.data, sex=form.sex.data, course_registered='none', course_taught='none', user_type='student', password=hashed_password)
        details = AcademicDetails(name = form.username.data, Marks = 'none', CGPA = 'none')
        db.session.add(details)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, type='student')

@users.route("/register_faculty", methods=['GET', 'POST'])
def register_faculty():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, image_file='default.jpg', date_of_birth=form.date_of_birth.data, contact_number=form.contact_number.data, address=form.address.data, sex=form.sex.data, course_registered='none', course_taught=form.course_taught.data, user_type='faculty', password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='register_faculty', form=form, type='faculty')


@users.route("/register_admin", methods=['GET', 'POST'])
def register_admin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, image_file='default.jpg', date_of_birth='none', contact_number='none', address='none', sex='none', course_registered='none', course_taught='none', user_type='admin', password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='register_admin', form=form, type='admin')


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/gallery")
def gallery():
    return render_template('gallery.html')



@users.route("/announcement")
def announcement():
    return render_template('announcement.html')


@users.route("/events")
def events():
    return render_template('events.html')


@users.route("/research")
def research():
    return render_template('research.html')


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file)

@users.route("/update_account", methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        if current_user.user_type=='student':
            details=AcademicDetails.query.filter_by(name=current_user.username).first()
            details.name=form.username.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.sex = form.sex.data
        current_user.address = form.address.data
        current_user.contact_number = form.contact_number.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('update_account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/course/<int:course_id>")
def course(course_id):
    course = Courses.query.get_or_404(course_id)
    return render_template('course.html', course=course)


@users.route("/courses")
def courses():
    courses = Courses.query.all()
    return render_template('courses.html', courses=courses)

@users.route("/student/<int:student_id>")
def student(student_id):
    student = User.query.get_or_404(student_id)
    return render_template('student.html', student=student)


@users.route("/students")
def students():
    students = User.query.filter_by(user_type='student')
    return render_template('students.html', students=students)

@users.route("/faculty/<int:faculty_id>")
def faculty(faculty_id):
    faculty = User.query.get_or_404(faculty_id)
    return render_template('faculty.html', faculty=faculty)


@users.route("/faculties")
def faculties():
    faculties = User.query.filter_by(user_type='faculty')
    return render_template('faculties.html', faculties=faculties)

@users.route("/create_course", methods=['GET', 'POST'])
@login_required
def create_course():
    form = CreateCourseForm()
    if form.validate_on_submit():
        course = Courses(name = form.name.data, OfferedCourses = form.OfferedCourses.data, CourseName = form.CourseName.data, CourseDetails = form.CourseDetails.data )
        db.session.add(course)
        db.session.commit()
        flash('Your course has been added!', 'success')
        return redirect(url_for('users.courses'))
    return render_template('create_course.html', title='Create Course', form=form)


@users.route("/update_department_details", methods=['GET', 'POST'])
@login_required
def update_department_details():
    details = DepartmentDetails.query.all()[0]
    form = UpdateDepartmentDetailsForm()
    if form.validate_on_submit():
        details.name = form.name.data
        details.Inventory = form.Inventory.data
        details.OngoingResearchProjects = form.OngoingResearchProjects.data
        details.FacultyPublication = form.FacultyPublication.data
        db.session.commit()
        flash('Department details has been updated!', 'success')
        return redirect(url_for('users.department_details'))
    return render_template('update_department_details.html', form=form, details=details)

@users.route("/update_courses")
def update_courses():
    courses = Courses.query.all()
    return render_template('update_courses.html', courses=courses)


@users.route("/update_course/<int:course_id>", methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    details = Courses.query.filter_by(id=course_id).first()
    form = UpdateCourseForm()
    if form.validate_on_submit():
        details.CourseName = form.CourseName.data
        details.OfferedCourses = form.OfferedCourses.data
        details.CourseDetails = form.CourseDetails.data
        db.session.commit()
        flash('Course details has been updated!', 'success')
        return redirect(url_for('users.courses'))
    return render_template('update_course.html', form=form, course=details)

@users.route("/select_student")
def select_student():
    students = User.query.filter_by(user_type='student')
    return render_template('select_student.html', students=students)

@users.route("/change_student_grade/<string:name>", methods=['GET', 'POST'])
@login_required
def change_student_grade(name):
    details = AcademicDetails.query.filter_by(name=name).first()
    form = AcademicDetailsForm()
    if form.validate_on_submit():
        details.Marks = form.Marks.data
        details.CGPA = form.CGPA.data
        db.session.commit()
        flash('Academic details has been updated!', 'success')
        return redirect(url_for('users.academic_details', username = name))
    return render_template('change_student_grade.html', form=form, details=details, name=name)

@users.route("/academic_details/<string:username>")
def academic_details(username):
    details = AcademicDetails.query.filter_by(name = username).first()
    return render_template('academic_details.html', details=details)

@users.route("/register_course")
def register_course(username, course_name):
    student = User.query.filter_by(username=student_name)
    student.course_registered = course_name
    flash('Course details has been updated!', 'success')
    return redirect(url_for('users.account'))

@users.route("/view_courses")
def view_courses():
    courses = Courses.query.all()
    return render_template('view_courses.html', courses=courses, name = current_user.username)


@users.route("/department_details")
def department_details():
    department_details = DepartmentDetails.query.all()[0]
    return render_template('department_details.html', details=department_details)

@users.route("/update_department_account_details", methods=['GET', 'POST'])
@login_required
def update_department_account_details():
    details = DepartmentAccountDetails.query.all()[0]
    form = UpdateDepartmentAccountDetailsForm()
    if form.validate_on_submit():
        details.Deposits = form.Deposits.data
        details.Expenditure = form.Expenditure.data
        db.session.commit()
        flash('Department account details has been updated!', 'success')
        return redirect(url_for('users.department_account_details'))
    return render_template('update_department_account_details.html', form=form, details=details)


@users.route("/department_account_details")
def department_account_details():
    department_account_details = DepartmentAccountDetails.query.all()[0]
    return render_template('department_account_details.html', details=department_account_details)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

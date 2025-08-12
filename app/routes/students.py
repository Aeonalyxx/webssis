from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.student_controller import (
    get_students_page, handle_add_student, handle_edit_student, handle_delete_student
)

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
def students_page():
    search_query = request.args.get('search_query', '')
    filter_by = request.args.get('filter_by', '')
    page = int(request.args.get('page', 1))
    per_page = 10

    students, courses, total_pages, start_page, end_page = get_students_page(search_query, filter_by, page, per_page)

    return render_template(
        'students.html',
        students=students,
        courses=courses,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page
    )


@students_bp.route('/add_student', methods=['POST'])
def add_student():
    success, message, category = handle_add_student(
        request.form['student_id'],
        request.form['first_name'],
        request.form['last_name'],
        request.form['gender'],
        request.form.get('course_code'),
        request.form['year'],
        request.files.get('photo')
    )
    flash(message, category)
    return redirect(url_for('students.students_page'))


@students_bp.route('/edit_student/<string:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        success, message, category = handle_edit_student(
            student_id=student_id,
            new_student_id=request.form['student_id'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            gender=request.form['gender'],
            course_code=request.form.get('course_code'),
            year=request.form['year'],
            photo=request.files.get('photo')
        )
        flash(message, category)
        return redirect(url_for('students.students_page'))

    return render_template('edit_student.html', student_id=student_id)


@students_bp.route('/delete_student', methods=['POST'])
def delete_student():
    success, message, category = handle_delete_student(request.form['student_id'])
    flash(message, category)
    return redirect(url_for('students.students_page'))

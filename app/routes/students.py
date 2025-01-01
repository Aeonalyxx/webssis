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
    per_page = 8
    students, courses, total_pages = get_students_page(search_query, filter_by, page, per_page)

    # Calculate the start and end of the pagination range
    start_page = max(page - 2, 1)
    end_page = min(page + 2, total_pages)

    # Ensure the range is exactly 5 pages when possible
    if end_page - start_page < 4:
        if start_page == 1:
            end_page = min(5, total_pages)
        else:
            start_page = max(total_pages - 4, 1)

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

#=======================================================================================ADD STUDENT=============================================================

@students_bp.route('/add_student', methods=['POST'])
def add_student():
    try:
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        course_code = request.form.get('course_code')
        year = request.form['year']
        photo = request.files.get('photo')

        success = handle_add_student(student_id, first_name, last_name, gender, course_code, year, photo)

        if not success:
            flash('Student ID already exists!', 'danger')
        else:
            flash('Student added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding student: {str(e)}', 'danger')

    return redirect(url_for('students.students_page'))

#=======================================================================================EDIT STUDENT=============================================================

@students_bp.route('/edit_student/<string:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        new_student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        course_code = request.form.get('course_code')
        year = request.form['year']
        photo = request.files.get('photo')  
        
        try:
            success = handle_edit_student(
                student_id=student_id,
                new_student_id=new_student_id,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                course_code=course_code,
                year=year,
                photo=photo
            )
            if not success:
                flash('Student ID already exists!', 'danger')
            else:
                flash('Student updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating student: {str(e)}', 'danger')
        
        return redirect(url_for('students.students_page'))

    return render_template('edit_student.html', student_id=student_id)

#=======================================================================================DELETE STUDENT=============================================================

@students_bp.route('/delete_student', methods=['POST'])
def delete_student():
    try:
        student_id = request.form['student_id']
        handle_delete_student(student_id)
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'danger')

    return redirect(url_for('students.students_page'))

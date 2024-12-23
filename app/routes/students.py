# students.py (Routes)
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.student_controller import (
    get_students_page, handle_add_student, handle_edit_student, handle_delete_student
)

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
def students_page():
    search_query = request.args.get('search_query', '')
    filter_by = request.args.get('filter_by', '')
    students, courses = get_students_page(search_query, filter_by)
    return render_template('students.html', students=students, courses=courses)

@students_bp.route('/add_student', methods=['POST'])
def add_student():
    try:
        student_data = request.form
        photo = request.files.get('photo')
        success = handle_add_student(student_data, photo)
        
        if not success:
            flash(f'Student ID already exists!', 'danger')
        else:
            flash('Student added successfully!', 'success')
    except Exception as e:
        flash(f'Student ID already exists!', 'danger')

    return redirect(url_for('students.students_page'))

#=======================================================================================EDIT STUDENT=============================================================

@students_bp.route('/edit_student/<string:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        student_data = request.form
        photo = request.files.get('photo')
        
        try:
            handle_edit_student(student_id, student_data, photo)
            flash('Student updated successfully!', 'success')
        except Exception as e:
            flash(f'Student ID already exists!', 'danger')
        
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
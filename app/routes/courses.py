from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.course_controller import get_courses_page, handle_add_course, handle_edit_course, handle_delete_course

courses_bp = Blueprint('courses', __name__)

#=======================================================================================COURSES PAGE=============================================================

@courses_bp.route('/', methods=['GET'])
def courses_page():
    search_query = request.args.get('search_query', '')  
    filter_by = request.args.get('filter_by', '')  

    courses, colleges = get_courses_page(search_query, filter_by)

    return render_template('courses.html', courses=courses, colleges=colleges)

#=======================================================================================ADD COURSE=============================================================

@courses_bp.route('/add_course', methods=['POST'])
def add_course():
    try:
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        col_code = request.form.get('col_code')

        success = handle_add_course(course_code, course_name, col_code)

        if not success:
            flash('Course Code already exists!', 'danger')
        else:
            flash('Course added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding course: {str(e)}', 'danger')

    return redirect(url_for('courses.courses_page'))

#=======================================================================================EDIT COURSE=============================================================

@courses_bp.route('/edit_course/<string:course_code>', methods=['GET', 'POST'])
def edit_course(course_code):
    if request.method == 'POST':
        new_course_code = request.form['course_code']
        course_name = request.form['course_name']
        col_code = request.form['col_code']
        
        try:
            handle_edit_course(course_code, new_course_code, course_name, col_code)
            flash('Course updated successfully!', 'success')
        except Exception as e:
            flash(f'Course Code already exists!', 'danger')
        
        return redirect(url_for('courses.courses_page'))

    return render_template('edit_course.html', course_code=course_code)

#=======================================================================================DELETE COURSE=============================================================

@courses_bp.route('/delete_course', methods=['POST'])
def delete_course():
    try:
        course_code = request.form['course_code']
        handle_delete_course(course_code)
        flash('Course deleted successfully, and students updated!', 'success')
    except Exception as e:
        flash(f'Error deleting course: {str(e)}', 'danger')

    return redirect(url_for('courses.courses_page'))

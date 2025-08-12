from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.course_controller import get_courses_page, handle_add_course, handle_edit_course, handle_delete_course

courses_bp = Blueprint('courses', __name__)

#=======================================================================================COURSES PAGE=============================================================

@courses_bp.route('/', methods=['GET'])
def courses_page():
    search_query = request.args.get('search_query', '')  
    filter_by = request.args.get('filter_by', '')  
    page = int(request.args.get('page', 1))  
    per_page = 10  

    courses, colleges, total_pages = get_courses_page(search_query, filter_by, page, per_page)

    return render_template(
        'courses.html',
        courses=courses,
        colleges=colleges,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

#=======================================================================================ADD COURSE=============================================================

@courses_bp.route('/add_course', methods=['POST'])
def add_course():
    success, message, category = handle_add_course(
        request.form['course_code'],
        request.form['course_name'],
        request.form.get('col_code')
    )
    flash(message, category)
    return redirect(url_for('courses.courses_page'))

#=======================================================================================EDIT COURSE=============================================================

@courses_bp.route('/edit_course/<string:course_code>', methods=['GET', 'POST'])
def edit_course(course_code):
    if request.method == 'POST':
        success, message, category = handle_edit_course(
            course_code,
            request.form['course_code'],
            request.form['course_name'],
            request.form['col_code']
        )
        flash(message, category)
        return redirect(url_for('courses.courses_page'))

    return render_template('edit_course.html', course_code=course_code)

#=======================================================================================DELETE COURSE=============================================================

@courses_bp.route('/delete_course', methods=['POST'])
def delete_course():
    success, message, category = handle_delete_course(request.form['course_code'])
    flash(message, category)
    return redirect(url_for('courses.courses_page'))

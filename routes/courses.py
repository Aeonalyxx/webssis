from flask import Blueprint, render_template, request, redirect, url_for, flash
from config.db_config import get_db_connection
import pymysql

courses_bp = Blueprint('courses', __name__)

#=======================================================================================COURSES PAGE=============================================================

@courses_bp.route('/', methods=['GET'])
def courses_page():
    search_query = request.args.get('search_query', '')  
    filter_by = request.args.get('filter_by', '') 

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT * FROM courses"
    where_clauses = []
    params = []

    if search_query:
        if filter_by:
            if filter_by == 'course_code':
                where_clauses.append("course_code LIKE %s")
                params.append(f"%{search_query}%")
            elif filter_by == 'course_name':
                where_clauses.append("course_name LIKE %s")
                params.append(f"%{search_query}%")
            elif filter_by == 'col_code':
                where_clauses.append("col_code LIKE %s")
                params.append(f"%{search_query}%")
        else:
            where_clauses.append("(course_code LIKE %s OR course_name LIKE %s OR col_code LIKE %s)")
            params.extend([f"%{search_query}%"] * 3)  
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    cursor.execute(sql, tuple(params))  

    courses = cursor.fetchall()

    cursor.execute("SELECT * FROM colleges")
    colleges = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('courses.html', courses=courses, colleges=colleges)



#=======================================================================================ADD COURSE=============================================================

@courses_bp.route('/add_course', methods=['POST'])
def add_course():
    try:
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        col_code = request.form.get('col_code')  

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO courses (course_code, course_name, col_code) VALUES (%s, %s, %s)",
            (course_code, course_name, col_code)
        )

        conn.commit()
        cursor.close()
        conn.close()

        flash('Course added successfully!', 'success')
    except pymysql.MySQLError as e:
        flash(f'Course Code already exists!', 'danger')

    return redirect(url_for('courses.courses_page'))

#=======================================================================================EDIT COURSE=============================================================

@courses_bp.route('/edit_course/<string:course_code>', methods=['GET', 'POST'])
def edit_course(course_code):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        try:
            new_course_code = request.form['course_code'] 
            course_name = request.form['course_name']
            col_code = request.form['col_code'] 

            cursor.execute(
                "UPDATE courses SET course_code = %s, course_name = %s, col_code = %s WHERE course_code = %s",
                (new_course_code, course_name, col_code, course_code)
            )

            conn.commit()
            flash('Course updated successfully!', 'success')
        except pymysql.MySQLError as e:
            flash(f'Course Code already exists!', 'danger')

        return redirect(url_for('courses.courses_page'))

    cursor.execute("SELECT * FROM courses WHERE course_code = %s", (course_code,))
    course = cursor.fetchone()

    cursor.execute("SELECT * FROM colleges")
    colleges = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('edit_course.html', course=course, colleges=colleges)

#=======================================================================================DELETE COURSE=============================================================

@courses_bp.route('/delete_course', methods=['POST'])
def delete_course():
    try:
        course_code = request.form['course_code']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE students SET course_code = NULL WHERE course_code = %s",
            (course_code,)
        )

        cursor.execute("DELETE FROM courses WHERE course_code = %s", (course_code,))

        conn.commit()
        cursor.close()
        conn.close()

        flash('Course deleted successfully, and students updated!', 'success')
    except pymysql.MySQLError as e:
        flash(f'Error deleting course: {str(e)}', 'danger')

    return redirect(url_for('courses.courses_page'))

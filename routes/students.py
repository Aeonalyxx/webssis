from flask import Blueprint, render_template, request, redirect, url_for, flash
from config.db_config import get_db_connection
import cloudinary.uploader
import cloudinary
import pymysql
import re

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
def students_page():
    search_query = request.args.get('search_query', '')
    filter_by = request.args.get('filter_by', '')

    query = "SELECT * FROM students"
    params = []

    if search_query:
        if filter_by:
            if filter_by == 'gender':
                query += " WHERE LOWER(gender) = LOWER(%s)"
                params.append(search_query)
            else:
                query += f" WHERE {filter_by} LIKE %s"
                params.append(f"%{search_query}%")
        else:
            query += """
                WHERE student_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s 
                OR LOWER(gender) = LOWER(%s) OR course_code LIKE %s OR year LIKE %s
            """
            params.extend([f"%{search_query}%"] * 3 + [search_query] + [f"%{search_query}%"] * 2)

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  
    cursor.execute(query, params)
    students = cursor.fetchall()
    
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('students.html', students=students, courses=courses)


#=========================================================================================UPLOAD ROUTE==================================================

@students_bp.route('/upload_students', methods=['POST'])
def upload_students():
    file = request.files.get('file')
    
    if not file or not file.filename.lower().endswith(('.png', '.jpg')):
        flash('Please upload a valid image (JPEG or PNG).', 'danger')
        return redirect(url_for('students.students_page'))

    try:
        upload_result = cloudinary.uploader.upload(file)

        photo_url = upload_result['secure_url']
        
        student_id = request.form['student_id']

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE students
            SET photo_url = %s
            WHERE student_id = %s
        """
        cursor.execute(query, (photo_url, student_id))
        conn.commit()

        flash('Student photo uploaded successfully!', 'success')
    except Exception as e:
        flash(f'Error uploading photo: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('students.students_page'))



@students_bp.route('/delete_photo', methods=['POST'])
def delete_photo():
    student_id = request.form['student_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT photo_url FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()

        if result and result['photo_url']:
            photo_url = result['photo_url']
            public_id = photo_url.split("/")[-1].split(".")[0]
            
            cloudinary.uploader.destroy(public_id)

            update_query = "UPDATE students SET photo_url = NULL WHERE student_id = %s"
            cursor.execute(update_query, (student_id,))
            conn.commit()

            flash('Student photo deleted successfully!', 'success')
        else:
            flash('No photo to delete.', 'warning')

    except Exception as e:
        flash(f'Error deleting photo: {str(e)}', 'danger')

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('students.students_page'))


#=========================================================================================ADD ROUTE==================================================

@students_bp.route('/add_student', methods=['POST'])
def add_student():
    student_id = request.form['student_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    gender = request.form.get('gender')
    course_code = request.form.get('course_code')
    year = request.form.get('year')

    if not re.match(r'^\d{4}-\d{4}$', student_id):
        flash('Student ID must be in YYYY-NNNN format', 'danger')
        return redirect(url_for('students.students_page'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO students (student_id, first_name, last_name, gender, course_code, year)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (student_id, first_name, last_name, gender, course_code, year))
        conn.commit()

        flash('Student added successfully!', 'success')
    except pymysql.MySQLError as e: 
        flash(f'Student ID already exists!', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('students.students_page'))

#=========================================================================================EDIT ROUTE==================================================

@students_bp.route('/edit_student/<string:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    if request.method == 'POST':
        new_student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        course_code = request.form['course_code']
        year = request.form['year']

        try:
            query = """
                UPDATE students
                SET student_id = %s, first_name = %s, last_name = %s, gender = %s, course_code = %s, year = %s
                WHERE student_id = %s
            """
            cursor.execute(query, (new_student_id, first_name, last_name, gender, course_code, year, student_id))
            conn.commit()
            flash('Student updated successfully!', 'success')
        except pymysql.MySQLError as e: 
            flash(f'Student ID already exists!', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('students.students_page'))

    cursor.close()
    conn.close()
    return render_template('edit_student.html', student=student, courses=courses)

#=========================================================================================DELETE ROUTE==================================================

@students_bp.route('/delete_student', methods=['POST'])
def delete_student():
    student_id = request.form['student_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "DELETE FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        conn.commit()

        flash('Student deleted successfully!', 'success')
    except pymysql.MySQLError as e:  
        flash(f'Error deleting student: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('students.students_page'))

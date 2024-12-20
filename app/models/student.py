# student.py (Model)
import pymysql
from app.database import get_db_connection

def get_students(search_query='', filter_by=''):
    query = "SELECT * FROM students"
    params = []
    
    if search_query:
        if filter_by:
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
    cursor.execute(query, tuple(params))
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    return students, courses

def add_student(student_id, first_name, last_name, gender, course_code, year, photo_url):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO students (student_id, first_name, last_name, gender, course_code, year, photo_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (student_id, first_name, last_name, gender, course_code, year, photo_url))
    conn.commit()

    cursor.close()
    conn.close()

def update_student(student_id, new_student_id, first_name, last_name, gender, course_code, year, photo_url):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE students
        SET student_id = %s, first_name = %s, last_name = %s, gender = %s, course_code = %s, year = %s, photo_url = %s
        WHERE student_id = %s
    """
    cursor.execute(query, (new_student_id, first_name, last_name, gender, course_code, year, photo_url, student_id))
    conn.commit()

    cursor.close()
    conn.close()

def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM students WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    conn.commit()

    cursor.close()
    conn.close()

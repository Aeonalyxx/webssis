import pymysql
from app.utils.database import get_db_connection

def get_courses(search_query='', filter_by=''):
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

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, tuple(params))
    courses = cursor.fetchall()

    cursor.execute("SELECT * FROM colleges")
    colleges = cursor.fetchall()

    cursor.close()
    conn.close()

    return courses, colleges

def add_course(course_code, course_name, col_code):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM courses WHERE course_code = %s", (course_code,))
    existing_course = cursor.fetchone()

    if existing_course:
        return False
    else:
        cursor.execute("INSERT INTO courses (course_code, course_name, col_code) VALUES (%s, %s, %s)", 
                    (course_code, course_name, col_code))
        conn.commit()
        cursor.close()
        conn.close()
        return True

def update_course(course_code, new_course_code, course_name, col_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE courses SET course_code = %s, course_name = %s, col_code = %s WHERE course_code = %s",
                   (new_course_code, course_name, col_code, course_code))
    conn.commit()
    cursor.close()
    conn.close()

def delete_course(course_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE students SET course_code = NULL WHERE course_code = %s", (course_code,))
    conn.commit()

    cursor.execute("DELETE FROM courses WHERE course_code = %s", (course_code,))
    conn.commit()

    cursor.close()
    conn.close()

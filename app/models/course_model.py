import pymysql
from app.utils.utils import get_db_connection

def get_courses(search_query='', filter_by='', page=1, per_page=8):
    sql = "SELECT * FROM courses"
    where_clauses = []
    params = []

    if search_query:
        sq_lower = search_query.lower()
        if filter_by:
            if filter_by == 'course_code':
                where_clauses.append("LOWER(course_code) LIKE %s")
                params.append(f"{sq_lower}%")  
            elif filter_by == 'course_name':
                where_clauses.append("LOWER(course_name) LIKE %s")
                params.append(f"%{sq_lower}%") 
            elif filter_by == 'col_code':
                where_clauses.append("LOWER(col_code) LIKE %s")
                params.append(f"{sq_lower}%")
        else:
            where_clauses.append(
                "("
                "LOWER(course_code) LIKE %s OR "
                "LOWER(course_name) LIKE %s OR "
                "LOWER(col_code) LIKE %s"
                ")"
            )
            params.extend([f"{sq_lower}%", f"%{sq_lower}%", f"{sq_lower}%"])

    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    count_sql = f"SELECT COUNT(*) as total FROM ({sql}) AS count_table"

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(count_sql, tuple(params))
    total_count = cursor.fetchone()['total']

    offset = (page - 1) * per_page
    sql += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    cursor.execute(sql, tuple(params))
    courses = cursor.fetchall()

    cursor.execute("SELECT * FROM colleges")
    colleges = cursor.fetchall()

    cursor.close()
    conn.close()

    return courses, colleges, total_count

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

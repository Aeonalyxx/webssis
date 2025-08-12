import pymysql
from app.utils.utils import get_db_connection

def get_students(search_query='', filter_by='', page=1, per_page=8):
    base_query = "SELECT * FROM students"
    params = []

    if search_query:
        if filter_by:
            if filter_by == "gender":
                base_query += " WHERE LOWER(gender) LIKE LOWER(%s)"
                params.append(f"{search_query}%")
            elif filter_by in ("first_name", "last_name"):
                base_query += f" WHERE {filter_by} LIKE %s"
                params.append(f"{search_query}%")
            else:
                base_query += f" WHERE {filter_by} LIKE %s"
                params.append(f"%{search_query}%")
        else:
            base_query += """
                WHERE student_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s 
                OR LOWER(gender) = LOWER(%s) OR course_code LIKE %s OR year LIKE %s
            """
            params.extend([f"%{search_query}%"] * 3 + [search_query] + [f"%{search_query}%"] * 2)

    if filter_by == "student_id":
        order_by = "student_id ASC, first_name ASC"
    elif filter_by == "first_name":
        order_by = "first_name ASC, student_id ASC"
    elif filter_by == "last_name":
        order_by = "last_name ASC, first_name ASC, student_id ASC"
    elif filter_by == "gender":
        order_by = """
            CASE 
                WHEN LOWER(gender) = 'female' THEN 0 
                WHEN LOWER(gender) = 'male' THEN 1 
                ELSE 2 
            END,
            first_name ASC,
            student_id ASC
        """
    elif filter_by == "year":
        order_by = "CAST(year AS UNSIGNED) ASC, first_name ASC, student_id ASC"
    elif filter_by == "course_code":
        order_by = "course_code ASC, first_name ASC, student_id ASC"
    else:
        order_by = "first_name ASC, student_id ASC"

    base_query += f" ORDER BY {order_by}"

    count_query = f"SELECT COUNT(*) AS total FROM ({base_query}) AS count_table"
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(count_query, tuple(params))
    total_count = cursor.fetchone()['total']

    offset = (page - 1) * per_page
    final_query = base_query + " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    cursor.execute(final_query, tuple(params))
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM courses ORDER BY course_code ASC")
    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    return students, courses, total_count

def add_student(student_id, first_name, last_name, gender, course_code, year, photo_url, photo_public_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    existing_student = cursor.fetchone()

    if existing_student:
        cursor.close()
        conn.close()
        return False 

    query = """
        INSERT INTO students (student_id, first_name, last_name, gender, course_code, year, photo_url, photo_public_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (student_id, first_name, last_name, gender, course_code, year, photo_url, photo_public_id))
    conn.commit()

    cursor.close()
    conn.close()
    return True  

def update_student(student_id, new_student_id, first_name, last_name, gender, course_code, year, photo_url, photo_public_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(
        "SELECT student_id FROM students WHERE student_id = %s AND student_id != %s",
        (new_student_id, student_id)
    )
    existing_student = cursor.fetchone()

    if existing_student:
        cursor.close()
        conn.close()
        return False  

    query = """
        UPDATE students
        SET student_id = %s, first_name = %s, last_name = %s, gender = %s, course_code = %s, year = %s, photo_url = %s, photo_public_id = %s
        WHERE student_id = %s
    """
    cursor.execute(query, (new_student_id, first_name, last_name, gender, course_code, year, photo_url, photo_public_id, student_id))
    conn.commit()

    cursor.close()
    conn.close()
    return True

def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM students WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    conn.commit()

    cursor.close()
    conn.close()

def get_student_by_id(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "SELECT * FROM students WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    student = cursor.fetchone()

    cursor.close()
    conn.close()
    return student

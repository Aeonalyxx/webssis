import pymysql
from app.utils.utils import get_db_connection

def get_students(search_query='', filter_by='', page=1, per_page=8):
    column_map = {
        "student_id": "s.student_id",
        "first_name": "s.first_name",
        "last_name": "s.last_name",
        "gender": "s.gender",
        "course_code": "c.course_code",
        "year": "s.year",
        "college": "col.col_name"
    }

    base_query = """
        SELECT 
            s.student_id,
            s.first_name,
            s.last_name,
            s.gender,
            s.year,
            s.photo_url,
            c.course_code,
            CONCAT(c.course_code, IF(col.col_name IS NOT NULL, CONCAT(' (', col.col_name, ')'), '')) AS program
        FROM students s
        LEFT JOIN courses c ON s.course_code = c.course_code
        LEFT JOIN colleges col ON c.col_code = col.col_code
    """
    params = []

    if search_query:
        if filter_by:
            col = column_map.get(filter_by, filter_by)
            if filter_by == "gender":
                base_query += f" WHERE LOWER({col}) LIKE LOWER(%s)"
                params.append(f"{search_query}%")
            elif filter_by in ("first_name", "last_name"):
                base_query += f" WHERE {col} LIKE %s"
                params.append(f"{search_query}%")
            else:
                base_query += f" WHERE {col} LIKE %s"
                params.append(f"%{search_query}%")
        else:
            base_query += """
                WHERE s.student_id LIKE %s 
                   OR s.first_name LIKE %s 
                   OR s.last_name LIKE %s 
                   OR LOWER(s.gender) = LOWER(%s) 
                   OR c.course_code LIKE %s 
                   OR s.year LIKE %s
                   OR col.col_name LIKE %s
                   OR CONCAT(c.course_code, ' (', col.col_name, ')') LIKE %s
            """
            params.extend([
                f"%{search_query}%",  #student_id
                f"%{search_query}%",  #first_name
                f"%{search_query}%",  #last_name
                search_query,         #gender exact
                f"%{search_query}%",  #course_code
                f"%{search_query}%",  #year
                f"%{search_query}%",  #college name
                f"%{search_query}%"   #program string
            ])

    if filter_by == "student_id":
        order_by = "s.student_id ASC, s.first_name ASC"
    elif filter_by == "first_name":
        order_by = "s.first_name ASC, s.student_id ASC"
    elif filter_by == "last_name":
        order_by = "s.last_name ASC, s.first_name ASC, s.student_id ASC"
    elif filter_by == "gender":
        order_by = """
            CASE 
                WHEN LOWER(s.gender) = 'female' THEN 0 
                WHEN LOWER(s.gender) = 'male' THEN 1 
                ELSE 2 
            END,
            s.first_name ASC,
            s.student_id ASC
        """
    elif filter_by == "year":
        order_by = "CAST(s.year AS UNSIGNED) ASC, s.first_name ASC, s.student_id ASC"
    elif filter_by == "course_code":
        order_by = "c.course_code ASC, s.first_name ASC, s.student_id ASC"
    elif filter_by == "college":
        order_by = "col.col_name ASC, s.first_name ASC, s.student_id ASC"
    else:
        order_by = "s.first_name ASC, s.student_id ASC"

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

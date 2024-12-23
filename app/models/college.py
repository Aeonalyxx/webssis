import pymysql
from app.utils.database import get_db_connection

def get_colleges(search_query='', filter_by=''):
    query = "SELECT * FROM colleges WHERE 1=1"
    params = []

    if search_query:
        if filter_by:
            if filter_by == 'col_code':
                query += " AND col_code LIKE %s"
                params.append(f'%{search_query}%')
            elif filter_by == 'col_name':
                query += " AND col_name LIKE %s"
                params.append(f'%{search_query}%')
        else:
            query += " AND (col_code LIKE %s OR col_name LIKE %s)"
            params.extend([f'%{search_query}%', f'%{search_query}%'])

    elif filter_by:
        if filter_by == 'college_code':
            query += " AND col_code IS NOT NULL"
        elif filter_by == 'college_name':
            query += " AND col_name IS NOT NULL"

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, params)
    colleges = cursor.fetchall()
    cursor.close()
    conn.close()

    return colleges

def add_college(col_code, col_name):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM colleges WHERE col_code = %s", (col_code,))
    existing_college = cursor.fetchone()

    if existing_college:
        return False  # College code already exists
    else:
        cursor.execute("INSERT INTO colleges (col_code, col_name) VALUES (%s, %s)", (col_code, col_name))
        conn.commit()
        cursor.close()
        conn.close()
        return True  # College added successfully

def update_college(col_code, new_col_code, col_name):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "UPDATE colleges SET col_code = %s, col_name = %s WHERE col_code = %s",
        (new_col_code, col_name, col_code)
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_college(col_code):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("UPDATE courses SET col_code = NULL WHERE col_code = %s", (col_code,))
    conn.commit()

    cursor.execute("DELETE FROM colleges WHERE col_code = %s", (col_code,))
    conn.commit()

    cursor.close()
    conn.close()

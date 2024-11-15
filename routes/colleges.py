from flask import Blueprint, render_template, request, redirect, url_for, flash
from config.db_config import get_db_connection
import pymysql

colleges_bp = Blueprint('colleges', __name__)

#=======================================================================================COLLEGES PAGE=============================================================

@colleges_bp.route('/', methods=['GET'])
def colleges_page():
    search_query = request.args.get('search_query', '')
    filter_by = request.args.get('filter_by', '')

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

    return render_template('colleges.html', colleges=colleges)


#=======================================================================================ADD COLLEGE=============================================================

@colleges_bp.route('/add_college', methods=['POST'])
def add_college():
    try:
        col_code = request.form['col_code']
        col_name = request.form['college_name']

        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM colleges WHERE col_code = %s", (col_code,))
        existing_college = cursor.fetchone()

        if existing_college:
            flash('College code already exists!', 'danger')
        else:
            cursor.execute("INSERT INTO colleges (col_code, col_name) VALUES (%s, %s)", (col_code, col_name))
            conn.commit()
            flash('College added successfully!', 'success')

        cursor.close()
        conn.close()

    except pymysql.MySQLError as e:
        flash(f'Error adding college: {str(e)}', 'danger')

    return redirect(url_for('colleges.colleges_page'))


#=======================================================================================EDIT COLLEGE=============================================================

@colleges_bp.route('/edit_college/<string:col_code>', methods=['GET', 'POST'])
def edit_college(col_code):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM colleges WHERE col_code = %s", (col_code,))
    college = cursor.fetchone()

    if request.method == 'POST':
        try:
            new_col_code = request.form['col_code']
            col_name = request.form['college_name']

            if college:
                cursor.execute(
                    "UPDATE colleges SET col_code = %s, col_name = %s WHERE col_code = %s",
                    (new_col_code, col_name, col_code)
                )
                conn.commit()
                flash('College updated successfully!', 'success')

        except pymysql.MySQLError as e:
            flash(f'College code already exists!', 'danger')
        
        return redirect(url_for('colleges.colleges_page'))

    cursor.close()
    conn.close()

    return render_template('edit_college.html', college=college)


#=======================================================================================DELETE COLLEGE=============================================================

@colleges_bp.route('/delete_college', methods=['POST'])
def delete_college():
    try:
        col_code = request.form['col_code']
        
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("UPDATE courses SET col_code = NULL WHERE col_code = %s", (col_code,))
        conn.commit()

        cursor.execute("DELETE FROM colleges WHERE col_code = %s", (col_code,))
        conn.commit()

        flash('College deleted successfully, and courses updated!', 'success')
        
        cursor.close()
        conn.close()

    except pymysql.MySQLError as e:
        flash(f'Error deleting college: {str(e)}', 'danger')

    return redirect(url_for('colleges.colleges_page'))

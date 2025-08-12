from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.college_controller import get_colleges_page, handle_add_college, handle_edit_college, handle_delete_college

colleges_bp = Blueprint('colleges', __name__)

#=======================================================================================COLLEGE PAGE=============================================================

@colleges_bp.route('/', methods=['GET'])
def colleges_page():
    search_query = request.args.get('search_query', '')
    filter_by = request.args.get('filter_by', '')

    colleges = get_colleges_page(search_query, filter_by)

    return render_template('colleges.html', colleges=colleges)

#=======================================================================================ADD COLLEGE=============================================================

@colleges_bp.route('/add_college', methods=['POST'])
def add_college():
    success, message, category = handle_add_college(
        request.form['col_code'],
        request.form['college_name']
    )
    flash(message, category)
    return redirect(url_for('colleges.colleges_page'))

#=======================================================================================EDIT COLLEGE=============================================================

@colleges_bp.route('/edit_college/<string:col_code>', methods=['GET', 'POST'])
def edit_college(col_code):
    if request.method == 'POST':
        success, message, category = handle_edit_college(
            col_code,
            request.form['col_code'],
            request.form['college_name']
        )
        flash(message, category)
        return redirect(url_for('colleges.colleges_page'))

    return render_template('edit_college.html', col_code=col_code)

#=======================================================================================DELETE COLLEGE=============================================================

@colleges_bp.route('/delete_college', methods=['POST'])
def delete_college():
    success, message, category = handle_delete_college(request.form['col_code'])
    flash(message, category)
    return redirect(url_for('colleges.colleges_page'))

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
    try:
        col_code = request.form['col_code']
        col_name = request.form['college_name']

        success = handle_add_college(col_code, col_name)
        
        if not success:
            flash('College code already exists!', 'danger')
        else:
            flash('College added successfully!', 'success')

    except Exception as e:
        flash(f'Error adding college: {str(e)}', 'danger')

    return redirect(url_for('colleges.colleges_page'))

#=======================================================================================EDIT COLLEGE=============================================================

@colleges_bp.route('/edit_college/<string:col_code>', methods=['GET', 'POST'])
def edit_college(col_code):
    if request.method == 'POST':
        new_col_code = request.form['col_code']
        col_name = request.form['college_name']
        try:
            handle_edit_college(col_code, new_col_code, col_name)
            flash('College updated successfully!', 'success')
        except Exception as e:
            flash(f'College code already exists!', 'danger')
        
        return redirect(url_for('colleges.colleges_page'))

    return render_template('edit_college.html', col_code=col_code)

#=======================================================================================DELETE COLLEGE=============================================================

@colleges_bp.route('/delete_college', methods=['POST'])
def delete_college():
    try:
        col_code = request.form['col_code']
        handle_delete_college(col_code)
        flash('College deleted successfully, and courses updated!', 'success')
    except Exception as e:
        flash(f'Error deleting college: {str(e)}', 'danger')

    return redirect(url_for('colleges.colleges_page'))

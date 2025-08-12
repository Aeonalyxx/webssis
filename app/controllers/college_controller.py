from app.models.college_model import get_colleges, add_college, update_college, delete_college
import re

def get_colleges_page(search_query='', filter_by=''):
    colleges = get_colleges(search_query, filter_by)
    return colleges

def handle_add_college(col_code, col_name):
    try:
        col_code = col_code.strip().upper()
        success = add_college(col_code, col_name)
        if not success:
            return False, 'College code already exists!', 'danger'
        return True, 'College added successfully!', 'success'
    except Exception as e:
        return False, f'Error adding college: {str(e)}', 'danger'

def handle_edit_college(col_code, new_col_code, col_name):
    try:
        new_col_code = new_col_code.strip().upper()
        update_college(col_code, new_col_code, col_name)
        return True, 'College updated successfully!', 'success'
    except Exception as e:
        return False, 'College code already exists!', 'danger'

def handle_delete_college(col_code):
    try:
        delete_college(col_code)
        return True, 'College deleted successfully, and courses updated!', 'success'
    except Exception as e:
        return False, f'Error deleting college: {str(e)}', 'danger'

from app.models.college import get_colleges, add_college, update_college, delete_college

def get_colleges_page(search_query='', filter_by=''):
    colleges = get_colleges(search_query, filter_by)
    return colleges

def handle_add_college(col_code, col_name):
    success = add_college(col_code, col_name)
    return success

def handle_edit_college(col_code, new_col_code, col_name):
    update_college(col_code, new_col_code, col_name)

def handle_delete_college(col_code):
    delete_college(col_code)

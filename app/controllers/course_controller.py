from app.models.course import get_courses, add_course, update_course, delete_course

def get_courses_page(search_query='', filter_by='', page=1, per_page=8):
    courses, colleges, total_count = get_courses(search_query, filter_by, page, per_page)
    total_pages = (total_count + per_page - 1) // per_page  
    return courses, colleges, total_pages

def handle_add_course(course_code, course_name, col_code):
    success = add_course(course_code, course_name, col_code)
    return success

def handle_edit_course(course_code, new_course_code, course_name, col_code):
    update_course(course_code, new_course_code, course_name, col_code)

def handle_delete_course(course_code):
    delete_course(course_code)

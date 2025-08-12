from app.models.course_model import get_courses, add_course, update_course, delete_course
import re

def get_courses_page(search_query='', filter_by='', page=1, per_page=8):
    courses, colleges, total_count = get_courses(search_query, filter_by, page, per_page)
    total_pages = (total_count + per_page - 1) // per_page  
    return courses, colleges, total_pages

def is_valid_course_code(course_code):
    return bool(re.match(r'^[A-Z0-9]+$', course_code))

def handle_add_course(course_code, course_name, col_code):
    try:
        course_code = course_code.strip().upper()
        success = add_course(course_code, course_name, col_code)
        if not success:
            return False, 'Course Code already exists!', 'danger'
        return True, 'Course added successfully!', 'success'
    except Exception as e:
        return False, f'Error adding course: {str(e)}', 'danger'

def handle_edit_course(course_code, new_course_code, course_name, col_code):
    try:
        new_course_code = new_course_code.strip().upper()
        update_course(course_code, new_course_code, course_name, col_code)
        return True, 'Course updated successfully!', 'success'
    except Exception as e:
        return False, 'Course Code already exists!', 'danger'

def handle_delete_course(course_code):
    try:
        delete_course(course_code)
        return True, 'Course deleted successfully, and students updated!', 'success'
    except Exception as e:
        return False, f'Error deleting course: {str(e)}', 'danger'

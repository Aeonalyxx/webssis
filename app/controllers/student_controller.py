from app.models.student_model import get_students, add_student, update_student, delete_student, get_student_by_id
import cloudinary.uploader
import re

MAX_FILE_SIZE_MB = 2
ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp')
DEFAULT_PHOTO_URL = "/static/images/default_student.webp"

def get_students_page(search_query='', filter_by='', page=1, per_page=8):
    students, courses, total_count = get_students(search_query, filter_by, page, per_page)
    total_pages = (total_count + per_page - 1) // per_page  

    # Pagination range calculation
    start_page = max(page - 2, 1)
    end_page = min(page + 2, total_pages)

    if end_page - start_page < 4:
        if start_page == 1:
            end_page = min(5, total_pages)
        else:
            start_page = max(total_pages - 4, 1)

    return students, courses, total_pages, start_page, end_page


def is_valid_student_id(student_id):
    return bool(re.match(r"^\d{4}-\d{4}$", student_id))

def is_valid_photo(photo):
    if not photo.filename.lower().endswith(ALLOWED_EXTENSIONS):
        return False, "Invalid file type. Only PNG, JPEG, JPG and WEBP are allowed."

    photo.seek(0, 2)  
    file_size = photo.tell()
    photo.seek(0)  
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        return False, "File size exceeds 2MB limit."

    return True, None


def handle_add_student(student_id, first_name, last_name, gender, course_code, year, photo):
    try:
        if not is_valid_student_id(student_id):
            return False, "Invalid Student ID format. Use YYYY-NNNN.", 'danger'

        photo_url = DEFAULT_PHOTO_URL
        photo_public_id = None

        if photo:
            is_valid, error_msg = is_valid_photo(photo)
            if not is_valid:
                return False, error_msg, 'danger'

            upload_result = cloudinary.uploader.upload(photo)
            photo_url = upload_result['secure_url']
            photo_public_id = upload_result['public_id']

        success = add_student(student_id, first_name, last_name, gender, course_code, year, photo_url, photo_public_id)
        if not success:
            return False, "Student ID already exists!", 'danger'

        return True, "Student added successfully!", 'success'

    except Exception as e:
        return False, f"Error adding student: {str(e)}", 'danger'


def handle_edit_student(student_id, new_student_id, first_name, last_name, gender, course_code, year, photo):
    try:
        if not is_valid_student_id(new_student_id):
            return False, "Invalid Student ID format. Use YYYY-NNNN.", 'danger'

        existing_student = get_student_by_id(student_id)
        photo_url = existing_student['photo_url'] if existing_student and existing_student['photo_url'] else DEFAULT_PHOTO_URL
        photo_public_id = existing_student.get('photo_public_id') if existing_student else None

        if photo:
            is_valid, error_msg = is_valid_photo(photo)
            if not is_valid:
                return False, error_msg, 'danger'

            if photo_public_id:
                try:
                    cloudinary.uploader.destroy(photo_public_id)
                except Exception as e:
                    print(f"Warning: Could not delete old Cloudinary image: {e}")

            upload_result = cloudinary.uploader.upload(photo)
            photo_url = upload_result['secure_url']
            photo_public_id = upload_result['public_id']

        success = update_student(student_id, new_student_id, first_name, last_name, gender, course_code, year, photo_url, photo_public_id)
        if not success:
            return False, "Student ID already exists!", 'danger'

        return True, "Student updated successfully!", 'success'

    except Exception as e:
        return False, f"Error updating student: {str(e)}", 'danger'


def handle_delete_student(student_id):
    try:
        student = get_student_by_id(student_id)
        if not student:
            return False, "Student not found.", 'danger'

        photo_public_id = student.get("photo_public_id")

        if photo_public_id:
            try:
                cloudinary.uploader.destroy(photo_public_id)
            except Exception as e:
                print(f"Warning: Could not delete Cloudinary image: {e}")

        delete_student(student_id)
        return True, "Student deleted successfully!", 'success'

    except Exception as e:
        return False, f"Error deleting student: {str(e)}", 'danger'

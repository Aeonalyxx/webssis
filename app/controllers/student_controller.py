from app.models.student import get_students, add_student, update_student, delete_student, get_student_by_id
import cloudinary.uploader

MAX_FILE_SIZE_MB = 2
ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp')
DEFAULT_PHOTO_URL = "/static/images/default_student.webp"

def get_students_page(search_query='', filter_by='', page=1, per_page=8):
    students, courses, total_count = get_students(search_query, filter_by, page, per_page)
    total_pages = (total_count + per_page - 1) // per_page  
    return students, courses, total_pages

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
    photo_url = DEFAULT_PHOTO_URL

    if photo:
        is_valid, error_msg = is_valid_photo(photo)
        if not is_valid:
            raise Exception(error_msg)

        try:
            upload_result = cloudinary.uploader.upload(photo)
            photo_url = upload_result['secure_url']
        except Exception as e:
            raise Exception(f"Error uploading photo: {str(e)}")

    success = add_student(student_id, first_name, last_name, gender, course_code, year, photo_url)
    return success


def handle_edit_student(student_id, new_student_id, first_name, last_name, gender, course_code, year, photo):
    existing_student = get_student_by_id(student_id)
    photo_url = existing_student['photo_url'] if existing_student and existing_student['photo_url'] else DEFAULT_PHOTO_URL

    if photo:
        is_valid, error_msg = is_valid_photo(photo)
        if not is_valid:
            raise Exception(error_msg)

        try:
            upload_result = cloudinary.uploader.upload(photo)
            photo_url = upload_result['secure_url']
        except Exception as e:
            raise Exception(f"Error uploading photo: {str(e)}")

    success = update_student(student_id, new_student_id, first_name, last_name, gender, course_code, year, photo_url)
    return success

def handle_delete_student(student_id):
    delete_student(student_id)

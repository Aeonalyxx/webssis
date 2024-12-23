from app.models.student import get_students, add_student, update_student, delete_student, get_student_by_id
import cloudinary.uploader

def get_students_page(search_query='', filter_by=''):
    students, courses = get_students(search_query, filter_by)
    return students, courses

def handle_add_student(student_id, first_name, last_name, gender, course_code, year, photo):
    photo_url = None
    if photo and photo.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            upload_result = cloudinary.uploader.upload(photo)
            photo_url = upload_result['secure_url']
        except Exception as e:
            raise Exception(f"Error uploading photo: {str(e)}")
    
    success = add_student(student_id, first_name, last_name, gender, course_code, year, photo_url)
    return success


def handle_edit_student(student_id, new_student_id, first_name, last_name, gender, course_code, year, photo):
    existing_photo = get_student_by_id(student_id)
    photo_url = existing_photo['photo_url'] if existing_photo else None

    # Upload new photo if provided
    if photo and photo.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            upload_result = cloudinary.uploader.upload(photo)
            photo_url = upload_result['secure_url']
        except Exception as e:
            raise Exception(f"Error uploading photo: {str(e)}")

    # Call the model to update the student record
    success = update_student(student_id, new_student_id, first_name, last_name, gender, course_code, year, photo_url)
    return success

def handle_delete_student(student_id):
    delete_student(student_id)

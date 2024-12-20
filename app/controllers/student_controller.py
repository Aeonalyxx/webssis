from app.models.student import get_students, add_student, update_student, delete_student
import cloudinary.uploader

def get_students_page(search_query='', filter_by=''):
    students, courses = get_students(search_query, filter_by)
    return students, courses

def handle_add_student(student_data, photo):

    student_id = student_data['student_id']
    first_name = student_data['first_name']
    last_name = student_data['last_name']
    gender = student_data['gender']
    course_code = student_data['course_code']
    year = student_data['year']

    photo_url = None
    if photo and photo.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            upload_result = cloudinary.uploader.upload(photo)
            photo_url = upload_result['secure_url']
        except Exception as e:
            raise Exception(f"Error uploading photo: {str(e)}")
    
    add_student(student_id, first_name, last_name, gender, course_code, year, photo_url)

def handle_edit_student(student_id, student_data, photo):
    # Extracting data from form
    new_student_id = student_data['student_id']
    first_name = student_data['first_name']
    last_name = student_data['last_name']
    gender = student_data['gender']
    course_code = student_data['course_code']
    year = student_data['year']

    # Handling photo upload via Cloudinary (if provided)
    photo_url = student_data.get('photo_url')  # Retain the existing photo URL if no new photo uploaded
    if photo and photo.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            upload_result = cloudinary.uploader.upload(photo)
            photo_url = upload_result['secure_url']
        except Exception as e:
            raise Exception(f"Error uploading photo: {str(e)}")

    update_student(student_id, new_student_id, first_name, last_name, gender, course_code, year, photo_url)

def handle_delete_student(student_id):
    delete_student(student_id)

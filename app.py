from flask import Flask, redirect, url_for
from routes import students_bp, courses_bp, colleges_bp
from config.cloudinary_config import configure_cloudinary

app = Flask(__name__)
app.secret_key = 'webssis'

configure_cloudinary()

@app.route('/')
def index():
    return redirect(url_for('students.students_page'))

app.register_blueprint(students_bp, url_prefix='/students')
app.register_blueprint(courses_bp, url_prefix='/courses')
app.register_blueprint(colleges_bp, url_prefix='/colleges')

if __name__ == '__main__':
    app.run(debug=True)

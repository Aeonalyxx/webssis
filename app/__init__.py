from flask import Flask, redirect, url_for
from app.routes import students_bp, courses_bp, colleges_bp
from app.utils.cloudinary_utils import configure_cloudinary
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY  

    configure_cloudinary()

    @app.route('/')
    def index():
        return redirect(url_for('students.students_page'))

    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(courses_bp, url_prefix='/courses')
    app.register_blueprint(colleges_bp, url_prefix='/colleges')

    return app

from flask import Flask, redirect, url_for
from app.routes import students_bp, courses_bp, colleges_bp
from app.cloudinary_utils import configure_cloudinary


def create_app():
    app = Flask(__name__)
    app.secret_key = 'webssis'

    # Configure Cloudinary
    configure_cloudinary()

    # Index route
    @app.route('/')
    def index():
        return redirect(url_for('students.students_page'))

    # Register blueprints
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(courses_bp, url_prefix='/courses')
    app.register_blueprint(colleges_bp, url_prefix='/colleges')

    return app

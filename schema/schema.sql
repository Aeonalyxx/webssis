CREATE DATABASE IF NOT EXISTS webssis;

USE webssis;

CREATE TABLE IF NOT EXISTS colleges (
    col_code VARCHAR(10) PRIMARY KEY,
    col_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS courses (
    course_code VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    col_code VARCHAR(10),
    FOREIGN KEY (col_code) REFERENCES colleges(col_code) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(9) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    course_code VARCHAR(10), 
    photo_url VARCHAR(255);

    year VARCHAR(1) NOT NULL,
    FOREIGN KEY (course_code) REFERENCES courses(course_code) ON DELETE SET NULL
);

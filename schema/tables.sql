CREATE DATABASE IF NOT EXISTS webssis;

USE webssis;

-- Table for colleges
CREATE TABLE IF NOT EXISTS colleges (
    col_code VARCHAR(10) PRIMARY KEY,
    col_name VARCHAR(100) NOT NULL
);

-- Table for courses
CREATE TABLE IF NOT EXISTS courses (
    course_code VARCHAR(20) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    col_code VARCHAR(10),
    FOREIGN KEY (col_code) REFERENCES colleges(col_code)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Table for students
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(9) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    course_code VARCHAR(20),
    year VARCHAR(1) NOT NULL,
    photo_url VARCHAR(255),
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);



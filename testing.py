import sqlite3

# Connect to the SQLite database (this will create the file if it doesn't exist)
conn = sqlite3.connect('edutrack.db')
cursor = conn.cursor()

# Create the tables
cursor.executescript('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE,
    course TEXT NOT NULL,
    semester INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE,
    department TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL,
    teacher_id INTEGER,
    semester INTEGER NOT NULL,
    course TEXT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    date DATE NOT NULL,
    status TEXT CHECK(status IN ('Present', 'Absent')),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS exams (
    exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    exam_type TEXT CHECK(exam_type IN ('Periodic Test 1', 'Periodic Test 2','End Semester', 'Practical')),
    date DATE NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE TABLE IF NOT EXISTS grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    exam_id INTEGER,
    marks_obtained INTEGER NOT NULL,
    total_marks INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS timetable (
    timetable_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    day_of_week TEXT CHECK(day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')),
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE TABLE IF NOT EXISTS meetings (
    meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    student_id INTEGER,
    date DATE NOT NULL,
    time TEXT NOT NULL,
    purpose TEXT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('Student', 'Teacher', 'Admin')),
    student_id INTEGER,
    teacher_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE SET NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE SET NULL
);
''')

# Insert sample data into the tables
cursor.executescript('''
INSERT INTO students (name, roll_number, email, phone, course, semester) VALUES 
('Aryan Salunke', '111', 'aryansalunke@gmail.com', '9876543210', 'Information Technology', 4),
('Heet Punamiya', '100', 'heet.p@gmail.com', '8765432109', 'Information Technology', 4),
('Vedant Raje', '103', 'vedantraje@gmail.com', '7654321098', 'Information Technology', 4);

INSERT INTO teachers (name, email, phone, department) VALUES 
('Sanjay Pandey', 'sanjaypandey@gmail.com', '9543216789', 'Information Technology'),
('Dr. Reshma Malik', 'reshma.malik@gmail.com', '9988776655', 'Information Technology'),
('Dr. Archana Kale', 'archana.kale@gmail.com', '8877665544', 'Information Technology');

INSERT INTO admin (username, password) VALUES 
('admin1', 'pass1'),
('admin2', 'pass2'),
('admin3', 'pass3');

INSERT INTO subjects (subject_name, teacher_id, semester, course) VALUES 
('Computer Networks', 1, 5, 'Information Technology'),
('Computer Organization and Architecture', 2, 4, 'Information Technology'),
('Operating System', 3, 6, 'Information Technology');

INSERT INTO attendance (student_id, subject_id, date, status) VALUES 
(1, 1, '2024-03-25', 'Present'),
(2, 2, '2024-03-25', 'Absent'),
(3, 3, '2024-03-25', 'Present');

INSERT INTO exams (subject_id, exam_type, date) VALUES 
(1, 'Periodic Test 2', '2025-04-10'),
(2, 'End Semester', '2025-05-20'),
(3, 'Practical', '2025-04-25');

INSERT INTO grades (student_id, exam_id, marks_obtained, total_marks) VALUES 
(1, 1, 85, 100),
(2, 2, 76, 100),
(3, 3, 90, 100);

INSERT INTO timetable (subject_id, day_of_week, start_time, end_time) VALUES 
(1, 'Monday', '10:00', '11:30'),
(2, 'Wednesday', '12:00', '13:30'),
(3, 'Friday', '14:00', '15:30');

INSERT INTO meetings (teacher_id, student_id, date, time, purpose) VALUES 
(1, 1, '2024-03-28', '15:00', 'Project Discussion'),
(2, 2, '2024-03-29', '14:30', 'Doubt Clearing'),
(3, 3, '2024-03-30', '16:00', 'Internship Guidance');

    INSERT INTO users (username, password, role, student_id, teacher_id) VALUES 
    ('Aryan_Salunke', 'pass1', 'Student', 1, NULL),
    ('Reshma_Malik', 'pass1', 'Teacher', NULL, 2),
    ('admin1', 'pass1', 'Admin', NULL, NULL);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
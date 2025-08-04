import sqlite3

def connect_db():
    conn = sqlite3.connect('edutrack.db')
    return conn

def fetch_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, roll_number, email, phone, course, semester FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student

def fetch_announcements():
    # This function should fetch announcements from the database
    # For now, we'll return static data for demonstration purposes
    return "Mid-Sem Exams from April 10"

def fetch_exams(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT subjects.subject_name, exams.date 
    FROM exams 
    JOIN subjects ON exams.subject_id = subjects.subject_id 
    WHERE subjects.semester = (
        SELECT semester FROM students WHERE student_id = ?
    )""", (student_id,))
    exams = cursor.fetchall()
    conn.close()
    return exams

def fetch_assignments(student_id):
    # This function should fetch assignments from the database
    # For now, we'll return static data for demonstration purposes
    return "AT Assignment - Due April 3"
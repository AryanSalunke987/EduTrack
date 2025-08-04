import customtkinter as ctk
import sqlite3
from PIL import Image

def show_dashboard(parent, user_data):
    # Fetch student details from the database
    conn = sqlite3.connect('edutrack.db')
    cursor = conn.cursor()
    
    # Fetch Student Info
    cursor.execute("SELECT name, course, semester FROM students WHERE student_id=?", (user_data[4],))
    student_details = cursor.fetchone()

    # Fetch Student Photo
    cursor.execute("SELECT photo_path FROM photostudent WHERE student_id=?", (user_data[4],))
    photo_result = cursor.fetchone()
    
    conn.close()

    # Clear existing widgets
    for widget in parent.winfo_children():
        widget.destroy()
    
    parent.configure(fg_color="#1E1E1E")
    
    # Dashboard Title
    title = ctk.CTkLabel(parent, text=f'Welcome "{student_details[0]}"', text_color="#00A2FF", font=("Arial", 24, "bold"))
    title.place(x=500, y=20)
    
    # Name & Info Section
    name_section = ctk.CTkFrame(parent, width=500, height=250, fg_color="#0F172A")
    name_section.place(x=100, y=80)
    
    name_label = ctk.CTkLabel(name_section, text=f"Name: {student_details[0]}\nCourse: {student_details[1]}\nSemester: {student_details[2]}", font=("Arial", 26, "bold"))
    name_label.place(x=50, y=50)

    # Photo Section
    photo_section = ctk.CTkFrame(parent, width=200, height=200, fg_color="#0F172A")
    photo_section.place(x=650, y=80)

    if photo_result:
        photo_path = photo_result[0]  # Get the photo path from DB
        
        try:
            # Load the Image
            image = ctk.CTkImage(light_image=Image.open(photo_path), size=(150, 150))
            
            # Display Image in a Label
            photo_label = ctk.CTkLabel(photo_section, image=image, text="")
            photo_label.place(x=25, y=25)  # Center inside frame
            
        except Exception as e:
            print("Error loading image:", e)
    else:
        print("No photo found for this student.")
    
    # Announcement Section
    announcements = ctk.CTkFrame(parent, width=350, height=250, fg_color="#121826")
    announcements.place(x=100, y=350)

    ann_title = ctk.CTkLabel(announcements, text="📢 Announcements", font=("Arial", 20, "bold"))
    ann_title.place(x=80, y=10)

    # Fetch announcements from DB
    conn = sqlite3.connect('edutrack.db')
    cursor = conn.cursor()
    cursor.execute("SELECT announcement_text FROM announcements ORDER BY created_at DESC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()

    # Display announcements
    if rows:
        y_position = 50
        for ann in rows:
            ann_text = f"• {ann[0]}"
            ann_label = ctk.CTkLabel(announcements, text=ann_text, font=("Arial", 15), wraplength=300, anchor="w", justify="left")
            ann_label.place(x=20, y=y_position)
            y_position += 40
    else:
        no_ann_label = ctk.CTkLabel(announcements, text="No announcements yet.", font=("Arial", 15))
        no_ann_label.place(x=50, y=100)
    
    # Exams Section
    exams = ctk.CTkFrame(parent, width=350, height=250, fg_color="#121826")
    exams.place(x=500, y=350)

    exam_title = ctk.CTkLabel(exams, text="📝 Exams", font=("Arial", 20, "bold"))
    exam_title.place(x=100, y=10)

    # Fetch upcoming exams from DB
    conn = sqlite3.connect('edutrack.db')
    cursor = conn.cursor()
    cursor.execute("SELECT exam_type, date FROM exams ORDER BY date ASC")
    exam_rows = cursor.fetchall()
    conn.close()

    # Display exams
    if exam_rows:
        y_position = 50
        for exam in exam_rows:
            exam_text = f"• {exam[0]} - {exam[1]}"
            exam_label = ctk.CTkLabel(exams, text=exam_text, font=("Arial", 15), wraplength=300, anchor="w", justify="left")
            exam_label.place(x=20, y=y_position)
            y_position += 30
    else:
        no_exam_label = ctk.CTkLabel(exams, text="No upcoming exams.", font=("Arial", 15))
        no_exam_label.place(x=50, y=100)
    
    # Attendance Section
    attendance = ctk.CTkFrame(parent, width=350, height=250, fg_color="#121826")
    attendance.place(x=900, y=350)

    attendance_title = ctk.CTkLabel(attendance, text="📊 Attendance", font=("Arial", 20, "bold"))
    attendance_title.place(x=100, y=10)

    # Fetch attendance data
    conn = sqlite3.connect('edutrack.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.subject_name, a.date, a.status
        FROM attendance a
        INNER JOIN subjects s ON a.subject_id = s.subject_id
        WHERE a.student_id = ?
        ORDER BY a.date DESC LIMIT 5
    """, (user_data[4],))
    attendance_rows = cursor.fetchall()
    conn.close()

    # Display attendance
    if attendance_rows:
        y_position = 50
        for att in attendance_rows:
            att_text = f"• {att[0]} ({att[1]}): {att[2]}"
            att_label = ctk.CTkLabel(attendance, text=att_text, font=("Arial", 15), wraplength=300, anchor="w", justify="left")
            att_label.place(x=20, y=y_position)
            y_position += 30
    else:
        no_att_label = ctk.CTkLabel(attendance, text="No attendance records.", font=("Arial", 15))
        no_att_label.place(x=50, y=100)
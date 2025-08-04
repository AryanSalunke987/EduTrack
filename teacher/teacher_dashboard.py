import customtkinter as ctk
import sqlite3
from PIL import Image

def show_teacher_dashboard(parent, user_data):
    # Fetch teacher details from the database
    conn = sqlite3.connect('edutrack.db')
    cursor = conn.cursor()

    # Fetch Teacher Info
    cursor.execute("""
        SELECT name, department 
        FROM teachers 
        WHERE teacher_id=?
    """, (user_data[5],))
    teacher_details = cursor.fetchone()

    # Fetch Teacher Photo
    cursor.execute("""
        SELECT photo_path 
        FROM phototeacher 
        WHERE teacher_id=?
    """, (user_data[5],))
    photo_result = cursor.fetchone()

    conn.close()

    # Clear existing widgets
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(fg_color="#1E1E1E")

    # Dashboard Title
    title = ctk.CTkLabel(
        parent,
        text=f'Welcome "{teacher_details[0]}"',
        text_color="#00A2FF",
        font=("Arial", 24, "bold")
    )
    title.place(x=500, y=20)

    # Name & Info Section
    info_section = ctk.CTkFrame(parent, width=500, height=250, fg_color="#0F172A")
    info_section.place(x=100, y=80)

    info_label = ctk.CTkLabel(
        info_section,
        text=f"Name: {teacher_details[0]}\nDepartment: {teacher_details[1]}",
        font=("Arial", 24, "bold"),
        text_color="white"
    )
    info_label.place(x=50, y=50)

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
        print("No photo found for this teacher.")

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
            ann_label = ctk.CTkLabel(
                announcements,
                text=ann_text,
                font=("Arial", 14),
                wraplength=300,
                anchor="w",
                justify="left"
            )
            ann_label.place(x=20, y=y_position)
            y_position += 40
    else:
        no_ann_label = ctk.CTkLabel(announcements, text="No announcements yet.", font=("Arial", 14))
        no_ann_label.place(x=50, y=100)

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
    # Meetings Section
    meetings = ctk.CTkFrame(parent, width=350, height=250, fg_color="#121826")
    meetings.place(x=900, y=350)

    meet_label = ctk.CTkLabel(meetings, text="📅 Meetings", font=("Arial", 20, "bold"))
    meet_label.place(x=100, y=10)

    # Fetch meetings from DB
    conn = sqlite3.connect('edutrack.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, time, purpose, link 
        FROM meetings 
        WHERE teacher_id=? 
        ORDER BY date, time LIMIT 5
    """, (user_data[5],))
    meetings_data = cursor.fetchall()
    conn.close()

    # Display meetings
    if meetings_data:
        y_position = 50
        for meeting in meetings_data:
            date, time, purpose, link = meeting
            meeting_text = f"{date} {time}\nPurpose: {purpose}"
            meeting_label = ctk.CTkLabel(
                meetings,
                text=meeting_text,
                font=("Arial", 14),
                wraplength=300,
                anchor="w",
                justify="left"
            )
            meeting_label.place(x=20, y=y_position)

            join_button = ctk.CTkButton(
                meetings,
                text="Join",
                command=lambda l=link: open_meeting_link(l),
                width=50,
                height=20
            )
            join_button.place(x=250, y=y_position + 40)  # Adjusted placement below the purpose text

            y_position += 100  # Increased spacing between meetings to avoid overlap
    else:
        no_meet_label = ctk.CTkLabel(meetings, text="No meetings scheduled.", font=("Arial", 14))
        no_meet_label.place(x=50, y=100)

def open_meeting_link(link):
    import webbrowser
    webbrowser.open(link)
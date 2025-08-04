import customtkinter as ctk
import sqlite3

# ---------------------- Database ----------------------
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("edutrack.db")
        self.cursor = self.conn.cursor()

    def search_student(self, search_type, value):
        query = f"SELECT * FROM students WHERE {search_type} = ?"
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def add_student(self, name, roll, email, phone, course, semester):
        try:
            self.cursor.execute("INSERT INTO students (name, roll_number, email, phone, course, semester) VALUES (?, ?, ?, ?, ?, ?)", 
                                (name, roll, email, phone, course, semester))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return "Error: Student already exists"

    def remove_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

# ---------------------- Student ----------------------
class StudentManagement:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Manage Students", font=("Arial", 20)).pack(pady=10)

        self.search_entry = ctk.CTkEntry(self.frame, width=200, placeholder_text="Search by Name or ID")
        self.search_entry.pack(pady=5)

        self.search_button = ctk.CTkButton(self.frame, text="Search", command=self.search_student)
        self.search_button.pack(pady=5)

        self.result_label = ctk.CTkLabel(self.frame, text="")
        self.result_label.pack()

        ctk.CTkButton(self.frame, text="Add Student", command=self.add_student_form).pack(pady=10)

    def search_student(self):
        value = self.search_entry.get()
        results = self.db.search_student("name", value) or self.db.search_student("student_id", value)

        if results:
            self.result_label.configure(text=f"Found: {results[0][1]}")
        else:
            self.result_label.configure(text="No student found", text_color="red")

    def add_student_form(self):
        form = ctk.CTkToplevel(self.frame)
        form.geometry("300x300")
        ctk.CTkLabel(form, text="Add Student").pack(pady=10)

        name_entry = ctk.CTkEntry(form, placeholder_text="Name")
        name_entry.pack(pady=5)
        roll_entry = ctk.CTkEntry(form, placeholder_text="Roll Number")
        roll_entry.pack(pady=5)
        email_entry = ctk.CTkEntry(form, placeholder_text="Email")
        email_entry.pack(pady=5)
        phone_entry = ctk.CTkEntry(form, placeholder_text="Phone")
        phone_entry.pack(pady=5)
        course_entry = ctk.CTkEntry(form, placeholder_text="Course")
        course_entry.pack(pady=5)
        semester_entry = ctk.CTkEntry(form, placeholder_text="Semester")
        semester_entry.pack(pady=5)

        submit_button = ctk.CTkButton(form, text="Submit", command=lambda: self.db.add_student(
            name_entry.get(), roll_entry.get(), email_entry.get(), phone_entry.get(), course_entry.get(), semester_entry.get()
        ))
        submit_button.pack(pady=10)

# ---------------------- Teacher ----------------------
class TeacherManagement:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Manage Teachers", font=("Arial", 20)).pack(pady=10)

        self.search_entry = ctk.CTkEntry(self.frame, width=200, placeholder_text="Search by Name or ID")
        self.search_entry.pack(pady=5)

        self.search_button = ctk.CTkButton(self.frame, text="Search", command=self.search_teacher)
        self.search_button.pack(pady=5)

        self.result_label = ctk.CTkLabel(self.frame, text="")
        self.result_label.pack()

    def search_teacher(self):
        value = self.search_entry.get()
        query = f"SELECT * FROM teachers WHERE name = ? OR teacher_id = ?"
        self.db.cursor.execute(query, (value, value))
        results = self.db.cursor.fetchall()

        if results:
            self.result_label.configure(text=f"Found: {results[0][1]}")
        else:
            self.result_label.configure(text="No teacher found", text_color="red")

# ---------------------- Attendance ----------------------
class AttendanceManagement:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Attendance Management", font=("Arial", 20)).pack(pady=10)

        student_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Student ID")
        student_entry.pack(pady=5)

        status_var = ctk.StringVar(value="Present")
        ctk.CTkRadioButton(self.frame, text="Present", variable=status_var, value="Present").pack()
        ctk.CTkRadioButton(self.frame, text="Absent", variable=status_var, value="Absent").pack()

        submit_button = ctk.CTkButton(self.frame, text="Mark Attendance",
                                      command=lambda: self.db.cursor.execute(
                                          "INSERT INTO attendance (student_id, date, status) VALUES (?, CURRENT_DATE, ?)",
                                          (student_entry.get(), status_var.get())
                                      ))
        submit_button.pack(pady=10)

# ---------------------- Announcements ----------------------
class AnnouncementManagement:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Make Announcement", font=("Arial", 20)).pack(pady=10)

        msg_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter message", width=300)
        msg_entry.pack(pady=5)

        send_button = ctk.CTkButton(self.frame, text="Send", command=lambda: self.db.cursor.execute(
            "INSERT INTO announcements (message) VALUES (?)", (msg_entry.get(),)
        ))
        send_button.pack(pady=10)

# ---------------------- Settings ----------------------
class SettingsManagement:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Settings & Customization", font=("Arial", 20)).pack(pady=10)

# ---------------------- Main App ----------------------
class EduTrackAdminApp:
    def __init__(self, root):
        self.db = Database()

        root.geometry("800x600")
        root.title("EduTrack Admin Panel")

        self.sidebar = ctk.CTkFrame(root, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(side="right", fill="both", expand=True)

        buttons = [
            ("Students", StudentManagement),
            ("Teachers", TeacherManagement),
            ("Attendance", AttendanceManagement),
            ("Announcements", AnnouncementManagement),
            ("Settings", SettingsManagement),
        ]

        for text, handler in buttons:
            ctk.CTkButton(self.sidebar, text=text, width=180, command=lambda h=handler: self.load_module(h)).pack(pady=5)

        self.load_module(StudentManagement)

    def load_module(self, handler):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        handler(self.main_frame, self.db)

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = EduTrackAdminApp(root)
    root.mainloop()

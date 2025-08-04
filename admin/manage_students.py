import customtkinter as ctk
import sqlite3
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ManageStudents(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = ctk.CTkLabel(self, text="Manage Students", font=("Arial", 20))
        self.title.pack(pady=10)

        # Tab View (Wider to fill more space)
        self.tabview = ctk.CTkTabview(self, width=1000)  # Adjust width to fill more screen space
        self.tabview.pack(expand=True, fill="both", padx=40, pady=20)  # Add padding for better centering

        # Add tabs
        self.create_student_tab = self.tabview.add("Create Student")
        self.create_login_tab = self.tabview.add("Create Login")
        self.delete_student_tab = self.tabview.add("Delete Student")  # New tab for deleting a student

        self.create_student_widgets(self.create_student_tab)
        self.create_login_widgets(self.create_login_tab)
        self.delete_student_widgets(self.delete_student_tab)  # Add widgets to delete student tab

        # --- Student List (Database Bar) ---
        self.student_listbox = ctk.CTkTextbox(self, height=200, width=1000)  # Adjusted width for better alignment
        self.student_listbox.pack(pady=20, padx=40, fill="x")  # Positioned at the bottom, spans width

    def create_student_widgets(self, tab):
        # --- Left Side: Entry Fields ---
        left_frame = ctk.CTkFrame(tab, width=500)  # Adjust width for better centering
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.name_entry = ctk.CTkEntry(left_frame, placeholder_text="Name")
        self.roll_entry = ctk.CTkEntry(left_frame, placeholder_text="Roll Number")
        self.email_entry = ctk.CTkEntry(left_frame, placeholder_text="Email")
        self.phone_entry = ctk.CTkEntry(left_frame, placeholder_text="Phone")
        self.course_entry = ctk.CTkEntry(left_frame, placeholder_text="Course")
        self.semester_entry = ctk.CTkEntry(left_frame, placeholder_text="Semester")

        self.name_entry.pack(pady=5, fill="x")
        self.roll_entry.pack(pady=5, fill="x")
        self.email_entry.pack(pady=5, fill="x")
        self.phone_entry.pack(pady=5, fill="x")
        self.course_entry.pack(pady=5, fill="x")
        self.semester_entry.pack(pady=5, fill="x")

        ctk.CTkButton(left_frame, text="Add Student", command=self.add_student).pack(pady=10, fill="x")
        ctk.CTkButton(left_frame, text="Refresh List", command=self.load_students).pack(pady=5, fill="x")

        # --- Right Side: Photo Upload ---
        right_frame = ctk.CTkFrame(tab, width=500)  # Adjust width for better centering
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkButton(right_frame, text="Upload Photo", command=self.upload_photo).pack(pady=5)
        self.photo_path = None  # To store the selected photo path
        self.photo_label = ctk.CTkLabel(right_frame, text="No photo selected")
        self.photo_label.pack(pady=5)

    def create_login_widgets(self, tab):
        ctk.CTkLabel(tab, text="Create Student Login", font=("Arial", 16)).pack(pady=10)

        self.username_entry = ctk.CTkEntry(tab, placeholder_text="Username")
        self.password_entry = ctk.CTkEntry(tab, placeholder_text="Password", show="*")
        self.role_entry = ctk.CTkEntry(tab, placeholder_text="Role (e.g., Student)")
        self.student_id_entry = ctk.CTkEntry(tab, placeholder_text="Student ID (if applicable)")

        self.username_entry.pack(pady=5, fill="x", padx=20)
        self.password_entry.pack(pady=5, fill="x", padx=20)
        self.role_entry.pack(pady=5, fill="x", padx=20)
        self.student_id_entry.pack(pady=5, fill="x", padx=20)

        ctk.CTkButton(tab, text="Create Login", command=self.create_login).pack(pady=10, fill="x", padx=20)

    def delete_student_widgets(self, tab):
        ctk.CTkLabel(tab, text="Delete Student", font=("Arial", 16)).pack(pady=10)

        self.delete_id_entry = ctk.CTkEntry(tab, placeholder_text="Enter Student ID or Roll Number")
        self.delete_id_entry.pack(pady=5, fill="x", padx=20)

        ctk.CTkButton(tab, text="Delete Student", command=self.delete_student).pack(pady=10, fill="x", padx=20)

    def upload_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.photo_path = file_path
            img = Image.open(file_path).resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            self.photo_label.configure(image=photo, text="")
            self.photo_label.image = photo

    def add_student(self):
        name = self.name_entry.get()
        roll = self.roll_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        course = self.course_entry.get()
        semester = self.semester_entry.get()

        if not all([name, roll, email, course, semester]):
            messagebox.showwarning("Incomplete", "Please fill in all required fields.")
            return

        if not self.photo_path:
            messagebox.showwarning("No Photo", "Please upload a photo for the student.")
            return

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (name, roll_number, email, phone, course, semester)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, roll, email, phone, course, semester))
            conn.commit()

            student_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO photostudent (student_id, name, photo_path)
                VALUES (?, ?, ?)
            """, (student_id, name, self.photo_path))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Student added successfully.")
            self.load_students()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Duplicate Entry: {e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def validate_password(self, password):
        """Validate password based on the given criteria."""
        if len(password) < 8:
            return "Password must be at least 8 characters long."
        if not any(char.isupper() for char in password):
            return "Password must contain at least one uppercase letter."
        if not any(char.isdigit() for char in password):
            return "Password must contain at least one numeric digit."
        if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for char in password):
            return "Password must contain at least one special character."
        return None

    def create_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()
        student_id = self.student_id_entry.get()

        # Validate password
        validation_error = self.validate_password(password)
        if validation_error:
            messagebox.showerror("Invalid Password", validation_error)
            return

        if not all([username, password, role]):
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        try:
            student_id = int(student_id) if student_id else None
        except ValueError:
            messagebox.showerror("Invalid Input", "Student ID must be a number.")
            return

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, role, student_id)
                VALUES (?, ?, ?, ?)
            """, (username, password, role, student_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Login created successfully.")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Duplicate Username: {e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        delete_id = self.delete_id_entry.get()

        if not delete_id:
            messagebox.showwarning("Missing Input", "Please enter a Student ID or Roll Number.")
            return

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()

            # Check if the input is a valid student_id or roll_number
            cursor.execute("""
                DELETE FROM students
                WHERE student_id = ? OR roll_number = ?
            """, (delete_id, delete_id))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Student deleted successfully.")
                self.load_students()
            else:
                messagebox.showwarning("Not Found", "No student found with the given ID or Roll Number.")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_students(self):
        self.student_listbox.delete("0.0", "end")
        conn = sqlite3.connect("edutrack.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.student_listbox.insert("end", f"ID: {row[0]} | Name: {row[1]} | Roll: {row[2]} | Email: {row[3]} | Phone: {row[4]} | Course: {row[5]} | Semester: {row[6]}\n")
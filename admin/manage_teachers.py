import customtkinter as ctk
import sqlite3
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ManageTeachers(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = ctk.CTkLabel(self, text="Manage Teachers", font=("Arial", 20))
        self.title.pack(pady=10)

        # Tab View (Wider to fill more space)
        self.tabview = ctk.CTkTabview(self, width=1000)  # Adjust width to fill more screen space
        self.tabview.pack(expand=True, fill="both", padx=40, pady=20)  # Add padding for better centering

        # Add tabs
        self.add_teacher_tab = self.tabview.add("Add Teacher")
        self.create_login_tab = self.tabview.add("Create Login")
        self.delete_teacher_tab = self.tabview.add("Delete Teacher")  # New tab for deleting a teacher

        self.add_teacher_widgets(self.add_teacher_tab)
        self.create_login_widgets(self.create_login_tab)
        self.delete_teacher_widgets(self.delete_teacher_tab)  # Add widgets to delete teacher tab

        # --- Teacher List (Database Bar) ---
        self.teacher_listbox = ctk.CTkTextbox(self, height=200, width=1000)  # Adjusted width for better alignment
        self.teacher_listbox.pack(pady=20, padx=40, fill="x")  # Positioned at the bottom, spans width

    def add_teacher_widgets(self, tab):
        # --- Left Side: Entry Fields ---
        left_frame = ctk.CTkFrame(tab, width=500)  # Adjust width for better centering
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.name_entry = ctk.CTkEntry(left_frame, placeholder_text="Name")
        self.email_entry = ctk.CTkEntry(left_frame, placeholder_text="Email")
        self.phone_entry = ctk.CTkEntry(left_frame, placeholder_text="Phone")
        self.department_entry = ctk.CTkEntry(left_frame, placeholder_text="Department")

        self.name_entry.pack(pady=5, fill="x")
        self.email_entry.pack(pady=5, fill="x")
        self.phone_entry.pack(pady=5, fill="x")
        self.department_entry.pack(pady=5, fill="x")

        ctk.CTkButton(left_frame, text="Add Teacher", command=self.add_teacher).pack(pady=10, fill="x")
        ctk.CTkButton(left_frame, text="Refresh List", command=self.load_teachers).pack(pady=5, fill="x")

        # --- Right Side: Photo Upload ---
        right_frame = ctk.CTkFrame(tab, width=500)  # Adjust width for better centering
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkButton(right_frame, text="Upload Photo", command=self.upload_photo).pack(pady=5)
        self.photo_path = None  # To store the selected photo path
        self.photo_label = ctk.CTkLabel(right_frame, text="No photo selected")
        self.photo_label.pack(pady=5)

    def create_login_widgets(self, tab):
        ctk.CTkLabel(tab, text="Create Teacher Login", font=("Arial", 16)).pack(pady=10)

        self.username_entry = ctk.CTkEntry(tab, placeholder_text="Username")
        self.password_entry = ctk.CTkEntry(tab, placeholder_text="Password", show="*")
        self.role_entry = ctk.CTkEntry(tab, placeholder_text="Role (e.g., Teacher)")
        self.teacher_id_entry = ctk.CTkEntry(tab, placeholder_text="Teacher ID (if applicable)")

        self.username_entry.pack(pady=5, fill="x", padx=20)
        self.password_entry.pack(pady=5, fill="x", padx=20)
        self.role_entry.pack(pady=5, fill="x", padx=20)
        self.teacher_id_entry.pack(pady=5, fill="x", padx=20)

        ctk.CTkButton(tab, text="Create Login", command=self.create_login).pack(pady=10, fill="x", padx=20)

    def delete_teacher_widgets(self, tab):
        ctk.CTkLabel(tab, text="Delete Teacher", font=("Arial", 16)).pack(pady=10)

        self.delete_id_entry = ctk.CTkEntry(tab, placeholder_text="Enter Teacher ID or Email")
        self.delete_id_entry.pack(pady=5, fill="x", padx=20)

        ctk.CTkButton(tab, text="Delete Teacher", command=self.delete_teacher).pack(pady=10, fill="x", padx=20)

    def upload_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.photo_path = file_path
            img = Image.open(file_path).resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            self.photo_label.configure(image=photo, text="")
            self.photo_label.image = photo

    def add_teacher(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        department = self.department_entry.get()

        if not all([name, email, department]):
            messagebox.showwarning("Incomplete", "Please fill in all required fields.")
            return

        if not self.photo_path:
            messagebox.showwarning("No Photo", "Please upload a photo for the teacher.")
            return

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teachers (name, email, phone, department)
                VALUES (?, ?, ?, ?)
            """, (name, email, phone, department))
            conn.commit()

            teacher_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO phototeacher (teacher_id, name, photo_path)
                VALUES (?, ?, ?)
            """, (teacher_id, name, self.photo_path))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Teacher added successfully.")
            self.load_teachers()
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
        teacher_id = self.teacher_id_entry.get()

        # Validate password
        validation_error = self.validate_password(password)
        if validation_error:
            messagebox.showerror("Invalid Password", validation_error)
            return

        if not all([username, password, role]):
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        try:
            teacher_id = int(teacher_id) if teacher_id else None
        except ValueError:
            messagebox.showerror("Invalid Input", "Teacher ID must be a number.")
            return

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, role, teacher_id)
                VALUES (?, ?, ?, ?)
            """, (username, password, role, teacher_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Login created successfully.")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Duplicate Username: {e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_teacher(self):
        delete_id = self.delete_id_entry.get()

        if not delete_id:
            messagebox.showwarning("Missing Input", "Please enter a Teacher ID or Email.")
            return

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()

            # Check if the input is a valid teacher_id or email
            cursor.execute("""
                DELETE FROM teachers
                WHERE teacher_id = ? OR email = ?
            """, (delete_id, delete_id))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Teacher deleted successfully.")
                self.load_teachers()
            else:
                messagebox.showwarning("Not Found", "No teacher found with the given ID or Email.")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_teachers(self):
        self.teacher_listbox.delete("0.0", "end")
        conn = sqlite3.connect("edutrack.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.teacher_listbox.insert("end", f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Phone: {row[3]} | Department: {row[4]}\n")
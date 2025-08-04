import customtkinter as ctk
import sqlite3
from tkinter import messagebox


class SubjectManager(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = ctk.CTkLabel(self, text="Subject Manager", font=("Arial", 24, "bold"))
        self.title.pack(pady=20)

        # Subject Name Entry
        self.subject_name_label = ctk.CTkLabel(self, text="Subject Name:")
        self.subject_name_label.pack(pady=5)
        self.subject_name_entry = ctk.CTkEntry(self, placeholder_text="Enter subject name")
        self.subject_name_entry.pack(pady=5)

        # Teacher ID Entry
        self.teacher_id_label = ctk.CTkLabel(self, text="Teacher ID:")
        self.teacher_id_label.pack(pady=5)
        self.teacher_id_entry = ctk.CTkEntry(self, placeholder_text="Enter teacher ID")
        self.teacher_id_entry.pack(pady=5)

        # Semester Entry
        self.semester_label = ctk.CTkLabel(self, text="Semester:")
        self.semester_label.pack(pady=5)
        self.semester_entry = ctk.CTkEntry(self, placeholder_text="Enter semester")
        self.semester_entry.pack(pady=5)

        # Course Entry
        self.course_label = ctk.CTkLabel(self, text="Course:")
        self.course_label.pack(pady=5)
        self.course_entry = ctk.CTkEntry(self, placeholder_text="Enter course")
        self.course_entry.pack(pady=5)

        # Add Subject Button
        self.add_subject_button = ctk.CTkButton(self, text="Add Subject", command=self.add_subject)
        self.add_subject_button.pack(pady=10)

        # Delete Subject Section
        self.delete_subject_label = ctk.CTkLabel(self, text="Delete Subject by ID:")
        self.delete_subject_label.pack(pady=5)
        self.delete_subject_entry = ctk.CTkEntry(self, placeholder_text="Enter subject ID to delete")
        self.delete_subject_entry.pack(pady=5)
        self.delete_subject_button = ctk.CTkButton(self, text="Delete Subject", command=self.delete_subject)
        self.delete_subject_button.pack(pady=10)

        # Frame for Textbox and Scrollbar
        display_frame = ctk.CTkFrame(self)
        display_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Subject Display Bar
        self.subject_display = ctk.CTkTextbox(display_frame, height=250, width=900)
        self.subject_display.pack(side="left", fill="both", expand=True)
        self.subject_display.configure(state="disabled", font=("Arial", 14))  # Increased font size

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(display_frame, orientation="vertical", command=self.subject_display.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.subject_display.configure(yscrollcommand=self.scrollbar.set)

        # Load existing subjects
        self.load_subjects()

    def add_subject(self):
        # Get values from entry fields
        subject_name = self.subject_name_entry.get().strip()
        teacher_id = self.teacher_id_entry.get().strip()
        semester = self.semester_entry.get().strip()
        course = self.course_entry.get().strip()

        # Validate inputs
        if not subject_name or not semester or not course:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        if not teacher_id.isdigit() and teacher_id != "":
            messagebox.showerror("Input Error", "Teacher ID must be a valid integer or left blank.")
            return

        try:
            # Insert subject into the database
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO subjects (subject_name, teacher_id, semester, course)
                VALUES (?, ?, ?, ?)
            """, (subject_name, teacher_id if teacher_id else None, semester, course))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Subject '{subject_name}' added successfully.")
            self.clear_fields()
            self.load_subjects()  # Refresh the subject list
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Database Error", f"Failed to add subject: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def delete_subject(self):
        # Get the subject ID to delete
        subject_id = self.delete_subject_entry.get().strip()

        # Validate input
        if not subject_id.isdigit():
            messagebox.showerror("Input Error", "Subject ID must be a valid integer.")
            return

        try:
            # Delete subject from the database
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subjects WHERE subject_id = ?", (subject_id,))
            conn.commit()
            conn.close()

            if cursor.rowcount == 0:
                messagebox.showwarning("Not Found", f"No subject found with ID {subject_id}.")
            else:
                messagebox.showinfo("Success", f"Subject with ID {subject_id} deleted successfully.")
                self.load_subjects()  # Refresh the subject list
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def load_subjects(self):
        # Clear the display
        self.subject_display.configure(state="normal")
        self.subject_display.delete("1.0", "end")

        try:
            # Fetch all subjects from the database
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT subject_id, subject_name, teacher_id, semester, course
                FROM subjects
                ORDER BY subject_id
            """)
            subjects = cursor.fetchall()
            conn.close()

            # Display subjects
            if subjects:
                for subject in subjects:
                    self.subject_display.insert("end", f"ID: {subject[0]} \t|\t Name: {subject[1]} \t|\t Teacher ID: {subject[2]} \t|\t Semester: {subject[3]} \t|\t Course: {subject[4]}\n{'-' * 135}\n")
            else:
                self.subject_display.insert("end", "No subjects found.\n")
            self.subject_display.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load subjects: {e}")
            self.subject_display.configure(state="disabled")

    def clear_fields(self):
        """Clear all input fields."""
        self.subject_name_entry.delete(0, "end")
        self.teacher_id_entry.delete(0, "end")
        self.semester_entry.delete(0, "end")
        self.course_entry.delete(0, "end")
        self.delete_subject_entry.delete(0, "end")
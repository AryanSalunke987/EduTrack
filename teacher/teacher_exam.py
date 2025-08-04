import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry  # For date selection


class TeacherExam(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)  # Ensure the frame fills the parent area
        self.subject_map = {}  # To store subject_name -> subject_id mapping
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = ctk.CTkLabel(self, text="Teacher Exam Panel", font=("Arial", 24, "bold"))
        self.title.pack(pady=20)

        # Dropdown for Options
        self.option_menu = ctk.CTkOptionMenu(
            self,
            values=["Add Exam", "View Exams", "Edit Exam", "Delete Exam"],
            command=self.update_view
        )
        self.option_menu.pack(pady=10)

        # Frames for Actions
        self.add_exam_frame = ctk.CTkFrame(self)
        self.view_exam_frame = ctk.CTkFrame(self)
        self.edit_exam_frame = ctk.CTkFrame(self)
        self.delete_exam_frame = ctk.CTkFrame(self)

        # Add Exam Section
        self.add_exam_widgets()

        # View Exams Section
        self.view_exam_widgets()

        # Edit Exam Section
        self.edit_exam_widgets()

        # Delete Exam Section
        self.delete_exam_widgets()

        # Show the default view
        self.update_view("Add Exam")

    def fetch_subjects(self):
        """Fetch the list of subjects from the database."""
        try:
            # Connect to the database
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()

            # Correct the query to fetch subject_id and subject_name
            cursor.execute("SELECT subject_id, subject_name FROM subjects")
            subjects = cursor.fetchall()

            # Close the connection
            conn.close()

            # Debugging: Print the fetched subjects
            print("Fetched subjects:", subjects)

            # Map subject names to their IDs
            self.subject_map = {subject[1]: subject[0] for subject in subjects}

            # Return the list of subject names
            return list(self.subject_map.keys())
        except Exception as e:
            # Handle any errors and display an error message
            messagebox.showerror("Error", f"Failed to load subjects: {str(e)}")
            return []

    def add_exam_widgets(self):
        """Define the widgets for adding an exam."""
        self.add_exam_frame.pack(fill="both", expand=True)

        # Subject Name Dropdown
        self.subject_label = ctk.CTkLabel(self.add_exam_frame, text="Subject:", font=("Arial", 14))
        self.subject_label.pack(pady=5)

        # Fetch subjects and populate dropdown
        subject_names = self.fetch_subjects()
        if not subject_names:
            subject_names = ["No Subjects Available"]

        self.subject_menu = ctk.CTkOptionMenu(self.add_exam_frame, values=subject_names)
        self.subject_menu.pack(pady=5)

        # Exam Type
        self.exam_type_label = ctk.CTkLabel(self.add_exam_frame, text="Exam Type:", font=("Arial", 14))
        self.exam_type_label.pack(pady=5)
        self.exam_type_menu = ctk.CTkOptionMenu(
            self.add_exam_frame,
            values=["Periodic Test 1", "Periodic Test 2", "End Semester", "Practical"]
        )
        self.exam_type_menu.pack(pady=5)

        # Exam Date
        self.date_label = ctk.CTkLabel(self.add_exam_frame, text="Exam Date (YYYY/MM/DD):", font=("Arial", 14))
        self.date_label.pack(pady=5)
        self.date_picker = DateEntry(
            self.add_exam_frame,
            date_pattern="yyyy/mm/dd",
            font=("Arial", 16),
            justify="center",
            width=20
        )
        self.date_picker.pack(pady=5)

        # Submit Button
        self.submit_button = ctk.CTkButton(
            self.add_exam_frame,
            text="Add Exam",
            command=self.add_exam,
            fg_color="green",
            width=200
        )
        self.submit_button.pack(pady=20)

    def view_exam_widgets(self):
        """Define the widgets for viewing exams."""
        self.view_exam_frame.pack(fill="both", expand=True)

        # List of Exams
        self.exams_frame = ctk.CTkFrame(self.view_exam_frame)
        self.exams_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def edit_exam_widgets(self):
        """Define the widgets for editing an exam."""
        self.edit_exam_frame.pack(fill="both", expand=True)

        # Exam ID
        self.edit_id_label = ctk.CTkLabel(self.edit_exam_frame, text="Exam ID:", font=("Arial", 14))
        self.edit_id_label.pack(pady=5)
        self.edit_id_entry = ctk.CTkEntry(self.edit_exam_frame, width=200)
        self.edit_id_entry.pack(pady=5)

        # New Exam Type
        self.new_exam_type_label = ctk.CTkLabel(self.edit_exam_frame, text="New Exam Type:", font=("Arial", 14))
        self.new_exam_type_label.pack(pady=5)
        self.new_exam_type_menu = ctk.CTkOptionMenu(
            self.edit_exam_frame,
            values=["Periodic Test 1", "Periodic Test 2", "End Semester", "Practical"]
        )
        self.new_exam_type_menu.pack(pady=5)

        # New Exam Date
        self.new_date_label = ctk.CTkLabel(self.edit_exam_frame, text="New Exam Date (YYYY/MM/DD):", font=("Arial", 14))
        self.new_date_label.pack(pady=5)
        self.new_date_picker = DateEntry(
            self.edit_exam_frame,
            date_pattern="yyyy/mm/dd",
            font=("Arial", 16),
            justify="center",
            width=20
        )
        self.new_date_picker.pack(pady=5)

        # Update Button
        self.update_button = ctk.CTkButton(
            self.edit_exam_frame,
            text="Update Exam",
            command=self.edit_exam,
            fg_color="blue",
            width=200
        )
        self.update_button.pack(pady=20)

    def delete_exam_widgets(self):
        """Define the widgets for deleting an exam."""
        self.delete_exam_frame.pack(fill="both", expand=True)

        # Exam ID
        self.delete_id_label = ctk.CTkLabel(self.delete_exam_frame, text="Exam ID:", font=("Arial", 14))
        self.delete_id_label.pack(pady=5)
        self.delete_id_entry = ctk.CTkEntry(self.delete_exam_frame, width=200)
        self.delete_id_entry.pack(pady=5)

        # Delete Button
        self.delete_button = ctk.CTkButton(
            self.delete_exam_frame,
            text="Delete Exam",
            command=self.delete_exam,
            fg_color="red",
            width=200
        )
        self.delete_button.pack(pady=20)

    def update_view(self, selected_option):
        """Show the appropriate section based on the selected option."""
        self.add_exam_frame.pack_forget()
        self.view_exam_frame.pack_forget()
        self.edit_exam_frame.pack_forget()
        self.delete_exam_frame.pack_forget()

        if selected_option == "Add Exam":
            self.add_exam_frame.pack(fill="both", expand=True)
        elif selected_option == "View Exams":
            self.view_exam_frame.pack(fill="both", expand=True)
            self.load_exams()
        elif selected_option == "Edit Exam":
            self.edit_exam_frame.pack(fill="both", expand=True)
        elif selected_option == "Delete Exam":
            self.delete_exam_frame.pack(fill="both", expand=True)

    def add_exam(self):
        """Add a new exam to the database."""
        subject_name = self.subject_menu.get()
        if subject_name not in self.subject_map:
            messagebox.showwarning("Validation Error", "Invalid subject selected.")
            return

        subject_id = self.subject_map[subject_name]
        exam_type = self.exam_type_menu.get()
        exam_date = self.date_picker.get_date().strftime("%Y-%m-%d")

        if not subject_id or not exam_type or not exam_date:
            messagebox.showwarning("Validation Error", "All fields are required.")
            return

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO exams (subject_id, exam_type, date)
                VALUES (?, ?, ?)
            """, (subject_id, exam_type, exam_date))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Exam added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add exam: {str(e)}")

    def load_exams(self):
        """Load and display all exams."""
        try:
            for widget in self.exams_frame.winfo_children():
                widget.destroy()

            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT exam_id, subject_id, exam_type, date
                FROM exams
                ORDER BY date
            """)
            exams = cursor.fetchall()
            conn.close()

            if exams:
                for exam in exams:
                    exam_label = ctk.CTkLabel(
                        self.exams_frame,
                        text=f"ID: {exam[0]} | Subject: {exam[1]} | Type: {exam[2]} | Date: {exam[3]}",
                        font=("Arial", 12)
                    )
                    exam_label.pack(anchor="w", padx=10, pady=2)
            else:
                no_exam_label = ctk.CTkLabel(
                    self.exams_frame,
                    text="No exams scheduled.",
                    font=("Arial", 12)
                )
                no_exam_label.pack(anchor="center", padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load exams: {str(e)}")

    def edit_exam(self):
        """Edit an existing exam."""
        exam_id = self.edit_id_entry.get()
        new_exam_type = self.new_exam_type_menu.get()
        new_exam_date = self.new_date_picker.get_date().strftime("%Y-%m-%d")

        if not exam_id or not new_exam_type or not new_exam_date:
            messagebox.showwarning("Validation Error", "All fields are required.")
            return

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE exams
                SET exam_type = ?, date = ?
                WHERE exam_id = ?
            """, (new_exam_type, new_exam_date, exam_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Exam updated successfully!")
            self.edit_id_entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update exam: {str(e)}")

    def delete_exam(self):
        """Delete an exam from the database."""
        exam_id = self.delete_id_entry.get()

        if not exam_id:
            messagebox.showwarning("Validation Error", "Exam ID is required.")
            return

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM exams
                WHERE exam_id = ?
            """, (exam_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Exam deleted successfully!")
            self.delete_id_entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete exam: {str(e)}")


if __name__ == "__main__":
    # Test the teacher exam interface as a standalone application
    app = ctk.CTk()
    app.title("Teacher Exam Panel")
    app.geometry("800x800")
    TeacherExam(app)
    app.mainloop()
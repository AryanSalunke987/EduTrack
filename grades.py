import customtkinter as ctk
from tkinter import messagebox
import sqlite3


class StudentGrades(ctk.CTkFrame):
    def __init__(self, parent, student_id):

        super().__init__(parent)
        self.student_id = student_id  # Store the logged-in student's ID
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Title with Styling
        self.title = ctk.CTkLabel(
            self,
            text="🎓 Student Grades Panel",
            font=("Arial", 26, "bold"),
            text_color="white",
        )
        self.title.pack(pady=20)

        # Subject Dropdown
        self.subject_label = ctk.CTkLabel(
            self,
            text="📘 Select Subject:",
            font=("Arial", 16),
            text_color="white",
        )
        self.subject_label.pack(pady=5)

        self.subject_menu = ctk.CTkOptionMenu(
            self,
            values=[],
            command=self.load_grades,
            fg_color="#1E88E5",  # Blue Dropdown
            button_color="#1565C0",
            button_hover_color="#42A5F5",
        )
        self.subject_menu.pack(pady=10)

        # Grades Frame
        self.grades_frame = ctk.CTkFrame(self, fg_color="#2E2E2E")  # Dark Background
        self.grades_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load Subjects into Dropdown
        self.load_subjects()

    def load_subjects(self):
        """Load the list of subjects into the dropdown menu."""
        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT subjects.subject_name
                FROM grades
                INNER JOIN exams ON grades.exam_id = exams.exam_id
                INNER JOIN subjects ON exams.subject_id = subjects.subject_id
                WHERE grades.student_id = ?
            """, (self.student_id,))
            subjects = cursor.fetchall()
            conn.close()

            subject_list = [subject[0] for subject in subjects]
            self.subject_menu.configure(values=subject_list)
            if subject_list:
                self.subject_menu.set(subject_list[0])  # Set the first subject as default
                self.load_grades(subject_list[0])  # Load grades for the default subject
            else:
                self.subject_menu.set("No Subjects Available")
                messagebox.showinfo("No Subjects", "No subjects found for this student.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load subjects: {str(e)}")

    def load_grades(self, selected_subject):
        """Load and display the student's grades for the selected subject."""
        try:
            # Clear previous grades
            for widget in self.grades_frame.winfo_children():
                widget.destroy()

            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT exams.exam_type, grades.marks_obtained, grades.total_marks
                FROM grades
                INNER JOIN exams ON grades.exam_id = exams.exam_id
                INNER JOIN subjects ON exams.subject_id = subjects.subject_id
                WHERE grades.student_id = ? AND subjects.subject_name = ?
            """, (self.student_id, selected_subject))
            grades = cursor.fetchall()
            conn.close()

            if grades:
                for grade in grades:
                    exam_type, marks_obtained, total_marks = grade

                    # Create a card-like entry for each grade
                    grade_card = ctk.CTkFrame(
                        self.grades_frame,
                        fg_color="#1E1E1E",  # Slightly lighter dark background
                        corner_radius=8,
                    )
                    grade_card.pack(fill="x", padx=10, pady=5)

                    grade_label = ctk.CTkLabel(
                        grade_card,
                        text=(
                            f"📝 Exam Type: {exam_type} \t 📊 Marks: {marks_obtained}/{total_marks}"
                        ),
                        font=("Arial", 20, "bold"),
                        text_color="white",
                        anchor="w",
                        justify="left",
                    )
                    grade_label.pack(padx=10, pady=10)
            else:
                no_grades_label = ctk.CTkLabel(
                    self.grades_frame,
                    text="🚫 No grades available for this subject.",
                    font=("Arial", 14),
                    text_color="white",
                )
                no_grades_label.pack(anchor="center", padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load grades: {str(e)}")


if __name__ == "__main__":
    # Test the student grades interface with a sample student ID
    app = ctk.CTk()
    app.title("Student Grades Panel")
    app.geometry("900x700")
    app.configure(fg_color="#121212")  # Dark theme background
    StudentGrades(app, student_id=1)  # Pass the logged-in student's ID here
    app.mainloop()
import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
import pandas as pd


class TeacherGrades(ctk.CTkFrame):
    def __init__(self, parent, teacher_id):
        
        super().__init__(parent)
        self.teacher_id = teacher_id  # Store the logged-in teacher's ID
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = ctk.CTkLabel(self, text="Teacher Grades Panel", font=("Arial", 24, "bold"))
        self.title.pack(pady=20)

        # Dropdown for Options
        self.option_menu = ctk.CTkOptionMenu(
            self,
            values=["Add Grades", "View Grades"],
            command=self.update_view
        )
        self.option_menu.pack(pady=10)

        # Frames for Actions
        self.add_grades_frame = ctk.CTkFrame(self)
        self.view_grades_frame = ctk.CTkFrame(self)

        # Add Grades Section
        self.add_grades_widgets()

        # View Grades Section
        self.view_grades_widgets()

        # Show the default view
        self.update_view("Add Grades")

    def add_grades_widgets(self):
        """Define the widgets for adding grades."""
        self.add_grades_frame.pack(fill="both", expand=True)

        # Exam Dropdown
        self.exam_label = ctk.CTkLabel(self.add_grades_frame, text="Select Exam:", font=("Arial", 14))
        self.exam_label.pack(pady=5)
        self.exam_menu = ctk.CTkOptionMenu(self.add_grades_frame, values=[], command=self.load_students)
        self.exam_menu.pack(pady=5)

        # Out Of Marks
        self.out_of_label = ctk.CTkLabel(self.add_grades_frame, text="Out Of Marks:", font=("Arial", 14))
        self.out_of_label.pack(pady=5)
        self.out_of_entry = ctk.CTkEntry(self.add_grades_frame, width=200)
        self.out_of_entry.pack(pady=5)

        # Load Students Button
        self.load_students_button = ctk.CTkButton(
            self.add_grades_frame,
            text="Load Students",
            command=self.load_students,
            fg_color="blue",
            width=150
        )
        self.load_students_button.pack(pady=10)

        # Students List
        self.students_frame = ctk.CTkFrame(self.add_grades_frame)
        self.students_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load Exams into Dropdown
        self.load_exams()

    def view_grades_widgets(self):
        """Define the widgets for viewing grades."""
        self.view_grades_frame.pack(fill="both", expand=True)

        # Exam Dropdown
        self.view_exam_label = ctk.CTkLabel(self.view_grades_frame, text="Select Exam:", font=("Arial", 14))
        self.view_exam_label.pack(pady=5)
        self.view_exam_menu = ctk.CTkOptionMenu(self.view_grades_frame, values=[], command=self.load_grades)
        self.view_exam_menu.pack(pady=5)

        # Grades Table
        self.grades_table = ctk.CTkTextbox(self.view_grades_frame, height=400, width=800)
        self.grades_table.pack(pady=10)

        # Export Button
        self.export_button = ctk.CTkButton(
            self.view_grades_frame,
            text="Export to CSV",
            command=self.export_grades,
            fg_color="blue",
            width=200
        )
        self.export_button.pack(pady=10)

        # Load Exams into Dropdown
        self.load_exams(for_view=True)

    def load_exams(self, for_view=False):
        """Load exams into the dropdown menu for the logged-in teacher."""
        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT exam_id, exam_type, date
                FROM exams
                WHERE subject_id IN (
                    SELECT subject_id
                    FROM subjects
                    WHERE teacher_id = ?
                )
                ORDER BY date ASC
            """, (self.teacher_id,))
            exams = cursor.fetchall()
            conn.close()

            exam_list = [f"{exam[0]} - {exam[1]} ({exam[2]})" for exam in exams]
            if for_view:
                self.view_exam_menu.configure(values=exam_list)
                if exam_list:
                    self.view_exam_menu.set(exam_list[0])
            else:
                self.exam_menu.configure(values=exam_list)
                if exam_list:
                    self.exam_menu.set(exam_list[0])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load exams: {str(e)}")

    def load_students(self, *args):
        """Load all students for the teacher to input grades."""
        try:
            # Clear the students list frame
            for widget in self.students_frame.winfo_children():
                widget.destroy()

            # Fetch students from the database
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT student_id, name, roll_number, course
                FROM students
            """)
            students = cursor.fetchall()
            conn.close()

            if not students:
                messagebox.showwarning("No Students", "No students found in the database.")
                return

            # Display students with entry fields for marks
            self.students_label = ctk.CTkLabel(self.students_frame, text="Enter Marks for Each Student", font=("Arial", 18, "bold"))
            self.students_label.pack(pady=10)

            self.student_marks_entries = {}  # Dictionary to store marks entry widgets

            for student in students:
                student_id, name, roll_number, course = student

                # Create a frame for each student
                student_frame = ctk.CTkFrame(self.students_frame)
                student_frame.pack(fill="x", padx=10, pady=5)

                # Student Info
                student_label = ctk.CTkLabel(
                    student_frame,
                    text=f"Name: {name} | Roll No: {roll_number} | Course: {course}",
                    font=("Arial", 14)
                )
                student_label.pack(side="left", padx=10)

                # Marks Entry
                marks_entry = ctk.CTkEntry(student_frame, width=100)
                marks_entry.pack(side="right", padx=10)
                self.student_marks_entries[student_id] = marks_entry

            # Submit Grades Button
            self.submit_button = ctk.CTkButton(
                self.students_frame,
                text="Submit Grades",
                command=self.submit_grades,
                fg_color="green",
                width=200
            )
            self.submit_button.pack(pady=20)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students: {str(e)}")

    def submit_grades(self):
        """Submit grades for all students."""
        selected_exam = self.exam_menu.get()
        exam_id = selected_exam.split(" - ")[0]
        out_of_marks = self.out_of_entry.get().strip()

        if not exam_id or not out_of_marks:
            messagebox.showwarning("Validation Error", "Please select an Exam and enter Out Of Marks.")
            return

        try:
            # Validate out_of_marks
            out_of_marks = int(out_of_marks)

            # Connect to the database
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()

            # Insert grades for each student
            for student_id, marks_entry in self.student_marks_entries.items():
                marks_obtained = marks_entry.get().strip()

                if not marks_obtained:
                    continue  # Skip if no marks entered

                marks_obtained = int(marks_obtained)

                # Ensure marks are within range
                if marks_obtained > out_of_marks:
                    messagebox.showerror("Validation Error", f"Marks for student ID {student_id} exceed Out Of Marks.")
                    return

                # Insert grade into the database
                cursor.execute("""
                    INSERT INTO grades (student_id, exam_id, marks_obtained, total_marks)
                    VALUES (?, ?, ?, ?)
                """, (student_id, exam_id, marks_obtained, out_of_marks))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Grades submitted successfully!")
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid marks entered. Please enter numeric values.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit grades: {str(e)}")

    def load_grades(self, *args):
        """Load and display all grades for the selected exam."""
        selected_exam = self.view_exam_menu.get()
        exam_id = selected_exam.split(" - ")[0]

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT students.name, grades.marks_obtained, grades.total_marks
                FROM grades
                INNER JOIN students ON grades.student_id = students.student_id
                WHERE grades.exam_id = ?
            """, (exam_id,))
            grades = cursor.fetchall()
            conn.close()

            self.grades_table.delete("1.0", "end")
            for grade in grades:
                student_name, marks_obtained, total_marks = grade
                self.grades_table.insert("end", f"Student: {student_name}, Marks: {marks_obtained}/{total_marks}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load grades: {str(e)}")

    def export_grades(self):
        """Export grades to a CSV file."""
        selected_exam = self.view_exam_menu.get()
        exam_id = selected_exam.split(" - ")[0]

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT students.name, grades.marks_obtained, grades.total_marks
                FROM grades
                INNER JOIN students ON grades.student_id = students.student_id
                WHERE grades.exam_id = ?
            """, (exam_id,))
            grades = cursor.fetchall()
            conn.close()

            # Convert to DataFrame
            df = pd.DataFrame(grades, columns=["Student Name", "Marks Obtained", "Total Marks"])

            # Save to CSV
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Grades exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export grades: {str(e)}")

    def update_view(self, selected_option):
        """Show the appropriate section based on the selected option."""
        self.add_grades_frame.pack_forget()
        self.view_grades_frame.pack_forget()

        if selected_option == "Add Grades":
            self.add_grades_frame.pack(fill="both", expand=True)
        elif selected_option == "View Grades":
            self.view_grades_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    # Test the teacher grades interface with a sample teacher ID
    app = ctk.CTk()
    app.title("Teacher Grades Panel")
    app.geometry("900x700")
    TeacherGrades(app, teacher_id=4)  # Pass the logged-in teacher's ID here
    app.mainloop()
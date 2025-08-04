import customtkinter as ctk
import sqlite3
import datetime
from tkinter import messagebox


class TeacherAttendance(ctk.CTkFrame):
    def __init__(self, parent, teacher_id):
        super().__init__(parent)
        self.pack(fill="both", expand=True)  # Ensure the frame fills the parent area
        self.teacher_id = teacher_id
        self.subject_id = None  # This can be dynamically selected based on the subject taught by the teacher
        self.date = datetime.date.today()
        self.student_checkboxes = {}  # Dictionary to store student_id and selected attendance
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = ctk.CTkLabel(self, text="Mark Attendance", font=("Arial", 24, "bold"))
        self.title.pack(pady=20)

        # Subject Selection Dropdown
        self.subject_var = ctk.StringVar(value="Select Subject")
        self.subject_dropdown = ctk.CTkOptionMenu(
            self,
            variable=self.subject_var,
            values=self.get_teacher_subjects(),
            command=self.load_students
        )
        self.subject_dropdown.pack(pady=10)

        # Student List Frame
        self.student_list_frame = ctk.CTkFrame(self)
        self.student_list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Submit Attendance Button
        self.submit_button = ctk.CTkButton(
            self,
            text="Submit Attendance",
            command=self.submit_attendance,
            fg_color="blue",
            width=200
        )
        self.submit_button.pack(pady=20)

    def get_teacher_subjects(self):
        """Fetch the subjects taught by the teacher."""
        conn = sqlite3.connect("edutrack.db")
        cursor = conn.cursor()

        # Ensure teacher_id is passed correctly
        cursor.execute("""
            SELECT subject_name || " (" || course || " - Sem " || semester || ")" AS subject_display, subject_id
            FROM subjects
            WHERE teacher_id=?
        """, (self.teacher_id,))
        subjects = cursor.fetchall()
        conn.close()
        self.subject_mapping = {subject[0]: subject[1] for subject in subjects}  # Map display name to subject_id

        return list(self.subject_mapping.keys())

    def get_attendance_percentage(self, subject_id, student_id):
        """Calculate and return the attendance percentage for a given student in the selected subject."""
        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()

            # Total sessions for the student in the subject
            cursor.execute("""
                SELECT COUNT(*) FROM attendance
                WHERE student_id = ? AND subject_id = ?
            """, (student_id, subject_id))
            total_sessions = cursor.fetchone()[0]

            # Sessions attended by the student in the subject
            cursor.execute("""
                SELECT COUNT(*) FROM attendance
                WHERE student_id = ? AND subject_id = ? AND status = 'Present'
            """, (student_id, subject_id))
            attended_sessions = cursor.fetchone()[0]

            conn.close()

            # Calculate attendance percentage
            if total_sessions == 0:
                return "0%"  # Avoid division by zero
            percentage = (attended_sessions / total_sessions) * 100
            return f"{percentage:.2f}%"
        except Exception as e:
            return "Error"

    def load_students(self, selected_subject):
        """Load all students in the database and display their current attendance percentage."""
        self.subject_id = self.subject_mapping[selected_subject]

        # Clear the student list frame
        for widget in self.student_list_frame.winfo_children():
            widget.destroy()

        # Fetch all students from the database
        conn = sqlite3.connect("edutrack.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT student_id, name, roll_number
            FROM students
        """)
        students = cursor.fetchall()
        conn.close()

        # Display students with checkboxes for attendance and their current attendance percentage
        self.student_checkboxes = {}  # Reset the dictionary
        for student in students:
            student_frame = ctk.CTkFrame(self.student_list_frame)
            student_frame.pack(fill="x", pady=5)

            # Fetch current attendance percentage
            attendance_percentage = self.get_attendance_percentage(self.subject_id, student[0])

            # Student Name, Roll Number, and Attendance Percentage
            student_label = ctk.CTkLabel(
                student_frame,
                text=f"{student[2]} - {student[1]} (Attendance: {attendance_percentage})",
                font=("Arial", 14)
            )
            student_label.pack(side="left", padx=10)

            # Checkbox for Present
            present_var = ctk.BooleanVar(value=False)  # Default to not checked
            present_checkbox = ctk.CTkCheckBox(
                student_frame,
                text="Present",
                variable=present_var,
                onvalue=True,
                offvalue=False
            )
            present_checkbox.pack(side="right", padx=5)

            # Checkbox for Absent
            absent_var = ctk.BooleanVar(value=False)  # Default to not checked
            absent_checkbox = ctk.CTkCheckBox(
                student_frame,
                text="Absent",
                variable=absent_var,
                onvalue=True,
                offvalue=False
            )
            absent_checkbox.pack(side="right", padx=5)

            # Store both checkboxes in the dictionary
            self.student_checkboxes[student[0]] = {
                "present": present_var,
                "absent": absent_var
            }

    def submit_attendance(self):
        """Submit attendance for all students."""
        if not self.subject_id:
            messagebox.showwarning("Warning", "Please select a subject to mark attendance.")
            return

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()

            for student_id, attendance_vars in self.student_checkboxes.items():
                present_status = attendance_vars["present"].get()
                absent_status = attendance_vars["absent"].get()

                # Determine attendance status
                if present_status and absent_status:
                    messagebox.showerror("Error", f"Student ID {student_id} cannot be both Present and Absent.")
                    return
                elif present_status:
                    attendance_status = "Present"
                elif absent_status:
                    attendance_status = "Absent"
                else:
                    messagebox.showerror("Error", f"Please mark attendance for Student ID {student_id}.")
                    return

                # Insert a new attendance record for the current session (no overwriting)
                cursor.execute("""
                    INSERT INTO attendance (student_id, subject_id, date, status)
                    VALUES (?, ?, ?, ?)
                """, (student_id, self.subject_id, self.date, attendance_status))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Attendance submitted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit attendance: {str(e)}")


if __name__ == "__main__":
    # Test the attendance marking interface as a standalone application
    app = ctk.CTk()
    app.title("Teacher Attendance")
    app.geometry("800x600")
    TeacherAttendance(app, teacher_id=4)  # Use teacher_id=4 for testing
    app.mainloop()
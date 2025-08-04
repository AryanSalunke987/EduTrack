import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import datetime  # To calculate day of the week


class StudentExam(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)  # Ensure the frame fills the parent area
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = ctk.CTkLabel(
            self,
            text="🎓 Student Exam Panel",
            font=("Arial", 26, "bold"),
            text_color="white",
        )
        self.title.pack(pady=20)

        # Filter Options
        self.filter_frame = ctk.CTkFrame(self, fg_color="#2E2E2E")  # Dark background for filter section
        self.filter_frame.pack(pady=10, fill="x", padx=10)

        # Filter by Subject Name
        self.subject_filter_label = ctk.CTkLabel(
            self.filter_frame,
            text="📘 Subject Name:",
            font=("Arial", 14),
            text_color="white",
        )
        self.subject_filter_label.grid(row=0, column=0, padx=10, pady=5)
        self.subject_filter_entry = ctk.CTkEntry(self.filter_frame, width=200, placeholder_text="Enter subject name")
        self.subject_filter_entry.grid(row=0, column=1, padx=10, pady=5)

        # Filter by Exam Type
        self.exam_type_label = ctk.CTkLabel(
            self.filter_frame,
            text="📑 Exam Type:",
            font=("Arial", 14),
            text_color="white",
        )
        self.exam_type_label.grid(row=0, column=2, padx=10, pady=5)
        self.exam_type_menu = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["All", "Periodic Test 1", "Periodic Test 2", "End Semester", "Practical"],
            command=self.load_exams,
            fg_color="#1E88E5",  # Blue Dropdown
            button_color="#1565C0",
            button_hover_color="#42A5F5",
        )
        self.exam_type_menu.grid(row=0, column=3, padx=10, pady=5)
        self.exam_type_menu.set("All")  # Default value

        # Search Button
        self.search_button = ctk.CTkButton(
            self.filter_frame,
            text="Search Exams",
            command=self.load_exams,
            fg_color="blue",
            hover_color="#42A5F5",
            width=150,
        )
        self.search_button.grid(row=0, column=4, padx=10, pady=5)

        # Scheduled Exams Section
        self.scheduled_exams_label = ctk.CTkLabel(
            self,
            text="📅 Scheduled Exams",
            font=("Arial", 18, "bold"),
            text_color="white",
        )
        self.scheduled_exams_label.pack(pady=10)
        self.exams_frame = ctk.CTkFrame(self, fg_color="#2E2E2E")  # Dark background for exams list
        self.exams_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load all exams initially
        self.load_exams(default=True)

    def load_exams(self, *args, default=False):
        """Load and display the scheduled exams for the student."""
        try:
            # Clear previous exam entries
            for widget in self.exams_frame.winfo_children():
                widget.destroy()

            # Connect to the database
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()

            # By default, fetch all exams
            query = """
                SELECT exams.date, subjects.subject_name, exams.exam_type
                FROM exams
                INNER JOIN subjects ON exams.subject_id = subjects.subject_id
            """
            params = []

            if not default:
                # Build query with filters if not default
                query += " WHERE 1=1"

                # Apply subject name filter
                subject_name = self.subject_filter_entry.get().strip()
                if subject_name:
                    query += " AND subjects.subject_name LIKE ?"
                    params.append(f"%{subject_name}%")

                # Apply exam type filter
                exam_type = self.exam_type_menu.get()
                if exam_type != "All":
                    query += " AND exams.exam_type = ?"
                    params.append(exam_type)

            # Add sorting by date
            query += " ORDER BY exams.date ASC"

            # Execute the query
            cursor.execute(query, params)
            exams = cursor.fetchall()
            conn.close()

            # Display the exams
            if exams:
                for exam in exams:
                    exam_date = exam[0]
                    subject_name = exam[1]
                    exam_type = exam[2]

                    # Format the date and calculate the day of the week
                    formatted_date = datetime.datetime.strptime(exam_date, "%Y-%m-%d")
                    exam_day = formatted_date.strftime("%A")  # e.g., Monday, Tuesday

                    # Create card-like entry for each exam
                    exam_card = ctk.CTkFrame(
                        self.exams_frame,
                        fg_color="#1E1E1E",  # Slightly lighter dark background
                        corner_radius=8,
                    )
                    exam_card.pack(fill="x", padx=10, pady=5)

                    exam_label = ctk.CTkLabel(
                        exam_card,
                        text=(
                            f"📅 Date: {formatted_date.strftime('%Y-%m-%d')}\t"
                            f"🕒 Day: {exam_day}\t "
                            f"📘 Subject: {subject_name}\t "
                            f"📑 Type: {exam_type}"
                        ),
                        font=("Arial", 18, "bold"),
                        text_color="white",
                        anchor="w",
                        justify="left",
                    )
                    exam_label.pack(padx=10, pady=10)
            else:
                no_exam_label = ctk.CTkLabel(
                    self.exams_frame,
                    text="🚫 No exams scheduled.",
                    font=("Arial", 14, "bold"),
                    text_color="white",
                )
                no_exam_label.pack(anchor="center", padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load exams: {str(e)}")


if __name__ == "__main__":
    # Test the student exam interface as a standalone application
    app = ctk.CTk()
    app.title("Student Exam Panel")
    app.geometry("900x700")
    app.configure(fg_color="#121212")  # Dark theme background
    StudentExam(app)  # Initialize the StudentExam class
    app.mainloop()
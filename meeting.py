import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import webbrowser
from tkcalendar import DateEntry  # For date filtering


class StudentMeeting(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)  # Ensure the frame fills the parent area
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = ctk.CTkLabel(self, text="Student Meeting Panel", font=("Arial", 24, "bold"))
        self.title.pack(pady=20)

        # Filter by Date
        self.filter_label = ctk.CTkLabel(self, text="Filter by Date (Optional):", font=("Arial", 14))
        self.filter_label.pack(pady=5)
        self.date_picker = DateEntry(
            self,
            date_pattern="yyyy/mm/dd",
            font=("Arial", 16),
            justify="center",
            width=20
        )
        self.date_picker.pack(pady=5)

        # Filter Button
        self.filter_button = ctk.CTkButton(
            self,
            text="Filter Meetings",
            command=self.filter_meetings,
            fg_color="blue",
            width=200
        )
        self.filter_button.pack(pady=10)

        # Scheduled Meetings Section
        self.scheduled_meetings_label = ctk.CTkLabel(self, text="All Scheduled Meetings", font=("Arial", 18, "bold"))
        self.scheduled_meetings_label.pack(pady=10)
        self.meetings_frame = ctk.CTkFrame(self)
        self.meetings_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load all meetings initially
        self.load_all_meetings()

    def load_all_meetings(self, filter_date=None):
        """Load and display all scheduled meetings."""
        try:
            # Clear previous meeting entries
            for widget in self.meetings_frame.winfo_children():
                widget.destroy()

            # Connect to the database and fetch meetings
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()

            if filter_date:
                cursor.execute("""
                    SELECT meeting_id, date, time, purpose, link, teacher_id
                    FROM meetings
                    WHERE date = ?
                    ORDER BY date, time
                """, (filter_date,))
            else:
                cursor.execute("""
                    SELECT meeting_id, date, time, purpose, link, teacher_id
                    FROM meetings
                    ORDER BY date, time
                """)
            
            meetings = cursor.fetchall()
            conn.close()

            # Display the meetings
            if meetings:
                for meeting in meetings:
                    meeting_details = (
                        f"ID: {meeting[0]} | {meeting[1]} at {meeting[2]} - {meeting[3]} "
                        f"(Teacher ID: {meeting[5]})"
                    )
                    
                    # Display meeting details
                    meeting_label = ctk.CTkLabel(
                        self.meetings_frame,
                        text=meeting_details,
                        font=("Arial", 12)
                    )
                    meeting_label.pack(anchor="w", padx=10, pady=5)

                    # Join Meeting Button
                    join_button = ctk.CTkButton(
                        self.meetings_frame,
                        text="Join Meeting",
                        command=lambda link=meeting[4]: self.open_meeting_link(link),
                        fg_color="green",
                        width=150
                    )
                    join_button.pack(anchor="w", padx=10, pady=5)
            else:
                no_meeting_label = ctk.CTkLabel(
                    self.meetings_frame,
                    text="No scheduled meetings.",
                    font=("Arial", 12)
                )
                no_meeting_label.pack(anchor="center", padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load meetings: {str(e)}")

    def filter_meetings(self):
        """Filter meetings by the selected date."""
        selected_date = self.date_picker.get_date().strftime("%Y-%m-%d")
        self.load_all_meetings(filter_date=selected_date)

    def open_meeting_link(self, link):
        """Open the meeting link in the default web browser."""
        try:
            webbrowser.open(link)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open meeting link: {str(e)}")


if __name__ == "__main__":
    # Test the student meeting interface as a standalone application
    app = ctk.CTk()
    app.title("Student Meeting Panel")
    app.geometry("800x800")
    StudentMeeting(app)  # No student_id needed as all meetings are visible
    app.mainloop()
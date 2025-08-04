import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry  # For selecting a date


class TeacherMeeting(ctk.CTkFrame):
    def __init__(self, parent, teacher_id):
        super().__init__(parent)
        self.pack(fill="both", expand=True)  # Ensure the frame fills the parent area
        self.teacher_id = teacher_id
        self.current_option = ctk.StringVar(value="Create Meeting")  # Default option
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = ctk.CTkLabel(self, text="Teacher Meeting Panel", font=("Arial", 24, "bold"))
        self.title.pack(pady=20)

        # Dropdown Menu to Select Action
        self.option_menu = ctk.CTkOptionMenu(
            self,
            values=["Create Meeting", "Delete Meeting"],
            variable=self.current_option,
            command=self.update_view
        )
        self.option_menu.pack(pady=10)

        # Frames for Create and Delete Meeting
        self.create_frame = ctk.CTkFrame(self)
        self.delete_frame = ctk.CTkFrame(self)

        # Create Meeting Section
        self.create_meeting_widgets()

        # Delete Meeting Section
        self.delete_meeting_widgets()

        # Display the default view (Create Meeting)
        self.update_view("Create Meeting")

        # Scheduled Meetings Section
        self.scheduled_meetings_label = ctk.CTkLabel(self, text="Scheduled Meetings", font=("Arial", 18, "bold"))
        self.scheduled_meetings_label.pack(pady=10)
        self.meetings_frame = ctk.CTkFrame(self)
        self.meetings_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load Scheduled Meetings
        self.load_scheduled_meetings()

    def create_meeting_widgets(self):
        """Define the widgets for creating a meeting."""
        self.create_frame.pack(fill="both", expand=True)

        # Meeting Link
        self.link_label = ctk.CTkLabel(self.create_frame, text="Meeting Link:", font=("Arial", 14))
        self.link_label.pack(pady=5)
        self.link_entry = ctk.CTkEntry(self.create_frame, width=400)
        self.link_entry.pack(pady=5)

        # Meeting Date
        self.date_label = ctk.CTkLabel(self.create_frame, text="Meeting Date (YYYY/MM/DD):", font=("Arial", 14))
        self.date_label.pack(pady=5)
        self.date_picker = DateEntry(
            self.create_frame,
            date_pattern="yyyy/mm/dd",
            font=("Arial", 16),  # Larger font size
            justify="center",
            width=20
        )
        self.date_picker.pack(pady=5)

        # Meeting Time
        self.time_label = ctk.CTkLabel(self.create_frame, text="Meeting Time (24-Hour Clock):", font=("Arial", 14))
        self.time_label.pack(pady=5)
        self.time_entry = ctk.CTkEntry(self.create_frame, placeholder_text="HH:MM (e.g., 14:00)", width=200)
        self.time_entry.pack(pady=5)

        # Meeting Purpose
        self.purpose_label = ctk.CTkLabel(self.create_frame, text="Meeting Purpose:", font=("Arial", 14))
        self.purpose_label.pack(pady=5)
        self.purpose_entry = ctk.CTkEntry(self.create_frame, width=400)
        self.purpose_entry.pack(pady=5)

        # Submit Button
        self.submit_button = ctk.CTkButton(
            self.create_frame,
            text="Schedule Meeting",
            command=self.schedule_meeting,
            fg_color="green",
            width=200
        )
        self.submit_button.pack(pady=20)

    def delete_meeting_widgets(self):
        """Define the widgets for deleting a meeting."""
        self.delete_frame.pack(fill="both", expand=True)

        # Meeting ID (for deletion)
        self.delete_id_label = ctk.CTkLabel(self.delete_frame, text="Meeting ID (Optional):", font=("Arial", 14))
        self.delete_id_label.pack(pady=5)
        self.delete_id_entry = ctk.CTkEntry(self.delete_frame, width=200)
        self.delete_id_entry.pack(pady=5)

        # Date and Time (for deletion)
        self.delete_date_label = ctk.CTkLabel(self.delete_frame, text="Meeting Date (YYYY/MM/DD):", font=("Arial", 14))
        self.delete_date_label.pack(pady=5)
        self.delete_date_picker = DateEntry(
            self.delete_frame,
            date_pattern="yyyy/mm/dd",
            font=("Arial", 16),
            justify="center",
            width=20
        )
        self.delete_date_picker.pack(pady=5)

        self.delete_time_label = ctk.CTkLabel(self.delete_frame, text="Meeting Time (24-Hour Clock):", font=("Arial", 14))
        self.delete_time_label.pack(pady=5)
        self.delete_time_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="HH:MM (e.g., 14:00)", width=200)
        self.delete_time_entry.pack(pady=5)

        # Delete Button
        self.delete_button = ctk.CTkButton(
            self.delete_frame,
            text="Delete Meeting",
            command=self.delete_meeting,
            fg_color="red",
            width=200
        )
        self.delete_button.pack(pady=20)

    def update_view(self, selected_option):
        """Show the appropriate section based on the selected option."""
        if selected_option == "Create Meeting":
            self.delete_frame.pack_forget()
            self.create_frame.pack(fill="both", expand=True)
        elif selected_option == "Delete Meeting":
            self.create_frame.pack_forget()
            self.delete_frame.pack(fill="both", expand=True)

    def schedule_meeting(self):
        """Store the meeting details in the database."""
        meeting_link = self.link_entry.get()
        meeting_date = self.date_picker.get_date().strftime("%Y-%m-%d")
        meeting_time = self.time_entry.get()
        meeting_purpose = self.purpose_entry.get()

        # Validate inputs
        if not meeting_link or not meeting_date or not meeting_time or not meeting_purpose:
            messagebox.showwarning("Validation Error", "All fields are required.")
            return

        if ":" not in meeting_time or len(meeting_time.split(":")) != 2:
            messagebox.showwarning("Validation Error", "Please enter a valid 24-hour time format (HH:MM).")
            return

        try:
            # Save the meeting details in the database
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO meetings (teacher_id, date, time, purpose, link)
                VALUES (?, ?, ?, ?, ?)
            """, (self.teacher_id, meeting_date, meeting_time, meeting_purpose, meeting_link))
            conn.commit()
            conn.close()

            # Show success message
            messagebox.showinfo("Success", "Meeting scheduled successfully!")
            self.clear_create_form()

            # Reload Scheduled Meetings
            self.load_scheduled_meetings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule meeting: {str(e)}")

    def delete_meeting(self):
        """Delete a meeting from the database."""
        meeting_id = self.delete_id_entry.get()
        meeting_date = self.delete_date_picker.get_date().strftime("%Y-%m-%d")
        meeting_time = self.delete_time_entry.get()

        try:
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()

            if meeting_id:
                # Delete by meeting ID
                cursor.execute("DELETE FROM meetings WHERE meeting_id = ? AND teacher_id = ?", (meeting_id, self.teacher_id))
            elif meeting_date and meeting_time:
                # Delete by date and time
                cursor.execute("DELETE FROM meetings WHERE date = ? AND time = ? AND teacher_id = ?", (meeting_date, meeting_time, self.teacher_id))
            else:
                messagebox.showwarning("Validation Error", "Please provide either the Meeting ID or both Date and Time.")
                return

            conn.commit()
            rows_deleted = cursor.rowcount
            conn.close()

            if rows_deleted > 0:
                messagebox.showinfo("Success", "Meeting deleted successfully!")
            else:
                messagebox.showwarning("Not Found", "No matching meeting found.")

            # Reload Scheduled Meetings
            self.load_scheduled_meetings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete meeting: {str(e)}")

    def load_scheduled_meetings(self):
        """Load and display the scheduled meetings for the teacher."""
        try:
            # Clear the meetings frame first
            for widget in self.meetings_frame.winfo_children():
                widget.destroy()

            # Connect to the database and fetch meetings
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT meeting_id, date, time, purpose, link
                FROM meetings
                WHERE teacher_id = ?
                ORDER BY date, time
            """, (self.teacher_id,))
            meetings = cursor.fetchall()
            conn.close()

            # Display the meetings
            if meetings:
                for meeting in meetings:
                    meeting_label = ctk.CTkLabel(
                        self.meetings_frame,
                        text=f"ID: {meeting[0]} | {meeting[1]} at {meeting[2]} - {meeting[3]} (Link: {meeting[4]})",
                        font=("Arial", 12)
                    )
                    meeting_label.pack(anchor="w", padx=10, pady=2)
            else:
                no_meeting_label = ctk.CTkLabel(
                    self.meetings_frame,
                    text="No scheduled meetings.",
                    font=("Arial", 12)
                )
                no_meeting_label.pack(anchor="center", padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load scheduled meetings: {str(e)}")

    def clear_create_form(self):
        """Clear the form inputs for creating a meeting."""
        self.link_entry.delete(0, 'end')
        self.time_entry.delete(0, 'end')
        self.purpose_entry.delete(0, 'end')


if __name__ == "__main__":
    # Test the meeting scheduling interface as a standalone application
    app = ctk.CTk()
    app.title("Teacher Meeting Panel")
    app.geometry("800x800")
    TeacherMeeting(app, teacher_id=4)  # Use teacher_id=1 for testing
    app.mainloop()
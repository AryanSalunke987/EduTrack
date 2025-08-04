import customtkinter as ctk
from sidebar import create_sidebar
from attendance import show_attendance
from exams import StudentExam
from timetable import StudentTimetable
from grades import StudentGrades
from meeting import StudentMeeting
from dashboard import show_dashboard
from settings import create_settings  # Updated settings import
from auth import logout
import sqlite3
from tkinter import messagebox  # For logout confirmation dialogs


class EduTrackApp(ctk.CTk):
    def __init__(self, user_data):
        super().__init__()

        self.title("EduTrack: Student Performance Monitoring")
        self.geometry("1920x1080")

        self.user_data = user_data

        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create Content Frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Create Sidebar with proper function calls
        self.sidebar = create_sidebar(
            self,
            lambda: self.navigate("dashboard"),
            lambda: self.navigate("attendance"),
            lambda: self.navigate("exams"),
            lambda: self.navigate("timetable"),
            lambda: self.navigate("grades"),
            lambda: self.navigate("meeting"),
            lambda: self.navigate("settings"),
            self.logout_confirmation  # Updated logout to include confirmation
        )

        # Show the default page based on the role
        self.show_default_page()

    def navigate(self, page):
        """Navigate to the selected page."""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Load the selected page
        if page == "dashboard":
            show_dashboard(self.content_frame, self.user_data)
        elif page == "attendance":
            show_attendance(self.content_frame, self.user_data)
        elif page == "exams":
            StudentExam(self.content_frame)
        elif page == "timetable":
            StudentTimetable(self.content_frame)
        elif page == "grades":
            StudentGrades(self.content_frame, self.user_data[4])
        elif page == "meeting":
            StudentMeeting(self.content_frame)
        elif page == "settings": 
            create_settings(self.content_frame, self.user_data)
        elif page == "logout":
            self.logout_confirmation()
        else:
            raise ValueError(f"Unknown page: {page}")

    def logout_confirmation(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.quit()  # Close the app

    def show_default_page(self):
        role = self.user_data[3]  # Assuming the 4th element in user_data is the role
        if role == "Student":
            self.navigate("dashboard")
        elif role == "Teacher":
            self.navigate("performance")  # Example: Teachers might start with performance
        elif role == "Admin":
            self.navigate("settings")  # Example: Admins might start with settings
        else:
            messagebox.showerror("Error", f"Unknown role: {role}")
            self.quit()


if __name__ == "__main__":
    # Example user_data tuple (user_id, username, password, role, student_id, teacher_id)
    user_data = (1, "John", "pass", "Student", 1, None)
    app = EduTrackApp(user_data)
    app.mainloop()
import customtkinter as ctk
from  teacher.teacher_sidebar import create_teacher_sidebar
from  teacher.teacher_dashboard import show_teacher_dashboard  # Import the dashboard function
from  teacher.teacher_announcements import MakeAnnouncements  # Import the MakeAnnouncements class
from  teacher.teacher_timetable import TeacherTimetable
from  teacher.teacher_attendance import TeacherAttendance
from  teacher.teacher_meeting import TeacherMeeting
from  teacher.teacher_grades1 import TeacherGrades
from  teacher.teacher_exam import TeacherExam
from teacher.teacher_performance import TeacherPerformance
from teacher.teacher_settings import create_teacher_settings
from  teacher.db_manager import DatabaseManager  # Import the DatabaseManager class

class TeacherPanelApp(ctk.CTk):
    def __init__(self, user_data=None):
        super().__init__()

        self.title("EduTrack: Teacher Performance Monitoring")
        self.geometry("1920x1080")
        self.configure(fg_color="#1a1a1a")  # Set background color to dark

        # Default to teacher_id = 4 unless overridden by user_data
        self.user_data = user_data or (None, "default_teacher", "password", "Teacher", None, 4)  # Example: teacher_id = 4

        # Sidebar
        self.sidebar = create_teacher_sidebar(
            self,
            self.on_dashboard,
            self.on_attendance,
            self.on_exams,
            self.on_grades,
            self.on_performance,
            self.on_meetings,
            self.on_announcements,
            self.on_timetable,
            self.on_settings,
            self.logout_confirmation,
        )

        # Content Frame
        self.content_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Show the dashboard by default
        self.on_dashboard()

    # Navigation Functions
    def on_dashboard(self):
        self.clear_content()
        show_teacher_dashboard(self.content_frame, self.user_data)  # Pass user_data to the dashboard function

    def on_attendance(self):
        self.clear_content()
        teacher_id = self.user_data[5]  # Extract teacher_id from user_data
        TeacherAttendance(self.content_frame, teacher_id)  # Pass teacher_id as an integer

    def on_exams(self):
        self.clear_content()
        TeacherExam(self.content_frame)

    def on_grades(self):
        self.clear_content()
        teacher_id = self.user_data[5]
        grades_module = TeacherGrades(self.content_frame, teacher_id)
        grades_module.show()  # Make sure to call show() to display the interface
        
    def on_performance(self):
        self.clear_content()
        teacher_id = self.user_data[5]
        self.performance_module = TeacherPerformance(self.content_frame, teacher_id)
        self.performance_module.show()  # Display the performance analysis interface


    def on_meetings(self):
        self.clear_content()
        teacher_id = self.user_data[5]
        TeacherMeeting(self.content_frame, teacher_id)

    def on_announcements(self):
        self.clear_content()
        MakeAnnouncements(self.content_frame)  # Display the MakeAnnouncements frame in the content area

    def on_timetable(self):
        self.clear_content()
        TeacherTimetable(self.content_frame)  # Display the timetable in the content area

    def on_settings(self):
        self.clear_content()
        teacher_id = self.user_data[5]
        create_teacher_settings(self.content_frame, teacher_id)

    def logout_confirmation(self):
        self.quit()  # Exit the application

    def clear_content(self):
        """Clear all widgets in the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    # Default teacher_id = 4 if no user_data is provided
    app = TeacherPanelApp()
    app.mainloop()
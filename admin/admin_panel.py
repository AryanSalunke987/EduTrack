import customtkinter as ctk
from admin.manage_students import ManageStudents
from admin.manage_teachers import ManageTeachers  # Import the ManageTeachers class
from admin.make_announcements import MakeAnnouncements
from admin.subject_manager import SubjectManager
import sqlite3  # Used for database operations


class AdminPanel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("1920x1080")
        self.configure(bg="#1e1e1e")  # Set background color

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, corner_radius=15, bg_color="#2e2e2e", width=200, height=1080)
        self.sidebar.place(x=10, y=10)

        ctk.CTkLabel(self.sidebar, text="Admin Panel", font=("Arial", 20, "bold"), text_color="white").pack(pady=20)

        buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("📅Manage Students", self.manage_students),
            ("📅Manage Teachers", self.manage_teachers),
            ("📝Manage Subjects", self.manage_subjects),
            ("📢Make Announcements", self.make_announcements),
            ("⚙️Settings", self.show_settings),
            ("🚪Logout", self.logout)
        ]

  
        for name, command in buttons:
            ctk.CTkButton(self.sidebar, text=name, command=command).pack(pady=5, fill="x", padx=10)

        # Main content area
        self.main_area = ctk.CTkFrame(self, corner_radius=15, bg_color="#1e1e1e", width=1200, height=700)
        self.main_area.place(x=220, y=10)

        self.show_dashboard()

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def get_counts(self):
        """Fetch the count of students, teachers, and admins from the database."""
        connection = sqlite3.connect("edutrack.db")  # Connects to your database
        cursor = connection.cursor()
        try:
            # Query to get student count
            cursor.execute("SELECT COUNT(*) FROM students")
            student_count = cursor.fetchone()[0]

            # Query to get teacher count
            cursor.execute("SELECT COUNT(*) FROM teachers")
            teacher_count = cursor.fetchone()[0]

            # Query to get admin count
            cursor.execute("SELECT COUNT(*) FROM admin")
            admin_count = cursor.fetchone()[0]

        except sqlite3.Error as e:
            student_count = teacher_count = admin_count = "Error"
            print(f"Database error: {e}")

        finally:
            connection.close()

        return student_count, teacher_count, admin_count

    def get_announcements(self):
        """Fetch announcements from the database."""
        connection = sqlite3.connect("edutrack.db")  # Connects to your database
        cursor = connection.cursor()
        try:
            # Query to fetch all announcements, ordered by the newest first
            cursor.execute("""
                SELECT announcement_text, created_at 
                FROM announcements 
                ORDER BY created_at DESC
            """)
            announcements = cursor.fetchall()  # Returns a list of tuples (announcement_text, created_at)
        except sqlite3.Error as e:
            announcements = [("Error fetching announcements", "")]
            print(f"Database error: {e}")
        finally:
            connection.close()

        return announcements

    def create_stat_card(self, parent, title, count, x, y, color):
        """Helper function to create a larger statistics card."""
        card = ctk.CTkFrame(parent, corner_radius=15, width=400, height=200, bg_color="#2e2e2e")  # Increased size
        card.place(x=x, y=y)
        ctk.CTkLabel(card, text=title, font=("Arial", 16, "bold"), text_color="white").pack(pady=15)  # Adjusted font size
        ctk.CTkLabel(card, text=str(count), font=("Arial", 40, "bold"), text_color=color).pack()  # Larger count font

    def create_announcements_section(self, parent, announcements, x, y):
        """Helper function to create a scrollable announcements section."""
        announcements_frame = ctk.CTkScrollableFrame(parent, width=1000, height=250, corner_radius=15, bg_color="#2e2e2e")
        announcements_frame.place(x=x, y=y)

        ctk.CTkLabel(announcements_frame, text="Announcements", font=("Arial", 18, "bold"), text_color="white").pack(pady=10)

        for announcement_text, created_at in announcements:
            announcement_frame = ctk.CTkFrame(announcements_frame, width=950, height=50, corner_radius=15, bg_color="#393939")
            announcement_frame.pack(pady=5, padx=10, fill="x")

            ctk.CTkLabel(announcement_frame, text=announcement_text, font=("Arial", 14), text_color="white").pack(side="left", padx=10)
            ctk.CTkLabel(announcement_frame, text=created_at, font=("Arial", 12), text_color="#aaaaaa").pack(side="right", padx=10)

    def show_dashboard(self):
        self.clear_main_area()

        # Center the title
        title_label = ctk.CTkLabel(
            self.main_area,
            text="Welcome to the Admin Dashboard",
            font=("Arial", 28, "bold"),  # Reduced font size
            text_color="white",
            anchor="center",
        )
        title_label.place(x=600, y=30, anchor="center")  # Centered at the top of the main area

        # Fetch counts
        student_count, teacher_count, admin_count = self.get_counts()

        # Place the statistic cards statically and center them
        self.create_stat_card(self.main_area, "Total Students", student_count, 150, 150, "#00aaff")
        self.create_stat_card(self.main_area, "Total Teachers", teacher_count, 550, 150, "#00ff00")
        self.create_stat_card(self.main_area, "Total Admins", admin_count, 950, 150, "#ff4500")

        # Fetch and display announcements
        announcements = self.get_announcements()
        self.create_announcements_section(self.main_area, announcements, x=100, y=400)

    def manage_students(self):
        self.clear_main_area()
        ManageStudents(self.main_area)

    def manage_teachers(self):
        self.clear_main_area()
        ManageTeachers(self.main_area)

    def manage_subjects(self):
        self.clear_main_area()
        SubjectManager(self.main_area)

    def make_announcements(self):
        self.clear_main_area()
        MakeAnnouncements(self.main_area)

    def show_settings(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Settings (Coming Soon)", font=("Arial", 20), text_color="white").place(x=180, y=250)

    def logout(self):
        self.destroy()
        import os
        os.system("python main_login.py")  # Update this if your login file has a different name


# Run the Admin Panel only if this file is executed directly
if __name__ == "__main__":
    app = AdminPanel()
    app.mainloop()
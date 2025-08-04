import customtkinter as ctk

def create_teacher_sidebar(parent, on_dashboard, on_attendance, on_exams, on_grades, on_performance, on_meetings, on_announcements, on_timetable, on_settings, on_logout):
    """
    Create the sidebar for the teacher panel.

    Parameters:
    - parent: The parent tkinter widget where the sidebar will be placed.
    - on_dashboard, on_attendance, etc.: Callback functions for each navigation button.
    """
    sidebar_frame = ctk.CTkFrame(parent, width=200, corner_radius=0, fg_color="#2b2b2b")
    sidebar_frame.grid(row=0, column=0, sticky="ns")
    sidebar_frame.grid_rowconfigure(10, weight=1)  # Space at the bottom

    # Sidebar Header
    ctk.CTkLabel(
        sidebar_frame,
        text="EduTrack",
        font=("Arial", 20, "bold"),
        text_color="white"
    ).grid(row=0, column=0, padx=20, pady=20)

    # Sidebar Buttons
    buttons = [
        ("📊 Dashboard", on_dashboard),
        ("📅 Attendance", on_attendance),
        ("📝 Exams", on_exams),
        ("🎓 Grades", on_grades),
        ("📈 Performance", on_performance),
        ("📢 Meetings", on_meetings),
        ("📋 Announcements", on_announcements),
        ("📋 Timetable", on_timetable),
        ("⚙️ Settings", on_settings),  # Second last
        ("🚪 Logout", on_logout)  # Last
    ]

    for i, (text, command) in enumerate(buttons):
        fg_color = "#d9534f" if text == "🚪 Logout" else "#007acc"  # Red for Logout, Blue for others
        hover_color = "#b22222" if text == "🚪 Logout" else "#005f99"  # Darker hover colors
        text_color = "white"

        ctk.CTkButton(
            sidebar_frame,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            corner_radius=5,
            font=("Arial", 14)
        ).grid(row=i+1, column=0, padx=20, pady=10, sticky="ew")  # Padding for spacing

    return sidebar_frame
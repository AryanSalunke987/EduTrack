import customtkinter as ctk

def create_sidebar(parent, on_dashboard, on_attendance, on_exams, on_timetable, on_grades, on_meeting,on_settings, on_logout):
    sidebar_frame = ctk.CTkFrame(parent, width=200, corner_radius=0)
    sidebar_frame.grid(row=0, column=0, sticky="ns")
    sidebar_frame.grid_rowconfigure(10, weight=1)

    ctk.CTkLabel(sidebar_frame, text="EduTrack", font=("Arial", 20, "bold")).grid(row=0, column=0, padx=20, pady=20)

    # Sidebar buttons
    buttons = [
        ("📊 Dashboard", on_dashboard),
        ("📅 Attendance", on_attendance),
        ("📝 Exams", on_exams),
        ("📆 Timetable", on_timetable),
        ("🎓 Grades", on_grades),
        ("📢 Meetings", on_meeting),
        ("⚙️ Settings", on_settings),  # Second last
        ("🚪 Logout", on_logout)  # Last
    ]

    for i, (text, command) in enumerate(buttons):
        fg_color = "#d9534f" if text == "🚪 Logout" else None  # Red Logout Button
        text_color = "white" if text == "🚪 Logout" else None

        ctk.CTkButton(sidebar_frame, text=text, command=command, fg_color=fg_color, text_color=text_color).grid(
            row=i+1, column=0, padx=20, pady=10, sticky="ew"
        )

    return sidebar_frame

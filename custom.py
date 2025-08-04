import customtkinter as ctk
from PIL import Image, ImageTk
import os
from datetime import datetime
import calendar

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TeacherDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Teacher Dashboard")
        self.geometry("1200x700")
        self.minsize(900, 600)
        
        # Load icons (placeholder paths - you'll need to add your own icons)
        self.icon_path = "icons/"
        self.load_icons()
        
        # Create variables
        self.current_view = ctk.StringVar(value="home")
        self.username = ctk.StringVar(value="John Doe")
        self.notifications = [
            "Exam on Monday! Prepare well!",
            "Staff meeting tomorrow at 3 PM",
            "Grade submissions due by Friday"
        ]
        
        # Create layout
        self.create_layout()
        
        # Default view
        self.show_home_view()
    
    def load_icons(self):
        # Create a dictionary to store icons
        self.icons = {}
        
        # If icons directory doesn't exist, create empty icons
        if not os.path.exists(self.icon_path):
            os.makedirs(self.icon_path)
            
            # Create empty PhotoImage objects as placeholders
            for icon_name in ["home", "students", "attendance", "grades", "schedule", 
                            "report", "assignments", "lectures", "notification", "user"]:
                self.icons[icon_name] = None
        else:
            # Load icons from directory if they exist
            try:
                for icon_name in ["home", "students", "attendance", "grades", "schedule", 
                                "report", "assignments", "lectures", "notification", "user"]:
                    icon_file = os.path.join(self.icon_path, f"{icon_name}.png")
                    if os.path.exists(icon_file):
                        img = Image.open(icon_file).resize((24, 24))
                        self.icons[icon_name] = ImageTk.PhotoImage(img)
                    else:
                        self.icons[icon_name] = None
            except Exception as e:
                print(f"Error loading icons: {e}")
                # Create empty PhotoImage objects as placeholders
                for icon_name in ["home", "students", "attendance", "grades", "schedule", 
                                "report", "assignments", "lectures", "notification", "user"]:
                    self.icons[icon_name] = None
    
    def create_layout(self):
        # Create main grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)  # Push items to the top
        
        # Create sidebar header with menu button
        self.sidebar_header = ctk.CTkFrame(self.sidebar_frame, corner_radius=0, fg_color=("gray85", "gray25"))
        self.sidebar_header.pack(fill="x", padx=0, pady=0)
        
        self.menu_button = ctk.CTkButton(self.sidebar_header, text="≡", width=40, height=40, 
                                        corner_radius=0, fg_color="transparent", 
                                        hover_color=("gray75", "gray35"),
                                        command=self.toggle_sidebar)
        self.menu_button.pack(side="left", padx=10, pady=10)
        
        # Create sidebar buttons
        self.sidebar_buttons = []
        
        # Home button
        self.home_button = self.create_sidebar_button("Home", self.icons.get("home"), 
                                                    lambda: self.change_view("home"))
        
        # Students button
        self.students_button = self.create_sidebar_button("Students", self.icons.get("students"), 
                                                        lambda: self.change_view("students"))
        
        # Attendance button
        self.attendance_button = self.create_sidebar_button("Attendance", self.icons.get("attendance"), 
                                                        lambda: self.change_view("attendance"))
        
        # Grades button
        self.grades_button = self.create_sidebar_button("Grades", self.icons.get("grades"), 
                                                    lambda: self.change_view("grades"))
        
        # Schedule button
        self.schedule_button = self.create_sidebar_button("Schedule", self.icons.get("schedule"), 
                                                        lambda: self.change_view("schedule"))
        
        # Create main content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Create header in content frame
        self.content_header = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color=("gray85", "gray25"))
        self.content_header.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.content_header.grid_columnconfigure(0, weight=1)
        
        # Add title label to header
        self.title_label = ctk.CTkLabel(self.content_header, text="Dashboard", 
                                      font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Add user profile to header
        self.profile_frame = ctk.CTkFrame(self.content_header, corner_radius=10, fg_color="transparent")
        self.profile_frame.grid(row=0, column=1, padx=20, pady=10, sticky="e")
        
        self.profile_name = ctk.CTkLabel(self.profile_frame, text=self.username.get(), 
                                       font=ctk.CTkFont(size=14))
        self.profile_name.pack(side="left", padx=(0, 10))
        
        self.profile_icon = ctk.CTkButton(self.profile_frame, text="", image=self.icons.get("user"), 
                                        width=40, height=40, corner_radius=20,
                                        fg_color=("#3B8ED0", "#1F6AA5"), hover_color=("#36719F", "#144870"))
        self.profile_icon.pack(side="left")
        
        # Create main container for views
        self.main_container = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.main_container.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Initialize views dictionary to store different views
        self.views = {}
    
    def create_sidebar_button(self, text, icon, command):
        """Helper function to create sidebar buttons with consistent styling"""
        button = ctk.CTkButton(self.sidebar_frame, text=text, image=icon, 
                             corner_radius=0, height=50, border_spacing=10, 
                             fg_color="transparent", text_color=("gray10", "gray90"),
                             hover_color=("gray70", "gray30"), anchor="w", 
                             command=command)
        button.pack(fill="x", padx=0, pady=(5, 0))
        self.sidebar_buttons.append(button)
        return button
    
    def toggle_sidebar(self):
        """Toggle sidebar expanded/collapsed state"""
        # Implement sidebar collapse/expand functionality
        current_width = self.sidebar_frame.winfo_width()
        if current_width > 50:  # If sidebar is expanded
            # Collapse sidebar
            for button in self.sidebar_buttons:
                button.configure(text="")
        else:
            # Expand sidebar
            for i, button in enumerate(self.sidebar_buttons):
                texts = ["Home", "Students", "Attendance", "Grades", "Schedule"]
                if i < len(texts):
                    button.configure(text=texts[i])
    
    def change_view(self, view_name):
        """Change the current view in the main container"""
        self.current_view.set(view_name)
        self.title_label.configure(text=view_name.capitalize())
        
        # Call the appropriate view function
        if view_name == "home":
            self.show_home_view()
        elif view_name == "students":
            self.show_students_view()
        elif view_name == "attendance":
            self.show_attendance_view()
        elif view_name == "grades":
            self.show_grades_view()
        elif view_name == "schedule":
            self.show_schedule_view()
    
    def show_home_view(self):
        """Display the home dashboard view"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create home view content
        self.home_view = ctk.CTkFrame(self.main_container, corner_radius=0, fg_color="transparent")
        self.home_view.grid(row=0, column=0, sticky="nsew")
        self.home_view.grid_columnconfigure((0, 1, 2), weight=1)
        self.home_view.grid_rowconfigure(0, weight=1)
        self.home_view.grid_rowconfigure(1, weight=1)
        
        # Action cards row
        # Card 1: Generate Report
        self.report_card = self.create_action_card(
            self.home_view, "Generate Report", 
            "Click to generate reports for classes, students, or grades",
            self.icons.get("report")
        )
        self.report_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Card 2: Assignments
        self.assignments_card = self.create_action_card(
            self.home_view, "Assignments", 
            "Create and manage assignments for your classes",
            self.icons.get("assignments")
        )
        self.assignments_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Card 3: Lectures
        self.lectures_card = self.create_action_card(
            self.home_view, "Lectures", 
            "Schedule and organize your upcoming lectures",
            self.icons.get("lectures")
        )
        self.lectures_card.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        # Notifications section
        self.notifications_frame = ctk.CTkFrame(self.home_view, corner_radius=10)
        self.notifications_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.notifications_frame.grid_columnconfigure(0, weight=1)
        
        # Notifications header
        self.notif_header = ctk.CTkFrame(self.notifications_frame, corner_radius=0, height=40, 
                                        fg_color=("#3B8ED0", "#1F6AA5"))
        self.notif_header.grid(row=0, column=0, sticky="ew")
        self.notif_header.grid_propagate(False)
        
        self.notif_label = ctk.CTkLabel(self.notif_header, text="Notifications", 
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       image=self.icons.get("notification"),
                                       compound="left")
        self.notif_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        
        # Add notifications
        for i, notification in enumerate(self.notifications):
            notif_item = ctk.CTkFrame(self.notifications_frame, corner_radius=5, fg_color="transparent")
            notif_item.grid(row=i+1, column=0, padx=10, pady=(5, 0), sticky="ew")
            
            notif_text = ctk.CTkLabel(notif_item, text=notification, anchor="w")
            notif_text.grid(row=0, column=0, padx=20, pady=10, sticky="w")
            
            # Add separator except for the last item
            if i < len(self.notifications) - 1:
                separator = ctk.CTkFrame(self.notifications_frame, height=1, fg_color=("gray85", "gray30"))
                separator.grid(row=i+2, column=0, padx=20, pady=0, sticky="ew")
    
    def create_action_card(self, parent, title, description, icon):
        """Create an action card for the dashboard"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid_columnconfigure(0, weight=1)
        
        # Card header
        header = ctk.CTkFrame(card, corner_radius=0, height=40, fg_color=("#3B8ED0", "#1F6AA5"))
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        header_label = ctk.CTkLabel(header, text=title, font=ctk.CTkFont(size=16, weight="bold"),
                                  image=icon, compound="left")
        header_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        
        # Card content
        content = ctk.CTkLabel(card, text=description, anchor="w", height=80, wraplength=200)
        content.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Action button
        action_button = ctk.CTkButton(card, text=f"{title}", corner_radius=5)
        action_button.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        return card
    
    def show_students_view(self):
        """Display the students view"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create students view content
        students_view = ctk.CTkFrame(self.main_container, corner_radius=0, fg_color="transparent")
        students_view.grid(row=0, column=0, sticky="nsew")
        students_view.grid_columnconfigure(0, weight=1)
        students_view.grid_rowconfigure(1, weight=1)
        
        # Search and filter section
        search_frame = ctk.CTkFrame(students_view, corner_radius=10)
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        search_label = ctk.CTkLabel(search_frame, text="Students", font=ctk.CTkFont(size=16, weight="bold"))
        search_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        
        search_input = ctk.CTkEntry(search_frame, placeholder_text="Search students...")
        search_input.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        filter_button = ctk.CTkButton(search_frame, text="Filter", width=100)
        filter_button.grid(row=1, column=1, padx=(0, 20), pady=10)
        
        add_button = ctk.CTkButton(search_frame, text="Add Student", width=120)
        add_button.grid(row=1, column=2, padx=(0, 20), pady=10)
        
        # Students list section
        students_list = ctk.CTkFrame(students_view, corner_radius=10)
        students_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        students_list.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Sample student data
        sample_students = [
            {"id": "ST001", "name": "Emma Johnson", "class": "10A", "email": "emma.j@school.edu"},
            {"id": "ST002", "name": "Liam Smith", "class": "10A", "email": "liam.s@school.edu"},
            {"id": "ST003", "name": "Olivia Brown", "class": "10B", "email": "olivia.b@school.edu"},
            {"id": "ST004", "name": "Noah Davis", "class": "10B", "email": "noah.d@school.edu"},
            {"id": "ST005", "name": "Ava Wilson", "class": "10C", "email": "ava.w@school.edu"},
        ]
        
        # Table header
        header_frame = ctk.CTkFrame(students_list, corner_radius=0, height=40, 
                                  fg_color=("#3B8ED0", "#1F6AA5"))
        header_frame.grid(row=0, column=0, columnspan=5, sticky="ew")
        header_frame.grid_propagate(False)
        
        headers = ["ID", "Name", "Class", "Email", "Actions"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(header_frame, text=header, 
                                     font=ctk.CTkFont(weight="bold"))
            header_label.grid(row=0, column=i, padx=20, pady=10, sticky="ew")
        
        # Student rows
        for i, student in enumerate(sample_students):
            row_bg = "transparent" if i % 2 == 0 else ("gray90", "gray20")
            row = ctk.CTkFrame(students_list, corner_radius=0, fg_color=row_bg)
            row.grid(row=i+1, column=0, columnspan=5, sticky="ew")
            
            id_label = ctk.CTkLabel(row, text=student["id"])
            id_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
            
            name_label = ctk.CTkLabel(row, text=student["name"])
            name_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")
            
            class_label = ctk.CTkLabel(row, text=student["class"])
            class_label.grid(row=0, column=2, padx=20, pady=10, sticky="w")
            
            email_label = ctk.CTkLabel(row, text=student["email"])
            email_label.grid(row=0, column=3, padx=20, pady=10, sticky="w")
            
            action_frame = ctk.CTkFrame(row, fg_color="transparent")
            action_frame.grid(row=0, column=4, padx=20, pady=5, sticky="e")
            
            edit_btn = ctk.CTkButton(action_frame, text="Edit", width=60, height=30)
            edit_btn.grid(row=0, column=0, padx=(0, 5))
            
            view_btn = ctk.CTkButton(action_frame, text="View", width=60, height=30)
            view_btn.grid(row=0, column=1, padx=5)
        
        # Pagination
        pagination = ctk.CTkFrame(students_view, corner_radius=10, fg_color="transparent")
        pagination.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        prev_btn = ctk.CTkButton(pagination, text="< Prev", width=80, fg_color="transparent",
                               border_width=1, text_color=("gray10", "gray90"))
        prev_btn.grid(row=0, column=0, padx=5, pady=10)
        
        page_label = ctk.CTkLabel(pagination, text="Page 1 of 3")
        page_label.grid(row=0, column=1, padx=10, pady=10)
        
        next_btn = ctk.CTkButton(pagination, text="Next >", width=80, fg_color="transparent",
                               border_width=1, text_color=("gray10", "gray90"))
        next_btn.grid(row=0, column=2, padx=5, pady=10)
    
    def show_attendance_view(self):
        """Display the attendance view"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create attendance view
        attendance_view = ctk.CTkFrame(self.main_container, corner_radius=0, fg_color="transparent")
        attendance_view.grid(row=0, column=0, sticky="nsew")
        attendance_view.grid_columnconfigure(0, weight=1)
        attendance_view.grid_rowconfigure(1, weight=1)
        
        # Header section with class selection and date picker
        header_frame = ctk.CTkFrame(attendance_view, corner_radius=10)
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        class_label = ctk.CTkLabel(header_frame, text="Class:")
        class_label.grid(row=0, column=0, padx=(20, 5), pady=10, sticky="w")
        
        class_options = ["10A", "10B", "10C", "11A", "11B", "12A"]
        class_selector = ctk.CTkOptionMenu(header_frame, values=class_options)
        class_selector.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        
        date_label = ctk.CTkLabel(header_frame, text="Date:")
        date_label.grid(row=0, column=2, padx=(20, 5), pady=10, sticky="w")
        
        # Use today's date as default
        today = datetime.now().strftime("%Y-%m-%d")
        date_entry = ctk.CTkEntry(header_frame, width=120)
        date_entry.insert(0, today)
        date_entry.grid(row=0, column=3, padx=5, pady=10, sticky="w")
        
        load_btn = ctk.CTkButton(header_frame, text="Load", width=80)
        load_btn.grid(row=0, column=4, padx=20, pady=10)
        
        # Attendance list
        attendance_frame = ctk.CTkFrame(attendance_view, corner_radius=10)
        attendance_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        attendance_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Table header
        header_row = ctk.CTkFrame(attendance_frame, corner_radius=0, height=40, 
                                fg_color=("#3B8ED0", "#1F6AA5"))
        header_row.grid(row=0, column=0, columnspan=4, sticky="ew")
        header_row.grid_propagate(False)
        
        id_header = ctk.CTkLabel(header_row, text="ID", font=ctk.CTkFont(weight="bold"))
        id_header.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        name_header = ctk.CTkLabel(header_row, text="Name", font=ctk.CTkFont(weight="bold"))
        name_header.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        
        status_header = ctk.CTkLabel(header_row, text="Status", font=ctk.CTkFont(weight="bold"))
        status_header.grid(row=0, column=2, padx=20, pady=10, sticky="w")
        
        note_header = ctk.CTkLabel(header_row, text="Notes", font=ctk.CTkFont(weight="bold"))
        note_header.grid(row=0, column=3, padx=20, pady=10, sticky="w")
        
        # Sample student data
        sample_students = [
            {"id": "ST001", "name": "Emma Johnson"},
            {"id": "ST002", "name": "Liam Smith"},
            {"id": "ST003", "name": "Olivia Brown"},
            {"id": "ST004", "name": "Noah Davis"},
            {"id": "ST005", "name": "Ava Wilson"},
        ]
        
        # Create attendance rows
        for i, student in enumerate(sample_students):
            row_bg = "transparent" if i % 2 == 0 else ("gray90", "gray20")
            row = ctk.CTkFrame(attendance_frame, corner_radius=0, fg_color=row_bg)
            row.grid(row=i+1, column=0, columnspan=4, sticky="ew")
            
            id_label = ctk.CTkLabel(row, text=student["id"])
            id_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
            
            name_label = ctk.CTkLabel(row, text=student["name"])
            name_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")
            
            status_frame = ctk.CTkFrame(row, fg_color="transparent")
            status_frame.grid(row=0, column=2, padx=20, pady=10, sticky="w")
            
            present_var = ctk.StringVar(value="present")
            present_rb = ctk.CTkRadioButton(status_frame, text="Present", variable=present_var, value="present")
            present_rb.grid(row=0, column=0, padx=(0, 10))
            
            absent_rb = ctk.CTkRadioButton(status_frame, text="Absent", variable=present_var, value="absent")
            absent_rb.grid(row=0, column=1, padx=10)
            
            late_rb = ctk.CTkRadioButton(status_frame, text="Late", variable=present_var, value="late")
            late_rb.grid(row=0, column=2, padx=10)
            
            note_entry = ctk.CTkEntry(row, placeholder_text="Add notes here...", width=200)
            note_entry.grid(row=0, column=3, padx=20, pady=10, sticky="ew")
        
        # Footer with save button
        footer_frame = ctk.CTkFrame(attendance_view, corner_radius=10, fg_color="transparent")
        footer_frame.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        save_btn = ctk.CTkButton(footer_frame, text="Save Attendance")
        save_btn.grid(row=0, column=0, padx=5, pady=10)
    
    def show_grades_view(self):
        """Display the grades view"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create grades view
        grades_view = ctk.CTkFrame(self.main_container, corner_radius=0, fg_color="transparent")
        grades_view.grid(row=0, column=0, sticky="nsew")
        grades_view.grid_columnconfigure(0, weight=1)
        grades_view.grid_rowconfigure(1, weight=1)
        
        # Header with filters
        filter_frame = ctk.CTkFrame(grades_view, corner_radius=10)
        filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        class_label = ctk.CTkLabel(filter_frame, text="Class:")
        class_label.grid(row=0, column=0, padx=(20, 5), pady=10, sticky="w")
        
        class_options = ["10A", "10B", "10C", "11A", "11B", "12A"]
        class_selector = ctk.CTkOptionMenu(filter_frame, values=class_options)
        class_selector.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        
        assessment_label = ctk.CTkLabel(filter_frame, text="Assessment:")
        assessment_label.grid(row=0, column=2, padx=(20, 5), pady=10, sticky="w")
        
        assessment_options = ["Quiz 1", "Mid-term Exam", "Project", "Final Exam"]
        assessment_selector = ctk.CTkOptionMenu(filter_frame, values=assessment_options)
        assessment_selector.grid(row=0, column=3, padx=5, pady=10, sticky="w")
        
        load_btn = ctk.CTkButton(filter_frame, text="Load", width=80)
        load_btn.grid(row=0, column=4, padx=10, pady=10)
        
        add_assessment_btn = ctk.CTkButton(filter_frame, text="+ New Assessment")
        add_assessment_btn.grid(row=0, column=5, padx=10, pady=10)
        
        # Grades table
        grades_frame = ctk.CTkFrame(grades_view, corner_radius=10)
        grades_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        grades_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Table header
        header_row = ctk.CTkFrame(grades_frame, corner_radius=0, height=40, 
                                fg_color=("#3B8ED0", "#1F6AA5"))
        header_row.grid(row=0, column=0, columnspan=5, sticky="ew")
        header_row.grid_propagate(False)
        
        id_header = ctk.CTkLabel(header_row, text="ID", font=ctk.CTkFont(weight="bold"))
        id_header.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        name_header = ctk.CTkLabel(header_row, text="Name", font=ctk.CTkFont(weight="bold"))
        name_header.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        
        grade_header = ctk.CTkLabel(header_row, text="Grade", font=ctk.CTkFont(weight="bold"))
        grade_header.grid(row=0, column=2, padx=20, pady=10, sticky="w")

app = TeacherDashboard()
app.mainloop()
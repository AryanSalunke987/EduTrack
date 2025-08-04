import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from admin.admin_panel import AdminPanel
from teacher.teacher_panel import TeacherPanelApp

def verify_login(username, password, user_type):
    # Connect to SQLite database
    conn = sqlite3.connect('edutrack.db')
    cursor = conn.cursor()
    
    # Query to check if the user exists and the password matches
    cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, user_type))
    result = cursor.fetchone()
    
    # Close the database connection
    conn.close()
    
    
    return result

def login():
    username = entry_username.get()
    password = entry_password.get()
    user_type = user_type_var.get()
    
    user_data = verify_login(username, password, user_type)
    if user_data:
        messagebox.showinfo("Login Success", f"Logged in as {user_type}")
        
        if user_type == "Student":
            start_main_app(user_data)
        elif user_type == "Teacher":
            start_teacher_app(user_data)
        elif user_type == "Admin":
            root.destroy()
            app = AdminPanel()
            app.mainloop()
    else:
        messagebox.showerror("Login Failed", f"Invalid {user_type} Credentials")

def start_teacher_app(user_data):
    root.destroy()
    app = TeacherPanelApp(user_data)
    app.mainloop()

def start_main_app(user_data):
    root.destroy()
    from main import EduTrackApp  
    app = EduTrackApp(user_data)
    app.mainloop()

root = ctk.CTk()
root.title("EduTrack Login")
root.geometry("400x300")

ctk.CTkLabel(root, text="Username:").pack(pady=5)
entry_username = ctk.CTkEntry(root)
entry_username.pack(pady=5)

ctk.CTkLabel(root, text="Password:").pack(pady=5)
entry_password = ctk.CTkEntry(root, show="*")
entry_password.pack(pady=5)

user_type_var = ctk.StringVar(value="Student")
ctk.CTkLabel(root, text="Login as:").pack(pady=5)
user_type_menu = ctk.CTkOptionMenu(root, variable=user_type_var, values=["Student", "Teacher","Admin"])
user_type_menu.pack(pady=5)

login_button = ctk.CTkButton(root, text="Login", command=login)
login_button.pack(pady=20)

root.mainloop()
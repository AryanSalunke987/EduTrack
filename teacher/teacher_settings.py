import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import re  # For password validation


def validate_password(password):
    """Validate password based on the given criteria."""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one numeric digit."
    if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for char in password):
        return "Password must contain at least one special character."
    return None


def change_password(user_id, current_password, new_password, confirm_password):
    """Handle password change functionality."""
    try:
        conn = sqlite3.connect("edutrack.db")
        cursor = conn.cursor()

        # Verify current password
        cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if not result or result[0] != current_password:
            return "Current password is incorrect."

        # Validate new password
        validation_error = validate_password(new_password)
        if validation_error:
            return validation_error

        # Check if new password matches confirm password
        if new_password != confirm_password:
            return "New password and confirm password do not match."

        # Update password in the database
        cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", (new_password, user_id))
        conn.commit()

        return "Password changed successfully."

    except sqlite3.Error as e:
        return f"Database error: {e}"

    finally:
        if conn:
            conn.close()


def create_teacher_settings(parent, teacher_id):
    """Function to display the Settings page for teachers."""
    try:
        # Database connection
        conn = sqlite3.connect("edutrack.db")
        cursor = conn.cursor()

        # Fetch user details
        cursor.execute("SELECT username, user_id FROM users WHERE teacher_id = ?", (teacher_id,))
        user_details = cursor.fetchone()

        if not user_details:
            messagebox.showerror("Error", "User details not found.")
            return

        username, user_id = user_details

        # Fetch Teacher Details
        cursor.execute("SELECT name, department FROM teachers WHERE teacher_id = ?", (teacher_id,))
        teacher_details = cursor.fetchone()

        if not teacher_details:
            messagebox.showerror("Error", "Teacher details not found.")
            return

        teacher_name, department = teacher_details

        cursor.execute("SELECT DISTINCT subject_name FROM subjects WHERE teacher_id = ?", (teacher_id,))
        subjects = cursor.fetchall()
        subject_list= ", ".join([subject[0] for subject in subjects]) if subjects else "No courses assigned"

        # Clear previous widgets
        for widget in parent.winfo_children():
            widget.destroy()

        # Create Header for Settings
        title_label = ctk.CTkLabel(parent, text="Teacher Settings", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        # Create a frame for teacher details with padding and border
        details_frame = ctk.CTkFrame(parent, fg_color="gray20", corner_radius=10)
        details_frame.pack(pady=20, padx=20, fill="both", expand=False)

        # Display Teacher Details
        teacher_info = (
            f"Name: {teacher_name}\n"
            f"Department: {department}\n"
            f"Subject: {subject_list}\n"
            f"Username: {username}"
        )
        teacher_label = ctk.CTkLabel(details_frame, text=teacher_info, font=("Calibri", 20), justify="left")
        teacher_label.pack(pady=10)

        # Create Change Password Section
        password_frame = ctk.CTkFrame(parent, fg_color="gray20", corner_radius=10)
        password_frame.pack(pady=20, padx=20, fill="both", expand=False)

        change_password_label = ctk.CTkLabel(password_frame, text="Change Password", font=("Calibri", 20, "bold"))
        change_password_label.pack(pady=10)

        current_password_entry = ctk.CTkEntry(password_frame, placeholder_text="Current Password", show="*")
        current_password_entry.pack(pady=5)

        new_password_entry = ctk.CTkEntry(password_frame, placeholder_text="New Password", show="*")
        new_password_entry.pack(pady=5)

        confirm_password_entry = ctk.CTkEntry(password_frame, placeholder_text="Confirm New Password", show="*")
        confirm_password_entry.pack(pady=5)

        def handle_change_password():
            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            result = change_password(user_id, current_password, new_password, confirm_password)
            messagebox.showinfo("Change Password", result)

        change_password_button = ctk.CTkButton(password_frame, text="Change Password", command=handle_change_password)
        change_password_button.pack(pady=10)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


# Execution Entry Point
if __name__ == "__main__":
    import tkinter as tk

    root = ctk.CTk()
    root.geometry("700x600")
    root.title("Teacher Settings")

    teacher_id = 4  # Replace with the logged-in teacher's ID
    app = ctk.CTkFrame(master=root, width=700, height=600)
    app.pack(fill="both", expand=True)

    create_teacher_settings(app, teacher_id)

    root.mainloop()
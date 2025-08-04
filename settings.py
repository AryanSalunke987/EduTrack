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


def create_settings(parent, user_data):
    try:
        # Database connection
        conn = sqlite3.connect("edutrack.db")
        cursor = conn.cursor()

        # Fetch user details
        user_id = user_data[0]  # Get user_id from user_data
        cursor.execute("SELECT username, role, student_id FROM users WHERE user_id = ?", (user_id,))
        user_details = cursor.fetchone()

        if not user_details:
            messagebox.showerror("Error", "User details not found.")
            return

        username, role, student_id = user_details

        # Create Header for Settings
        title_label = ctk.CTkLabel(parent, text="Settings", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        # Create a frame for user and student details with padding and border
        details_frame = ctk.CTkFrame(parent, fg_color="gray20", corner_radius=10)
        details_frame.pack(pady=20, padx=20, fill="both", expand=False)

        # Display User Details
        user_info = f"Username: {username}\nRole: {role}"
        user_label = ctk.CTkLabel(details_frame, text=user_info, font=("Arial", 20))
        user_label.pack(pady=10)

        if role == "Student" and student_id:
            # Fetch Student Details
            cursor.execute("SELECT name, roll_number, email, phone, course, semester FROM students WHERE student_id = ?", (student_id,))
            student_details = cursor.fetchone()

            if student_details:
                student_info = (
                    f"Name: {student_details[0]}\n"
                    f"Roll Number: {student_details[1]}\n"
                    f"Email: {student_details[2]}\n"
                    f"Phone: {student_details[3]}\n"
                    f"Course: {student_details[4]}\n"
                    f"Semester: {student_details[5]}"
                )
                student_label = ctk.CTkLabel(details_frame, text=student_info, font=("Calibri", 20))
                student_label.pack(pady=10)
            else:
                student_label = ctk.CTkLabel(details_frame, text="No student details found.", font=("Calibri", 24))
                student_label.pack(pady=10)

        # Create Change Password Section
        password_frame = ctk.CTkFrame(parent, fg_color="gray20", corner_radius=10)
        password_frame.pack(pady=20, padx=20, fill="both", expand=False)

        change_password_label = ctk.CTkLabel(password_frame, text="Change Password", font=("Arial", 20, "bold"))
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
import customtkinter as ctk
import sqlite3

def show_attendance(parent, user_data):
    # Fetch attendance details from the database
    conn = sqlite3.connect('edutrack.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT subjects.subject_id, subjects.subject_name, attendance.status, COUNT(attendance.status) as count
        FROM attendance
        JOIN subjects ON attendance.subject_id = subjects.subject_id
        WHERE attendance.student_id = ? AND (attendance.status = 'Present' OR attendance.status = 'Absent')
        GROUP BY subjects.subject_id, subjects.subject_name, attendance.status
    """, (user_data[4],))
    
    records = cursor.fetchall()
    conn.close()

    # Process the fetched data into a dictionary
    attendance_data = {}
    for record in records:
        subject_id, subject_name, status, count = record
        if subject_id not in attendance_data:
            attendance_data[subject_id] = {"subject_name": subject_name, "present": 0, "total": 0}
        if status == 'Present':
            attendance_data[subject_id]["present"] = count
        attendance_data[subject_id]["total"] += count
    
    # Calculate overall attendance
    total_present = sum([data["present"] for data in attendance_data.values()])
    total_classes = sum([data["total"] for data in attendance_data.values()])
    overall_percentage = (total_present / total_classes) * 100 if total_classes > 0 else 0

    # Clear previous widgets
    for widget in parent.winfo_children():
        widget.destroy()

    # Header label
    ctk.CTkLabel(parent, text="📊 Attendance Dashboard", font=("Arial", 24, "bold"), text_color="#00A2FF").pack(pady=20)

    # Display overall attendance
    overall_frame = ctk.CTkFrame(parent, fg_color="#1E1E2E", corner_radius=10)
    overall_frame.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(overall_frame, text="Overall Attendance", font=("Arial", 20, "bold"), text_color="#FFFFFF").pack(pady=10)
    ctk.CTkLabel(overall_frame, text=f"{overall_percentage:.2f}%", font=("Arial", 26, "bold"), text_color="#00FF00" if overall_percentage >= 75 else "#FF0000").pack()
    ctk.CTkLabel(overall_frame, text=f"Classes Attended: {total_present}/{total_classes}", font=("Arial", 16), text_color="#FFFFFF").pack()

    # Scrollable frame for subjects
    scroll_frame = ctk.CTkScrollableFrame(parent, width=500, height=400, fg_color="#121212", border_width=0, corner_radius=10)
    scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Create subject-wise attendance UI
    for subject_id, data in attendance_data.items():
        subject_frame = ctk.CTkFrame(scroll_frame, fg_color="#2A2A3B", corner_radius=10)
        subject_frame.pack(pady=10, padx=10, fill="x")

        subject_percentage = (data["present"] / data["total"]) * 100 if data["total"] > 0 else 0

        ctk.CTkLabel(subject_frame, text=data["subject_name"], font=("Arial", 18, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(subject_frame, text=f"Attendance: {data['present']}/{data['total']}", font=("Arial", 14), text_color="#AAB6FE").pack(anchor="w", padx=20)

        # Color-coded Progress Bar
        progress_bar = ctk.CTkProgressBar(subject_frame, width=400, height=10, progress_color="#00FF00" if subject_percentage >= 75 else "#FF0000")
        progress_bar.set(subject_percentage / 100)
        progress_bar.pack(pady=10, padx=20)

        ctk.CTkLabel(subject_frame, text=f"Attendance Rate: {subject_percentage:.0f}%", font=("Arial", 14), text_color="#FFFFFF").pack(anchor="w", padx=20)

        # Motivational message
        message = "✅ Great job! Keep up the good work!" if subject_percentage >= 75 else "⚠️ Attendance needs improvement. Please stay consistent."
        ctk.CTkLabel(subject_frame, text=message, font=("Arial", 12, "italic"), text_color="#AAB6FE").pack(pady=10)

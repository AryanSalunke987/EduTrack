import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from teacher.db_manager import DatabaseManager

class TeacherPerformance:
    def __init__(self, parent_frame, teacher_id):
        """Initialize the TeacherPerformance class with the parent frame and teacher ID."""
        self.parent_frame = parent_frame
        self.teacher_id = teacher_id
        self.frame = None
        self.db = DatabaseManager()
        self.selected_exam_id = None
        self.selected_student_id = None
        self.selected_subject_id = None
        
    def show(self):
        """Create and display the performance graphs frame."""
        # Create a new frame each time show is called
        self.frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.frame.pack(fill="both", expand=True)
        self.setup_performance_graphs()
        
    def hide(self):
        """Hide the performance graphs frame."""
        if self.frame:
            self.frame.pack_forget()
            
    def setup_performance_graphs(self):
        """Set up the main performance graphs interface."""
        # Simple header
        header_label = ctk.CTkLabel(self.frame, text="Performance Analysis", font=("Arial", 18))
        header_label.pack(anchor="w", pady=5)
        
        # Create a simple tabview
        self.tabview = ctk.CTkTabview(self.frame)
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add tabs
        self.tabview.add("Class Report")
        self.tabview.add("Individual Report")
        
        # Setup tabs
        self.setup_class_report_tab()
        self.setup_individual_report_tab()
        
    def setup_class_report_tab(self):
        """Set up the class report tab with filters and graph area."""
        tab = self.tabview.tab("Class Report")
        
        # Create a scrollable frame for the tab
        scrollable_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True)
        
        # Create filter frame
        filter_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        filter_frame.pack(fill="x", pady=10)
        
        # Subject selection
        ctk.CTkLabel(filter_frame, text="Subject:").pack(side="left", padx=5)
        self.subjects = self.get_teacher_subjects()
        self.subject_combo = ctk.CTkComboBox(filter_frame, values=self.subjects, width=200, 
                                           command=self.load_exams_for_subject)
        self.subject_combo.pack(side="left", padx=5)
        
        # Exam selection
        ctk.CTkLabel(filter_frame, text="Exam:").pack(side="left", padx=5)
        self.exam_combo = ctk.CTkComboBox(filter_frame, values=["Select subject first"], width=250)
        self.exam_combo.pack(side="left", padx=5)
        
        # Generate button
        generate_btn = ctk.CTkButton(filter_frame, text="Generate Report", 
                                  command=self.generate_class_report, width=150)
        generate_btn.pack(side="left", padx=20)
        
        # Create frame for the matplotlib figure
        self.class_report_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        self.class_report_frame.pack(fill="both", expand=True, pady=10)
        
        # Stats frame
        self.stats_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=10)
        
    def setup_individual_report_tab(self):
        """Set up the individual report tab with student selection and graph area."""
        tab = self.tabview.tab("Individual Report")
        
        # Create a scrollable frame for the tab
        scrollable_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True)
        
        # Create filter frame
        filter_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        filter_frame.pack(fill="x", pady=10)
        
        # Student selection
        ctk.CTkLabel(filter_frame, text="Student:").pack(side="left", padx=5)
        students = self.get_all_students()
        self.student_combo = ctk.CTkComboBox(filter_frame, values=students, width=300)
        self.student_combo.pack(side="left", padx=5)
        
        # Generate button
        generate_btn = ctk.CTkButton(filter_frame, text="Generate Report", 
                                  command=self.generate_individual_report, width=150)
        generate_btn.pack(side="left", padx=20)
        
        # Create frame for the matplotlib figure
        self.individual_report_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        self.individual_report_frame.pack(fill="both", expand=True, pady=10)
        
    def get_teacher_subjects(self):
        """Get subjects taught by this teacher."""
        try:
            query = """
                SELECT subject_id, subject_name
                FROM subjects
                WHERE teacher_id = ?
                ORDER BY subject_name
            """
            self.db.cursor.execute(query, (self.teacher_id,))
            subjects = self.db.cursor.fetchall()
            
            if not subjects:
                return ["No subjects found"]
                
            # Store subject IDs for later use
            self.subject_ids = {f"{subject[1]}": subject[0] for subject in subjects}
            return [subject[1] for subject in subjects]
        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return ["Error loading subjects"]
    
    def load_exams_for_subject(self, subject_name):
        """Load exams for the selected subject."""
        if subject_name == "No subjects found" or not subject_name:
            self.exam_combo.configure(values=["No exams found"])
            return
            
        try:
            subject_id = self.subject_ids.get(subject_name)
            if not subject_id:
                self.exam_combo.configure(values=["Invalid subject"])
                return
                
            # Store the selected subject ID
            self.selected_subject_id = subject_id
                
            # Get exams for this subject
            query = """
                SELECT exam_id, exam_type, date
                FROM exams
                WHERE subject_id = ?
                ORDER BY date DESC
            """
            self.db.cursor.execute(query, (subject_id,))
            exams = self.db.cursor.fetchall()
            
            if not exams:
                self.exam_combo.configure(values=["No exams found for this subject"])
                return
                
            # Create a mapping of exam display text to exam ID
            self.exam_ids = {f"{exam[1]} on {exam[2]}": exam[0] for exam in exams}
            
            # Update the exam combo box
            exam_values = [f"{exam[1]} on {exam[2]}" for exam in exams]
            self.exam_combo.configure(values=exam_values)
            self.exam_combo.set(exam_values[0])  # Select the first exam by default
            
        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            self.exam_combo.configure(values=["Error loading exams"])
    
    def get_all_students(self):
        """Get all students for individual reports."""
        try:
            query = """
                SELECT student_id, name, roll_number, course
                FROM students
                ORDER BY name
            """
            self.db.cursor.execute(query)
            students = self.db.cursor.fetchall()
            
            if not students:
                return ["No students found"]
                
            # Store student IDs for later use
            self.student_ids = {f"{student[1]} (Roll: {student[2]}, Course: {student[3]})": student[0] 
                               for student in students}
            
            return [f"{student[1]} (Roll: {student[2]}, Course: {student[3]})" for student in students]
        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return ["Error loading students"]
    
    def generate_class_report(self):
        """Generate and display class performance report."""
        exam_text = self.exam_combo.get()
        if "No exams found" in exam_text or not exam_text:
            self.show_message("No exam selected", "error")
            return
            
        # Get exam ID from selection
        exam_id = self.exam_ids.get(exam_text)
        if not exam_id:
            self.show_message("Invalid exam selection", "error")
            return
            
        # Store the selected exam ID
        self.selected_exam_id = exam_id
            
        try:
            # Get exam grades
            query = """
                SELECT s.name, g.marks_obtained, g.total_marks
                FROM grades g
                JOIN students s ON g.student_id = s.student_id
                WHERE g.exam_id = ?
                ORDER BY g.marks_obtained DESC
            """
            self.db.cursor.execute(query, (exam_id,))
            grades = self.db.cursor.fetchall()
            
            if not grades:
                self.show_message("No grades found for this exam", "error")
                return
                
            # Process the data
            names = [grade[0] for grade in grades]
            marks = [grade[1] for grade in grades]
            total_marks = grades[0][2]  # Assuming total marks is the same for all students
            
            # Calculate percentages
            percentages = [(mark / total_marks) * 100 for mark in marks]
            
            # Clear previous plots
            for widget in self.class_report_frame.winfo_children():
                widget.destroy()
                
            # Clear previous stats
            for widget in self.stats_frame.winfo_children():
                widget.destroy()
                
            # Create figure with 2 subplots (removed pie charts)
            fig = plt.figure(figsize=(10, 6), dpi=100)  # Reduced height to fit better
            
            # First subplot - Bar chart of marks (enlarged to take full width)
            ax1 = fig.add_subplot(2, 1, 1)
            bars = ax1.bar(names, marks, color='skyblue')
            ax1.set_title('Student Marks')
            ax1.set_xlabel('Students')
            ax1.set_ylabel('Marks')
            ax1.axhline(y=total_marks * 0.4, color='r', linestyle='--', label='Pass Threshold (40%)')
            ax1.set_xticklabels(names, rotation=90, ha='center', fontsize=8)  # Adjusted for more students
            ax1.tick_params(axis='x', which='major', pad=5)
            ax1.legend()
            
            # Second subplot - Distribution of marks (enlarged to take full width)
            ax2 = fig.add_subplot(2, 1, 2)
            ax2.hist(percentages, bins=10, color='lightgreen', edgecolor='black')
            ax2.set_title('Distribution of Marks (%)')
            ax2.set_xlabel('Percentage')
            ax2.set_ylabel('Number of Students')
            
            # Adjust layout
            plt.tight_layout()
            
            # Create canvas and add to frame
            canvas = FigureCanvasTkAgg(fig, master=self.class_report_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Calculate statistics
            avg_percentage = sum(percentages) / len(percentages)
            highest_percentage = max(percentages)
            lowest_percentage = min(percentages)
            pass_count = sum(1 for p in percentages if p >= 40)
            pass_percentage = (pass_count / len(percentages)) * 100
            
            # Display statistics
            stats_header = ctk.CTkLabel(self.stats_frame, 
                                      text="Class Statistics", 
                                      font=("Arial", 14, "bold"))
            stats_header.pack(anchor="w", padx=10, pady=5)
            
            stats_text = (
                f"Total Students: {len(percentages)}  |  "
                f"Average Mark: {avg_percentage:.2f}%  |  "
                f"Highest Mark: {highest_percentage:.2f}%  |  "
                f"Lowest Mark: {lowest_percentage:.2f}%  |  "
                f"Pass Rate: {pass_percentage:.2f}%"
            )
            
            stats_label = ctk.CTkLabel(self.stats_frame, text=stats_text, 
                                     font=("Arial", 12))
            stats_label.pack(anchor="w", padx=10, pady=5)
            
            # Add performance comments
            comment = "Performance Analysis: "
            if avg_percentage >= 75:
                comment += "Excellent class performance. Most students are performing well above expectations."
            elif avg_percentage >= 60:
                comment += "Good class performance. Most students are performing at or above expectations."
            elif avg_percentage >= 40:
                comment += "Average class performance. Many students are just meeting minimum requirements."
            else:
                comment += "Below average class performance. Intervention may be needed to improve results."
                
            comment_label = ctk.CTkLabel(self.stats_frame, text=comment, 
                                       font=("Arial", 12), 
                                       wraplength=700)
            comment_label.pack(anchor="w", padx=10, pady=5)
            
        except sqlite3.Error as e:
            self.show_message(f"Database error: {str(e)}", "error")
        except Exception as e:
            self.show_message(f"Error generating report: {str(e)}", "error")
            
    def generate_individual_report(self):
        """Generate and display individual student report."""
        student_text = self.student_combo.get()
        if "No students found" in student_text or not student_text:
            self.show_message("No student selected", "error")
            return
            
        # Get student ID from selection
        student_id = self.student_ids.get(student_text)
        if not student_id:
            self.show_message("Invalid student selection", "error")
            return
            
        # Store the selected student ID
        self.selected_student_id = student_id
            
        try:
            # Get all grades for this student
            query = """
                SELECT e.exam_type, s.subject_name, g.marks_obtained, g.total_marks, e.date
                FROM grades g
                JOIN exams e ON g.exam_id = e.exam_id
                JOIN subjects s ON e.subject_id = s.subject_id
                JOIN teachers t ON s.teacher_id = t.teacher_id
                WHERE g.student_id = ? AND t.teacher_id = ?
                ORDER BY e.date DESC
            """
            self.db.cursor.execute(query, (student_id, self.teacher_id))
            grades = self.db.cursor.fetchall()
            
            if not grades:
                self.show_message("No grades found for this student", "error")
                return
                
            # Process the data
            exam_names = [f"{grade[0]} - {grade[1]}" for grade in grades]
            marks = [grade[2] for grade in grades]
            total_marks = [grade[3] for grade in grades]
            dates = [grade[4] for grade in grades]
            
            # Calculate percentages
            percentages = [(mark / total) * 100 for mark, total in zip(marks, total_marks)]
            
            # Clear previous plots
            for widget in self.individual_report_frame.winfo_children():
                widget.destroy()
                
            # Create figure with multiple subplots - reduced figure size
            fig = plt.figure(figsize=(10, 6), dpi=100)  # Reduced height to fit better
            
            # First subplot - Line chart of performance over time
            ax1 = fig.add_subplot(2, 1, 1)
            ax1.plot(dates, percentages, marker='o', linestyle='-', color='blue')
            ax1.set_title('Performance Over Time')
            ax1.set_xlabel('Exam Date')
            ax1.set_ylabel('Percentage (%)')
            ax1.axhline(y=40, color='r', linestyle='--', label='Pass Threshold (40%)')
            ax1.set_xticklabels(dates, rotation=45, ha='right')
            ax1.grid(True, linestyle='--', alpha=0.7)
            ax1.legend()
            
            # Second subplot - Bar chart comparing with class average
            ax2 = fig.add_subplot(2, 1, 2)
            
            # Get class average for each exam
            class_averages = []
            
            for i, grade in enumerate(grades):
                # Get the exam_id for this grade
                self.db.cursor.execute("""
                    SELECT exam_id FROM exams 
                    WHERE exam_type = ? AND subject_id = (SELECT subject_id FROM subjects WHERE subject_name = ?)
                    AND date = ?
                """, (grade[0], grade[1], grade[4]))
                
                exam_id = self.db.cursor.fetchone()
                
                if exam_id:
                    # Get all grades for this exam
                    self.db.cursor.execute("""
                        SELECT AVG(marks_obtained * 100.0 / total_marks) 
                        FROM grades 
                        WHERE exam_id = ?
                    """, (exam_id[0],))
                    
                    avg = self.db.cursor.fetchone()[0]
                    class_averages.append(avg)
                else:
                    class_averages.append(0)  # Default if exam not found
            
            # Set up bar chart data
            x = np.arange(len(exam_names))
            width = 0.35
            
            ax2.bar(x - width/2, percentages, width, label='Student')
            ax2.bar(x + width/2, class_averages, width, label='Class Average')
            
            ax2.set_title('Student vs Class Average')
            ax2.set_xlabel('Exams')
            ax2.set_ylabel('Percentage (%)')
            ax2.set_xticks(x)
            ax2.set_xticklabels(exam_names, rotation=45, ha='right')
            ax2.legend()
            ax2.grid(True, linestyle='--', alpha=0.3)
            
            # Adjust layout
            plt.tight_layout()
            
            # Create canvas and add to frame
            canvas = FigureCanvasTkAgg(fig, master=self.individual_report_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add statistics and comments
            stats_frame = ctk.CTkFrame(self.individual_report_frame, fg_color="transparent")
            stats_frame.pack(fill="x", pady=10)
            
            # Get student name
            student_name = student_text.split(" (")[0]
            
            # Calculate overall performance
            avg_percentage = sum(percentages) / len(percentages)
            highest_percentage = max(percentages)
            lowest_percentage = min(percentages)
            pass_count = sum(1 for p in percentages if p >= 40)
            pass_rate = (pass_count / len(percentages)) * 100
            
            # Check for improvement trend
            if len(percentages) >= 2:
                # Check the trend of most recent exams (last 3 or all if less than 3)
                recent_count = min(3, len(percentages))
                recent_percentages = percentages[:recent_count]  # Most recent first
                
                if all(recent_percentages[i] >= recent_percentages[i+1] for i in range(len(recent_percentages)-1)):
                    trend = "improving"
                elif all(recent_percentages[i] <= recent_percentages[i+1] for i in range(len(recent_percentages)-1)):
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "not enough data"
            
            # Display statistics
            stats_header = ctk.CTkLabel(stats_frame, 
                                      text=f"Performance Report for {student_name}", 
                                      font=("Arial", 14, "bold"))
            stats_header.pack(anchor="w", padx=10, pady=5)
            
            stats_text = (
                f"Total Exams: {len(percentages)}  |  "
                f"Average Performance: {avg_percentage:.2f}%  |  "
                f"Highest: {highest_percentage:.2f}%  |  "
                f"Lowest: {lowest_percentage:.2f}%  |  "
                f"Pass Rate: {pass_rate:.2f}%"
            )
            
            stats_label = ctk.CTkLabel(stats_frame, text=stats_text, 
                                     font=("Arial", 12))
            stats_label.pack(anchor="w", padx=10, pady=5)
            
            # Add performance comments
            comment = "Performance Analysis: "
            
            # Overall performance comment
            if avg_percentage >= 75:
                comment += f"{student_name} is performing excellently. "
            elif avg_percentage >= 60:
                comment += f"{student_name} is performing well. "
            elif avg_percentage >= 40:
                comment += f"{student_name} is performing adequately but has room for improvement. "
            else:
                comment += f"{student_name} is performing below expectations. Additional support may be needed. "
            
            # Trend comment
            if trend == "improving":
                comment += "Their performance shows an improving trend in recent exams."
            elif trend == "declining":
                comment += "Their performance shows a declining trend in recent exams. This may require attention."
            elif trend == "stable":
                comment += "Their performance has been relatively stable across exams."
            else:
                comment += "Not enough data to determine performance trends."
                
            comment_label = ctk.CTkLabel(stats_frame, text=comment, 
                                       font=("Arial", 12), 
                                       wraplength=700)
            comment_label.pack(anchor="w", padx=10, pady=5)
            
        except sqlite3.Error as e:
            self.show_message(f"Database error: {str(e)}", "error")
        except Exception as e:
            self.show_message(f"Error generating report: {str(e)}", "error")
            
    def show_message(self, message, msg_type="info"):
        """Show simple message dialog."""
        message_window = ctk.CTkToplevel(self.frame)
        message_window.title("Message")
        message_window.geometry("300x150")
        message_window.attributes("-topmost", True)
        
        ctk.CTkLabel(message_window, text=message, wraplength=250).pack(expand=True)
        ctk.CTkButton(message_window, text="OK", command=message_window.destroy).pack(pady=10)


# Example usage
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Teacher Performance Graphs")
    app.geometry("900x700")
    
    # Example: teacher_id=4
    teacher_performance = TeacherPerformance(app, teacher_id=4)
    teacher_performance.show()
    
    app.mainloop()
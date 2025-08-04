import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import pandas as pd
from teacher.db_manager import DatabaseManager
class TeacherGrades:
    def __init__(self, parent_frame, teacher_id):
        self.parent_frame = parent_frame
        self.teacher_id = teacher_id
        self.frame = None
        self.db = DatabaseManager()
        
    def show(self):
        # Create a new frame each time show is called
        self.frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.frame.pack(fill="both", expand=True)
        self.setup_teacher_grades()
        
    def hide(self):
        if self.frame:
            self.frame.pack_forget()
            
    def setup_teacher_grades(self):
        # Simple header
        header_label = ctk.CTkLabel(self.frame, text="Teacher Grades Management", font=("Arial", 18))
        header_label.pack(anchor="w", pady=5)
        
        # Create a simple tabview
        self.tabview = ctk.CTkTabview(self.frame)
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add tabs
        self.tabview.add("Add Grades")
        self.tabview.add("View Grades")
        self.tabview.add("Export Data")
        
        # Setup tabs
        self.setup_add_grades_tab()
        self.setup_view_grades_tab()
        self.setup_export_tab()
        
    def setup_add_grades_tab(self):
        tab = self.tabview.tab("Add Grades")
        
        # Exam selection area
        exam_frame = ctk.CTkFrame(tab, fg_color="transparent")
        exam_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(exam_frame, text="Select Exam:").pack(side="left", padx=5)
        
        # Get exam list for this teacher
        exams = self.get_teacher_exams()
        self.exam_combo = ctk.CTkComboBox(exam_frame, values=exams or ["No exams found"], width=300)
        self.exam_combo.pack(side="left", padx=5)
        
        # Total marks entry
        marks_frame = ctk.CTkFrame(tab, fg_color="transparent")
        marks_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(marks_frame, text="Total Marks:").pack(side="left", padx=5)
        self.total_marks_entry = ctk.CTkEntry(marks_frame, width=100)
        self.total_marks_entry.pack(side="left", padx=5)
        
        # Load students button
        load_btn = ctk.CTkButton(tab, text="Load Students", 
                              command=self.load_students_for_grading,
                              width=200)
        load_btn.pack(pady=10)
        
        # Scrollable frame for students
        self.students_frame = ctk.CTkScrollableFrame(tab)
        self.students_frame.pack(fill="both", expand=True, pady=10)
        
        # Submit button at bottom
        submit_btn = ctk.CTkButton(tab, text="Submit All Grades", 
                                command=self.submit_grades,
                                width=200)
        submit_btn.pack(pady=10)
        
    def setup_view_grades_tab(self):
        tab = self.tabview.tab("View Grades")
        
        # Exam filter area
        filter_frame = ctk.CTkFrame(tab, fg_color="transparent")
        filter_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(filter_frame, text="Select Exam:").pack(side="left", padx=5)
        
        # Get exam list for this teacher
        exams = self.get_teacher_exams()
        self.view_exam_combo = ctk.CTkComboBox(filter_frame, values=exams or ["No exams found"], width=300)
        self.view_exam_combo.pack(side="left", padx=5)
        
        view_btn = ctk.CTkButton(filter_frame, text="View Grades", 
                              command=self.view_exam_grades,
                              width=120)
        view_btn.pack(side="left", padx=10)
        
        # Grades display area with a textbox
        self.grades_textbox = ctk.CTkTextbox(tab, width=600, height=400)
        self.grades_textbox.pack(fill="both", expand=True, pady=10)
        
    def setup_export_tab(self):
        tab = self.tabview.tab("Export Data")
        
        # Export options
        export_frame = ctk.CTkFrame(tab, fg_color="transparent")
        export_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(export_frame, text="Export Grades Data", font=("Arial", 16)).pack(pady=10)
        
        # Select exam to export
        exam_frame = ctk.CTkFrame(export_frame, fg_color="transparent")
        exam_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(exam_frame, text="Select Exam:").pack(side="left", padx=5)
        
        exams = self.get_teacher_exams()
        self.export_exam_combo = ctk.CTkComboBox(exam_frame, values=exams or ["No exams found"], width=300)
        self.export_exam_combo.pack(side="left", padx=5)
        
        # Export format options
        format_frame = ctk.CTkFrame(export_frame, fg_color="transparent")
        format_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(format_frame, text="Export Format:").pack(side="left", padx=5)
        
        self.export_format = ctk.CTkComboBox(format_frame, values=["CSV", "Excel"], width=100)
        self.export_format.set("CSV")
        self.export_format.pack(side="left", padx=5)
        
        # Export button
        export_btn = ctk.CTkButton(export_frame, text="Export Grades", 
                                command=self.export_grades,
                                width=200)
        export_btn.pack(pady=20)
        
    def get_teacher_exams(self):
        """Get exams associated with this teacher's subjects"""
        try:
            query = """
                SELECT e.exam_id, e.exam_type, s.subject_name, e.date
                FROM exams e
                JOIN subjects s ON e.subject_id = s.subject_id
                WHERE s.teacher_id = ?
                ORDER BY e.date DESC
            """
            self.db.cursor.execute(query, (self.teacher_id,))
            exams = self.db.cursor.fetchall()
            
            if not exams:
                return ["No exams found"]
                
            return [f"{exam[0]} - {exam[1]} ({exam[2]}) on {exam[3]}" for exam in exams]
        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return ["Error loading exams"]
    
    def load_students_for_grading(self):
        """Load students for grading based on selected exam"""
        # Clear existing entries
        for widget in self.students_frame.winfo_children():
            widget.destroy()
            
        exam_text = self.exam_combo.get()
        if "No exams found" in exam_text or not exam_text:
            self.show_message("No exam selected or no exams available", "error")
            return
            
        # Extract exam_id from the selection
        try:
            exam_id = int(exam_text.split(" - ")[0])
        except (ValueError, IndexError):
            self.show_message("Invalid exam selection", "error")
            return
            
        try:
            # Get subject_id for this exam
            self.db.cursor.execute("SELECT subject_id FROM exams WHERE exam_id = ?", (exam_id,))
            result = self.db.cursor.fetchone()
            if not result:
                self.show_message("Exam not found", "error")
                return
                
            subject_id = result[0]
            
            # Get students eligible for this exam
            query = """
                SELECT s.student_id, s.name, s.roll_number, s.course
                FROM students s
                ORDER BY s.name
            """
            self.db.cursor.execute(query)
            students = self.db.cursor.fetchall()
            
            if not students:
                ctk.CTkLabel(self.students_frame, text="No students found").pack(pady=10)
                return
                
            # Store entries for later submission
            self.student_mark_entries = {}
            
            # List of students with entry fields
            for student in students:
                row_frame = ctk.CTkFrame(self.students_frame)
                row_frame.pack(fill="x", pady=2)
                
                student_info = f"{student[1]} (Roll: {student[2]}, Course: {student[3]})"
                ctk.CTkLabel(row_frame, text=student_info, width=400, anchor="w").pack(side="left", padx=5)
                
                # Check if student already has grade for this exam
                self.db.cursor.execute("""
                    SELECT marks_obtained FROM grades 
                    WHERE student_id = ? AND exam_id = ?
                """, (student[0], exam_id))
                existing_mark = self.db.cursor.fetchone()
                
                # Mark entry field
                mark_entry = ctk.CTkEntry(row_frame, width=80)
                mark_entry.pack(side="right", padx=10)
                
                # Add to dict for later collection
                self.student_mark_entries[student[0]] = mark_entry
                
                # Fill in existing mark if any
                if existing_mark:
                    mark_entry.insert(0, str(existing_mark[0]))
                    
        except sqlite3.Error as e:
            self.show_message(f"Database error: {str(e)}", "error")
    
    def submit_grades(self):
        """Submit all entered grades to database"""
        exam_text = self.exam_combo.get()
        if "No exams found" in exam_text or not exam_text:
            self.show_message("No exam selected", "error")
            return
            
        # Extract exam_id
        try:
            exam_id = int(exam_text.split(" - ")[0])
        except (ValueError, IndexError):
            self.show_message("Invalid exam selection", "error")
            return
            
        # Get total marks
        total_marks = self.total_marks_entry.get().strip()
        if not total_marks:
            self.show_message("Please enter total marks", "error")
            return
            
        try:
            total_marks = int(total_marks)
            if total_marks <= 0:
                self.show_message("Total marks must be greater than zero", "error")
                return
        except ValueError:
            self.show_message("Total marks must be a number", "error")
            return
            
        # Begin submission
        try:
            for student_id, mark_entry in self.student_mark_entries.items():
                mark = mark_entry.get().strip()
                if not mark:
                    continue  # Skip empty entries
                    
                try:
                    mark = int(mark)
                    if mark < 0 or mark > total_marks:
                        self.show_message(f"Invalid mark for student {student_id}: must be between 0 and {total_marks}", "error")
                        return
                except ValueError:
                    self.show_message(f"Invalid mark for student {student_id}: must be a number", "error")
                    return
                    
                # Check if grade already exists
                self.db.cursor.execute("""
                    SELECT grade_id FROM grades 
                    WHERE student_id = ? AND exam_id = ?
                """, (student_id, exam_id))
                existing = self.db.cursor.fetchone()
                
                if existing:
                    # Update existing grade
                    self.db.cursor.execute("""
                        UPDATE grades SET marks_obtained = ?, total_marks = ?
                        WHERE student_id = ? AND exam_id = ?
                    """, (mark, total_marks, student_id, exam_id))
                else:
                    # Insert new grade
                    self.db.cursor.execute("""
                        INSERT INTO grades (student_id, exam_id, marks_obtained, total_marks)
                        VALUES (?, ?, ?, ?)
                    """, (student_id, exam_id, mark, total_marks))
                    
            self.db.conn.commit()
            self.show_message("Grades submitted successfully")
            
        except sqlite3.Error as e:
            self.db.conn.rollback()
            self.show_message(f"Database error: {str(e)}", "error")
    
    def view_exam_grades(self):
        """View grades for the selected exam"""
        exam_text = self.view_exam_combo.get()
        if "No exams found" in exam_text or not exam_text:
            self.show_message("No exam selected", "error")
            return
            
        # Extract exam_id
        try:
            exam_id = int(exam_text.split(" - ")[0])
        except (ValueError, IndexError):
            self.show_message("Invalid exam selection", "error")
            return
            
        try:
            # Get exam info
            self.db.cursor.execute("""
                SELECT e.exam_type, s.subject_name, e.date
                FROM exams e
                JOIN subjects s ON e.subject_id = s.subject_id
                WHERE e.exam_id = ?
            """, (exam_id,))
            exam_info = self.db.cursor.fetchone()
            
            if not exam_info:
                self.show_message("Exam not found", "error")
                return
                
            # Get grades
            query = """
                SELECT s.name, s.roll_number, g.marks_obtained, g.total_marks
                FROM grades g
                JOIN students s ON g.student_id = s.student_id
                WHERE g.exam_id = ?
                ORDER BY s.name
            """
            self.db.cursor.execute(query, (exam_id,))
            grades = self.db.cursor.fetchall()
            
            # Clear and update the textbox
            self.grades_textbox.delete("1.0", "end")
            
            # Exam header
            exam_header = f"Exam: {exam_info[0]} - {exam_info[1]} on {exam_info[2]}\n"
            self.grades_textbox.insert("end", exam_header)
            self.grades_textbox.insert("end", "=" * len(exam_header) + "\n\n")
            
            if not grades:
                self.grades_textbox.insert("end", "No grades recorded for this exam.")
                return
                
            # Calculate statistics
            total_students = len(grades)
            sum_percentage = 0
            highest_mark = 0
            lowest_mark = float('inf')
            
            # Display grades and gather stats
            for grade in grades:
                name, roll, marks, total = grade
                percentage = (marks / total) * 100 if total > 0 else 0
                sum_percentage += percentage
                highest_mark = max(highest_mark, percentage)
                lowest_mark = min(lowest_mark, percentage)
                
                self.grades_textbox.insert("end", f"Student: {name} (Roll: {roll})\n")
                self.grades_textbox.insert("end", f"Marks: {marks}/{total} ({percentage:.2f}%)\n")
                self.grades_textbox.insert("end", "-" * 40 + "\n")
                
            # Class statistics
            self.grades_textbox.insert("end", "\nCLASS STATISTICS\n")
            self.grades_textbox.insert("end", "-" * 20 + "\n")
            self.grades_textbox.insert("end", f"Total Students: {total_students}\n")
            
            if total_students > 0:
                avg_percentage = sum_percentage / total_students
                self.grades_textbox.insert("end", f"Average Percentage: {avg_percentage:.2f}%\n")
                self.grades_textbox.insert("end", f"Highest Percentage: {highest_mark:.2f}%\n")
                if lowest_mark != float('inf'):
                    self.grades_textbox.insert("end", f"Lowest Percentage: {lowest_mark:.2f}%\n")
                
        except sqlite3.Error as e:
            self.show_message(f"Database error: {str(e)}", "error")
    
    def export_grades(self):
        """Export grades data to CSV or Excel"""
        exam_text = self.export_exam_combo.get()
        if "No exams found" in exam_text or not exam_text:
            self.show_message("No exam selected", "error")
            return
            
        # Extract exam_id
        try:
            exam_id = int(exam_text.split(" - ")[0])
        except (ValueError, IndexError):
            self.show_message("Invalid exam selection", "error")
            return
            
        export_format = self.export_format.get()
        
        try:
            # Get exam info for filename
            self.db.cursor.execute("""
                SELECT exam_type, date FROM exams WHERE exam_id = ?
            """, (exam_id,))
            exam_info = self.db.cursor.fetchone()
            
            if not exam_info:
                self.show_message("Exam not found", "error")
                return
                
            # Create a safe filename
            exam_name = f"{exam_info[0]}_{exam_info[1]}".replace(" ", "_").replace(":", "-")
            
            # Get grades data
            query = """
                SELECT s.student_id, s.name, s.roll_number, s.course, 
                    g.marks_obtained, g.total_marks
                FROM grades g
                JOIN students s ON g.student_id = s.student_id
                WHERE g.exam_id = ?
                ORDER BY s.name
            """
            self.db.cursor.execute(query, (exam_id,))
            grades = self.db.cursor.fetchall()
            
            if not grades:
                self.show_message("No grades to export", "error")
                return
                
            # Convert to DataFrame
            df = pd.DataFrame(grades, columns=[
                "Student ID", "Student Name", "Roll Number", "Course",
                "Marks Obtained", "Total Marks"
            ])
            
            # Add percentage column
            df["Percentage"] = (df["Marks Obtained"] / df["Total Marks"] * 100).round(2)
            
            # Create a directory for exports if it doesn't exist
            import os
            export_dir = "exports"
            os.makedirs(export_dir, exist_ok=True)
            
            # Fix extension for different export formats
            if export_format == "CSV":
                filename = os.path.join(export_dir, f"grades_{exam_name}.csv")
                df.to_csv(filename, index=False)
                self.show_message(f"Grades exported successfully to CSV file:\n{filename}")
            elif export_format == "Excel":
                try:
                    # Use .xlsx extension for Excel files
                    filename = os.path.join(export_dir, f"grades_{exam_name}.xlsx")
                    df.to_excel(filename, index=False, sheet_name="Grades", engine="openpyxl")
                    self.show_message(f"Grades exported successfully to Excel file:\n{filename}")
                except ImportError:
                    self.show_message("Error: openpyxl package is required for Excel export.\nPlease install it with: pip install openpyxl", "error")
                    # Fallback to CSV
                    csv_filename = os.path.join(export_dir, f"grades_{exam_name}.csv")
                    df.to_csv(csv_filename, index=False)
                    self.show_message(f"Exported as CSV instead:\n{csv_filename}")
                except Exception as e:
                    self.show_message(f"Excel export error: {str(e)}\nTrying CSV format instead.", "error")
                    # Fallback to CSV on any other error
                    csv_filename = os.path.join(export_dir, f"grades_{exam_name}.csv")
                    df.to_csv(csv_filename, index=False)
                    self.show_message(f"Exported as CSV instead:\n{csv_filename}")
                
        except sqlite3.Error as e:
            self.show_message(f"Database error: {str(e)}", "error")
        except Exception as e:
            self.show_message(f"Export error: {str(e)}", "error")  
    def show_message(self, message, msg_type="info"):
        """Show simple message dialog"""
        message_window = ctk.CTkToplevel(self.frame)
        message_window.title("Message")
        message_window.geometry("300x150")
        message_window.attributes("-topmost", True)
        
        ctk.CTkLabel(message_window, text=message, wraplength=250).pack(expand=True)
        ctk.CTkButton(message_window, text="OK", command=message_window.destroy).pack(pady=10)


# Example usage
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Teacher Grades Interface")
    app.geometry("900x700")
    
    teacher = TeacherGrades(app, teacher_id=4)
    teacher.show()
    
    app.mainloop()
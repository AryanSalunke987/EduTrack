import customtkinter as ctk


class StudentTimetable(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)  # Ensure the frame fills the parent area
        self.create_timetable()

    def create_timetable(self):
        # Timetable Data
        timetable = [
            ["Day \\ Time", "8:30 - 9:30", "9:30 - 10:30", "10:30 - 11:30", "11:30 - 12:30", "1:30 - 2:30", "2:30 - 3:30", "3:30 - 4:30"],
            ["MONDAY", "Remedial Lecture", "Remedial Lecture", "EM-IV MK(1001)", "AT KS(1001)", "OS AK(1001)", "S21 UL AK (1003)\nS22 PL NRJ (1003)\nS23 PL ABK (1004)", "S21 UL AK (1003)\nS22 PL NRJ (1003)\nS23 PL ABK (1004)"],
            ["TUESDAY", "Remedial Lecture", "Mini Project Meet", "S21 MPL MI (906)\nS22 NL SKP (1003)\nS23 MPL ABM (906)", "S21 MPL MI (906)\nS22 NL SKP (1003)\nS23 MPL ABM (906)", "COA RM(1104)", "EM-IV MK(1001)", "CNND SKP(1001)"],
            ["WEDNESDAY", "Remedial Lecture", "Mini Project Meet", "CNND SKP(1104)", "AT KS(1104)", "COA RM(1104)", "PL S21 SP (1003)\nUL S22 AK (1003)\nNL S23 SKP (1004)", "PL S21 SP (1003)\nUL S22 AK (1003)\nNL S23 SKP (1004)"],
            ["THURSDAY", "Remedial Lecture", "EM-IV Tutorial", "S21 NL SKP (1003)\nS22 PL NRJ (1004)\nS23 PL ABK (1004)", "S21 NL SKP (1003)\nS22 PL NRJ (1004)\nS23 PL ABK (1004)", "CNND SKP(1104)", "EM-IV MK(1104)", "OS AK(1104)"],
            ["FRIDAY", "EM-IV Tutorial", "EM-IV Tutorial", "AT KS(1001)", "OS AK(1001)", "COA RM(1104)", "S21 PL SP (1004)\nS22 MPL RM(906)\nS23 UL AK (1003)", "S21 PL SP (1004)\nS22 MPL RM(906)\nS23 UL AK (1003)"],
        ]

        # Create Timetable Header
        for row_idx, row in enumerate(timetable):
            for col_idx, cell in enumerate(row):
                # Create cell
                fg_color = "#9aa0a1" if row_idx == 0 or col_idx == 0 else "#d9dbdb"  # Header and Day cells have a different color
                text_color = "white" if row_idx == 0 or col_idx == 0 else "black"
                font = ("Arial", 16, "bold") if row_idx == 0 or col_idx == 0 else ("Arial", 14)

                cell_label = ctk.CTkLabel(
                    self,
                    text=cell,
                    font=font,
                    fg_color=fg_color,
                    text_color=text_color,
                    corner_radius=5,
                )
                cell_label.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="nsew")

        # Configure grid weights for responsiveness
        total_columns = len(timetable[0])
        total_rows = len(timetable)
        for col_idx in range(total_columns):
            self.grid_columnconfigure(col_idx, weight=1)
        for row_idx in range(total_rows):
            self.grid_rowconfigure(row_idx, weight=1)


if __name__ == "__main__":
    # Test the timetable as a standalone application
    app = ctk.CTk()
    app.title("Teacher Timetable")
    app.geometry("1920x1080")
    timetable = StudentTimetable(app)
    app.mainloop()
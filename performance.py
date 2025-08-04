import customtkinter as ctk

def create_performance(parent):
    """Function to display the Performance page."""
    label = ctk.CTkLabel(parent, text="Performance", font=("Arial", 20, "bold"))
    label.pack(pady=20)

    content = ctk.CTkLabel(parent, text="View student performance analytics here.", font=("Arial", 14))
    content.pack(pady=10)

import customtkinter as ctk
import sqlite3
from tkinter import messagebox


class MakeAnnouncements(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)  # Ensure the frame fills the parent area
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = ctk.CTkLabel(self, text="Make Announcements", font=("Arial", 24, "bold"))
        self.title.pack(pady=20)

        # Announcement Input Field with Manual Placeholder
        self.announcement_entry = ctk.CTkTextbox(self, height=200, width=700)
        self.announcement_entry.pack(pady=20)
        self.placeholder_text = "Type your announcement here..."  # Placeholder text
        self.set_placeholder()  # Set placeholder initially

        # Bind events for placeholder functionality
        self.announcement_entry.bind("<FocusIn>", self.clear_placeholder)
        self.announcement_entry.bind("<FocusOut>", self.set_placeholder)

        # Post Announcement Button
        self.post_button = ctk.CTkButton(self, text="Post Announcement", command=self.post_announcement, width=200)
        self.post_button.pack(pady=10)

        # Announcement Display Bar
        self.announcement_listbox = ctk.CTkTextbox(self, height=300, width=600)
        self.announcement_listbox.pack(pady=20, padx=20)
        self.announcement_listbox.configure(state="disabled")  # Make it read-only

        # Load existing announcements
        self.load_announcements()

    def set_placeholder(self, event=None):
        """Set placeholder text in the announcement entry."""
        if not self.announcement_entry.get("1.0", "end").strip():  # Check if the textbox is empty
            self.announcement_entry.insert("1.0", self.placeholder_text)
            self.announcement_entry.configure(fg_color="gray")  # Set placeholder color

    def clear_placeholder(self, event=None):
        """Clear placeholder text when the user focuses on the textbox."""
        if self.announcement_entry.get("1.0", "end").strip() == self.placeholder_text:
            self.announcement_entry.delete("1.0", "end")
            self.announcement_entry.configure(fg_color="black")  # Reset text color

    def post_announcement(self):
        # Get the announcement text
        announcement_text = self.announcement_entry.get("1.0", "end").strip()

        # Check if the announcement is empty or still has the placeholder text
        if not announcement_text or announcement_text == self.placeholder_text:
            messagebox.showwarning("Empty Announcement", "Please type an announcement before posting.")
            return

        try:
            # Save the announcement to the database
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO announcements (announcement_text)
                VALUES (?)
            """, (announcement_text,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Announcement posted successfully.")
            self.announcement_entry.delete("1.0", "end")  # Clear the textbox
            self.set_placeholder()  # Reset placeholder
            self.load_announcements()  # Refresh the announcements list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to post announcement: {str(e)}")

    def load_announcements(self):
        # Clear the listbox
        self.announcement_listbox.configure(state="normal")  # Enable writing to clear the listbox
        self.announcement_listbox.delete("1.0", "end")

        try:
            # Fetch all announcements from the database
            conn = sqlite3.connect("edutrack.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, announcement_text, created_at
                FROM announcements
                ORDER BY created_at DESC
            """)
            announcements = cursor.fetchall()
            conn.close()

            # Display announcements in the listbox
            for announcement in announcements:
                self.announcement_listbox.insert("end", f"ID: {announcement[0]} | Date: {announcement[2]}\n{announcement[1]}\n{'-' * 80}\n")
            self.announcement_listbox.configure(state="disabled")  # Make it read-only again
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load announcements: {str(e)}")
            self.announcement_listbox.configure(state="disabled")  # Make it read-only again
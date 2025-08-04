import customtkinter as ctk
from PIL import Image
import sqlite3

# Connect to SQLite Database
conn = sqlite3.connect("edutrack.db")
cursor = conn.cursor()

# Fetch Image Path
student_id = 1  # Example student
cursor.execute("SELECT photo_path FROM photostudent WHERE student_id = ?", (student_id,))
result = cursor.fetchone()

if result:
    photo_path = result[0]  # Get stored image path

    # Load and Display Image
    app = ctk.CTk()
    app.geometry("400x500")
    app.title("Student Profile")

    image = ctk.CTkImage(light_image=Image.open(photo_path), size=(150, 150))
    label = ctk.CTkLabel(app, image=image, text="")
    label.pack(pady=20)

    app.mainloop()
else:
    print("No photo found for this student.")

# Close Connection
cursor.close()
conn.close()

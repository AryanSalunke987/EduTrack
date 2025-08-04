import sqlite3

def get_db_connection():
    try:
        conn = sqlite3.connect('edutrack.db')
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None, None

def insert_sample_exam_data():
    conn, cursor = get_db_connection()
    if conn and cursor:
        try:

            # Insert sample examsnnd_id,))
            cursor.execute("INSERT INTO exams (subject_id, date) VALUES (1, '2025-04-15');")
            cursor.execute("INSERT INTO exams (subject_id, date) VALUES (2, '2025-04-10');")
            cursor.execute("INSERT INTO exams (subject_id, date) VALUES (3, '2025-03-25');")

            conn.commit()
            print("Sample exam data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    insert_sample_exam_data()
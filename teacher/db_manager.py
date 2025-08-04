import sqlite3

class DatabaseManager:
    """
    Simple database manager class to handle connections and operations
    with the SQLite database.
    """
    
    def __init__(self, db_path="edutrack.db"):
        """Initialize database connection and cursor"""
        try:
            # Connect to database
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row  # Enable row access by name
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {str(e)}")
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
    
    def get_class_list(self):
        """Get list of class names"""
        try:
            self.cursor.execute("SELECT class_name FROM classes ORDER BY class_name")
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error:
            return ["Error loading classes"]
    
    def execute_query(self, query, params=None):
        """Execute a query with optional parameters"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Query error: {str(e)}")
            return None
    
    def execute_and_commit(self, query, params=None):
        """Execute a query and commit changes"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Query error: {str(e)}")
            return False

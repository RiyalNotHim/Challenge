import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'urls.db')

def init_db():
    """Initializes the database and creates the 'links' table."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            clicks INTEGER NOT NULL DEFAULT 0
        )
        """)
        
        conn.commit()
        print(f"Database initialized successfully at {DB_FILE}")
        
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
    finally:
        if conn:
            conn.close()

def get_db_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# This allows the file to be run directly to initialize the DB
if __name__ == "__main__":
    print("Initializing database...")
    init_db()
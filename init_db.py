import sqlite3

def create_tables():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        
        # Create the students table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                attendance INTEGER DEFAULT 0
            )
        ''')

        # Create the users table for authentication
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'student'  -- Added role column
            )
        ''')

        # Create the tasks table for tracking student tasks
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                task_name TEXT NOT NULL,
                status INTEGER DEFAULT 0,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        ''')
        
        con.commit()
    print("Tables created successfully!")

# Verify tables function
def verify_tables():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        print("Existing tables:", tables)

if __name__ == '__main__':
    create_tables()
    verify_tables()  # Check if tables were created successfully

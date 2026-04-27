import sqlite3
import bcrypt

def get_connection():
    return sqlite3.connect("data/app_database.db")

def initialize_database():
    """Creates the necessary tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create Users Table for RBAC
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Check if old records table exists (migration check)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='records'")
    old_table_exists = cursor.fetchone()
    
    if old_table_exists:
        # Check if table has old column names
        cursor.execute("PRAGMA table_info(records)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'no' in columns or 'gemphil' in columns:  # Old schema detected
            # Rename old table
            cursor.execute("ALTER TABLE records RENAME TO records_old")
    
    # Create new Data Table with capitalized column names and combined GEMPHIL_DEVICE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NO TEXT,
            CLIENT TEXT,
            LOCATION TEXT,
            CURRENCY TEXT,
            PROGRESS TEXT,
            IMAGE_PATH TEXT,
            PROJECT TEXT,
            GEMPHIL_DEVICE TEXT,
            DETAILS TEXT,
            CONTACT_PERSON TEXT,
            EMAIL TEXT
        )
    ''')
    
    # If old table exists, migrate data
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='records_old'")
    if cursor.fetchone():
        try:
            cursor.execute("""
                INSERT INTO records (NO, CLIENT, LOCATION, CURRENCY, PROGRESS, IMAGE_PATH, PROJECT, GEMPHIL_DEVICE, DETAILS, CONTACT_PERSON, EMAIL)
                SELECT 
                    COALESCE(no, ''), 
                    COALESCE(client, ''), 
                    COALESCE(location, ''), 
                    COALESCE(currency, ''), 
                    COALESCE(progress, ''), 
                    COALESCE(image_path, ''), 
                    COALESCE(project, ''),
                    CASE 
                        WHEN device IS NOT NULL AND TRIM(device) != '' 
                        THEN TRIM(COALESCE(gemphil, '') || ' ' || TRIM(device))
                        ELSE COALESCE(gemphil, '')
                    END as gemphil_device,
                    COALESCE(details, ''), 
                    COALESCE(contact_person, ''), 
                    COALESCE(email, '')
                FROM records_old
            """)
            cursor.execute("DROP TABLE records_old")
        except sqlite3.OperationalError:
            # Old table might not have data, so just continue
            pass
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# Helper to add a default admin user for testing
def create_default_admin():
    conn = get_connection()
    cursor = conn.cursor()
    # Check if admin exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                       ('admin', hashed, 'admin'))
        conn.commit()
    conn.close()

if __name__ == "__main__":
    # Create the 'data' directory if it doesn't exist
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
    
    initialize_database()
    create_default_admin()
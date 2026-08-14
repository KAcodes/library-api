import sqlite3


DATABASE_PATH = "library.db"


def get_connection():
    con = sqlite3.connect(DATABASE_PATH)
    con.row_factory = sqlite3.Row
    return con

def create_table():
    con = get_connection()
    cur = con.cursor()


    # cur.execute("DROP TABLE IF EXISTS BOOKS")

    cur.execute(
    """
        CREATE TABLE IF NOT EXISTS BOOKS (
            id VARCHAR PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            isbn VARCHAR(255)
        );
    """
    )

    cur.execute("DROP TABLE IF EXISTS USERS")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS USERS (
            id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
        );
    """)


    cur.execute("DROP TABLE IF EXISTS LOANS")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS LOANS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            borrowed_at TEXT NOT NULL,
            due_date TEXT NOT NULL,
            returned_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        );
    """)

    con.commit()
    con.close()


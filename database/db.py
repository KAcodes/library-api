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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            borrowed_at TEXT NOT NULL,
            due_date TEXT NOT NULL,
            returned_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    con.commit()
    con.close()


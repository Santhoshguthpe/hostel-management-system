import sqlite3

DATABASE = "hostel.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS students(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        age INTEGER,

        gender TEXT,

        room TEXT,

        phone TEXT,

        course TEXT,

        fee_status TEXT

    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    print("Database Created Successfully")
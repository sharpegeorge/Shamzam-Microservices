import sqlite3
import os

DB_NAME = 'tracks.db'

def init_db():
    """Creates the database and tables if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Track table with a composite primary key (title, artist)
    cursor.execute('''
        CREATE TABLE tracks (
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            song TEXT NOT NULL,
            PRIMARY KEY (title, artist)
        )
    ''')

    conn.commit()
    conn.close()

def reset_db():
    """Drops all tables and recreates them to ensure a clean state."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)  # Deletes the database file to reset everything

    init_db()  # Reinitialize the database

if __name__ == '__main__':
    reset_db()

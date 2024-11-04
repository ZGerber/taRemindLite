import sqlite3
from typing import List, Dict, Any, Tuple, Optional
from contextlib import contextmanager


@contextmanager
def connect_to_db(db_file: str):
    """Context manager for database connection."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    try:
        yield cursor
    finally:
        conn.commit()
        conn.close()


class SQLiteDatabase:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.create_tables()

    def create_tables(self) -> None:
        with connect_to_db(self.db_file) as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Meetings (
                id INTEGER PRIMARY KEY,
                meeting_name TEXT NOT NULL,
                day_of_week TEXT NOT NULL,
                time TEXT NOT NULL,
                zoom_link TEXT,
                zoom_meeting_id TEXT,
                zoom_passcode TEXT
            );
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Contacts (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone_number TEXT
            );
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Reminders (
                id INTEGER PRIMARY KEY,
                meeting_id INTEGER,
                reminder_day TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY (meeting_id) REFERENCES Meetings(id) ON DELETE CASCADE
            );
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Participants (
                meeting_id INTEGER,
                contact_id INTEGER,
                PRIMARY KEY (meeting_id, contact_id),
                FOREIGN KEY (meeting_id) REFERENCES Meetings(id) ON DELETE CASCADE,
                FOREIGN KEY (contact_id) REFERENCES Contacts(id) ON DELETE CASCADE
            );
            ''')

    def query(self, sql: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
        with connect_to_db(self.db_file) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    @staticmethod
    def display(results: List[Tuple[Any, ...]]) -> None:
        for row in results:
            print(row)

    def add(self, table: str, values: Dict[str, Any]) -> None:
        try:
            placeholders = ', '.join('?' * len(values))
            columns = ', '.join(values.keys())
            sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
            with connect_to_db(self.db_file) as cursor:
                cursor.execute(sql, tuple(values.values()))
        except sqlite3.Error as e:
            print(f"An error occurred while adding to {table}: {e}")

    def delete(self, table: str, record_id: int) -> None:
        try:
            sql = f'DELETE FROM {table} WHERE id = ?'
            with connect_to_db(self.db_file) as cursor:
                cursor.execute(sql, (record_id,))
        except sqlite3.Error as e:
            print(f"An error occurred while deleting from {table}: {e}")

    def edit(self, table: str, record_id: int, column: str, new_value: Any) -> None:
        try:
            sql = f'UPDATE {table} SET {column} = ? WHERE id = ?'
            with connect_to_db(self.db_file) as cursor:
                cursor.execute(sql, (new_value, record_id))
        except sqlite3.Error as e:
            print(f"An error occurred while editing {table}: {e}")

    def get_property(self, table: str, entry_id: int, property_name: str) -> Optional[str]:
        """Get a specific property for a meeting or contact by ID."""
        sql = f'SELECT {property_name} FROM {table} WHERE id = ?;'
        result = self.query(sql, (entry_id,))

        if result:
            return result[0][0]
        return None

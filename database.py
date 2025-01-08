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
    """Class to handle database operations."""

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.create_tables()

    def create_tables(self) -> None:
        """Create necessary tables in the database."""
        with connect_to_db(self.db_file) as cursor:
            cursor.executescript('''
            CREATE TABLE IF NOT EXISTS Meetings (
                id INTEGER PRIMARY KEY,
                meeting_name TEXT NOT NULL,
                day_of_week TEXT NOT NULL,
                time TEXT NOT NULL,
                zoom_link TEXT,
                zoom_meeting_id TEXT,
                zoom_passcode TEXT
            );
            CREATE TABLE IF NOT EXISTS Contacts (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone_number TEXT
            );
            CREATE TABLE IF NOT EXISTS Reminders (
                id INTEGER PRIMARY KEY,
                meeting_id INTEGER,
                reminder_day TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY (meeting_id) REFERENCES Meetings(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS Participants (
                meeting_id INTEGER,
                contact_id INTEGER,
                PRIMARY KEY (meeting_id, contact_id),
                FOREIGN KEY (meeting_id) REFERENCES Meetings(id) ON DELETE CASCADE,
                FOREIGN KEY (contact_id) REFERENCES Contacts(id) ON DELETE CASCADE
            );
            ''')

    def read(self, sql: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
        """Execute a read and return the results."""
        with connect_to_db(self.db_file) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    @staticmethod
    def display(results: List[Tuple[Any, ...]]) -> None:
        """Display read results in a user-friendly format."""
        for row in results:
            print(row)

    def create(self, table: str, values: Dict[str, Any]) -> None:
        """Insert a new record into the specified table."""
        placeholders = ', '.join('?' * len(values))
        columns = ', '.join(values.keys())
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        with connect_to_db(self.db_file) as cursor:
            cursor.execute(sql, tuple(values.values()))

    def delete(self, table: str, record_id: int) -> None:
        """Delete a record from the specified table."""
        sql = f'DELETE FROM {table} WHERE id = ?'
        with connect_to_db(self.db_file) as cursor:
            cursor.execute(sql, (record_id,))

    def update(self, table: str, record_id: int, column: str, new_value: Any) -> None:
        """Edit a specific field of a record in the specified table."""
        sql = f'UPDATE {table} SET {column} = ? WHERE id = ?'
        with connect_to_db(self.db_file) as cursor:
            cursor.execute(sql, (new_value, record_id))

    def get_property(self, table: str, entry_id: int, property_name: str) -> Optional[str]:
        """Retrieve a specific property of a record from a table."""
        sql = f'SELECT {property_name} FROM {table} WHERE id = ?;'
        result = self.read(sql, (entry_id,))
        return result[0][0] if result else None

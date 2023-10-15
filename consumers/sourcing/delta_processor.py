import sqlite3
from state import State

class DeltaProcessor:
    """Handles operations for determining data changes using an in-memory SQLite database."""

    def __init__(self, init_data):
        """Initializes the in-memory SQLite database and inserts the initial data."""

        self.conn = sqlite3.connect(':memory:')
        cursor = self.conn.cursor()

        self._init_table(cursor)

        for record in init_data:
            self._insert_data(record, cursor)

        self.conn.commit()
        cursor.close()

    def __del__(self):
        """Ensures the SQLite connection is closed upon object destruction."""

        self.conn.close()
        

    def _init_table(self, cursor):
        """Creates the `listings` table in the SQLite database if it doesn't exist."""

        cursor.execute('''
CREATE TABLE IF NOT EXISTS listings (
    url TEXT PRIMARY KEY,
    reference TEXT
)
''')

    def _insert_data(self, record, cursor):
        """Inserts a single record into the `listings` table."""

        cursor.execute('''
INSERT INTO listings (url, reference)
VALUES (:url, :reference)''', record)

    def insert_or_update(self, record):
        """Inserts a new record or updates an existing one in the `listings` table."""

        cursor = self.conn.cursor()
        try:
            cursor.execute('SELECT 1 FROM listings WHERE url = (:url)', record)
            result = cursor.fetchone()
            if result is None:
                self._insert_data(record, cursor)
                return State.INSERTED
            else:
                cursor.execute('UPDATE listings SET reference = (:reference) WHERE url = (:url)', record)
                return State.UPDATED
        except Exception as e:
            print(f'Error: {str(e)}')
            return State.ERROR
        finally:
            cursor.close()

    def remove_data(self, ids):
        """Removes records with the given ids from the `listings` table."""

        cursor = self.conn.cursor()
        try:
            placeholders = ', '.join(['?'] * len(ids))
            cursor.execute(f'DELETE FROM listings WHERE url IN ({placeholders})', ids)
        finally:
            cursor.close()

    def get_outdated_ids(self, reference):
        """Returns the ids of records that do not match the given reference."""

        cursor = self.conn.cursor()
        try:
            cursor.execute('SELECT url FROM listings WHERE reference != (?)', (reference,))
            result = cursor.fetchall()
            if not result:
                return []
            
            print('outdated:', len(result))
            return [x[0] for x in result]
        finally:
            cursor.close()

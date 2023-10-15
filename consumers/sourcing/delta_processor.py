import sqlite3
from state import State

class DeltaProcessor:
    def __init__(self, init_data):
        self.conn = sqlite3.connect(':memory:')
        cursor = self.conn.cursor()

        self._init_table(cursor)

        for record in init_data:
            self._insert_data(record, cursor)

        self.conn.commit()
        cursor.close()

    def __del__(self):
        self.conn.close()
        

    def _init_table(self, cursor):
        cursor.execute('''
CREATE TABLE IF NOT EXISTS listings (
    url TEXT PRIMARY KEY,
    reference TEXT
)
''')

    def _insert_data(self, record, cursor):
        cursor.execute('''
INSERT INTO listings (url, reference)
VALUES (:url, :reference)''', record)

    def insert_or_update(self, record):
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

    def get_outdated_ids(self, reference):
        cursor = self.conn.cursor()
        try:
            cursor.execute('SELECT url FROM listings WHERE reference != (?)', (reference,))
            result = cursor.fetchall()
            return [x[0] for x in result]
        finally:
            cursor.close()

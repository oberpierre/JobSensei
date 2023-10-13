import sqlite3

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
INSERT INTO listings (url)
VALUES (:url)''', record)

    def is_new(self, record):
        cursor = self.conn.cursor()
        try:
            cursor.execute('SELECT 1 FROM listings WHERE url = (:url)', record)
            result = cursor.fetchone()
            return result is None
        finally:
            cursor.close()

# sqlite_storage.py
import sqlite3
import time


class SQLiteStorage:
    def __init__(self):
        self.conn = sqlite3.connect('web_data.db')
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                url TEXT PRIMARY KEY,
                content TEXT,
                timestamp REAL
            )
        ''')

    def save_data(self, url, content):
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO pages 
                VALUES (?, ?, ?)
            ''', (url, content, time.time()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"存储失败: {str(e)}")
            return False


# 修改ES同步代码
def sync_from_sqlite(self):
    conn = sqlite3.connect('web_data.db')
    cursor = conn.cursor()
    for url, content, _ in cursor.execute('SELECT * FROM pages'):
        self.es.index(...)
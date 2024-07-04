import sqlite3
import os

class Database:
    def __init__(self, db_path="../Data/chat_app.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    avatar TEXT DEFAULT 'default_avatar.png'
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS friends (
                    user_id INTEGER,
                    friend_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (friend_id) REFERENCES users(id),
                    PRIMARY KEY (user_id, friend_id)
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER,
                    receiver_id INTEGER,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    type TEXT CHECK(type IN ('text', 'file', 'image', 'gif', 'emoji')),
                    FOREIGN KEY (sender_id) REFERENCES users(id),
                    FOREIGN KEY (receiver_id) REFERENCES users(id)
                )
            ''')

    def execute_query(self, query, params=()):
        with self.conn:
            cur = self.conn.execute(query, params)
            return cur.fetchall()

    def execute_non_query(self, query, params=()):
        with self.conn:
            self.conn.execute(query, params)


if __name__ == '__main__':
    database = Database()

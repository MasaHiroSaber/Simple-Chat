from database import Database
import sqlite3


class UserManager:
    def __init__(self):
        self.db = Database()

    def register_user(self, username, password, avatar='default_avatar.png'):
        try:
            self.db.execute_non_query('''
                INSERT INTO users (username, password, avatar)
                VALUES (?, ?, ?)
            ''', (username, password, avatar))
            return True, "Registration successful"
        except sqlite3.IntegrityError:
            return False, "Username already exists"

    def login_user(self, username, password):
        result = self.db.execute_query('''
            SELECT id FROM users WHERE username = ? AND password = ?
        ''', (username, password))
        if result:
            return True, "Login successful"
        else:
            return False, "Incorrect username or password"

    def update_avatar(self, username, avatar_path):
        self.db.execute_non_query('''
            UPDATE users SET avatar = ? WHERE username = ?
        ''', (avatar_path, username))
        return True, "Avatar updated successfully"

import logging

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

    def get_user_friends(self, username):
        query = '''
            SELECT u2.username, u2.avatar
            FROM users u1
            JOIN friends f ON u1.id = f.user_id
            JOIN users u2 ON f.friend_id = u2.id
            WHERE u1.username = ?
        '''
        result = self.db.execute_query(query, (username,))
        return True, result

    def get_all_users(self, username):
        query = '''
            SELECT id, username
            FROM users 
            WHERE username != ?
            ORDER BY id
        '''
        result = self.db.execute_query(query, (username,))
        return True, result

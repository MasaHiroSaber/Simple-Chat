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

    def send_friend_request(self, sender_username, receiver_username):
        sender_id = self.db.execute_query('SELECT id FROM users WHERE username = ?', (sender_username,))
        receiver_id = self.db.execute_query('SELECT id FROM users WHERE username = ?', (receiver_username,))
        if not sender_id or not receiver_id:
            return False, "User not found"

        # Check if there are any existing friend requests between the users
        existing_request = self.db.execute_query('''
            SELECT id FROM friend_requests
            WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
        ''', (sender_id[0][0], receiver_id[0][0], receiver_id[0][0], sender_id[0][0]))

        if existing_request:
            status = self.db.execute_query('''
                SELECT status FROM friend_requests
                WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ''', (sender_id[0][0], receiver_id[0][0], receiver_id[0][0], sender_id[0][0]))[0][0]
            if status in ['pending', 'accepted']:
                return False, "Friend request already exists or has been accepted"
            else:
                self.db.execute_non_query('''
                    UPDATE friend_requests SET status = 'pending', timestamp = datetime('now', 'localtime')
                    WHERE id = ?
                ''', (existing_request[0][0],))
                return True, "Friend request resent"

        try:
            self.db.execute_non_query('''
                INSERT INTO friend_requests (sender_id, receiver_id, timestamp)
                VALUES (?, ?, datetime('now', 'localtime'))
            ''', (sender_id[0][0], receiver_id[0][0]))
            return True, "Friend request sent"
        except sqlite3.IntegrityError:
            return False, "Unable to send friend request"

    def respond_friend_request(self, request_id, response):
        if response not in ['accepted', 'rejected']:
            return False, "Invalid response"

        self.db.execute_non_query('''
            UPDATE friend_requests SET status = ? WHERE id = ?
        ''', (response, request_id))

        if response == 'accepted':
            request = self.db.execute_query('SELECT sender_id, receiver_id FROM friend_requests WHERE id = ?',
                                            (request_id,))
            if request:
                sender_id, receiver_id = request[0]
                self.db.execute_non_query('''
                    INSERT INTO friends (user_id, friend_id) VALUES (?, ?)
                ''', (sender_id, receiver_id))
                self.db.execute_non_query('''
                    INSERT INTO friends (user_id, friend_id) VALUES (?, ?)
                ''', (receiver_id, sender_id))
        return True, "Friend request responded"

    def get_friend_requests(self, username):
        user_id = self.db.execute_query('SELECT id FROM users WHERE username = ?', (username,))
        if not user_id:
            return False, "User not found"
        user_id = user_id[0][0]

        query = '''
            SELECT fr.id, u.username, fr.status, fr.timestamp
            FROM friend_requests fr
            JOIN users u ON fr.sender_id = u.id
            WHERE fr.receiver_id = ? AND fr.status = 'pending'
        '''
        result = self.db.execute_query(query, (user_id,))
        return True, result

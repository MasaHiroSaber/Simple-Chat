from database import Database
class ChatManager:
    def __init__(self):
        self.db = Database()

    def send_message(self, sender_id, receiver_id, message, msg_type='text'):
        self.db.execute_non_query('''
            INSERT INTO messages (sender_id, receiver_id, message, type)
            VALUES (?, ?, ?, ?)
        ''', (sender_id, receiver_id, message, msg_type))
        return True, "Message sent successfully"

    def get_messages(self, user1_id, user2_id):
        return self.db.execute_query('''
            SELECT * FROM messages
            WHERE (sender_id = ? AND receiver_id = ?)
               OR (sender_id = ? AND receiver_id = ?)
            ORDER BY timestamp
        ''', (user1_id, user2_id, user2_id, user1_id))

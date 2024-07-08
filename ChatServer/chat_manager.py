import logging

from database import Database


class ChatManager:
    def __init__(self):
        self.db = Database()

    # 接收到消息后，将消息存入数据库
    def send_message(self, sender_id, receiver_id, message, msg_type='text'):
        if message:
            self.db.execute_non_query('''
                INSERT INTO messages (sender_id, receiver_id, message, type)
                VALUES (?, ?, ?, ?)
            ''', (sender_id, receiver_id, message, msg_type))
            return True, "Message sent successfully"
        else:
            return False, "No message to send"

    # 获取指定用户之间的聊天记录
    def get_messages(self, user1_name, user2_name):
        result = self.db.execute_query('''
            SELECT sender_id, receiver_id, message FROM messages
            WHERE (sender_id = ? AND receiver_id = ?)
               OR (sender_id = ? AND receiver_id = ?)
            ORDER BY timestamp DESC
            LIMIT 50
        ''', (user1_name, user2_name, user2_name, user1_name))
        if result:
            return True, result
        else:
            return False, "No messages found"

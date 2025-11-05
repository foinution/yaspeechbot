import sqlite3
import logging
from config import LOGS, DB_FILE

logging.basicConfig(filename=LOGS, level=logging.INFO,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

def create_database():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT,
                total_gpt_tokens INTEGER,
                tts_symbols INTEGER,
                stt_blocks INTEGER)
            ''')
            logging.info('База данных создана')
    except Exception as e:
        logging.error(e)

def add_messages(user_id, full_message):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            message, total_gpt_tokens, tts_symbols, stt_blocks = full_message
            cursor.execute('''
                INSERT INTO messages (user_id, message, total_gpt_tokens, tts_symbols, stt_blocks)
                VALUES (?, ?, ?, ?, ?)''', (user_id, message, total_gpt_tokens, tts_symbols, stt_blocks))
            conn.commit()
            logging.info('Добавлена запись')
    except Exception as e:
        logging.error(e)

def select_last_messages(user_id, last_messages=4):
    messages = []
    total_spent_token = 0
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT message, total_gpt_tokens 
                FROM messages
                WHERE user_id=?
                ORDER BY id DESC LIMIT ?''',
            (user_id, last_messages))
            data = cursor.fetchall()
            if data and data[0]:
                for message in reversed(data):
                    messages.append({'text': message[0]})
                    total_spent_token = max(total_spent_token, message[2])
            return messages, total_spent_token
    except Exception as e:
        logging.error(e)
        return messages, total_spent_token

def count_all_limits(user_id, limit_type):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
            SELECT SUM({limit_type})
                FROM messages
                WHERE user_id = ?''',
                           (user_id,))
            data = cursor.fetchall()
            if data and data[0]:
                return data[0]
            else:
                return 0
    except Exception as e:
        logging.error(e)
        return 0

def count_users(user_id):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT COUNT(DISTINCT user_id) 
                FROM messages 
                WHERE user_id <> ?''', (user_id,))
            data = cursor.fetchone()[0]
            return data
    except Exception as e:
        logging.error(e)
        return None
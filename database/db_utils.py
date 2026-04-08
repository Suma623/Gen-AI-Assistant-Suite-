import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_user(username, email, password_hash):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
                       (username, email, password_hash))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id
    except sqlite3.IntegrityError:
        return False, "Username or Email already exists."
    except Exception as e:
        return False, str(e)

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, password_hash, display_name, profile_image_path FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
            "display_name": row[4],
        }
    return None

def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, password_hash, display_name, profile_image_path FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
            "display_name": row[4],
            "profile_image_path": row[5]
        }
    return None

def update_user_profile(user_id, display_name=None, profile_image_path=None):
    conn = get_connection()
    cursor = conn.cursor()
    if display_name:
        cursor.execute("UPDATE users SET display_name = ? WHERE id = ?", (display_name, user_id))
    if profile_image_path:
        cursor.execute("UPDATE users SET profile_image_path = ? WHERE id = ?", (profile_image_path, user_id))
    conn.commit()
    conn.close()

def save_chat(user_id, domain, query, response, file_context=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, domain, query, response, file_context) VALUES (?, ?, ?, ?, ?)",
                   (user_id, domain, query, response, file_context))
    conn.commit()
    chat_id = cursor.lastrowid
    conn.close()
    return chat_id

def get_user_chat_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, domain, query, response, file_context, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "domain": r[1], "query": r[2], "response": r[3], "file_context": r[4], "timestamp": r[5]} for r in rows]

def bookmark_chat(user_id, chat_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookmarks (user_id, chat_id) VALUES (?, ?)", (user_id, chat_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def get_user_bookmarks(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id, c.domain, c.query, c.response, b.saved_at
        FROM bookmarks b
        JOIN chat_history c ON b.chat_id = c.id
        WHERE b.user_id = ?
        ORDER BY b.saved_at DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"chat_id": r[0], "domain": r[1], "query": r[2], "response": r[3], "saved_at": r[4]} for r in rows]

def save_feedback(user_id, chat_id, is_helpful, feedback_text):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (user_id, chat_id, is_helpful, feedback_text) VALUES (?, ?, ?, ?)",
                   (user_id, chat_id, is_helpful, feedback_text))
    conn.commit()
    conn.close()

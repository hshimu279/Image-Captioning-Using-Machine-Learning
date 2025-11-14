import sqlite3
from sqlite3 import Connection
from typing import Optional
import hashlib

DB_PATH = "users_data.db"

def get_db_connection() -> Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS captions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            image_path TEXT,
            caption TEXT,
            analysis TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username: str, password: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?,?)', (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_user(username: str, password: str) -> Optional[int]:
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute('SELECT id FROM users WHERE username=? AND password_hash=?', (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def save_caption(user_id: int, image_path: str, caption: str, analysis: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO captions (user_id, image_path, caption, analysis)
        VALUES (?, ?, ?, ?)
    ''', (user_id, image_path, caption, analysis))
    conn.commit()
    conn.close()

def get_user_captions(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT image_path, caption, analysis FROM captions WHERE user_id=?', (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data

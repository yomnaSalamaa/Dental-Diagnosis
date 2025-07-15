import sqlite3
import os

def init_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/diagnosis.db")
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

    # Create diagnosis logs table
    c.execute('''CREATE TABLE IF NOT EXISTS diagnosis_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    input_image TEXT,
                    output_image TEXT,
                    model_used TEXT
                )''')

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("database/diagnosis.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def check_user(username, password):
    conn = sqlite3.connect("database/diagnosis.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result

def log_image(username, input_path, output_path, model_used):
    conn = sqlite3.connect("database/diagnosis.db")
    c = conn.cursor()
    c.execute("INSERT INTO diagnosis_logs (username, input_image, output_image, model_used) VALUES (?, ?, ?, ?)",
              (username, input_path, output_path, model_used))
    conn.commit()
    conn.close()
    
def get_user_logs(username):
    conn = sqlite3.connect("database/diagnosis.db")
    c = conn.cursor()
    c.execute("SELECT input_image, output_image, model_used FROM diagnosis_logs WHERE username=?", (username,))
    results = c.fetchall()
    conn.close()
    return results


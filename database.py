import sqlite3

DB_NAME = "saiyan_origin.db"

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS custom_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT NOT NULL,
        penalty_type TEXT NOT NULL,
        penalty_duration INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

def add_rule(keyword, penalty_type, penalty_duration):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO custom_rules (keyword, penalty_type, penalty_duration) VALUES (?, ?, ?)",
                   (keyword, penalty_type, penalty_duration))
    conn.commit()
    conn.close()

def get_all_rules():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, keyword, penalty_type, penalty_duration FROM custom_rules")
    rules = cursor.fetchall()
    conn.close()
    return rules

def delete_rule(rule_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM custom_rules WHERE id = ?", (rule_id,))
    conn.commit()
    conn.close()

import sqlite3
from datetime import datetime
from config import DB_PATH

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY, type TEXT, description TEXT, points INTEGER, is_done INTEGER DEFAULT 0, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS points (id INTEGER PRIMARY KEY, amount INTEGER, date TEXT)''')
    conn.commit()
    conn.close()

def get_all_completion_dates():
    conn = get_conn()
    res = conn.execute("SELECT DISTINCT date FROM points").fetchall()
    conn.close()
    return [r['date'] for r in res]

def get_total_points():
    conn = get_conn()
    res = conn.execute("SELECT SUM(amount) as total FROM points").fetchone()
    conn.close()
    return res['total'] or 0

def get_points_today(date=None):
    if not date: date = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    res = conn.execute("SELECT SUM(amount) as total FROM points WHERE date=?", (date,)).fetchone()
    conn.close()
    return res['total'] or 0

def get_goals_for_date(date=None):
    if not date: date = datetime.now().strftime("%Y-%m-%d")
    conn = get_conn()
    goals = conn.execute("SELECT * FROM goals WHERE date=?", (date,)).fetchall()
    conn.close()
    return [dict(g) for g in goals]

def add_goal(goal_type, description, points):
    conn = get_conn()
    date = datetime.now().strftime("%Y-%m-%d")
    conn.execute("INSERT INTO goals (type, description, points, date) VALUES (?,?,?,?)", (goal_type, description, points, date))
    conn.commit()
    conn.close()

def toggle_goal(goal_id, is_done):
    conn = get_conn()
    conn.execute("UPDATE goals SET is_done=? WHERE id=?", (int(is_done), goal_id))
    if is_done:
        goal = conn.execute("SELECT points FROM goals WHERE id=?", (goal_id,)).fetchone()
        if goal:
            date = datetime.now().strftime("%Y-%m-%d")
            conn.execute("INSERT INTO points (amount, date) VALUES (?,?)", (goal['points'], date))
    conn.commit()
    conn.close()

import sqlite3

conn = sqlite3.connect("fitness.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS progress(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    biceps REAL,
    chest REAL,
    waist REAL,
    weight REAL
)
""")

conn.commit()
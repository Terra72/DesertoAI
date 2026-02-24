from config import DB_PATH
import sqlite3

def init_db():
    print("INIT DB PATH:", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id TEXT,
        title TEXT,
        region TEXT,
        topic TEXT,
        semantic_score REAL,
        rule_score REAL,
        final_score REAL,
        summary TEXT,
        confidence_delta REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()
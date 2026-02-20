import sqlite3
from pathlib import Path

DB_PATH = Path("memory/desertification.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        source_id TEXT,
        source_title TEXT,
        region TEXT,
        topic TEXT,
        signal_type TEXT,
        impact_direction TEXT,
        confidence_delta REAL,
        summary TEXT
    )
    """)

    conn.commit()
    conn.close()
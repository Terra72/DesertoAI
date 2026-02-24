import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        source_id TEXT NOT NULL,
        title TEXT NOT NULL,
        url TEXT,

        region TEXT NOT NULL,
        subregion TEXT,
        country TEXT,

        topic TEXT NOT NULL,
        signal_type TEXT NOT NULL,
        impact_direction TEXT NOT NULL,

        semantic_score REAL,
        rule_score REAL,
        final_score REAL,

        summary TEXT NOT NULL,

        confidence_delta REAL,

        published_at TEXT,
        ingested_at TEXT NOT NULL
    )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_region ON events(region)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_signal ON events(signal_type)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON events(ingested_at)")
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_source ON events(source_id)")

    conn.commit()
    conn.close()

    print("Database initialized.")
import sqlite3
from dataclasses import dataclass
from datetime import datetime, UTC
from config import DB_PATH


@dataclass
class Event:
    source_id: str
    title: str
    region: str
    topic: str
    semantic_score: float
    rule_score: float
    final_score: float
    summary: str
    confidence_delta: float
    timestamp: str | None = None

    def save(self):
        if not self.timestamp:
            self.timestamp = datetime.now(UTC).isoformat()

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO events (
            source_id,
            title,
            region,
            topic,
            semantic_score,
            rule_score,
            final_score,
            summary,
            confidence_delta,
            timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.source_id,
            self.title,
            self.region,
            self.topic,
            self.semantic_score,
            self.rule_score,
            self.final_score,
            self.summary,
            self.confidence_delta,
            self.timestamp
        ))

        conn.commit()
        conn.close()
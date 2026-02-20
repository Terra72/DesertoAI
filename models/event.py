# models/event.py

from dataclasses import dataclass
from datetime import datetime, UTC
import sqlite3


@dataclass
class Event:
    source_id: str
    title: str
    region: str
    topic: str
    category: str
    impact: str
    confidence: float
    summary: str
    timestamp: str | None = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(UTC).isoformat()

    def save(self, conn: sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO events (
                timestamp,
                source_id,
                title,
                region,
                topic,
                category,
                impact,
                confidence,
                summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.timestamp,
            self.source_id,
            self.title,
            self.region,
            self.topic,
            self.category,
            self.impact,
            self.confidence,
            self.summary
        ))
        conn.commit()
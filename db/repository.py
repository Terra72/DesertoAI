import sqlite3
from config import DB_PATH
from models.event import Event

class EventRepository:

    def __init__(self):
        self.db_path = DB_PATH

    def save(self, event: Event):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("""
            INSERT OR IGNORE INTO events (
                source_id, title, url,
                region, subregion, country,
                topic, signal_type, impact_direction,
                semantic_score, rule_score, final_score,
                summary, confidence_delta,
                published_at, ingested_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.source_id,
            event.title,
            event.url,
            event.region,
            event.subregion,
            event.country,
            event.topic,
            event.signal_type,
            event.impact_direction,
            event.semantic_score,
            event.rule_score,
            event.final_score,
            event.summary,
            event.confidence_delta,
            event.published_at,
            event.ingested_at
        ))

        conn.commit()
        conn.close()
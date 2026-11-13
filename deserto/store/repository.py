import sqlite3
from deserto.config import DB_PATH
from deserto.models import Event
from eval.taxonomy import PARENTS, REGIONS

class EventRepository:

    def __init__(self):
        self.db_path = DB_PATH

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def save(self, event: Event):
        conn = self._connect()
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


    def get_latest_by_region(self, region: str):
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT title, summary, signal_type, impact_direction, ingested_at
            FROM events
            WHERE region = ?
            ORDER BY ingested_at DESC
            LIMIT 1
        """, (region,))

        row = cur.fetchone()
        conn.close()
        return row

    def get_events(self, region=None, topic=None, signal_type=None, limit=50):
        """Newest first. A parent region also matches events stored under its leaves."""
        where, params = [], []
        if region is not None:
            regions = [region] + PARENTS.get(region, [])
            where.append(f"region IN ({', '.join('?' * len(regions))})")
            params += regions
        if topic is not None:
            where.append("topic = ?")
            params.append(topic)
        if signal_type is not None:
            where.append("signal_type = ?")
            params.append(signal_type)

        sql = """
            SELECT title, summary, url, topic, region, signal_type,
                   impact_direction, published_at, ingested_at
            FROM events
        """
        if where:
            sql += "WHERE " + " AND ".join(where) + " "
        sql += "ORDER BY ingested_at DESC, id DESC LIMIT ?"

        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql, params + [limit])
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def count_by_region(self):
        """Event count for every taxonomy region. A parent counts its leaves too."""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT region, COUNT(*) FROM events GROUP BY region")
        counts = dict(cur.fetchall())
        conn.close()

        return {
            r: sum(counts.get(x, 0) for x in [r] + PARENTS.get(r, []))
            for r in REGIONS
        }
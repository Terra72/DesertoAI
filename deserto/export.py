import json
import sqlite3
from datetime import datetime, UTC

from deserto.config import DB_PATH, EXPORT_DIR

# Every events column except the local id
COLUMNS = [
    "source_id", "title", "url", "region", "subregion", "country",
    "topic", "signal_type", "impact_direction",
    "semantic_score", "rule_score", "final_score",
    "summary", "confidence_delta", "published_at", "ingested_at",
]


def export_path(out_dir=EXPORT_DIR, now=None):
    year, week, _ = (now or datetime.now(UTC)).isocalendar()
    return out_dir / f"events-{year}-W{week:02d}.jsonl"


def exported_ids(out_dir=EXPORT_DIR):
    """source_ids already present in any export."""
    ids = set()
    for path in out_dir.glob("events-*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                ids.add(json.loads(line)["source_id"])
    return ids


def write_export(db_path=DB_PATH, out_dir=EXPORT_DIR, now=None):
    """Append events not yet exported to this week's file. Returns (path, count)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    done = exported_ids(out_dir)

    conn = sqlite3.connect(db_path)
    rows = conn.execute(f"SELECT {', '.join(COLUMNS)} FROM events ORDER BY id").fetchall()
    conn.close()

    new = [dict(zip(COLUMNS, r)) for r in rows if r[0] not in done]
    path = export_path(out_dir, now)
    if new:
        with path.open("a", encoding="utf-8") as f:
            for event in new:
                f.write(json.dumps(event) + "\n")
    return path, len(new)

"""Load the labelled eval set into the DB as a fixture, so a fresh clone works offline."""
from datetime import datetime, UTC

from deserto.evaluate import load_rows
from deserto.models import Event
from deserto.store.repository import EventRepository
from deserto.store.schema import init_db


def load_fixture(repo, rows=None):
    """Save every relevant eval row as an event. Returns the count."""
    rows = load_rows() if rows is None else rows
    now = datetime.now(UTC).isoformat()
    n = 0
    for r in rows:
        if not r.get("relevant", True):
            continue
        repo.save(Event(
            source_id=r["id"], title=r["title"], url=r.get("link"),
            region=r["region"], subregion=None, country=None, topic=r["topic"],
            signal_type="new", impact_direction="neutral",
            semantic_score=0.0, rule_score=0.0, final_score=0.0,
            summary=r.get("summary") or r["title"], confidence_delta=0.1,
            published_at=None, ingested_at=now,
        ))
        n += 1
    return n


if __name__ == "__main__":
    init_db()
    print(f"Loaded {load_fixture(EventRepository())} fixture events")

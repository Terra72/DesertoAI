import json
from datetime import datetime, UTC

from deserto.export import exported_ids, export_path, write_export
from deserto.models import Event


def make_event(source_id):
    return Event(
        source_id=source_id, title="t" + source_id, url="http://x",
        region="africa", subregion=None, country=None, topic="water",
        signal_type="new", impact_direction="neutral",
        semantic_score=0.5, rule_score=0.1, final_score=0.6,
        summary="s", confidence_delta=0.25,
        published_at=None, ingested_at="2026-11-30T00:00:00+00:00",
    )


NOW = datetime(2026, 11, 30, tzinfo=UTC)


def test_export_path_uses_iso_week(tmp_path):
    assert export_path(tmp_path, NOW).name == "events-2026-W49.jsonl"


def test_writes_events_without_local_id(db, repo, tmp_path):
    repo.save(make_event("a"))
    path, count = write_export(db, tmp_path, NOW)
    assert count == 1
    row = json.loads(path.read_text().splitlines()[0])
    assert row["source_id"] == "a"
    assert "id" not in row


def test_second_export_adds_only_new_events(db, repo, tmp_path):
    repo.save(make_event("a"))
    write_export(db, tmp_path, NOW)
    repo.save(make_event("b"))
    path, count = write_export(db, tmp_path, NOW)
    assert count == 1
    assert exported_ids(tmp_path) == {"a", "b"}
    assert len(path.read_text().splitlines()) == 2


def test_nothing_new_writes_no_file(db, tmp_path):
    path, count = write_export(db, tmp_path, NOW)
    assert count == 0
    assert not path.exists()

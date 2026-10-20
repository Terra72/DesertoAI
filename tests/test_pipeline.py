import sqlite3

from deserto.pipeline import Pipeline


def run_pipeline(state, repo, embed, items, summarize=None, **kw):
    summarize = summarize or (lambda item, cur: {"novel": True, "update": "u:" + item["title"]})
    p = Pipeline(state, lambda: items, embed, summarize, repo, **kw)
    p.run()
    return p


RELEVANT = {
    "id": "r1",
    "title": "Desertification in the Sahel",
    "summary": "dryland restoration policy",
    "source": "FAO",
    "link": "http://x",
}
IRRELEVANT = {"id": "i1", "title": "Coffee shop", "summary": "", "source": "Blog"}


def count(db):
    return sqlite3.connect(db).execute("select count(*) from events").fetchone()[0]


def test_relevant_item_becomes_event_irrelevant_ignored(db, repo, embed, fresh_state):
    run_pipeline(fresh_state, repo, embed, [RELEVANT, IRRELEVANT])
    assert count(db) == 1
    assert "u:Desertification in the Sahel" in fresh_state["global_summary"]
    assert set(fresh_state["sources_seen"]) == {"r1", "i1"}


def test_seen_items_skipped_unless_force(db, repo, embed, fresh_state):
    fresh_state["sources_seen"] = ["r1"]
    run_pipeline(fresh_state, repo, embed, [RELEVANT])
    assert count(db) == 0
    run_pipeline(fresh_state, repo, embed, [RELEVANT], force=True)
    assert count(db) == 1


def test_dry_run_writes_nothing(db, repo, embed, fresh_state):
    run_pipeline(fresh_state, repo, embed, [RELEVANT], dry_run=True)
    assert count(db) == 0
    assert fresh_state["sources_seen"] == []
    assert fresh_state["last_run"] is None


def test_non_novel_item_is_reinforcement(db, repo, embed, fresh_state):
    run_pipeline(fresh_state, repo, embed, [RELEVANT],
                 summarize=lambda i, c: {"novel": False, "update": ""})
    row = sqlite3.connect(db).execute("select signal_type from events").fetchone()
    assert row[0] == "reinforcement"


def test_region_state_accumulates_confidence(db, repo, embed, fresh_state):
    run_pipeline(fresh_state, repo, embed, [RELEVANT])
    (region_data,) = [r for r in fresh_state["regions"].values()]
    assert region_data["confidence"] == 0.25  # FAO

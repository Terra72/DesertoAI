from deserto.models import Event


def make_event(**kw):
    base = dict(
        source_id="a1", title="T", url="http://x", region="africa", subregion=None,
        country=None, topic="soil", signal_type="new", impact_direction="neutral",
        semantic_score=0.5, rule_score=0.5, final_score=1.0, summary="S",
        confidence_delta=0.1, published_at=None, ingested_at="2026-01-01T00:00:00+00:00",
    )
    base.update(kw)
    return Event(**base)


def test_save_and_get_latest_by_region(repo):
    repo.save(make_event(source_id="a", title="old", ingested_at="2026-01-01"))
    repo.save(make_event(source_id="b", title="new", ingested_at="2026-02-01"))
    row = repo.get_latest_by_region("africa")
    assert row[0] == "new"


def test_duplicate_source_id_is_ignored(repo):
    repo.save(make_event(title="first"))
    repo.save(make_event(title="second"))
    assert repo.get_latest_by_region("africa")[0] == "first"


def test_unknown_region_returns_none(repo):
    assert repo.get_latest_by_region("nowhere") is None


def test_get_events_fields_and_newest_first(repo):
    repo.save(make_event(source_id="a", title="old", ingested_at="2026-01-01"))
    repo.save(make_event(source_id="b", title="new", ingested_at="2026-02-01"))
    events = repo.get_events()
    assert [e["title"] for e in events] == ["new", "old"]
    assert set(events[0]) == {
        "title", "summary", "url", "topic", "region", "signal_type",
        "impact_direction", "published_at", "ingested_at",
    }


def test_get_events_parent_includes_leaves(repo):
    repo.save(make_event(source_id="a", region="sahel-west-africa"))
    repo.save(make_event(source_id="b", region="mena"))
    repo.save(make_event(source_id="c", region="africa"))
    repo.save(make_event(source_id="d", region="europe"))
    assert len(repo.get_events(region="africa")) == 3
    # a leaf under two parents shows up under both
    assert [e["region"] for e in repo.get_events(region="middle-east")] == ["mena"]


def test_get_events_leaf_excludes_parent_and_siblings(repo):
    repo.save(make_event(source_id="a", region="sahel-west-africa"))
    repo.save(make_event(source_id="b", region="africa"))
    repo.save(make_event(source_id="c", region="horn-east-africa"))
    events = repo.get_events(region="sahel-west-africa")
    assert [e["region"] for e in events] == ["sahel-west-africa"]


def test_get_events_filters_combine(repo):
    repo.save(make_event(source_id="a", region="mena", topic="water", signal_type="new"))
    repo.save(make_event(source_id="b", region="mena", topic="water", signal_type="reinforcement"))
    repo.save(make_event(source_id="c", region="mena", topic="soil", signal_type="new"))
    repo.save(make_event(source_id="d", region="europe", topic="water", signal_type="new"))
    assert len(repo.get_events(topic="water")) == 3
    assert len(repo.get_events(signal_type="new")) == 3
    assert len(repo.get_events(region="africa", topic="water", signal_type="new")) == 1


def test_get_events_limit(repo):
    for i in range(5):
        repo.save(make_event(source_id=str(i)))
    assert len(repo.get_events(limit=2)) == 2


def test_get_events_unknown_region_is_empty(repo):
    repo.save(make_event())
    assert repo.get_events(region="nowhere") == []


def test_count_by_region_parent_includes_leaves(repo):
    repo.save(make_event(source_id="a", region="sahel-west-africa"))
    repo.save(make_event(source_id="b", region="mena"))
    repo.save(make_event(source_id="c", region="africa"))
    counts = repo.count_by_region()
    assert counts["sahel-west-africa"] == 1
    assert counts["mena"] == 1
    assert counts["africa"] == 3
    assert counts["middle-east"] == 1
    assert counts["europe"] == 0

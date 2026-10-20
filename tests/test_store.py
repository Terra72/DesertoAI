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

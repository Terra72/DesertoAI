from deserto.fixture import load_fixture


def test_fixture_loads_relevant_rows_only(repo):
    rows = [
        {"id": "1", "title": "A", "source": "x", "region": "africa", "topic": "soil"},
        {"id": "2", "title": "B", "source": "x", "relevant": False},
    ]
    assert load_fixture(repo, rows) == 1
    assert repo.get_latest_by_region("africa")[0] == "A"


def test_fixture_from_real_eval_set(repo):
    assert load_fixture(repo) > 0

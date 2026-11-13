import pytest

import app as app_module
from deserto.fixture import load_fixture


@pytest.fixture
def client(repo, monkeypatch):
    monkeypatch.setattr(app_module, "repo", repo)
    return app_module.app.test_client()


@pytest.fixture
def loaded(repo):
    load_fixture(repo, [
        {"id": "1", "title": "Sahel", "region": "sahel-west-africa", "topic": "fmnr"},
        {"id": "2", "title": "Horn", "region": "horn-east-africa", "topic": "water"},
        {"id": "3", "title": "Spain", "region": "mediterranean-southern-europe", "topic": "water"},
    ])


def test_events_parent_returns_leaf_events(client, loaded):
    data = client.get("/api/events?region=africa").get_json()
    assert sorted(e["title"] for e in data) == ["Horn", "Sahel"]


def test_events_fields(client, loaded):
    event = client.get("/api/events?region=europe").get_json()[0]
    assert event["title"] == "Spain"
    assert event["region"] == "mediterranean-southern-europe"
    assert set(event) == {
        "title", "summary", "url", "topic", "region", "signal_type",
        "impact_direction", "published_at", "ingested_at",
    }


def test_events_filters(client, loaded):
    data = client.get("/api/events?region=africa&topic=water&signal_type=new").get_json()
    assert [e["title"] for e in data] == ["Horn"]


def test_events_limit(client, loaded):
    assert len(client.get("/api/events?limit=1").get_json()) == 1


def test_events_limit_is_capped(client, loaded, monkeypatch):
    monkeypatch.setattr(app_module, "MAX_LIMIT", 2)
    assert len(client.get("/api/events?limit=1000").get_json()) == 2


def test_events_empty_db_returns_empty_list(client):
    resp = client.get("/api/events")
    assert resp.status_code == 200
    assert resp.get_json() == []


@pytest.mark.parametrize("query", [
    "region=nowhere", "topic=cheese", "signal_type=loud", "region=",
])
def test_events_unknown_filter_is_400(client, query):
    resp = client.get(f"/api/events?{query}")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


@pytest.mark.parametrize("limit", ["abc", "0", "-5", ""])
def test_events_bad_limit_is_400(client, limit):
    assert client.get(f"/api/events?limit={limit}").status_code == 400


def test_regions_counts(client, loaded):
    counts = client.get("/api/regions").get_json()
    assert counts["sahel-west-africa"] == 1
    assert counts["africa"] == 2
    assert counts["europe"] == 1
    assert counts["australia"] == 0


def test_region_route_unchanged(client, loaded):
    resp = client.get("/region/sahel-west-africa")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Sahel"
    # exact match only: the parent has no events stored under it
    assert client.get("/region/africa").status_code == 404

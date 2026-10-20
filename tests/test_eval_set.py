import json
from pathlib import Path

import pytest

EVAL = Path(__file__).resolve().parent.parent / "eval" / "eval_set.jsonl"

REGIONS = {
    "sahel-west-africa", "horn-east-africa", "southern-africa",
    "mediterranean-southern-europe", "mena", "central-asia", "south-east-asia",
    "australia", "americas-drylands", "global", "multi-region",
}
TOPICS = {"fmnr", "agroforestry", "water", "soil", "policy", "funding", "technology", "ecosystem"}


def rows():
    return [json.loads(l) for l in EVAL.read_text(encoding="utf-8").splitlines() if l.strip()]


def test_eval_rows_are_valid():
    data = rows()
    if not data:
        pytest.skip("eval set not labelled yet")
    ids = [r["id"] for r in data]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for r in data:
        for key in ("id", "title", "source"):
            assert r.get(key), f"{r.get('id')}: missing {key}"
        if r.get("relevant", True):
            assert r.get("region") in REGIONS, f"{r['id']}: bad region {r.get('region')}"
            assert r.get("topic") in TOPICS, f"{r['id']}: bad topic {r.get('topic')}"

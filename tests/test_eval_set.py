import json
from pathlib import Path

import pytest

from eval.taxonomy import PARENTS, REGIONS, TOPICS, region_correct

EVAL = Path(__file__).resolve().parent.parent / "eval" / "eval_set.jsonl"



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


def test_parent_regions_cover_their_children_only():
    assert region_correct("sahel-west-africa", "africa")
    assert region_correct("horn-east-africa", "horn-east-africa")
    assert not region_correct("africa", "sahel-west-africa")
    assert region_correct("mena", "africa") and region_correct("mena", "middle-east")
    assert region_correct("americas-drylands", "north-america")
    assert region_correct("americas-drylands", "south-america")
    assert not region_correct("australia", "east-asia")
    assert all(c in REGIONS for kids in PARENTS.values() for c in kids)

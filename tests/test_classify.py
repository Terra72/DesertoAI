import numpy as np

from deserto.classify.confidence import confidence_delta
from deserto.classify.region_semantic import detect_region_semantic, init_region_vectors
from deserto.classify.topic_semantic import detect_topic_semantic, ensure_topic_vectors


def unit(i, dim=32):
    v = np.zeros(dim)
    v[i] = 1.0
    return v


def test_confidence_by_source():
    assert confidence_delta("Journal of Soil") == 0.2
    assert confidence_delta("FAO") == 0.25
    assert confidence_delta("Random") == 0.1


def test_region_picks_closest_vector():
    state = {"region_vectors": {"africa": unit(0).tolist(), "asia": unit(1).tolist()}}
    region, score = detect_region_semantic("t", state, embed=lambda _t: unit(1))
    assert (region, round(score, 2)) == ("asia", 1.0)


def test_region_below_threshold_falls_back_to_global():
    state = {"region_vectors": {"africa": unit(0).tolist()}}
    region, _ = detect_region_semantic("t", state, embed=lambda _t: unit(5))
    assert region == "global"


def test_topic_below_threshold_is_unknown():
    state = {"topic_vectors": {"soil": unit(0).tolist()}}
    topic, _ = detect_topic_semantic("t", state, embed=lambda _t: unit(5))
    assert topic == "unknown"


def test_vector_init_is_idempotent(embed):
    state = {}
    init_region_vectors(state, embed)
    ensure_topic_vectors(state, embed)
    before = dict(state["region_vectors"])
    calls = []
    init_region_vectors(state, lambda t: calls.append(t))
    assert calls == [] and state["region_vectors"].keys() == before.keys()

from deserto.evaluate import evaluate, load_rows, passes


def test_metrics_on_tiny_set(embed):
    rows = [
        {"id": "1", "title": "Sahel FMNR", "source": "x", "region": "sahel-west-africa", "topic": "fmnr"},
        {"id": "2", "title": "Coffee shop opens", "source": "x", "relevant": False},
    ]
    m = evaluate(rows, embed)
    assert m["rows"] == 2 and m["relevant_rows"] == 1
    assert m["has_region"] == 1.0
    assert m["relevance"] == 0.5  # irrelevant row ignored; relevant one scores 0 on rules
    assert not passes(m)


def test_real_eval_set_loads():
    assert load_rows()

from deserto.relevance import decide, score


def item(title="", summary="", source="Blog"):
    return {"title": title, "summary": summary, "source": source}


def test_irrelevant_item_scores_zero():
    assert score(item("New coffee shop opens in Nairobi", "Local business news.")) == 0.0


def test_strong_keyword_adds_half_point():
    assert score(item("Desertification advances")) == 0.5


def test_trusted_source_adds_boost_and_institutional_boost():
    # trusted (0.4) + institutional (0.5)
    assert score(item("x", source="FAO News")) == 0.9


def test_research_source_boost():
    assert score(item("x", source="Journal of Arid Environments")) == 0.3


def test_decide_threshold():
    assert decide(item("desertification")) == "ignore"  # 0.5 < 0.6
    assert decide(item("desertification", "dryland")) == "consider"

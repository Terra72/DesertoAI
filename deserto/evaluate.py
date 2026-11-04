"""Score the classifier against the hand-labelled eval set (ADR-0001 bar)."""
import json
from pathlib import Path

from deserto.classify.region_semantic import detect_region_semantic, init_region_vectors
from deserto.classify.topic_semantic import detect_topic_semantic, ensure_topic_vectors
from deserto.relevance import decide
from eval.taxonomy import region_correct

EVAL_PATH = Path(__file__).resolve().parent.parent / "eval" / "eval_set.jsonl"
BAR = {"region": 0.85, "topic": 0.80, "has_region": 1.0}


def load_rows(path=EVAL_PATH):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return [json.loads(l) for l in lines if l.strip()]


def evaluate(rows, embed, state=None):
    """Return metrics. Region and topic are scored on relevant rows only."""
    state = state if state is not None else {}
    init_region_vectors(state, embed)
    ensure_topic_vectors(state, embed)

    region_ok = topic_ok = has_region = n = rel_ok = 0
    for r in rows:
        relevant = r.get("relevant", True)
        item = {"title": r["title"], "summary": r.get("summary", ""), "source": r["source"]}
        rel_ok += (decide(item) == "consider") == relevant
        if not relevant:
            continue
        text = f"{r['title']} {r.get('summary', '')}"
        region, _ = detect_region_semantic(text, state, embed)
        topic, _ = detect_topic_semantic(text, state, embed)
        n += 1
        has_region += bool(region)
        region_ok += region_correct(region, r["region"])
        topic_ok += topic == r["topic"]

    div = lambda a, b: a / b if b else 0.0
    return {
        "rows": len(rows),
        "relevant_rows": n,
        "relevance": div(rel_ok, len(rows)),
        "region": div(region_ok, n),
        "topic": div(topic_ok, n),
        "has_region": div(has_region, n),
    }


def passes(m):
    return all(m[k] >= v for k, v in BAR.items())


if __name__ == "__main__":
    from dotenv import load_dotenv
    from deserto.embedding import embed_text

    load_dotenv()
    m = evaluate(load_rows(), embed_text)
    for k, v in m.items():
        print(f"{k}: {v:.0%}" if isinstance(v, float) else f"{k}: {v}")
    print("PASS" if passes(m) else "FAIL (Step 2 bar not met)")

"""Hand-label eval candidates. Usage: python -m eval.label

Shows each unlabelled candidate and asks for relevance, region and topic, then
appends to eval/eval_set.jsonl. Ctrl+C or 'q' stops; progress is saved per row.
The classifier is never consulted: labels are yours.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
CANDIDATES = HERE / "candidates.jsonl"
EVAL_SET = HERE / "eval_set.jsonl"

REGIONS = [
    "sahel-west-africa", "horn-east-africa", "southern-africa",
    "mediterranean-southern-europe", "mena", "central-asia", "south-east-asia",
    "australia", "americas-drylands", "global", "multi-region",
]
TOPICS = ["fmnr", "agroforestry", "water", "soil", "policy", "funding", "technology", "ecosystem"]


def load(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def ask(prompt, options):
    for i, o in enumerate(options, 1):
        print(f"  {i:>2}. {o}")
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("q", "quit"):
            raise KeyboardInterrupt
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        if raw in options:
            return raw
        print("  not a valid choice")


def main():
    done = {r["id"] for r in load(EVAL_SET)}
    todo = [c for c in load(CANDIDATES) if c["id"] not in done]
    print(f"{len(done)} labelled, {len(todo)} to go. 'q' quits, 's' skips an article.\n")
    for c in todo:
        print("=" * 70)
        print(c["title"], f"[{c['source']}]")
        print(c["summary"][:400])
        print(c["link"])
        try:
            rel = input("Relevant to desertification/land degradation/restoration? [y/n/s] ").strip().lower()
            if rel in ("q", "quit"):
                break
            if rel == "s":
                continue
            row = {k: c[k] for k in ("id", "title", "summary", "source", "link")}
            if rel == "n":
                row["relevant"] = False
            else:
                row["region"] = ask("Region #: ", REGIONS)
                row["topic"] = ask("Topic #: ", TOPICS)
        except (KeyboardInterrupt, EOFError):
            break
        with EVAL_SET.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("\nSaved. Run: pytest tests/test_eval_set.py")


if __name__ == "__main__":
    main()

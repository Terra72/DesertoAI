"""Pull unlabelled candidate articles for the eval set from Google News RSS.

Usage: python -m eval.pull_candidates
Appends new articles to eval/candidates.jsonl (deduped by id). Search terms are
only used to widen coverage; they are not stored, so they cannot bias labelling.
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

import feedparser

from deserto.ingest.rss import make_id

OUT = Path(__file__).parent / "candidates.jsonl"
PER_QUERY = 6
QUERIES = [
    "desertification Sahel", "land restoration Niger OR Mali OR Burkina Faso",
    "Great Green Wall", "desertification Ethiopia OR Kenya OR Somalia",
    "land degradation Southern Africa OR Namibia OR Botswana",
    "desertification Spain OR Italy OR Greece OR Mediterranean",
    "desertification Morocco OR Tunisia OR Jordan OR Saudi Arabia",
    "desertification Central Asia OR Uzbekistan OR Kazakhstan",
    "desertification China OR Mongolia OR India", "dryland restoration Australia",
    "desertification Brazil OR Argentina OR Mexico OR Chile",
    "UNCCD desertification global report", "FMNR farmer managed natural regeneration",
    "agroforestry drylands", "rainwater harvesting drylands",
    "soil erosion restoration drylands", "land restoration policy funding",
    "satellite monitoring land degradation", "drought land degradation global",
    "coffee shop opening", "football transfer news",
]


def clean(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).replace(" ", " ").strip()


def main():
    existing = {}
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                existing[row["id"]] = row
    before = len(existing)
    for q in QUERIES:
        url = f"https://news.google.com/rss/search?q={quote(q)}&hl=en-US&gl=US&ceid=US:en"
        for e in feedparser.parse(url).entries[:PER_QUERY]:
            title, link = e.get("title", ""), e.get("link", "")
            uid = make_id(title + link)
            summary = clean(e.get("summary"))
            if summary.startswith(title.split(" - ")[0]):  # Google repeats the headline
                summary = ""
            existing.setdefault(uid, {
                "id": uid, "title": title, "summary": summary[:500],
                "source": e.get("source", {}).get("title", "Unknown"), "link": link,
            })
    with OUT.open("w", encoding="utf-8", newline="\n") as f:
        for row in existing.values():
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"{len(existing) - before} new, {len(existing)} total")


if __name__ == "__main__":
    main()

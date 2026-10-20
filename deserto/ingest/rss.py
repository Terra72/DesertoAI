import feedparser
import hashlib
from datetime import datetime, UTC

FEEDS = [
    "https://www.fao.org/news/rss/en/",
    "https://www.unccd.int/news-stories/rss.xml",
    "https://news.google.com/rss/search?q=desertification+land+degradation+restoration"
]

def make_id(text):
    return hashlib.sha1(text.encode()).hexdigest()[:12]

def fetch_items():
    items = []

    for url in FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:10]:  # keep it cheap
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            source = feed.feed.get("title", "Unknown")

            uid = make_id(title + link)

            items.append({
                "id": uid,
                "title": title,
                "summary": summary,
                "source": source,
                "link": link,
                "fetched_at": datetime.now(UTC).isoformat()
            })

    return items

import feedparser
import hashlib
from urllib.parse import quote
from datetime import datetime, UTC

def news_search(query):
    return "https://news.google.com/rss/search?q=" + quote(query) + "&hl=en"


# (region the feed is scoped to, url). Global feeds have region None.
# The tag tracks coverage only; the classifier still decides each item's region.
FEEDS = [
    (None, "https://www.fao.org/news/rss/en/"),
    (None, "https://www.unccd.int/news-stories/rss.xml"),
    (None, news_search("desertification land degradation restoration")),

    ("north-america", news_search('desertification OR "land degradation" OR drought restoration United States Canada Mexico')),
    ("south-america", news_search('desertification OR "land degradation" OR drought restoration Brazil Argentina Chile Peru')),
    ("north-asia", news_search('desertification OR "land degradation" OR steppe restoration Mongolia Siberia Russia')),
    ("east-asia", news_search('desertification OR sandstorm OR "land restoration" China Gobi Korea Japan')),
    ("europe", news_search('desertification OR "land degradation" OR drought soil restoration Europe EU')),
    ("oceania", news_search("land degradation OR drought OR revegetation Pacific New Zealand Oceania")),
    ("middle-east", news_search('desertification OR drought OR "land restoration" Saudi Arabia Iran Iraq Jordan Middle East')),
    ("africa", news_search('desertification OR "land restoration" OR agroforestry Africa')),
    ("sahel-west-africa", news_search('Sahel desertification OR "Great Green Wall" OR "farmer managed natural regeneration"')),
    ("horn-east-africa", news_search('drought OR desertification OR "land restoration" Ethiopia Kenya Somalia Horn of Africa')),
    ("southern-africa", news_search('drought OR desertification OR "land degradation" Namibia Botswana Zimbabwe South Africa')),
    ("mediterranean-southern-europe", news_search("desertification OR drought OR wildfire land Spain Portugal Italy Greece Mediterranean")),
    ("mena", news_search('desertification OR drought OR "land restoration" Morocco Algeria Egypt Tunisia Maghreb')),
    ("central-asia", news_search('desertification OR "land degradation" OR "Aral Sea" Kazakhstan Uzbekistan Central Asia')),
    ("south-east-asia", news_search("land degradation OR peatland restoration OR drought Indonesia Vietnam Thailand Philippines")),
    ("australia", news_search("land degradation OR drought OR rangeland restoration Australia")),
    ("americas-drylands", news_search('drylands OR desertification OR semi-arid Chaco OR Caatinga OR "Sonoran Desert" OR Patagonia')),
]

def make_id(text):
    return hashlib.sha1(text.encode()).hexdigest()[:12]

def fetch_items():
    items = []

    for _region, url in FEEDS:
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

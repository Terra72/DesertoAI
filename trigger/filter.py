KEYWORDS = [
    "desertification",
    "land degradation",
    "soil",
    "restoration",
    "arid",
    "dryland"
]

TRUSTED_SOURCES = [
    "Journal of Arid Environments",
    "FAO",
    "UNCCD"
]

def decide(item):
    text = f"{item['title']} {item['summary']}".lower()

    keyword_hit = any(k in text for k in KEYWORDS)
    trusted_source = item["source"] in TRUSTED_SOURCES

    if keyword_hit and trusted_source:
        return "consider"

    return "ignore"

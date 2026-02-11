KEYWORDS_STRONG = [
    "desertification",
    "land degradation",
    "dryland",
    "soil erosion",
    "ecosystem restoration",
    "land restoration",
    "restore the land"
]

KEYWORDS_WEAK = [
    "drought",
    "arid",
    "sustainability",
    "regeneration",
    "land crisis",
    "ecosystem",
    "soil",
    "regreening"
]

TRUSTED_SOURCES = [
    "FAO",
    "UNCCD",
    "United Nations",
    "IUCN"
]

POLICY_KEYWORDS = [
    "conference",
    "cop",
    "initiative",
    "policy",
    "framework",
    "funding",
    "pledge",
    "program",
    "strategy"
]

INSTITUTIONAL_SOURCES = [
    "unccd",
    "united nations",
    "fao",
    "iucn",
    "world bank",
    "undp"
]

SYSTEMIC_KEYWORDS = [
    "food systems",
    "land crisis",
    "soil loss",
    "degradation",
    "ecosystem decline",
    "climate resilience"
]

def score(item):
    text = f"{item['title']} {item['summary']}".lower()
    s = 0.0

    # Strong keywords
    for k in KEYWORDS_STRONG:
        if k in text:
            s += 0.5

    # Weak keywords
    for k in KEYWORDS_WEAK:
        if k in text:
            s += 0.2

    # Trusted institutional source
    if any(src.lower() in item["source"].lower() for src in TRUSTED_SOURCES):
        s += 0.4

    # Scientific / research indicator
    if any(x in item["source"].lower() for x in ["journal", "phys.org", "eurekalert"]):
        s += 0.3

    for k in POLICY_KEYWORDS:
        if k in text:
            s += 0.25

    # Institutional authority boost
    if any(src in item["source"].lower() for src in INSTITUTIONAL_SOURCES):
        s += 0.5

    # Systemic environmental risk
    for k in SYSTEMIC_KEYWORDS:
        if k in text:
            s += 0.3

    return s


def decide(item):
    s = score(item)

    if s >= 0.6:
        return "consider"

    return "ignore"

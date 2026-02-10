REGION_KEYWORDS = {
    "sahel": "Sahel",
    "niger": "Sahel",
    "mali": "Sahel",
    "burkina": "Sahel",
    "ethiopia": "Horn of Africa",
    "somalia": "Horn of Africa",
    "kenya": "Horn of Africa",
    "china": "Northern China",
    "inner mongolia": "Northern China",
    "australia": "Australia Drylands"
}

def detect_region(item):
    text = f"{item['title']} {item['summary']}".lower()

    for key, region in REGION_KEYWORDS.items():
        if key in text:
            return region

    return "Global"

from deserto.ingest.rss import FEEDS
from eval.taxonomy import REGIONS

NOT_REGIONAL = {"global", "multi-region"}


def test_every_region_has_a_feed():
    tagged = {region for region, _ in FEEDS}
    assert set(REGIONS) - NOT_REGIONAL <= tagged


def test_feed_urls_are_unique():
    urls = [url for _, url in FEEDS]
    assert len(urls) == len(set(urls))

from dataclasses import dataclass

@dataclass
class Event:
    source_id: str
    title: str
    url: str | None
    region: str
    subregion: str | None
    country: str | None
    topic: str
    signal_type: str
    impact_direction: str
    semantic_score: float
    rule_score: float
    final_score: float
    summary: str
    confidence_delta: float
    published_at: str | None
    ingested_at: str
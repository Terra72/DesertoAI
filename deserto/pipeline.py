from datetime import datetime, UTC
import numpy as np

from deserto.relevance import score
from deserto.embedding import cosine_similarity
from deserto.classify.region_semantic import init_region_vectors, detect_region_semantic
from deserto.classify.topic_semantic import ensure_topic_vectors, detect_topic_semantic
from deserto.classify.confidence import confidence_delta
from deserto.models import Event

class Pipeline:
    """ingest -> relevance -> classify -> summarize -> store.

    All I/O (feed fetch, embeddings, LLM summary, DB) is injected so tests run
    offline.
    """

    def __init__(self, state, fetch_items, embed, summarize, repo,
                 force=False, dry_run=False):
        self.state = state
        self.fetch_items = fetch_items
        self.embed = embed
        self.summarize = summarize
        self.repo = repo
        self.force = force
        self.dry_run = dry_run

        self._init_vectors()

    # ---------- Initialization ----------

    def _init_vectors(self):
        if not self.state.get("desert_vector"):
            print("Initializing desert concept vector...")
            concept_text = """
            Desertification mitigation, land restoration, soil regeneration,
            dryland ecosystem recovery, agroforestry, water retention,
            drought resilience, FMNR, sand stabilization,
            sustainable land management, nature-based solutions for drylands
            """
            vec = self.embed(concept_text)
            self.state["desert_vector"] = vec.tolist()

        init_region_vectors(self.state, self.embed)
        ensure_topic_vectors(self.state, self.embed)

    # ---------- Main Loop ----------

    def run(self):
        items = self.fetch_items()

        if self.force:
            print("FORCE MODE: Reprocessing all items")
        if self.dry_run:
            print("DRY RUN: No state will be written")

        seen = set(self.state.get("sources_seen", []))
        desert_vec = np.array(self.state["desert_vector"])

        for item in items:
            if not self.force and item["id"] in seen:
                continue

            if not self.dry_run:
                seen.add(item["id"])

            event = self._process_item(item, desert_vec)

            if event:
                self._apply_event(event)
                # later:
                # event.save(conn)

        if not self.dry_run:
            self.state["sources_seen"] = list(seen)
            self.state["last_run"] = datetime.now(UTC).isoformat()

    # ---------- Item Processing ----------

    def _process_item(self, item, desert_vec):

        text = item["title"] + " " + item.get("summary", "")
        article_vec = self.embed(text)

        semantic_score = cosine_similarity(article_vec, desert_vec)
        rule_score = score(item)

        final_score = semantic_score * 2.0 + rule_score * 0.5
        decision = "consider" if final_score >= 0.65 else "ignore"

        print(
            f"S:{semantic_score:.2f} "
            f"R:{rule_score:.2f} "
            f"F:{final_score:.2f} → {decision.upper()} | {item['title']}"
        )

        if decision == "ignore":
            return None

        region, region_score = detect_region_semantic(text, self.state, self.embed)
        topic, topic_score = detect_topic_semantic(text, self.state, self.embed)

        print(f"REGION {region} ({region_score:.2f})")
        print(f"TOPIC {topic} ({topic_score:.2f})")

        result = self.summarize(item, self.state.get("global_summary", ""))

        if not result["novel"]:
            signal_type = "reinforcement"
        else:
            signal_type = "new"

        update = result["update"]
        signal_type = "reinforcement" if not result["novel"] else "new"

        event = Event(
            source_id=item["id"],
            title=item["title"],
            url=item.get("link"),
            region=region,
            subregion=None,
            country=None,
            topic=topic,
            signal_type=signal_type,
            impact_direction="neutral",  # improve later
            semantic_score=semantic_score,
            rule_score=rule_score,
            final_score=final_score,
            summary=update,
            confidence_delta=confidence_delta(item["source"]),
            published_at=item.get("published"),
            ingested_at=datetime.now(UTC).isoformat()
        )
        if not self.dry_run:
            self.repo.save(event)

        print(f"UPDATED ({region}): {item['title']}")
        return event

    def _apply_event(self, event):

        # ---------- Global ----------
        self.state["global_updates"].append({
            "source": event.title,
            "region": event.region,
            "topic": event.topic,
            "update": event.summary
        })

        self.state["global_summary"] = (
            self.state["global_summary"] + "\n" + event.summary
        ).strip()

        # ---------- Region ----------
        if event.region not in self.state["regions"]:
            self.state["regions"][event.region] = {
                "summary": "",
                "confidence": 0.0,
                "updates": []
            }

        region_data = self.state["regions"][event.region]

        region_data["updates"].append(event.summary)
        region_data["summary"] = (
            region_data["summary"] + "\n" + event.summary
        ).strip()

        region_data["confidence"] += event.confidence_delta    
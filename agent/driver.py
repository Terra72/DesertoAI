from datetime import datetime, UTC
import numpy as np

from ingest.rss import fetch_items
from trigger.filter import score
from analyze.summarize import summarize
from analyze.embedding import embed_text, cosine_similarity
from analyze.region_semantic import ensure_region_vectors, detect_region_semantic
from analyze.topic_semantic import ensure_topic_vectors, detect_topic_semantic
from analyze.confidence import confidence_delta


class DesertificationAgent:

    def __init__(self, state, force=False, dry_run=False):
        self.state = state
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
            vec = embed_text(concept_text)
            self.state["desert_vector"] = vec.tolist()

        ensure_region_vectors(self.state)
        ensure_topic_vectors(self.state)

    # ---------- Main Loop ----------

    def run(self):
        items = fetch_items()

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

            self._process_item(item, desert_vec)

        if not self.dry_run:
            self.state["sources_seen"] = list(seen)
            self.state["last_run"] = datetime.now(UTC).isoformat()

    # ---------- Item Processing ----------

    def _process_item(self, item, desert_vec):

        text = item["title"] + " " + item.get("summary", "")
        article_vec = embed_text(text)

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
            print(f"IGNORED: {item['title']}")
            return

        # ---------- Region ----------
        region, region_score = detect_region_semantic(text, self.state)
        print(f"REGION {region} ({region_score:.2f})")

        # ---------- Topic ----------
        topic, topic_score = detect_topic_semantic(text, self.state)
        print(f"TOPIC {topic} ({topic_score:.2f})")

        # ---------- Summary ----------
        result = summarize(item, self.state.get("global_summary", ""))

        if not result["novel"]:
            print(f"REINFORCED: {item['title']}")
            return

        update = result["update"]

        # ---------- Global ----------
        self.state["global_updates"].append({
            "source": item["title"],
            "region": region,
            "topic": topic,
            "update": update
        })

        self.state["global_summary"] = (
            self.state["global_summary"] + "\n" + update
        ).strip()

        # ---------- Region Memory ----------
        if region not in self.state["regions"]:
            self.state["regions"][region] = {
                "summary": "",
                "confidence": 0.0,
                "updates": []
            }

        self.state["regions"][region]["updates"].append(update)
        self.state["regions"][region]["summary"] = (
            self.state["regions"][region]["summary"] + "\n" + update
        ).strip()

        self.state["regions"][region]["confidence"] += confidence_delta(item["source"])

        print(f"UPDATED ({region}): {item['title']}")

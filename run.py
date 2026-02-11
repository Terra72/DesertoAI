from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, UTC
from memory.store import load_state, save_state
from ingest.rss import fetch_items
from trigger.filter import decide, score

from analyze.summarize import summarize
from analyze.region import detect_region
from analyze.confidence import confidence_delta
from analyze.embedding import embed_text, cosine_similarity
from analyze.region_semantic import ensure_region_vectors
import numpy as np

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--force", "-f", action="store_true", help="Reprocess items even if already analyzed")
parser.add_argument("--dry-run", "-d", action="store_true",help="Run pipeline without writing state or outputs")

args = parser.parse_args()
FORCE_REFRESH = args.force
DRY_RUN = args.dry_run

def main():
    
    state = load_state()
    # 6B — Initialize desert concept vector (one-time)
    if not state.get("desert_vector"):
        print("Initializing desertification concept vector...")

        concept_text = """
        Desertification mitigation, land restoration, soil regeneration,
        dryland ecosystem recovery, agroforestry, water retention,
        drought resilience, FMNR, sand stabilization,
        sustainable land management, nature-based solutions for drylands
        """

        vec = embed_text(concept_text)

        if vec is None:
            raise RuntimeError("Embedding failed — desert vector is None")

        state["desert_vector"] = vec.tolist()

        if not DRY_RUN:
            save_state(state)

    items = fetch_items()
    ensure_region_vectors(state)
    if FORCE_REFRESH:
        print("FORCE MODE: Reprocessing all items (state will be updated)")
    if DRY_RUN:
        print("DRY RUN: No state will be written, no files will be modified")

    seen = set(state.get("sources_seen", []))

    for item in items:
        if not FORCE_REFRESH and item["id"] in seen:
            continue
        if not DRY_RUN:
            seen.add(item["id"])

        # SEMANTIC filter
        desert_vec = np.array(state["desert_vector"])
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

        if decision == "consider":
            result = summarize(item, state.get("global_summary", ""))

            if result["novel"]:
                update = result["update"]
                # Region Semantic
                from analyze.region_semantic import detect_region_semantic
                region_text = item["title"] + " " + item.get("summary", "")
                region, region_score = detect_region_semantic(region_text, state)
                print(f"REGION {region} ({region_score:.2f})")

                # --- GLOBAL MEMORY ---
                state["global_updates"].append({
                    "source": item["title"],
                    "region": region,
                    "update": update
                })

                state["global_summary"] = (
                    state["global_summary"] + "\n" + update
                ).strip()

                # --- REGIONAL MEMORY ---
                if region not in state["regions"]:
                    state["regions"][region] = {
                        "summary": "",
                        "confidence": 0.0,
                        "updates": []
                    }

                state["regions"][region]["updates"].append(update)
                state["regions"][region]["summary"] = (
                    state["regions"][region]["summary"] + "\n" + update
                ).strip()

                state["regions"][region]["confidence"] += confidence_delta(item["source"])

                print(f"UPDATED ({region}): {item['title']}")

            else:
                print(f"REINFORCED: {item['title']}")

        else:
            print(f"IGNORED: {item['title']}")


    state["last_run"] = datetime.now(UTC).isoformat()
    if not DRY_RUN:
        state["sources_seen"] = list(seen)
        save_state(state)

if __name__ == "__main__":
    main()

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, UTC
from memory.store import load_state, save_state
from ingest.rss import fetch_items
from trigger.filter import decide, score

from analyze.summarize import summarize
from analyze.region import detect_region
from analyze.confidence import confidence_delta

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--force", "-f", action="store_true", help="Reprocess items even if already analyzed")
parser.add_argument("--dry-run", "-d", action="store_true",help="Run pipeline without writing state or outputs")

args = parser.parse_args()
FORCE_REFRESH = args.force
DRY_RUN = args.dry_run

def main():
    
    state = load_state()
    items = fetch_items()

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

        decision = decide(item)
        print(f"SCORE {score(item):.2f} → {decision.upper()} | {item['title']}")
        if decision == "consider":
            result = summarize(item, state.get("global_summary", ""))

            if result["novel"]:
                update = result["update"]
                region = detect_region(item)

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

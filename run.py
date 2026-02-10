from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, UTC
from memory.store import load_state, save_state
from ingest.rss import fetch_items
from trigger.filter import decide

from analyze.summarize import summarize
from analyze.region import detect_region
from analyze.confidence import confidence_delta


def main():
    
    state = load_state()
    items = fetch_items()

    seen = set(state.get("sources_seen", []))
    new_items = []

    for item in items:
        if item["id"] not in seen:
            seen.add(item["id"])
            new_items.append(item)

    state["sources_seen"] = list(seen)

    for item in new_items:
        decision = decide(item)

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
    save_state(state)

if __name__ == "__main__":
    main()

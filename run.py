from dotenv import load_dotenv
load_dotenv()

from memory.store import load_state, save_state
from ingest.fake import fetch_items
from trigger.filter import decide
from analyze.summarize import summarize


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

                state["global_updates"].append({
                    "source": item["title"],
                    "update": update
                })

                state["global_summary"] = (
                    state["global_summary"] + "\n" + update
                ).strip()

                print(f"UPDATED: {item['title']}")
            else:
                print(f"REINFORCED: {item['title']}")

        else:
            print(f"IGNORED: {item['title']}")

    save_state(state)

if __name__ == "__main__":
    main()

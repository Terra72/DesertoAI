from memory.store import load_state, save_state
from ingest.fake import fetch_items
from trigger.filter import decide

def main():
    state = load_state()
    items = fetch_items()

    seen = set(state.get("sources_seen", []))
    new_items = []
    decisions = []

    for item in items:
        if item["id"] not in seen:
            seen.add(item["id"])
            new_items.append(item)

    for item in new_items:
        decision = decide(item)
        decisions.append((item, decision))

    state["sources_seen"] = list(seen)

    print(f"New items: {len(new_items)}")
    for item, decision in decisions:
        print(f"- {decision.upper()}: {item['title']}")

    save_state(state)

if __name__ == "__main__":
    main()

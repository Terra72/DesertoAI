from memory.store import load_state, save_state
from ingest.fake import fetch_items

def main():
    state = load_state()
    items = fetch_items()

    seen = set(state.get("sources_seen", []))
    new_items = []

    for item in items:
        if item["id"] not in seen:
            new_items.append(item)
            seen.add(item["id"])

    state["sources_seen"] = list(seen)

    print(f"Fetched {len(items)} items")
    print(f"New items: {len(new_items)}")

    save_state(state)

if __name__ == "__main__":
    main()
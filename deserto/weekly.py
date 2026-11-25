from dotenv import load_dotenv

load_dotenv()

from deserto import embedding, summarize
from deserto.config import EXPORT_DIR
from deserto.export import exported_ids, write_export
from deserto.ingest.rss import fetch_items
from deserto.pipeline import Pipeline
from deserto.state import load_state
from deserto.store.repository import EventRepository
from deserto.store.schema import init_db


def main():
    """Weekly CI run: scrape, then write only new events to data/exports.

    The runner has no state or DB, so items already exported are skipped.
    """
    state = load_state()
    state["sources_seen"] = list(exported_ids(EXPORT_DIR))
    init_db()

    Pipeline(
        state=state,
        fetch_items=fetch_items,
        embed=embedding.embed_text,
        summarize=summarize.summarize,
        repo=EventRepository(),
    ).run()

    path, count = write_export()
    print(f"Exported {count} new events to {path}")


if __name__ == "__main__":
    main()

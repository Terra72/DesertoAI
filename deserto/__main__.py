from dotenv import load_dotenv

load_dotenv()

import argparse

from deserto import embedding, summarize
from deserto.ingest.rss import fetch_items
from deserto.pipeline import Pipeline
from deserto.state import load_state, save_state
from deserto.store.repository import EventRepository
from deserto.store.schema import init_db


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m deserto")
    parser.add_argument("--force", "-f", action="store_true")
    parser.add_argument("--dry-run", "-d", action="store_true")
    args = parser.parse_args(argv)

    state = load_state()
    init_db()
    pipeline = Pipeline(
        state=state,
        fetch_items=fetch_items,
        embed=embedding.embed_text,
        summarize=summarize.summarize,
        repo=EventRepository(),
        force=args.force,
        dry_run=args.dry_run,
    )
    pipeline.run()

    if not args.dry_run:
        save_state(state)


if __name__ == "__main__":
    main()

from dotenv import load_dotenv
load_dotenv()

import argparse
from memory.store import load_state, save_state
from agent.driver import DesertificationAgent


parser = argparse.ArgumentParser()
parser.add_argument("--force", "-f", action="store_true")
parser.add_argument("--dry-run", "-d", action="store_true")
args = parser.parse_args()


def main():
    state = load_state()

    agent = DesertificationAgent(
        state=state,
        force=args.force,
        dry_run=args.dry_run
    )

    agent.run()

    if not args.dry_run:
        save_state(state)


if __name__ == "__main__":
    main()

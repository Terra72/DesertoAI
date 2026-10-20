import json
from datetime import datetime, UTC

from deserto.config import STATE_PATH, STATE_TEMPLATE_PATH


def load_state():
    if not STATE_PATH.exists():
        return json.loads(STATE_TEMPLATE_PATH.read_text())
    return json.loads(STATE_PATH.read_text())


def save_state(state):
    state["last_run"] = datetime.now(UTC).isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2))

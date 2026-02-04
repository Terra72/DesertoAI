import json
from datetime import datetime
from pathlib import Path

STATE_PATH = Path("memory/state.json")

def load_state():
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text())

def save_state(state):
    state["last_run"] = datetime.utcnow().isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2))

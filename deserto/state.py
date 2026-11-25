import json
from datetime import datetime, UTC

from deserto.config import EMBEDDING_MODEL, STATE_PATH, STATE_TEMPLATE_PATH


VECTOR_KEYS = ["desert_vector", "region_vectors", "topic_vectors", "embeddings_cache"]


def load_state():
    path = STATE_PATH if STATE_PATH.exists() else STATE_TEMPLATE_PATH
    state = json.loads(path.read_text())

    # Vectors from another embedding model are the wrong size, so drop them
    if state.get("embedding_model") != EMBEDDING_MODEL:
        template = json.loads(STATE_TEMPLATE_PATH.read_text())
        for key in VECTOR_KEYS:
            state[key] = template[key]
        state["embedding_model"] = EMBEDDING_MODEL
    return state


def save_state(state):
    state["last_run"] = datetime.now(UTC).isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2))

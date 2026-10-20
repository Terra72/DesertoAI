import hashlib
import json

import numpy as np
import pytest

from deserto import config
from deserto.store import queries, repository, schema

DIM = 32


def _vec(seed: str) -> np.ndarray:
    rng = np.random.default_rng(int(hashlib.md5(seed.encode()).hexdigest()[:8], 16))
    return rng.normal(size=DIM)


@pytest.fixture
def embed():
    """Offline embedder. Text containing a known concept word maps to that
    concept's vector, so cosine similarity is predictable."""
    concepts = {
        "desertification": _vec("desert"),
        "sahel": _vec("sahel"),
        "fmnr": _vec("fmnr"),
    }

    def _embed(text: str) -> np.ndarray:
        t = text.lower()
        for word, vec in concepts.items():
            if word in t:
                return vec
        return _vec(text)

    return _embed


@pytest.fixture
def fresh_state():
    return json.loads(config.STATE_TEMPLATE_PATH.read_text())


@pytest.fixture
def db(tmp_path, monkeypatch):
    path = tmp_path / "test.db"
    for mod in (schema, repository, queries):
        monkeypatch.setattr(mod, "DB_PATH", path)
    schema.init_db()
    return path


@pytest.fixture
def repo(db):
    return repository.EventRepository()

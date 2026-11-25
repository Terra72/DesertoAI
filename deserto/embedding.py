import numpy as np

from deserto.config import EMBEDDING_MODEL

_model = None


def _get_model():
    # Lazy: tests inject their own embedder and never load the model
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_text(text: str) -> np.ndarray:
    return _get_model().encode(text)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

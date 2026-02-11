from analyze.embedding import embed_text, cosine_similarity
import numpy as np


TOPIC_CONCEPTS = {
    "fmnr": "Farmer Managed Natural Regeneration, FMNR, natural tree regrowth, assisted natural regeneration drylands",
    "agroforestry": "Agroforestry drylands, trees on farms, regenerative agriculture dry regions",
    "water": "Water retention, rainwater harvesting, watershed restoration, water conservation drylands",
    "soil": "Soil regeneration, soil carbon, erosion control, soil stabilization desertification",
    "policy": "Government policy, land restoration policy, environmental regulation desertification",
    "funding": "Funding, climate finance, land restoration investment, green initiative desertification",
    "technology": "Satellite monitoring, remote sensing desertification, climate data drylands",
    "ecosystem": "Ecosystem restoration, biodiversity recovery, nature-based solutions drylands"
}


def ensure_topic_vectors(state):
    if "topic_vectors" not in state:
        state["topic_vectors"] = {}

    for topic, text in TOPIC_CONCEPTS.items():
        if topic not in state["topic_vectors"] or not state["topic_vectors"][topic]:
            print(f"Building topic vector: {topic}")
            vec = embed_text(text)
            if vec is None:
                raise RuntimeError(f"Embedding failed for topic {topic}")
            state["topic_vectors"][topic] = vec.tolist()


def detect_topic_semantic(text, state):
    article_vec = embed_text(text)
    if article_vec is None:
        return "unknown", 0.0

    article_vec = np.array(article_vec)

    best_topic = "unknown"
    best_score = 0.0

    for topic, vec in state["topic_vectors"].items():
        topic_vec = np.array(vec)
        sim = cosine_similarity(article_vec, topic_vec)

        if sim > best_score:
            best_score = sim
            best_topic = topic

    return best_topic, best_score

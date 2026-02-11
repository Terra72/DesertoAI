from analyze.embedding import embed_text, cosine_similarity
import numpy as np


REGION_CONCEPTS = {
    "sahel": "Sahel region, Niger, Mali, Burkina Faso, dryland Africa, desertification Sahel",
    "africa": "Africa drylands, sub-Saharan land restoration, African ecosystems, desertification Africa",
    "middle_east": "Middle East drylands, Saudi Arabia, Jordan, UAE, desertification Middle East",
    "india": "India drylands, Rajasthan, Indian land restoration, desertification India",
    "china": "China drylands, Loess Plateau, Inner Mongolia, desertification China, sand control China",
    "global": "Global desertification, worldwide drylands, international land restoration"
}


def ensure_region_vectors(state):
    if "region_vectors" not in state:
        state["region_vectors"] = {}

    for region, text in REGION_CONCEPTS.items():
        if region not in state["region_vectors"] or not state["region_vectors"][region]:
            print(f"Building region vector: {region}")
            vec = embed_text(text)
            if vec is None:
                raise RuntimeError(f"Embedding failed for region {region}")
            state["region_vectors"][region] = vec.tolist()


def detect_region_semantic(text, state):
    article_vec = embed_text(text)
    if article_vec is None:
        return "global"

    article_vec = np.array(article_vec)

    best_region = "global"
    best_score = 0.0

    for region, vec in state["region_vectors"].items():
        region_vec = np.array(vec)
        sim = cosine_similarity(article_vec, region_vec)

        if sim > best_score:
            best_score = sim
            best_region = region

    return best_region, best_score

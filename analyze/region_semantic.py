from analyze.embedding import embed_text, cosine_similarity
import numpy as np


REGION_DEFINITIONS = {
    "africa": "Sahel, Sub-Saharan Africa, Horn of Africa, African drylands, Sahara, East Africa, West Africa",
    "europe": "Southern Europe, Mediterranean Europe, Spain, Italy, Greece drylands, European drylands",
    "south_america": "Brazil, Argentina, Chile, Peru, Gran Chaco, South American drylands",
    "north_america": "United States Southwest, Mexico drylands, Arizona, California drought, North American drylands",
    "australia": "Australian outback, Western Australia drylands, Murray-Darling Basin, Australian desertification",
    "asia": "India, China, Mongolia, Central Asia, Gobi Desert, Middle East drylands",
    "global": "global international worldwide multilateral UN climate land restoration"
}


def init_region_vectors(state):
    if "region_vectors" not in state:
        state["region_vectors"] = {}

    for region, description in REGION_DEFINITIONS.items():
        if region not in state["region_vectors"]:
            vec = embed_text(description)
            state["region_vectors"][region] = vec.tolist()  # ✅ FIX

    return state["region_vectors"]


def detect_region_semantic(text, state):
    article_vec = embed_text(text)
    region_vectors = state["region_vectors"]

    best_region = "global"
    best_score = 0.0

    for region, vec_list in region_vectors.items():
        vec = np.array(vec_list)  # ✅ Convert back to numpy
        score = cosine_similarity(article_vec, vec)

        if score > best_score:
            best_region = region
            best_score = score

    if best_score < 0.30:
        return "global", best_score

    return best_region, best_score
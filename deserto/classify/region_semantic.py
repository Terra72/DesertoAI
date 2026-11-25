from deserto.embedding import embed_text, cosine_similarity
import numpy as np


# One entry per region in eval/taxonomy.py (except multi-region)
REGION_DEFINITIONS = {
    # parents
    "north-america": "United States Southwest, Canada prairies, Mexico, Arizona, California drought, North American drylands",
    "south-america": "Brazil, Argentina, Chile, Peru, Bolivia, Gran Chaco, South American drylands",
    "africa": "Africa, African drylands, Sub-Saharan Africa, Sahara, African Union, continent-wide African land restoration",
    "north-asia": "Mongolia, Siberia, Russia, steppe, northern Asia grasslands",
    "east-asia": "China, Gobi Desert, sandstorms, Korea, Japan, Loess Plateau, Chinese desertification",
    "europe": "Europe, European Union, European Commission, European soils and drought, EU land policy",
    "middle-east": "Saudi Arabia, Iran, Iraq, Jordan, Gulf states, Arabian Peninsula, Middle East drylands",
    "oceania": "Oceania, Pacific islands, New Zealand, Pacific land degradation",
    # leaves
    "sahel-west-africa": "Sahel, Niger, Mali, Burkina Faso, Senegal, Chad, Great Green Wall, West Africa farmer managed natural regeneration",
    "horn-east-africa": "Horn of Africa, Ethiopia, Kenya, Somalia, Sudan, Uganda, East Africa drought and rangelands",
    "southern-africa": "Southern Africa, Namibia, Botswana, Zimbabwe, South Africa, Zambia, Kalahari",
    "mediterranean-southern-europe": "Spain, Portugal, Italy, Greece, Mediterranean Europe, southern European desertification and wildfires",
    "mena": "Morocco, Algeria, Tunisia, Egypt, Libya, Maghreb, North Africa and Middle East, Green Dam",
    "central-asia": "Kazakhstan, Uzbekistan, Turkmenistan, Aral Sea, Central Asia",
    "south-east-asia": "Indonesia, Vietnam, Thailand, Philippines, Malaysia, peatland restoration, Southeast Asia",
    "australia": "Australian outback, Western Australia, Murray-Darling Basin, Australian rangelands and drought",
    "americas-drylands": "Gran Chaco, Caatinga, Sonoran Desert, Patagonia, Atacama, semi-arid drylands of the Americas",
    "global": "global international worldwide multilateral UN climate land restoration",
}


def init_region_vectors(state, embed=embed_text):
    vectors = state.setdefault("region_vectors", {})

    # Drop labels that are no longer defined
    for region in [r for r in vectors if r not in REGION_DEFINITIONS]:
        del vectors[region]

    for region, description in REGION_DEFINITIONS.items():
        if region not in vectors:
            vectors[region] = embed(description).tolist()

    return vectors


def detect_region_semantic(text, state, embed=embed_text):
    article_vec = embed(text)
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
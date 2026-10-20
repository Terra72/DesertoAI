"""Region taxonomy for the eval set (ADR-0004).

Regions are two-level; a leaf may sit under more than one parent. A label may be a leaf or a parent. A parent label such as
"africa" means "any region inside it is an acceptable answer".
"""

PARENTS = {
    "north-america": ["americas-drylands"],
    "south-america": ["americas-drylands"],
    "africa": ["sahel-west-africa", "horn-east-africa", "southern-africa", "mena"],
    "north-asia": ["central-asia"],
    "east-asia": ["south-east-asia"],
    "europe": ["mediterranean-southern-europe"],
    "oceania": ["australia"],
    "middle-east": ["mena"],
}
LEAVES = [
    "sahel-west-africa", "horn-east-africa", "southern-africa",
    "mediterranean-southern-europe", "mena", "central-asia", "south-east-asia",
    "australia", "americas-drylands", "global", "multi-region",
]
REGIONS = list(PARENTS) + LEAVES
TOPICS = ["fmnr", "agroforestry", "water", "soil", "policy", "funding", "technology", "ecosystem"]


def region_correct(predicted, expected):
    """Exact match, or the expected label is a parent containing the prediction.

    A coarse prediction against a fine label is wrong: the classifier must be at
    least as specific as the label.
    """
    return predicted == expected or predicted in PARENTS.get(expected, [])

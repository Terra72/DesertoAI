def confidence_delta(source):
    # crude but effective
    if "Journal" in source:
        return 0.2
    if source in ["FAO", "UNCCD"]:
        return 0.25
    return 0.1

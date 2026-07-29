"""Difficulty scoring — combines all feature dimensions into a single score."""


def compute_difficulty(feature_dims, weights):
    total = sum(feature_dims[k] * weights.get(k, 0.0) for k in feature_dims)

    if total < 0.75:
        level = "Easy"
    elif total < 1.15:
        level = "Moderate"
    elif total < 1.60:
        level = "Challenging"
    else:
        level = "Very Hard"

    return {
        "total_difficulty": round(total, 3),
        "level": level,
        "dimensions": {k: round(v, 3) for k, v in feature_dims.items()},
    }

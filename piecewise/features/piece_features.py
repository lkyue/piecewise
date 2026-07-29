"""Piece-count-based difficulty modeling."""


def analyze_piece_count(num_pieces, reference_pieces=500, exponent=0.35):
    if num_pieces <= 0:
        raise ValueError(f"Invalid piece count: {num_pieces}")

    base_difficulty = (num_pieces / reference_pieces) ** exponent

    if num_pieces <= 500:
        bracket = "small"
    elif num_pieces <= 1000:
        bracket = "medium"
    elif num_pieces <= 2000:
        bracket = "large"
    elif num_pieces <= 3000:
        bracket = "xl"
    else:
        bracket = "xxl"

    return {
        "num_pieces": num_pieces,
        "bracket": bracket,
        "base_difficulty": round(base_difficulty, 3),
    }

"""Time estimation based on difficulty score and piece count."""


def estimate_time(difficulty_score, num_pieces):
    base_piece_factors = {
        100: 0.3,
        300: 0.6,
        500: 1.0,
        750: 1.8,
        1000: 3.0,
        1500: 5.5,
        2000: 9.0,
        3000: 17.0,
        4000: 28.0,
        5000: 40.0,
    }

    keys = sorted(base_piece_factors.keys())
    piece_factor = base_piece_factors[keys[0]]
    if num_pieces >= keys[-1]:
        piece_factor = base_piece_factors[keys[-1]]
    elif num_pieces > keys[0]:
        for i in range(len(keys) - 1):
            if keys[i] <= num_pieces <= keys[i + 1]:
                t = (num_pieces - keys[i]) / (keys[i + 1] - keys[i])
                piece_factor = (
                    base_piece_factors[keys[i]] * (1 - t)
                    + base_piece_factors[keys[i + 1]] * t
                )
                break

    if difficulty_score < 0.8:
        base_hours = 2.5
    elif difficulty_score < 1.2:
        base_hours = 4.0
    elif difficulty_score < 1.7:
        base_hours = 6.5
    else:
        base_hours = 10.0

    estimated = base_hours * piece_factor * (difficulty_score**0.8)
    lower = estimated * 0.7
    upper = estimated * 1.3

    def fmt(h):
        if h < 1:
            return f"{h * 60:.0f} min"
        return f"{h:.1f}h"

    return {
        "best_case_hours": round(lower, 1),
        "worst_case_hours": round(upper, 1),
        "range_hours": f"{fmt(lower)} – {fmt(upper)}",
    }

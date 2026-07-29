"""Time estimation based on difficulty score and piece count.

Reference benchmarks (moderate difficulty, score ≈ 1.0):
  500pcs:    3–5h    → ref_500h = 4.0
  1000pcs:   6–10h   → piece_scale = 2.0
  1500pcs:  10–18h   → piece_scale = 3.5
  2000pcs:  15–25h   → piece_scale = 5.0
  3000pcs:  25–50h   → piece_scale = 9.375

Formula:  estimated = ref_500h * piece_scale(n) * score ^ 1.5
"""


def estimate_time(difficulty_score, num_pieces):
    ref_hours_for_500 = 4.0

    piece_scales = {
        100: 0.3,
        300: 0.6,
        500: 1.0,
        750: 1.8,
        1000: 2.0,
        1500: 3.5,
        2000: 5.0,
        3000: 9.375,
        4000: 15.0,
        5000: 25.0,
    }

    keys = sorted(piece_scales.keys())
    piece_scale = piece_scales[keys[0]]
    if num_pieces >= keys[-1]:
        piece_scale = piece_scales[keys[-1]]
    elif num_pieces > keys[0]:
        for i in range(len(keys) - 1):
            if keys[i] <= num_pieces <= keys[i + 1]:
                t = (num_pieces - keys[i]) / (keys[i + 1] - keys[i])
                piece_scale = (
                    piece_scales[keys[i]] * (1 - t) + piece_scales[keys[i + 1]] * t
                )
                break

    difficulty_multiplier = max(difficulty_score, 0.3) ** 1.5

    estimated = ref_hours_for_500 * piece_scale * difficulty_multiplier
    lower = estimated * 0.7
    upper = estimated * 1.3

    def fmt(h):
        if h < 1:
            return f"{h * 60:.0f} min"
        return f"{h:.1f}h"

    return {
        "estimated_hours": round(estimated, 1),
        "best_case_hours": round(lower, 1),
        "worst_case_hours": round(upper, 1),
        "range_hours": f"{fmt(lower)} – {fmt(upper)}",
    }

"""Top-level puzzle analyser orchestrator."""

import json
import textwrap
from piecewise.features.image_features import (
    analyze_color_richness,
    analyze_color_clustering,
    analyze_texture_complexity,
    analyze_pattern_repetition,
    analyze_sharpness,
)
from piecewise.features.piece_features import analyze_piece_count
from piecewise.features.meta_features import (
    analyze_cut_shape,
    analyze_backside,
    analyze_blind,
)
from piecewise.scoring.difficulty import compute_difficulty
from piecewise.scoring.time_estimate import estimate_time
from piecewise.utils.image_utils import load_image


def analyze(
    image_path,
    pieces,
    *,
    cut="ribbon",
    back="none",
    blind=False,
    weights=None,
    config=None,
):
    image_bgr = load_image(image_path)

    color = analyze_color_richness(image_bgr)
    cluster = analyze_color_clustering(image_bgr)
    texture = analyze_texture_complexity(image_bgr)
    pattern = analyze_pattern_repetition(image_bgr)
    sharpness = analyze_sharpness(image_bgr)
    piece = analyze_piece_count(
        pieces,
        reference_pieces=config.get("reference_pieces", 500) if config else 500,
        exponent=config.get("exponent", 0.35) if config else 0.35,
    )
    meta_cut = analyze_cut_shape(cut)
    meta_back = analyze_backside(back)
    meta_blind = analyze_blind(blind)

    feature_dims = {
        "pieces": piece["base_difficulty"],
        "color_richness": color["difficulty_factor"],
        "color_clustering": cluster["difficulty_factor"],
        "texture": texture["difficulty_factor"],
        "pattern_repetition": pattern["difficulty_factor"],
        "sharpness": sharpness["difficulty_factor"],
        "cut_shape": meta_cut["difficulty_factor"],
        "backside": meta_back["difficulty_factor"],
        "blind": meta_blind["difficulty_factor"],
    }

    default_weights = {
        "pieces": 0.25,
        "color_richness": 0.18,
        "color_clustering": 0.16,
        "texture": 0.10,
        "pattern_repetition": 0.08,
        "sharpness": 0.05,
        "cut_shape": 0.07,
        "backside": 0.06,
        "blind": 0.05,
    }

    diff_result = compute_difficulty(feature_dims, weights or default_weights)
    time_result = estimate_time(diff_result["total_difficulty"], pieces)

    return {
        "image_analysis": {
            "color": color,
            "clustering": cluster,
            "texture": texture,
            "pattern": pattern,
            "sharpness": sharpness,
        },
        "piece_analysis": piece,
        "meta_analysis": {
            "cut_shape": meta_cut,
            "backside": meta_back,
            "blind": meta_blind,
        },
        "difficulty": diff_result,
        "time_estimate": time_result,
    }


def format_text(result):
    c = result["image_analysis"]["color"]
    cl = result["image_analysis"]["clustering"]
    t = result["image_analysis"]["texture"]
    pat = result["image_analysis"]["pattern"]
    sh = result["image_analysis"]["sharpness"]
    p = result["piece_analysis"]
    m = result["meta_analysis"]
    d = result["difficulty"]
    te = result["time_estimate"]

    return textwrap.dedent(f"""\
    {"=" * 50}
    Puzzle Difficulty Analysis
    {"=" * 50}

    [Pieces] {p["num_pieces"]} pieces ({p["bracket"]}) — base difficulty: {p["base_difficulty"]:.3f}

    [Image Analysis]
      Color Richness:   {c["significant_hues"]} significant hues (sat ratio={c["saturation_ratio"]:.2f}) [{c["level"]}]  difficulty: {c["difficulty_factor"]:.3f}
      Color Clustering:  ΔE={cl["mean_adjacent_color_diff"]} [{cl["level"]}]  difficulty: {cl["difficulty_factor"]:.3f}
      Texture:           edges: {t["edge_density"]:.4f} [{t["edge_level"]}], entropy={t["texture_entropy"]:.3f} [{t["texture_level"]}]  difficulty: {t["difficulty_factor"]:.3f}
      Pattern:           periodicity={pat["periodicity_peak"]:.4f} [{pat["level"]}]  difficulty: {pat["difficulty_factor"]:.3f}
      Sharpness:         Laplacian var={sh["laplacian_variance"]:.1f} [{sh["level"]}]  difficulty: {sh["difficulty_factor"]:.3f}

    [Metadata]
      Cut Shape:   {m["cut_shape"]["label"]}  factor: {m["cut_shape"]["difficulty_factor"]:.2f}
      Backside:    {m["backside"]["label"]}  factor: {m["backside"]["difficulty_factor"]:.2f}
      Reference:   {m["blind"]["label"]}  factor: {m["blind"]["difficulty_factor"]:.2f}

    [Difficulty]
      Total Score: {d["total_difficulty"]:.3f}
      Level:       {d["level"]}
      Breakdown:   {" | ".join(f"{k}={v:.3f}" for k, v in d["dimensions"].items())}

    [Time Estimate]
      Range:       {te["range_hours"]}
      Best case:   {te["best_case_hours"]:.1f} hours
      Worst case:  {te["worst_case_hours"]:.1f} hours
    {"=" * 50}
    """)


def format_json(result):
    return json.dumps(result, indent=2, ensure_ascii=False)


def format_markdown(result):
    c = result["image_analysis"]["color"]
    cl = result["image_analysis"]["clustering"]
    t = result["image_analysis"]["texture"]
    pat = result["image_analysis"]["pattern"]
    sh = result["image_analysis"]["sharpness"]
    p = result["piece_analysis"]
    m = result["meta_analysis"]
    d = result["difficulty"]
    te = result["time_estimate"]

    return textwrap.dedent(f"""\
    # Puzzle Difficulty Analysis

    ## Pieces
    - **Count:** {p["num_pieces"]}
    - **Bracket:** {p["bracket"]}
    - **Base Difficulty:** {p["base_difficulty"]:.3f}

    ## Image Analysis

    | Feature | Value | Level | Difficulty Factor |
    |---------|-------|-------|-------------------|
    | Color Richness | {c["significant_hues"]} hues (sat={c["saturation_ratio"]:.2f}) | {c["level"]} | {c["difficulty_factor"]:.3f} |
    | Color Clustering | ΔE={cl["mean_adjacent_color_diff"]:.1f} | {cl["level"]} | {cl["difficulty_factor"]:.3f} |
    | Texture | edges={t["edge_density"]:.4f}, entropy={t["texture_entropy"]:.3f} | {t["edge_level"]}/{t["texture_level"]} | {t["difficulty_factor"]:.3f} |
    | Pattern | periodicity={pat["periodicity_peak"]:.4f} | {pat["level"]} | {pat["difficulty_factor"]:.3f} |
    | Sharpness | Laplacian var={sh["laplacian_variance"]:.1f} | {sh["level"]} | {sh["difficulty_factor"]:.3f} |

    ## Metadata

    | Attribute | Value | Factor |
    |-----------|-------|--------|
    | Cut Shape | {m["cut_shape"]["label"]} | {m["cut_shape"]["difficulty_factor"]:.2f} |
    | Backside | {m["backside"]["label"]} | {m["backside"]["difficulty_factor"]:.2f} |
    | Reference | {m["blind"]["label"]} | {m["blind"]["difficulty_factor"]:.2f} |

    ## Difficulty

    - **Total Score:** {d["total_difficulty"]:.3f}
    - **Level:** {d["level"]}

    ## Time Estimate

    - **Range:** {te["range_hours"]}
    - **Best Case:** {te["best_case_hours"]:.1f} hours
    - **Worst Case:** {te["worst_case_hours"]:.1f} hours
    """)

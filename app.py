"""Piecewise — Jigsaw Puzzle Difficulty Analyzer (Streamlit frontend)."""

import tempfile
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
from PIL import Image

from piecewise.analyser import analyze

st.set_page_config(
    page_title="Piecewise",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

LEVEL_COLORS = {
    "Easy": "#22c55e",
    "Moderate": "#eab308",
    "Challenging": "#f97316",
    "Hard": "#ef4444",
    "Very Hard": "#7c3aed",
}

DIM_LABELS = {
    "pieces": "Pieces Count",
    "color_richness": "Color Richness",
    "color_clustering": "Color Clustering",
    "texture": "Texture",
    "pattern_repetition": "Pattern Repetition",
    "sharpness": "Sharpness",
    "cut_shape": "Cut Shape",
    "backside": "Backside Hints",
    "blind": "Blind Puzzle",
}

CUT_OPTIONS = {
    "Ribbon Cut (规则切割)": "ribbon",
    "Random Cut (随机切割)": "random",
    "Shaped / Irregular (异形切割)": "irregular",
}
BACK_OPTIONS = {
    "None (无背面提示)": "none",
    "Alphabet Zones (字母分区)": "alphabet",
    "Pattern / Picture (背面图案)": "pattern",
}


def dimension_chart(dimensions):
    labels = [DIM_LABELS.get(k, k) for k in dimensions]
    values = list(dimensions.values())
    colors = [
        "#ef4444" if v > 1.4 else "#f97316" if v > 1.0 else "#22c55e" for v in values
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                marker_color=colors,
                text=[f"{v:.2f}" for v in values],
                textposition="outside",
                textfont=dict(size=12),
            )
        ]
    )
    fig.update_layout(
        height=360,
        margin=dict(l=10, r=60, t=10, b=10),
        xaxis=dict(
            title="Difficulty Factor",
            range=[0, max(values) * 1.3 + 0.1],
        ),
        yaxis=dict(autorange="reversed"),
        showlegend=False,
    )
    return fig


def image_features_table(result):
    c = result["image_analysis"]["color"]
    cl = result["image_analysis"]["clustering"]
    t = result["image_analysis"]["texture"]
    pat = result["image_analysis"]["pattern"]
    sh = result["image_analysis"]["sharpness"]

    return [
        {
            "Feature": "Color Richness",
            "Value": f"{c['significant_hues']} hues (sat={c['saturation_ratio']:.2f})",
            "Level": c["level"],
            "Factor": f"{c['difficulty_factor']:.2f}",
        },
        {
            "Feature": "Color Clustering",
            "Value": f"ΔE = {cl['mean_adjacent_color_diff']:.1f} ({cl['region_count']} regions)",
            "Level": cl["level"],
            "Factor": f"{cl['difficulty_factor']:.2f}",
        },
        {
            "Feature": "Texture",
            "Value": f"edges {t['edge_density']:.4f}, entropy {t['texture_entropy']:.3f}",
            "Level": f"{t['edge_level']} / {t['texture_level']}",
            "Factor": f"{t['difficulty_factor']:.3f}",
        },
        {
            "Feature": "Pattern Repetition",
            "Value": f"periodicity peak = {pat['periodicity_peak']:.4f}",
            "Level": pat["level"],
            "Factor": f"{pat['difficulty_factor']:.2f}",
        },
        {
            "Feature": "Sharpness",
            "Value": f"Laplacian variance = {sh['laplacian_variance']:.1f}",
            "Level": sh["level"],
            "Factor": f"{sh['difficulty_factor']:.2f}",
        },
    ]


def meta_features_table(result):
    m = result["meta_analysis"]
    p = result["piece_analysis"]
    return [
        {
            "Attribute": "Piece Count",
            "Value": f"{p['num_pieces']} ({p['bracket']})",
            "Base Difficulty": f"{p['base_difficulty']:.3f}",
        },
        {
            "Attribute": "Cut Shape",
            "Value": m["cut_shape"]["label"],
            "Factor": f"{m['cut_shape']['difficulty_factor']:.2f}",
        },
        {
            "Attribute": "Backside",
            "Value": m["backside"]["label"],
            "Factor": f"{m['backside']['difficulty_factor']:.2f}",
        },
        {
            "Attribute": "Reference Image",
            "Value": m["blind"]["label"],
            "Factor": f"{m['blind']['difficulty_factor']:.2f}",
        },
    ]


# --- UI ---

st.title("🧩 Piecewise")
st.caption(
    "Jigsaw Puzzle Difficulty Analyzer — estimate difficulty & completion time from the box image."
)

with st.sidebar:
    st.header("Parameters")

    uploaded = st.file_uploader(
        "Puzzle image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload the puzzle box / reference image.",
    )

    pieces = st.number_input(
        "Number of pieces",
        min_value=30,
        max_value=50000,
        value=1000,
        step=100,
        help="Total piece count of the puzzle.",
    )

    cut_label = st.selectbox("Piece cut type", list(CUT_OPTIONS))
    cut = CUT_OPTIONS[cut_label]

    back_label = st.selectbox("Backside hints", list(BACK_OPTIONS))
    back = BACK_OPTIONS[back_label]

    blind = st.checkbox("Blind puzzle (no reference image)")

    analyze_btn = st.button("Analyze Puzzle", type="primary", width="stretch")

# --- Main content ---

if not analyze_btn and "result" not in st.session_state:
    st.info("Upload a puzzle image, set parameters, and click **Analyze Puzzle**.")
    st.image(
        "https://placehold.co/600x400/e2e8f0/64748b?text=Puzzle+Image+Preview",
        caption="Preview will appear here",
        width="stretch",
    )

if analyze_btn:
    if not uploaded:
        st.error("Please upload a puzzle image first.")
    else:
        with tempfile.NamedTemporaryFile(
            suffix=Path(uploaded.name).suffix, delete=False
        ) as tmp:
            tmp.write(uploaded.getvalue())
            tmp_path = tmp.name

        with st.spinner("Analyzing puzzle..."):
            try:
                result = analyze(
                    image_path=tmp_path,
                    pieces=int(pieces),
                    cut=cut,
                    back=back,
                    blind=blind,
                )
                st.session_state.result = result
                st.session_state.image = uploaded
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.stop()
            finally:
                Path(tmp_path).unlink(missing_ok=True)

if "result" in st.session_state:
    result = st.session_state.result
    d = result["difficulty"]
    t = result["time_estimate"]
    img = st.session_state.image

    col_img, col_score = st.columns([2, 3])

    with col_img:
        st.image(
            Image.open(img),
            caption=f"Uploaded puzzle image",
            width="stretch",
        )

    with col_score:
        level = d["level"]
        color = LEVEL_COLORS.get(level, "#6b7280")

        st.markdown(
            f"""
        <div style='display:flex; gap:24px; align-items:flex-start; margin-bottom:16px;'>
          <div style='text-align:center;'>
            <div style='font-size:64px; font-weight:800; color:{color}; line-height:1.1;'>{d["total_difficulty"]:.3f}</div>
            <div style='font-size:14px; color:#94a3b8;'>Difficulty Score</div>
          </div>
          <div style='text-align:center;'>
            <div style='font-size:48px; font-weight:700; background:{color}; color:white; padding:4px 20px; border-radius:8px; display:inline-block;'>{level}</div>
            <div style='font-size:14px; color:#94a3b8;'>Level</div>
          </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.metric("Estimated Time", t["range_hours"])
        col_best, col_worst = st.columns(2)
        col_best.metric("Best Case", f"{t['best_case_hours']:.1f} h")
        col_worst.metric("Worst Case", f"{t['worst_case_hours']:.1f} h")

    st.divider()
    st.subheader("Difficulty Breakdown")

    st.plotly_chart(
        dimension_chart(d["dimensions"]),
        width="stretch",
        config={"displayModeBar": False},
    )

    col_img_features, col_meta = st.columns(2)

    with col_img_features:
        st.caption("Image Features")
        st.dataframe(
            image_features_table(result),
            width="stretch",
            hide_index=True,
            column_config={
                "Feature": st.column_config.TextColumn(width="small"),
                "Value": st.column_config.TextColumn(width="medium"),
                "Level": st.column_config.TextColumn(width="small"),
                "Factor": st.column_config.TextColumn(width="small"),
            },
        )

    with col_meta:
        st.caption("Puzzle Metadata")
        st.dataframe(
            meta_features_table(result),
            width="stretch",
            hide_index=True,
        )

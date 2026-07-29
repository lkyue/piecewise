"""Piecewise — Jigsaw Puzzle Difficulty Analyzer (Streamlit frontend)."""

import tempfile
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
from PIL import Image

from piecewise.analyser import analyze
from piecewise.i18n import (
    t,
    level_label,
    dim_label,
    cluster_label,
    pattern_label,
    sharpness_label,
    texture_label,
    color_label,
    piece_bracket_label,
    CUT_OPTIONS,
    BACK_OPTIONS,
)

LEVEL_COLORS = {
    "Easy": "#22c55e",
    "Moderate": "#eab308",
    "Challenging": "#f97316",
    "Hard": "#ef4444",
    "Very Hard": "#7c3aed",
}

# --- init session ---
if "lang" not in st.session_state:
    st.session_state.lang = "zh"

lang = st.session_state.lang


def toggle_lang():
    st.session_state.lang = "en" if st.session_state.lang == "zh" else "zh"


st.set_page_config(
    page_title=t("title", lang),
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.button(
        "🇨🇳 中文" if lang == "en" else "🇬🇧 English",
        on_click=toggle_lang,
        use_container_width=True,
    )

# --- helpers ---


def dimension_chart(dimensions, lang):
    labels = [dim_label(k, lang) for k in dimensions]
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
            title=t("xaxis_title", lang),
            range=[0, max(values) * 1.3 + 0.1],
        ),
        yaxis=dict(autorange="reversed"),
        showlegend=False,
    )
    return fig


def feature_rows(result, lang):
    c = result["image_analysis"]["color"]
    cl = result["image_analysis"]["clustering"]
    tx = result["image_analysis"]["texture"]
    pat = result["image_analysis"]["pattern"]
    sh = result["image_analysis"]["sharpness"]

    return [
        {
            t("feature_col", lang): dim_label("color_richness", lang),
            t(
                "value_col", lang
            ): f"{c['significant_hues']} {t('hues', lang)} ({t('sat', lang)}={c['saturation_ratio']:.2f})",
            t("level_col", lang): color_label(c["level"], lang),
            t("factor_col", lang): f"{c['difficulty_factor']:.2f}",
        },
        {
            t("feature_col", lang): dim_label("color_clustering", lang),
            t(
                "value_col", lang
            ): f"ΔE = {cl['mean_adjacent_color_diff']:.1f} ({cl['region_count']} {t('regions', lang)})",
            t("level_col", lang): cluster_label(cl["level"], lang),
            t("factor_col", lang): f"{cl['difficulty_factor']:.2f}",
        },
        {
            t("feature_col", lang): dim_label("texture", lang),
            t(
                "value_col", lang
            ): f"{t('edges', lang)}={tx['edge_density']:.4f}, {t('entropy', lang)}={tx['texture_entropy']:.3f}",
            t(
                "level_col", lang
            ): f"{texture_label(tx['edge_level'], lang)} / {texture_label(tx['texture_level'], lang)}",
            t("factor_col", lang): f"{tx['difficulty_factor']:.3f}",
        },
        {
            t("feature_col", lang): dim_label("pattern_repetition", lang),
            t(
                "value_col", lang
            ): f"{t('periodicity_peak', lang)} = {pat['periodicity_peak']:.4f}",
            t("level_col", lang): pattern_label(pat["level"], lang),
            t("factor_col", lang): f"{pat['difficulty_factor']:.2f}",
        },
        {
            t("feature_col", lang): dim_label("sharpness", lang),
            t(
                "value_col", lang
            ): f"{t('lap_var', lang)} = {sh['laplacian_variance']:.1f}",
            t("level_col", lang): sharpness_label(sh["level"], lang),
            t("factor_col", lang): f"{sh['difficulty_factor']:.2f}",
        },
    ]


def meta_rows(result, lang):
    p = result["piece_analysis"]
    m = result["meta_analysis"]
    return [
        {
            t("attr_col", lang): dim_label("pieces", lang),
            t(
                "value_col", lang
            ): f"{p['num_pieces']} ({piece_bracket_label(p['bracket'], lang)})",
            t("base_diff_col", lang): f"{p['base_difficulty']:.3f}",
        },
        {
            t("attr_col", lang): dim_label("cut_shape", lang),
            t("value_col", lang): m["cut_shape"]["label"],
            t("base_diff_col", lang): f"{m['cut_shape']['difficulty_factor']:.2f}",
        },
        {
            t("attr_col", lang): dim_label("backside", lang),
            t("value_col", lang): m["backside"]["label"],
            t("base_diff_col", lang): f"{m['backside']['difficulty_factor']:.2f}",
        },
        {
            t("attr_col", lang): dim_label("blind", lang),
            t("value_col", lang): m["blind"]["label"],
            t("base_diff_col", lang): f"{m['blind']['difficulty_factor']:.2f}",
        },
    ]


# --- Sidebar ---

with st.sidebar:
    st.header(t("sidebar_header", lang))

    uploaded = st.file_uploader(
        t("upload_label", lang),
        type=["jpg", "jpeg", "png", "webp"],
        help=t("upload_help", lang),
    )

    pieces = st.number_input(
        t("pieces_label", lang),
        min_value=30,
        max_value=50000,
        value=1000,
        step=100,
        help=t("pieces_help", lang),
    )

    cut_opts = CUT_OPTIONS[lang]
    cut_label = st.selectbox(t("cut_label", lang), list(cut_opts))
    cut = cut_opts[cut_label]

    back_opts = BACK_OPTIONS[lang]
    back_label = st.selectbox(t("back_label", lang), list(back_opts))
    back = back_opts[back_label]

    blind = st.checkbox(t("blind_label", lang))

    analyze_btn = st.button(
        t("analyze_btn", lang), type="primary", use_container_width=True
    )

# --- Main ---

if not analyze_btn and "result" not in st.session_state:
    st.title(f"🧩 {t('title', lang)}")
    st.caption(t("subtitle", lang))
    st.info(t("placeholder_title", lang))
    st.image(
        "https://placehold.co/600x400/e2e8f0/64748b?text=Puzzle+Image+Preview",
        caption=t("preview_caption", lang),
        width="stretch",
    )

if analyze_btn:
    if not uploaded:
        st.error(t("no_image_error", lang))
    else:
        with tempfile.NamedTemporaryFile(
            suffix=Path(uploaded.name).suffix, delete=False
        ) as tmp:
            tmp.write(uploaded.getvalue())
            tmp_path = tmp.name

        with st.spinner(t("analyzing", lang)):
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
                st.error(f"{t('analysis_failed', lang)}: {e}")
                st.stop()
            finally:
                Path(tmp_path).unlink(missing_ok=True)

if "result" in st.session_state:
    result = st.session_state.result
    d = result["difficulty"]
    te = result["time_estimate"]
    img = st.session_state.image

    st.title(f"🧩 {t('title', lang)}")
    st.caption(t("subtitle", lang))

    col_img, col_score = st.columns([2, 3])

    with col_img:
        st.image(
            Image.open(img),
            caption=t("uploaded_caption", lang),
            width="stretch",
        )

    with col_score:
        level_en = d["level"]
        level_display = level_label(level_en, lang)
        color = LEVEL_COLORS.get(level_en, "#6b7280")

        st.markdown(
            f"""
        <div style='display:flex; gap:24px; align-items:flex-start; margin-bottom:16px;'>
          <div style='text-align:center;'>
            <div style='font-size:64px; font-weight:800; color:{color}; line-height:1.1;'>{d["total_difficulty"]:.3f}</div>
            <div style='font-size:14px; color:#94a3b8;'>{t("score_label", lang)}</div>
          </div>
          <div style='text-align:center;'>
            <div style='font-size:48px; font-weight:700; background:{color}; color:white; padding:4px 20px; border-radius:8px; display:inline-block;'>{level_display}</div>
            <div style='font-size:14px; color:#94a3b8;'>{t("level_label", lang)}</div>
          </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        est = te["estimated_hours"]
        est_display = f"{est * 60:.0f} min" if est < 1 else f"{est:.1f}h"
        st.metric(f"⏱ {t('time_label', lang)}", est_display)

        col_range_header, _, _ = st.columns([2, 1, 1])
        col_range_header.caption(t("time_range_label", lang))
        col_best, col_worst = st.columns(2)
        col_best.metric(t("best_case_label", lang), f"{te['best_case_hours']:.1f} h")
        col_worst.metric(t("worst_case_label", lang), f"{te['worst_case_hours']:.1f} h")

    st.divider()
    st.subheader(t("breakdown_title", lang))

    st.plotly_chart(
        dimension_chart(d["dimensions"], lang),
        width="stretch",
        config={"displayModeBar": False},
    )

    col_f, col_m = st.columns(2)

    with col_f:
        st.caption(t("img_features_caption", lang))
        st.dataframe(
            feature_rows(result, lang),
            width="stretch",
            hide_index=True,
            column_config={
                t("feature_col", lang): st.column_config.TextColumn(width="small"),
                t("value_col", lang): st.column_config.TextColumn(width="medium"),
                t("level_col", lang): st.column_config.TextColumn(width="small"),
                t("factor_col", lang): st.column_config.TextColumn(width="small"),
            },
        )

    with col_m:
        st.caption(t("meta_caption", lang))
        st.dataframe(
            meta_rows(result, lang),
            width="stretch",
            hide_index=True,
        )

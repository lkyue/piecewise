"""Internationalization strings for the Piecewise UI."""

LEVELS_EN = {
    "Easy": "Easy",
    "Moderate": "Moderate",
    "Challenging": "Challenging",
    "Hard": "Hard",
    "Very Hard": "Very Hard",
}

LEVELS_ZH = {
    "Easy": "轻松",
    "Moderate": "适中",
    "Challenging": "有挑战",
    "Hard": "困难",
    "Very Hard": "地狱",
}

CUT_OPTIONS_EN = {
    "Ribbon Cut (规则切割)": "ribbon",
    "Random Cut (随机切割)": "random",
    "Shaped / Irregular (异形切割)": "irregular",
}

CUT_OPTIONS_ZH = {
    "规则切割 (Ribbon Cut)": "ribbon",
    "随机切割 (Random Cut)": "random",
    "异形切割 (Irregular / Shaped)": "irregular",
}

BACK_OPTIONS_EN = {
    "None (无背面提示)": "none",
    "Alphabet Zones (字母分区)": "alphabet",
    "Pattern / Picture (背面图案)": "pattern",
}

BACK_OPTIONS_ZH = {
    "无背面提示 (None)": "none",
    "字母分区 (Alphabet Zones)": "alphabet",
    "背面图案 (Pattern / Picture)": "pattern",
}

DIM_LABELS_EN = {
    "pieces": "Pieces Count",
    "color_richness": "Color Richness",
    "color_clustering": "Color Clustering",
    "texture": "Texture Complexity",
    "pattern_repetition": "Pattern Repetition",
    "sharpness": "Image Sharpness",
    "cut_shape": "Cut Shape",
    "backside": "Backside Hints",
    "blind": "Blind Puzzle",
}

DIM_LABELS_ZH = {
    "pieces": "片数",
    "color_richness": "色彩丰富度",
    "color_clustering": "色彩聚合度",
    "texture": "纹理复杂度",
    "pattern_repetition": "图案重复度",
    "sharpness": "图像锐度",
    "cut_shape": "切割形状",
    "backside": "背面提示",
    "blind": "盲拼",
}

CLUSTER_LEVELS_EN = {
    "scattered": "Scattered",
    "moderate_clumping": "Moderate Clumping",
    "large_patches": "Large Patches",
    "monolithic": "Monolithic",
}

CLUSTER_LEVELS_ZH = {
    "scattered": "零散分布",
    "moderate_clumping": "中等聚合",
    "large_patches": "大色块",
    "monolithic": "单调统一",
}

PATTERN_LEVELS_EN = {
    "unique": "Unique",
    "slightly_repetitive": "Slightly Repetitive",
    "moderately_repetitive": "Moderately Repetitive",
    "highly_repetitive": "Highly Repetitive",
}

PATTERN_LEVELS_ZH = {
    "unique": "无重复",
    "slightly_repetitive": "轻微重复",
    "moderately_repetitive": "中度重复",
    "highly_repetitive": "高度重复",
}

SHARPNESS_LEVELS_EN = {
    "very_blurry": "Very Blurry",
    "blurry": "Blurry",
    "normal": "Normal",
    "sharp": "Sharp",
    "very_sharp": "Very Sharp",
}

SHARPNESS_LEVELS_ZH = {
    "very_blurry": "非常模糊",
    "blurry": "模糊",
    "normal": "正常",
    "sharp": "清晰",
    "very_sharp": "非常清晰",
}

TEXTURE_LEVELS_EN = {
    "rich": "Rich",
    "moderate": "Moderate",
    "sparse": "Sparse",
    "minimal": "Minimal",
    "varied": "Varied",
    "uniform": "Uniform",
    "featureless": "Featureless",
}

TEXTURE_LEVELS_ZH = {
    "rich": "丰富",
    "moderate": "中等",
    "sparse": "稀疏",
    "minimal": "极少",
    "varied": "多变",
    "uniform": "均匀",
    "featureless": "无特征",
}

COLOR_LEVELS_EN = {
    "minimal": "Minimal",
    "low": "Low",
    "moderate": "Moderate",
    "high": "High",
}

COLOR_LEVELS_ZH = {
    "minimal": "极少",
    "low": "低",
    "moderate": "中等",
    "high": "高",
}

PIECE_BRACKETS_EN = {
    "small": "Small",
    "medium": "Medium",
    "large": "Large",
    "xl": "XL",
    "xxl": "XXL",
}

PIECE_BRACKETS_ZH = {
    "small": "小",
    "medium": "中",
    "large": "大",
    "xl": "超大",
    "xxl": "巨幅",
}

T = {
    "en": {
        "title": "Piecewise",
        "subtitle": "Jigsaw Puzzle Difficulty Analyzer — estimate difficulty & completion time from the box image.",
        "sidebar_header": "Parameters",
        "upload_label": "Puzzle image",
        "upload_help": "Upload the puzzle box / reference image.",
        "pieces_label": "Number of pieces",
        "pieces_help": "Total piece count of the puzzle.",
        "cut_label": "Piece cut type",
        "back_label": "Backside hints",
        "blind_label": "Blind puzzle (no reference image)",
        "analyze_btn": "Analyze Puzzle",
        "placeholder_title": "Upload a puzzle image, set parameters, and click Analyze Puzzle.",
        "preview_caption": "Preview will appear here",
        "no_image_error": "Please upload a puzzle image first.",
        "analyzing": "Analyzing puzzle…",
        "analysis_failed": "Analysis failed",
        "score_label": "Difficulty Score",
        "level_label": "Level",
        "time_label": "Estimated Time",
        "time_range_label": "Time Range",
        "best_case_label": "Best Case",
        "worst_case_label": "Worst Case",
        "breakdown_title": "Difficulty Breakdown",
        "img_features_caption": "Image Features",
        "meta_caption": "Puzzle Metadata",
        "xaxis_title": "Difficulty Factor",
        "uploaded_caption": "Uploaded puzzle image",
        "feature_col": "Feature",
        "value_col": "Value",
        "level_col": "Level",
        "factor_col": "Factor",
        "attr_col": "Attribute",
        "base_diff_col": "Base Difficulty",
        "hues": "hues",
        "sat": "sat",
        "edges": "edges",
        "entropy": "entropy",
        "periodicity_peak": "periodicity peak",
        "lap_var": "Laplacian variance",
        "regions": "regions",
    },
    "zh": {
        "title": "拼图难度分析",
        "subtitle": "从拼图盒封面图片出发，估算拼图难度等级和完成时间。",
        "sidebar_header": "参数设置",
        "upload_label": "拼图图片",
        "upload_help": "上传拼图包装盒 / 参考图。",
        "pieces_label": "片数",
        "pieces_help": "拼图的总片数。",
        "cut_label": "切割类型",
        "back_label": "背面提示",
        "blind_label": "盲拼（无参考图）",
        "analyze_btn": "分析拼图",
        "placeholder_title": "上传拼图图片，设置参数，然后点击「分析拼图」。",
        "preview_caption": "预览将在此显示",
        "no_image_error": "请先上传拼图图片。",
        "analyzing": "正在分析拼图…",
        "analysis_failed": "分析失败",
        "score_label": "难度分",
        "level_label": "难度等级",
        "time_label": "预估时间",
        "time_range_label": "时间区间",
        "best_case_label": "最佳情况",
        "worst_case_label": "最坏情况",
        "breakdown_title": "难度拆解",
        "img_features_caption": "图像特征",
        "meta_caption": "拼图元数据",
        "xaxis_title": "难度因子",
        "uploaded_caption": "上传的拼图图片",
        "feature_col": "特征",
        "value_col": "数值",
        "level_col": "等级",
        "factor_col": "因子",
        "attr_col": "属性",
        "base_diff_col": "基础难度",
        "hues": "色相",
        "sat": "饱和度",
        "edges": "边缘密度",
        "entropy": "纹理熵",
        "periodicity_peak": "周期性峰值",
        "lap_var": "拉普拉斯方差",
        "regions": "区域",
    },
}

CUT_OPTIONS = {"en": CUT_OPTIONS_EN, "zh": CUT_OPTIONS_ZH}
BACK_OPTIONS = {"en": BACK_OPTIONS_EN, "zh": BACK_OPTIONS_ZH}
DIM_LABELS = {"en": DIM_LABELS_EN, "zh": DIM_LABELS_ZH}
LEVELS = {"en": LEVELS_EN, "zh": LEVELS_ZH}
CLUSTER_LEVELS = {"en": CLUSTER_LEVELS_EN, "zh": CLUSTER_LEVELS_ZH}
PATTERN_LEVELS = {"en": PATTERN_LEVELS_EN, "zh": PATTERN_LEVELS_ZH}
SHARPNESS_LEVELS = {"en": SHARPNESS_LEVELS_EN, "zh": SHARPNESS_LEVELS_ZH}
TEXTURE_LEVELS = {"en": TEXTURE_LEVELS_EN, "zh": TEXTURE_LEVELS_ZH}
COLOR_LEVELS = {"en": COLOR_LEVELS_EN, "zh": COLOR_LEVELS_ZH}
PIECE_BRACKETS = {"en": PIECE_BRACKETS_EN, "zh": PIECE_BRACKETS_ZH}


def t(key, lang="en"):
    return T.get(lang, T["en"]).get(key, str(key))


def level_label(key, lang="en"):
    return LEVELS.get(lang, LEVELS["en"]).get(key, key)


def dim_label(key, lang="en"):
    return DIM_LABELS.get(lang, DIM_LABELS["en"]).get(key, key)


def cluster_label(key, lang="en"):
    return CLUSTER_LEVELS.get(lang, CLUSTER_LEVELS["en"]).get(key, key)


def pattern_label(key, lang="en"):
    return PATTERN_LEVELS.get(lang, PATTERN_LEVELS["en"]).get(key, key)


def sharpness_label(key, lang="en"):
    return SHARPNESS_LEVELS.get(lang, SHARPNESS_LEVELS["en"]).get(key, key)


def texture_label(key, lang="en"):
    return TEXTURE_LEVELS.get(lang, TEXTURE_LEVELS["en"]).get(key, key)


def color_label(key, lang="en"):
    return COLOR_LEVELS.get(lang, COLOR_LEVELS["en"]).get(key, key)


def piece_bracket_label(key, lang="en"):
    return PIECE_BRACKETS.get(lang, PIECE_BRACKETS["en"]).get(key, key)

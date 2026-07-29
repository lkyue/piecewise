"""Metadata-based feature analysis for puzzle difficulty."""


def analyze_cut_shape(cut_type="ribbon"):
    factors = {
        "ribbon": {"factor": 1.25, "label": "规则切割 (Ribbon Cut)"},
        "irregular": {"factor": 0.60, "label": "异形切割 (Shaped Cut)"},
        "random": {"factor": 0.85, "label": "随机切割 (Random Cut)"},
    }
    info = factors.get(cut_type, factors["ribbon"])
    return {
        "cut_type": cut_type,
        "label": info["label"],
        "difficulty_factor": info["factor"],
    }


def analyze_backside(back_type="none"):
    factors = {
        "none": {"factor": 1.0, "label": "无背面提示"},
        "alphabet": {"factor": 0.70, "label": "字母分区"},
        "pattern": {"factor": 0.45, "label": "背面图案"},
    }
    info = factors.get(back_type, factors["none"])
    return {
        "back_type": back_type,
        "label": info["label"],
        "difficulty_factor": info["factor"],
    }


def analyze_blind(blind=False):
    return {
        "blind": blind,
        "label": "盲拼（无参考图）" if blind else "有参考图",
        "difficulty_factor": 1.60 if blind else 1.0,
    }

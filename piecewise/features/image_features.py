"""Image-level feature extraction for puzzle difficulty analysis."""

import cv2
import numpy as np
from PIL import Image
from skimage.segmentation import slic
from skimage.color import rgb2lab
from skimage.feature import local_binary_pattern
from skimage.graph import rag_mean_color

from piecewise.utils.image_utils import load_image


def analyze_color_richness(image_bgr, bins=180, threshold=0.001):
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    valid = (s > 25) & (v > 50)
    sat_ratio = float(valid.sum() / valid.size)

    hist = cv2.calcHist([h], [0], valid.astype(np.uint8), [bins], [0, 180])
    cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    significant_colors = int(np.sum(hist > threshold))

    if significant_colors < 6:
        level = "minimal"
        score = 2.30
    elif significant_colors < 15:
        level = "low"
        score = 1.50
    elif significant_colors < 30:
        level = "moderate"
        score = 1.00
    else:
        level = "high"
        score = 0.45

    return {
        "significant_hues": significant_colors,
        "saturation_ratio": round(sat_ratio, 3),
        "level": level,
        "difficulty_factor": score,
    }


def analyze_color_clustering(image_bgr, n_segments=200, compactness=20):
    h, w = image_bgr.shape[:2]
    n_segments = min(n_segments, (h * w) // 200)
    n_segments = max(n_segments, 20)

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    segments = slic(
        image_rgb,
        n_segments=n_segments,
        compactness=compactness,
        start_label=1,
        channel_axis=-1,
    )

    lab = rgb2lab(image_rgb)

    graph = rag_mean_color(lab, segments)
    color_diffs = [d["weight"] for (_, _, d) in graph.edges(data=True)]

    if not color_diffs:
        avg_diff = 50.0
    else:
        avg_diff = np.mean(color_diffs)

    region_count = graph.number_of_nodes()

    if avg_diff > 30:
        level = "scattered"
        factor = 0.35
    elif avg_diff > 15:
        level = "moderate_clumping"
        factor = 1.00
    elif avg_diff > 8:
        level = "large_patches"
        factor = 1.30
    else:
        level = "monolithic"
        factor = 2.40

    return {
        "mean_adjacent_color_diff": round(float(avg_diff), 2),
        "region_count": region_count,
        "level": level,
        "difficulty_factor": factor,
    }


def analyze_texture_complexity(image_bgr):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])

    radius = 1
    n_points = 8 * radius
    lbp = local_binary_pattern(gray, n_points, radius, method="uniform")
    lbp_hist, _ = np.histogram(
        lbp.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2)
    )
    lbp_hist = lbp_hist.astype(np.float64)
    lbp_hist /= lbp_hist.sum() + 1e-8
    texture_entropy = -np.sum(lbp_hist * np.log2(lbp_hist + 1e-8))

    max_entropy = np.log2(n_points + 2)
    texture_score = 1.0 - (texture_entropy / max_entropy) if max_entropy > 0 else 0.5

    edge_factor = 2.50 - 2.20 * min(edge_density / 0.15, 1.0)

    if edge_density > 0.15:
        edge_level = "rich"
    elif edge_density > 0.07:
        edge_level = "moderate"
    elif edge_density > 0.03:
        edge_level = "sparse"
    else:
        edge_level = "minimal"

    if texture_score < 0.3:
        tex_level = "varied"
    elif texture_score < 0.5:
        tex_level = "moderate"
    elif texture_score < 0.7:
        tex_level = "uniform"
    else:
        tex_level = "featureless"

    combined_factor = 0.55 * edge_factor + 0.45 * texture_score

    return {
        "edge_density": round(edge_density, 4),
        "edge_level": edge_level,
        "texture_entropy": round(float(texture_entropy), 3),
        "texture_score": round(float(texture_score), 3),
        "texture_level": tex_level,
        "difficulty_factor": round(float(combined_factor), 3),
    }


def analyze_pattern_repetition(image_bgr):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY).astype(np.float64)
    gray -= gray.mean()

    fft = np.fft.fft2(gray)
    ac = np.fft.ifft2(fft * np.conj(fft)).real
    ac = np.fft.fftshift(ac)
    ac /= ac.max() + 1e-10

    h, w = ac.shape
    cy, cx = h // 2, w // 2
    r = max(min(h, w) // 30, 5)
    y1, y2 = max(0, cy - r), min(h, cy + r + 1)
    x1, x2 = max(0, cx - r), min(w, cx + r + 1)
    ac[y1:y2, x1:x2] = 0

    secondary_max = float(ac.max())

    if secondary_max < 0.05:
        level = "unique"
        factor = 0.65
    elif secondary_max < 0.15:
        level = "slightly_repetitive"
        factor = 1.00
    elif secondary_max < 0.30:
        level = "moderately_repetitive"
        factor = 1.30
    else:
        level = "highly_repetitive"
        factor = 2.10

    return {
        "periodicity_peak": round(secondary_max, 4),
        "level": level,
        "difficulty_factor": factor,
    }


def analyze_sharpness(image_bgr):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    if lap_var < 20:
        level = "very_blurry"
        factor = 1.70
    elif lap_var < 60:
        level = "blurry"
        factor = 1.30
    elif lap_var < 150:
        level = "normal"
        factor = 1.00
    elif lap_var < 400:
        level = "sharp"
        factor = 0.85
    else:
        level = "very_sharp"
        factor = 0.75

    return {
        "laplacian_variance": round(float(lap_var), 1),
        "level": level,
        "difficulty_factor": factor,
    }

# Piecewise 🧩

**Systematic jigsaw puzzle difficulty and completion-time estimation.**

Point Piecewise at a picture of your puzzle (the box art works great), tell it the piece count, and get a difficulty score, a qualitative level, and an estimated time range — powered by image analysis, not gut feeling.

- **CLI** — analyze a puzzle with a single command, output as text, JSON, or Markdown
- **Web UI** — a bilingual (English / 中文) Streamlit app with visual breakdown charts
- **Python API** — call `analyze()` directly from your own code

## Installation

Requires Python 3.9+.

```bash
git clone <this-repo>
cd piecewise
pip install -e .

# with the Streamlit web UI
pip install -e ".[ui]"
```

Core dependencies: `opencv-python-headless`, `numpy`, `Pillow`, `scikit-image`, `PyYAML`.

## Usage

### CLI

```bash
piecewise analyze -i box.jpg -p 1000
```

| Flag | Description | Default |
|------|-------------|---------|
| `-i`, `--image` | Path to the puzzle image (required) | — |
| `-p`, `--pieces` | Number of pieces (required) | — |
| `-c`, `--cut` | Piece cut type: `ribbon`, `random`, `irregular` | `ribbon` |
| `-b`, `--back` | Backside hints: `none`, `alphabet`, `pattern` | `none` |
| `--blind` | Puzzle has no reference image (blind puzzle) | off |
| `-f`, `--format` | Output format: `text`, `json`, `markdown` | `text` |

Example with the full report:

```bash
piecewise analyze -i box.jpg -p 1000 --cut random --back alphabet -f markdown
```

Sample output (`text` format):

```
==================================================
Puzzle Difficulty Analysis
==================================================

[Pieces] 1000 pieces (medium) — base difficulty: 1.275

[Image Analysis]
  Color Richness:   178 significant hues (sat ratio=0.99) [high]  difficulty: 0.450
  Color Clustering:  ΔE=55.73 [scattered]  difficulty: 0.350
  Texture:           edges: 0.0547 [sparse], entropy=2.574 [varied]  difficulty: 1.035
  Pattern:           periodicity=0.3802 [highly_repetitive]  difficulty: 2.100
  Sharpness:         Laplacian var=1111.9 [very_sharp]  difficulty: 0.750

[Metadata]
  Cut Shape:   规则切割 (Ribbon Cut)  factor: 1.25
  Backside:    无背面提示  factor: 1.00
  Reference:   有参考图  factor: 1.00

[Difficulty]
  Total Score: 0.893
  Level:       Moderate
  Breakdown:   pieces=1.275 | color_richness=0.450 | ...

[Time Estimate]
  Range:       4.7h – 8.8h
  Best case:   4.7 hours
  Worst case:  8.8 hours
==================================================
```

### Web UI

```bash
pip install -e ".[ui]"
streamlit run app.py
```

Upload a photo of the puzzle, set the piece count and metadata, and hit **Analyze**. The app shows the difficulty score, level, time range, a per-dimension bar chart, and full feature tables — switchable between English and 中文 via the sidebar.

### Python API

```python
from piecewise.analyser import analyze

result = analyze("box.jpg", pieces=1000, cut="random", back="alphabet")

print(result["difficulty"]["level"])        # e.g. "Moderate"
print(result["difficulty"]["dimensions"])   # per-dimension difficulty factors
print(result["time_estimate"]["range_hours"])  # e.g. "4.7h – 8.8h"
```

`analyze()` also accepts `weights` (per-dimension weight overrides) and `config` (tuning parameters) for custom models.

## How It Works

Piecewise models difficulty as **nine weighted dimensions**. Each analyzer produces a *difficulty factor* (higher = harder), and the weighted sum becomes the total difficulty score.

| Dimension | Weight | Measured by | Harder when... |
|-----------|-------:|-------------|----------------|
| Piece count | 0.10 | Power law `(n / 500)^0.35` | More pieces |
| Color richness | 0.24 | Hue histogram of saturated pixels | Fewer distinct hues — big areas of similar color (sky, water, grass) are hard to sort |
| Color clustering | 0.21 | SLIC superpixels + mean ΔE between adjacent regions | Colors clump into large uniform patches |
| Texture complexity | 0.13 | Canny edge density + local-binary-pattern entropy | Few defined edges / featureless texture |
| Pattern repetition | 0.12 | FFT-based autocorrelation periodicity | Repeating patterns make pieces interchangeable |
| Sharpness | 0.07 | Laplacian variance | Blurry, low-contrast images |
| Cut shape | 0.06 | Metadata: ribbon ×1.25, random ×0.85, shaped ×0.60 | — |
| Backside hints | 0.04 | Metadata: none ×1.00, alphabet zones ×0.70, printed pattern ×0.45 | — |
| Blind puzzle | 0.03 | No reference image ×1.60 | — |

### Difficulty Levels

| Score | Level |
|-------|-------|
| < 0.85 | Easy |
| 0.85 – 1.00 | Moderate |
| 1.00 – 1.25 | Challenging |
| 1.25 – 1.60 | Hard |
| ≥ 1.60 | Very Hard |

### Time Estimation

Time is anchored to a reference benchmark: a **500-piece puzzle of moderate difficulty (score 1.0) takes ~4 hours**.

```
estimated = 4h × piece_scale(n) × score^1.5
```

- `piece_scale(n)` is calibrated to real-world benchmarks and interpolated for in-between counts (e.g. ×2.0 at 1000 pcs, ×5.0 at 2000 pcs, ×25 at 5000 pcs).
- The `score^1.5` multiplier scales time super-linearly with difficulty.
- The result is reported as a **±30% range** (best case / worst case).

## Configuration

Model tuning lives in [`config/default.yaml`](config/default.yaml): dimension weights, difficulty-level thresholds, cut/backside/blind factors, the piece-count model, time calibration curves, and binning for each image feature. The CLI and web app use built-in defaults that mirror this file; the Python API lets you override weights and parameters programmatically.

## Project Structure

```
piecewise/
├── app.py                      # Streamlit web UI (English / 中文)
├── config/
│   └── default.yaml            # Model tuning: weights, thresholds, calibration
├── piecewise/
│   ├── cli.py                  # `piecewise` command-line interface
│   ├── analyser.py             # Orchestrator + text / JSON / Markdown reports
│   ├── i18n.py                 # UI strings (English / Chinese)
│   ├── features/
│   │   ├── image_features.py   # Color, texture, pattern, sharpness analysis
│   │   ├── piece_features.py   # Piece-count model
│   │   └── meta_features.py    # Cut shape, backside, blind-puzzle factors
│   ├── scoring/
│   │   ├── difficulty.py       # Weighted difficulty score + levels
│   │   └── time_estimate.py    # Completion-time estimation
│   └── utils/
│       └── image_utils.py      # Image loading helpers
└── archive/                    # Original single-file prototype
```

## Limitations

This tool produces an informed estimate, not a guarantee:

- **Piece cut** — the cut-shape model is a simple metadata factor; it can't see the actual die cut, piece size variation, or false-fit potential.
- **Image quality** — results depend on the photo you provide. A blurry or poorly lit image skews the sharpness and texture measurements (use the box art when possible).
- **Puzzler skill** — time estimates assume an average puzzler; experience, strategy, and mood matter a lot.
- **Environment** — a dedicated, well-lit puzzling space makes a real difference.

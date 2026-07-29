# Jigsaw Puzzle Difficulty Analyzer

This Python script provides an estimated difficulty level and completion time for a jigsaw puzzle based on its number of pieces and the complexity of its image.

## How It Works: The Methodology

The script breaks down puzzle difficulty into two main components:

### 1. Number of Pieces

This is the most significant factor. The script uses a baseline time estimate that grows with the number of pieces. This relationship is not linear; a 1000-piece puzzle is significantly more than twice as hard as a 500-piece one. The script models this increasing difficulty using a power function.

### 2. Image Complexity

This is where the image analysis comes in. A 1000-piece puzzle of a clear, colorful collage is much easier than a 1000-piece puzzle of a solid blue sky. The script quantifies this by measuring two key aspects of the image:

* **Color Variety**:
  * The script analyzes the image's color histogram to see how many distinct colors are present.
  * **Easier puzzles** have a wide range of different colors, allowing you to sort pieces into groups (e.g., "all the red pieces," "all the green pieces").
  * **Harder puzzles** have large areas of similar colors (like sky, water, or grass), making it difficult to distinguish between pieces.
  * The script generates a `color_score` from 0 to 1. A higher score means more color variety (easier).
* **Edge Density**:
  * Using the Canny edge detection algorithm, the script identifies all the distinct lines and edges within the image.
  * **Easier puzzles** have many clear, sharp edges that define objects, textures, and patterns. This helps you identify which pieces belong to which part of the picture.
  * **Harder puzzles** have blurry, out-of-focus areas or large gradients with very few defined edges.
  * The script generates an `edge_score` from 0 to 1. A higher score means more defined edges (easier).

### 3. The Final Calculation

The script combines these factors into a final estimation:

1. It calculates a `complexity_score` for the image by combining the `color_score` and `edge_score`. It gives slightly more weight to color variety. A higher `complexity_score` means a more difficult image.
2. It calculates a base time purely from the number of pieces.
3. It then adjusts this base time using the image's `complexity_score` to get a final estimated time range.
4. It also calculates an overall `difficulty_score` to give you a single number representing the puzzle's challenge, and translates this into a qualitative level like "Easy," "Moderate," or "Challenging."

## How to Use the Script

### 1. Prerequisites

You need to have Python installed on your computer. You will also need to install a few libraries. You can install them using `pip`:

```
pip install opencv-python-headless Pillow numpy
```

*`Pillow` is an image processing library, `opencv-python-headless` is for computer vision tasks, and `numpy` is for numerical operations.*

### 2. Prepare Your Image

Save a clear, well-lit image of the puzzle you want to analyze on your computer. The image on the box is perfect for this. Note the file path to this image.

### 3. Edit the Script

Open the `puzzle_analyzer.py` file in a text editor. At the bottom of the script, you will find the `if __name__ == '__main__':` block. Change the following two lines:

```
# --- USER INPUT ---
PUZZLE_IMAGE_PATH = "path/to/your/puzzle_image.jpg"  # <--- CHANGE THIS
PUZZLE_PIECES = 1000                                # <--- CHANGE THIS
```

* Replace `"path/to/your/puzzle_image.jpg"` with the actual file path to your puzzle image.
* Replace `1000` with the number of pieces in your puzzle.

### 4. Run the Script

Open a terminal or command prompt, navigate to the directory where you saved the script, and run it using:

```
python puzzle_analyzer.py
```

The script will print out its analysis, including the difficulty level and estimated completion time.

## Limitations

This tool provides a sophisticated estimate, but it's important to understand its limitations:

* **Piece Shape:** It cannot analyze the cut of the puzzle pieces. Unusually shaped or "random cut" pieces can add significant difficulty.
* **Image Quality:** The analysis depends on the quality of the image you provide. A blurry or poorly lit photo will not produce an accurate result.
* **Puzzler's Skill:** The time estimate is for an "average" puzzler. Your own experience, strategy, and even your mood can greatly affect your completion time.
* **Environment:** A dedicated, well-lit puzzling space makes a big difference.
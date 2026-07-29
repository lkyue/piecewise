import cv2
import numpy as np
from PIL import Image
import math

def calculate_image_complexity(image_path, resize_dim=500):
    """
    Analyzes an image to determine its complexity based on color variety and edge density.

    Args:
        image_path (str): The path to the puzzle image.
        resize_dim (int): The dimension to resize the image to for consistent analysis.

    Returns:
        dict: A dictionary containing color_score, edge_score, and a final complexity_score.
    """
    try:
        # Open the image using Pillow to handle various formats and orientations
        with Image.open(image_path) as img:
            # Convert to RGB if it's not
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Resize for consistent processing speed
            img.thumbnail((resize_dim, resize_dim))
            # Convert Pillow image to OpenCV format (NumPy array)
            image_np = np.array(img)
            # OpenCV expects BGR, so convert from RGB
            open_cv_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while opening or processing the image: {e}")
        return None

    # 1. Color Complexity Analysis
    # Convert to HSV color space which is better for quantifying color properties
    hsv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2HSV)
    
    # Calculate histogram for the 'Hue' channel (represents color)
    # We use 180 bins for hue
    hist = cv2.calcHist([hsv_image], [0], None, [180], [0, 180])
    
    # Normalize the histogram
    cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    # Calculate the number of significant colors
    # We consider a color "significant" if it covers more than 0.1% of the image
    significant_colors = np.sum(hist > 0.001)
    
    # Color score: More distinct colors make a puzzle easier.
    # We'll create a score between 0 and 1. 
    # A puzzle with very few colors (e.g., a solid blue sky) is very hard.
    # A puzzle with many colors (e.g., a collage) is easier.
    # We'll use a logarithmic scale to moderate the effect.
    # Let's say a good number of colors is around 50.
    color_score = min(math.log(1 + significant_colors) / math.log(50), 1.0)


    # 2. Edge Detection Analysis
    # Convert to grayscale for edge detection
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    
    # Apply a blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # Use Canny edge detector
    edges = cv2.Canny(blurred_image, threshold1=50, threshold2=150)
    
    # Calculate edge density: the proportion of pixels that are edges
    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    # Edge score: More defined edges (higher density) make a puzzle easier.
    # We'll create a score between 0 and 1. A typical "good" density might be around 10-20%.
    # We cap the score at a density of 0.25 to avoid over-weighting very busy images.
    edge_score = min(edge_density / 0.25, 1.0)

    # 3. Final Complexity Score
    # We'll weight color variety slightly more than edge density.
    # These weights can be tuned.
    complexity_score = (0.6 * (1 - color_score)) + (0.4 * (1 - edge_score))
    
    return {
        "color_score": color_score,
        "edge_score": edge_score,
        "complexity_score": complexity_score # Higher score means more complex/difficult
    }


def estimate_puzzle_time(num_pieces, complexity_score):
    """
    Estimates the time to complete a jigsaw puzzle.

    Args:
        num_pieces (int): The number of pieces in the puzzle.
        complexity_score (float): The calculated complexity score from the image analysis.

    Returns:
        dict: A dictionary with difficulty level and estimated time range.
    """
    # Base time estimation (in hours) based on piece count for an "average" puzzle
    # This is a rough heuristic based on common puzzle-solving times.
    if num_pieces <= 100:
        base_time = 0.75
    elif num_pieces <= 300:
        base_time = 2.5
    elif num_pieces <= 500:
        base_time = 5
    elif num_pieces <= 750:
        base_time = 8
    elif num_pieces <= 1000:
        base_time = 12
    elif num_pieces <= 2000:
        base_time = 25
    else:
        base_time = 40 + (num_pieces - 2000) * 0.02

    # Piece difficulty modifier: The difficulty scales faster than the piece count.
    # We use a power function to model this.
    piece_difficulty_factor = (num_pieces / 500) ** 0.3
    
    # Total difficulty score combines piece count factor and image complexity
    # We give more weight to the number of pieces.
    total_difficulty_score = (0.7 * piece_difficulty_factor) + (0.3 * (1 + complexity_score))

    # Determine qualitative difficulty level
    if total_difficulty_score < 1.0:
        difficulty_level = "Easy"
    elif total_difficulty_score < 1.3:
        difficulty_level = "Moderate"
    elif total_difficulty_score < 1.6:
        difficulty_level = "Challenging"
    else:
        difficulty_level = "Very Hard"
        
    # Adjust base time with the complexity modifier
    # The modifier can range from ~0.5 (very simple) to ~1.5 (very complex)
    time_modifier = 1 + (complexity_score - 0.5) 
    
    estimated_time = base_time * time_modifier

    # Provide a time range
    lower_bound = max(0.5, estimated_time * 0.8)
    upper_bound = estimated_time * 1.2
    

    return {
        "difficulty_level": difficulty_level,
        "difficulty_score": round(total_difficulty_score, 2),
        "estimated_time_hrs": f"{estimated_time:.1f}"
    }


if __name__ == '__main__':
    # --- USER INPUT ---
    # To use this script, change the values below.
    # Provide the path to your puzzle's image file.
    # Example for Windows: "C:\\Users\\YourUser\\Pictures\\puzzle.jpg"
    # Example for Mac/Linux: "/home/user/pictures/puzzle.jpg"
    PUZZLE_IMAGE_PATH = "/Users/yuelk/Library/Mobile Documents/com~apple~CloudDocs/Personal/Fun/Puzzle/Pic/" + input("Enter file with extention: ")  # <--- CHANGE THIS
    PUZZLE_PIECES = int(input("Enter number of pieces: "))  # <--- CHANGE THIS

    print(f"Analyzing puzzle: {PUZZLE_IMAGE_PATH}")
    print(f"Number of pieces: {PUZZLE_PIECES}")
    print("-" * 30)

    # Calculate image complexity
    complexity_results = calculate_image_complexity(PUZZLE_IMAGE_PATH)

    if complexity_results:
        # Estimate time based on complexity and piece count
        final_estimate = estimate_puzzle_time(
            PUZZLE_PIECES,
            complexity_results["complexity_score"]
        )

        print(f"Image Complexity Score: {complexity_results['complexity_score']:.3f} (0=Simple, 1=Complex)")
        print(f"  - Color Variety Score: {complexity_results['color_score']:.3f}")
        print(f"  - Edge Density Score: {complexity_results['edge_score']:.3f}")
        print("-" * 30)
        print(f"Overall Difficulty Score: {final_estimate['difficulty_score']}")
        print(f"Difficulty Level: {final_estimate['difficulty_level']}")
        print(f"Estimated Completion Time: {final_estimate['estimated_time_hrs']}")
        print("-" * 30)

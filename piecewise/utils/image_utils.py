"""Image loading and preprocessing utilities."""

import cv2
import numpy as np
from PIL import Image
import math


TARGET_AREA = 400_000
MAX_DIM = 1200


_MPL_PIL_RESIZE = None


def _get_resample_filter():
    global _MPL_PIL_RESIZE
    if _MPL_PIL_RESIZE is None:
        try:
            from PIL import Image as _PIL

            _MPL_PIL_RESIZE = _PIL.Resampling.LANCZOS
        except AttributeError:
            _MPL_PIL_RESIZE = Image.LANCZOS
    return _MPL_PIL_RESIZE


def load_image(image_path, target_area=TARGET_AREA):
    try:
        with Image.open(image_path) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")

            w, h = img.size
            area = w * h
            if area > target_area:
                scale = math.sqrt(target_area / area)
                new_w = int(w * scale)
                new_h = int(h * scale)
                if new_w > MAX_DIM:
                    new_w = MAX_DIM
                    new_h = int(h * (MAX_DIM / w))
                if new_h > MAX_DIM:
                    new_h = MAX_DIM
                    new_w = int(w * (MAX_DIM / h))
                img.thumbnail((new_w, new_h), _get_resample_filter())

            image_np = np.array(img)
        return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    except FileNotFoundError:
        raise FileNotFoundError(f"Image not found: {image_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to load image {image_path}: {e}")

import cv2
import numpy as np
from typing import Tuple


def safe_crop(
    image: np.ndarray,
    bbox: Tuple[int, int, int, int]
) -> np.ndarray:
    """
    Crop image safely with boundary checks.
    bbox: (x1, y1, x2, y2)
    """
    h, w = image.shape[:2]
    x1, y1, x2, y2 = bbox

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w, x2)
    y2 = min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return np.zeros((1, 1, 3), dtype=np.uint8)

    return image[y1:y2, x1:x2]


def resize_keep_aspect(
    image: np.ndarray,
    target_size: int
) -> np.ndarray:
    """
    Resize while keeping aspect ratio.
    """
    h, w = image.shape[:2]
    scale = target_size / max(h, w)

    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(image, (new_w, new_h))

# utils/image_utils.py

import numpy as np
import cv2

def crop(img, bbox):
    """
    img: BGR image (H, W, 3)
    bbox: (x1, y1, x2, y2)
    Returns cropped BGR image. If invalid bbox -> returns empty array.
    """
    x1, y1, x2, y2 = bbox
    h, w = img.shape[:2]

    x1 = max(0, min(x1, w - 1))
    x2 = max(0, min(x2, w))
    y1 = max(0, min(y1, h - 1))
    y2 = max(0, min(y2, h))

    if x2 <= x1 or y2 <= y1:
        return np.zeros((1, 1, 3), dtype=img.dtype)

    return img[y1:y2, x1:x2].copy()

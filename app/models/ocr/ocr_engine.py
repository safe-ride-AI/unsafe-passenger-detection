# app/models/ocr/ocr_engine.py

import easyocr
import numpy as np
import re


class OCRRecognizer:
    def __init__(self, languages=['en'], gpu=False):
        self.reader = easyocr.Reader(languages, gpu=gpu)

    def recognize(self, plate_crop: np.ndarray):
        """
        Input:
            plate_crop (np.ndarray)

        Output:
            plate_text (str) or None
        """

        results = self.reader.readtext(plate_crop)

        if not results:
            return None

        # Choose highest confidence result
        best = max(results, key=lambda x: x[2])
        text = best[1]

        # Clean text (remove non-alphanumeric)
        text = re.sub(r'[^A-Za-z0-9]', '', text)

        return text if text else None

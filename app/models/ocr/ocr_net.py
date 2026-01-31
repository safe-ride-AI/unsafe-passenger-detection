import easyocr
import numpy as np
from typing import List, Tuple


class OCRNet:
    def __init__(self, languages=None, gpu=False):
        if languages is None:
            languages = ["en"]

        self.reader = easyocr.Reader(
            languages,
            gpu=gpu
        )

    def predict(
        self,
        plate_image: np.ndarray
    ) -> List[Tuple[str, float, Tuple[int, int, int, int]]]:
        """
        Returns:
        List of (text, confidence, bbox)
        bbox: x1, y1, x2, y2
        """

        results = self.reader.readtext(plate_image)

        outputs = []

        for bbox, text, conf in results:
            xs = [int(p[0]) for p in bbox]
            ys = [int(p[1]) for p in bbox]

            outputs.append(
                (
                    text,
                    float(conf),
                    (min(xs), min(ys), max(xs), max(ys))
                )
            )

        return outputs

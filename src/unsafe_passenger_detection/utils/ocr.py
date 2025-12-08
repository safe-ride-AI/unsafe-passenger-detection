import easyocr
import numpy as np
import cv2


class PlateOCR:
    def __init__(self, lang=("en",)):
        self.reader = easyocr.Reader(list(lang), gpu=True)

    def read_plate(self, plate_bgr):
        gray = cv2.cvtColor(plate_bgr, cv2.COLOR_BGR2GRAY)
        # optional small preprocessing
        # gray = cv2.bilateralFilter(gray, 9, 75, 75)

        result = self.reader.readtext(gray)

        if not result:
            return "", 0.0

        # pick the highest confidence text
        result.sort(key=lambda x: x[2], reverse=True)
        (bbox, text, conf) = result[0]

        text = text.upper().replace(" ", "")
        return text, float(conf)

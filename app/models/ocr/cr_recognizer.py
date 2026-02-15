# app/models/ocr/cr_recognizer.py

from ultralytics import YOLO
import numpy as np


class CharacterRecognizer:
    def __init__(
        self,
        model_path: str,
        device: str = "cpu",
        conf_threshold: float = 0.4
    ):
        self.model = YOLO(model_path)
        self.model.to(device)
        self.conf_threshold = conf_threshold

    def recognize(self, plate_crop: np.ndarray):
        """
        Input:
            plate_crop (np.ndarray)

        Output:
            List of detected characters:
            [
              {
                'char': 'A',
                'bbox': [x1, y1, x2, y2],
                'confidence': float
              }
            ]
        """

        results = self.model.predict(
            plate_crop,
            conf=self.conf_threshold,
            verbose=False
        )

        characters = []

        if len(results[0].boxes) == 0:
            return characters

        boxes = results[0].boxes

        for i in range(len(boxes)):
            cls_id = int(boxes.cls[i])
            char = self.model.names[cls_id]

            x1, y1, x2, y2 = map(int, boxes.xyxy[i].tolist())
            conf = float(boxes.conf[i])

            characters.append({
                "char": char,
                "bbox": [x1, y1, x2, y2],
                "confidence": conf
            })

        return characters

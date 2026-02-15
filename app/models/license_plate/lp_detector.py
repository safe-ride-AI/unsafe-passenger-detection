# app/models/license_plate/lp_detector.py

from ultralytics import YOLO
import numpy as np


class LicensePlateDetector:
    def __init__(
        self,
        model_path: str,
        device: str = "cpu",
        conf_threshold: float = 0.4
    ):
        self.model = YOLO(model_path)
        self.model.to(device)
        self.conf_threshold = conf_threshold

    def detect(self, vehicle_crop: np.ndarray):
        """
        Input:
            vehicle_crop (np.ndarray)

        Output:
            dict or None
            {
              'bbox': [x1, y1, x2, y2],
              'confidence': float
            }
        """

        results = self.model.predict(
            vehicle_crop,
            conf=self.conf_threshold,
            verbose=False
        )

        if len(results[0].boxes) == 0:
            return None

        # Take highest-confidence plate
        boxes = results[0].boxes
        best_idx = boxes.conf.argmax()

        x1, y1, x2, y2 = map(
            int, boxes.xyxy[best_idx].tolist()
        )

        confidence = float(boxes.conf[best_idx])

        return {
            "bbox": [x1, y1, x2, y2],
            "confidence": confidence
        }

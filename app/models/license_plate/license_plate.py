from ultralytics import YOLO
import numpy as np
from .schema import LicensePlateOutput


class LicensePlateDetector:
    def __init__(self, weights_path: str, device: str = "cpu"):
        self.model = YOLO(weights_path)
        self.device = device

    def predict(self, vehicle_crop: np.ndarray) -> LicensePlateOutput:
        results = self.model(
            vehicle_crop,
            device=self.device,
            verbose=False
        )

        best_conf = 0.0
        best_bbox = None

        for r in results:
            for box in r.boxes:
                conf = float(box.conf[0])
                if conf > best_conf:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    best_conf = conf
                    best_bbox = (x1, y1, x2, y2)

        if best_bbox is None:
            return LicensePlateOutput(
                found=False,
                bbox=None,
                confidence=None
            )

        return LicensePlateOutput(
            found=True,
            bbox=best_bbox,
            confidence=best_conf
        )

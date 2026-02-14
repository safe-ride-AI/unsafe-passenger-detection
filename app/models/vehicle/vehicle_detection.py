from ultralytics import YOLO
import numpy as np
from typing import List
from .schema import VehicleDetection, VehicleNetOutput


class VehicleNet:
    def __init__(self, weights_path: str, device: str = "cpu"):
        self.model = YOLO(weights_path)
        self.device = device

    def predict(self, image: np.ndarray) -> VehicleNetOutput:
        """
        image: OpenCV image (BGR)
        returns: structured vehicle detections
        """
        results = self.model(image, device=self.device, verbose=False)

        detections: List[VehicleDetection] = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append(
                    VehicleDetection(
                        class_name=self.model.names[cls_id],
                        confidence=conf,
                        bbox=(x1, y1, x2, y2)
                    )
                )

        return VehicleNetOutput(vehicles=detections)

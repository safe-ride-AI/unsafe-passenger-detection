from ultralytics import YOLO
import numpy as np
import torch
from typing import List


class VehicleDetector:
    def __init__(self, model_path: str, device: str = None, conf_threshold: float = 0.4):

        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device

        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

        # ✅ FIXED SPELLING HERE
        self.allowed_classes = {
            0: 'bus',
            1: 'suzuki',
            2: 'chingchi'   # corrected
        }

    def detect_and_track(self, frame: np.ndarray) -> List:

        results = self.model.track(
            frame,
            persist=True,
            conf=self.conf_threshold,
            tracker="bytetrack.yaml",
            device=self.device,
            verbose=False
        )

        detections = []

        if results[0].boxes.id is None:
            return detections

        boxes = results[0].boxes

        for i in range(len(boxes)):
            cls_id = int(boxes.cls[i])

            if cls_id not in self.allowed_classes:
                continue

            track_id = int(boxes.id[i])
            x1, y1, x2, y2 = map(int, boxes.xyxy[i].tolist())
            confidence = float(boxes.conf[i])

            detections.append({
                "track_id": track_id,
                "bbox": [x1, y1, x2, y2],
                "class": self.allowed_classes[cls_id],
                "confidence": confidence
            })

        return detections
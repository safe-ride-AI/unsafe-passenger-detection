import cv2
from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path, device="cuda"):
        self.model = YOLO(model_path)
        self.device = device

    def detect(self, img_bgr, conf=0.5):
        results = self.model.predict(img_bgr, conf=conf, device=self.device)
        detections = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                detections.append({
                    "bbox": (x1, y1, x2, y2),
                    "cls": cls_id,
                    "conf": conf
                })

        return detections

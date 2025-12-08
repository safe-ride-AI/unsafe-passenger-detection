from ultralytics import YOLO

class PlateDetector:
    def __init__(self, model_path, device="cuda"):
        self.model = YOLO(model_path)
        self.device = device

    def detect(self, img_bgr, conf=0.4):
        results = self.model.predict(img_bgr, conf=conf, device=self.device)
        
        plates = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                conf = float(box.conf[0])
                plates.append((x1, y1, x2, y2, conf))

        return plates

import cv2
from utils.image_utils import crop

class SafetyPipeline:
    def __init__(self, vehicle_detector, passenger_classifier, plate_detector):
        self.vehicle_detector = vehicle_detector
        self.passenger_classifier = passenger_classifier
        self.plate_detector = plate_detector

    def run(self, img_path):
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Cannot read image: {img_path}")

        result = {
            "image_path": img_path,
            "vehicles": []
        }

        # 1. VEHICLE DETECTION
        vehicles = self.vehicle_detector.detect(img)

        for v in vehicles:
            x1, y1, x2, y2 = v["bbox"]
            crop_vehicle = crop(img, (x1, y1, x2, y2))

            # 2. PASSENGER CLASSIFICATION
            label, conf = self.passenger_classifier.predict(crop_vehicle)

            vehicle_entry = {
                "bbox": v["bbox"],
                "vehicle_class": v["cls"],
                "vehicle_conf": v["conf"],
                "passenger_label": label,
                "passenger_conf": conf,
            }

            # 3. IF UNSAFE → DETECT PLATE
            if label == "unsafe":
                plates = self.plate_detector.detect(crop_vehicle)
                vehicle_entry["plates"] = plates
            else:
                vehicle_entry["plates"] = []

            result["vehicles"].append(vehicle_entry)

        return result

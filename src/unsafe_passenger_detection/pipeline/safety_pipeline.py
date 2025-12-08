import os
import cv2

from unsafe_passenger_detection.utils.image_croping import crop  # you already had a crop helper


class SafetyPipeline:
    """
    Full image pipeline (single frame):

    1) detect vehicles
    2) classify each vehicle as safe / unsafe
    3) if unsafe -> detect plate inside vehicle crop
    4) run OCR on each plate crop
    5) format OCR text for Pakistan plates
    6) optionally save visualization images
    """

    def __init__(
        self,
        vehicle_detector,
        passenger_classifier,
        plate_detector,
        plate_ocr,
        plate_formatter,
        conf_vehicle=0.5,
        conf_plate=0.4,
    ):
        self.vehicle_detector = vehicle_detector
        self.passenger_classifier = passenger_classifier
        self.plate_detector = plate_detector
        self.plate_ocr = plate_ocr
        self.plate_formatter = plate_formatter
        self.conf_vehicle = conf_vehicle
        self.conf_plate = conf_plate

    def run_on_image(self, img_path, save_debug=False, out_dir="results/demo"):
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Cannot read image: {img_path}")

        H, W = img.shape[:2]

        result = {
            "image_path": img_path,
            "image_size": {"H": H, "W": W},
            "vehicles": [],
        }

        # folder for debug images
        debug_imgs = {}
        if save_debug:
            os.makedirs(out_dir, exist_ok=True)
            debug_imgs["original"] = img.copy()
            cv2.imwrite(os.path.join(out_dir, "0_original.jpg"), img)

        # 1) VEHICLE DETECTION
        vehicles = self.vehicle_detector.detect(img, conf=self.conf_vehicle)

        for vidx, v in enumerate(vehicles):
            x1, y1, x2, y2 = v["bbox"]
            crop_vehicle = crop(img, (x1, y1, x2, y2))

            # 2) PASSENGER CLASSIFICATION
            cls_label, cls_conf = self.passenger_classifier.predict(crop_vehicle)

            vehicle_dict = {
                "vehicle_id": vidx,
                "vehicle_bbox": (x1, y1, x2, y2),
                "vehicle_class_id": v["cls"],
                "vehicle_conf": v["conf"],
                "passenger_label": cls_label,   # "safe" / "unsafe"
                "passenger_conf": cls_conf,
                "plates": [],
            }

            if save_debug:
                cv2.imwrite(
                    os.path.join(out_dir, f"1_vehicle_{vidx}_{cls_label}.jpg"),
                    crop_vehicle,
                )

            # 3) ONLY IF UNSAFE → detect plates inside vehicle crop
            if cls_label == "unsafe":
                plates = self.plate_detector.detect(crop_vehicle, conf=self.conf_plate)

                for pidx, p in enumerate(plates):
                    px1, py1, px2, py2 = p["bbox"]
                    crop_plate = crop(crop_vehicle, (px1, py1, px2, py2))

                    # 4) OCR on cropped plate
                    ocr_text, ocr_conf = self.plate_ocr.read_plate(crop_plate)

                    # 5) format number (Pakistan style)
                    formatted = self.plate_formatter.format(ocr_text)

                    plate_entry = {
                        "plate_bbox": (px1, py1, px2, py2),
                        "raw_ocr": ocr_text,
                        "ocr_conf": ocr_conf,
                        "formatted_plate": formatted,
                    }

                    vehicle_dict["plates"].append(plate_entry)

                    if save_debug:
                        cv2.imwrite(
                            os.path.join(out_dir, f"2_vehicle_{vidx}_plate_{pidx}.jpg"),
                            crop_plate,
                        )

            result["vehicles"].append(vehicle_dict)

        # Optionally you could also draw everything on original image and save
        # but keep it simple for now.

        return result, debug_imgs

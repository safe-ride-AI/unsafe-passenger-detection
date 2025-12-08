# scripts/testing_pipeline.py

import torch
from torch.serialization import add_safe_globals
from ultralytics.nn.tasks import DetectionModel

# allow Ultralytics DetectionModel to be unpickled by torch.load(weights_only=True)
add_safe_globals([DetectionModel])

# now import the rest of your code
from unsafe_passenger_detection.detectors.vehicle import VehicleDetector
from unsafe_passenger_detection.detectors.plate import PlateDetector
from unsafe_passenger_detection.detectors.passenger_cls import PassengerClassifier
from unsafe_passenger_detection.pipeline.safety_pipeline import SafetyPipeline



def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device:", device)

    vehicle_detector = VehicleDetector("models/vehicle.pt", device=device)
    plate_detector = PlateDetector("models/plate.pt", device=device)
    passenger_cls = PassengerClassifier("models/passenger_cls.pth", device=device)

    plate_ocr = PlateOCR(lang=("en",))
    plate_formatter = PakistanPlateFormatter()

    pipeline = SafetyPipeline(
        vehicle_detector=vehicle_detector,
        passenger_classifier=passenger_cls,
        plate_detector=plate_detector,
        plate_ocr=plate_ocr,
        plate_formatter=plate_formatter,
        conf_vehicle=0.5,
        conf_plate=0.4,
    )

    img_path = "sample/5133.jpg"   # your test image
    result, debug = pipeline.run_on_image(
        img_path,
        save_debug=True,
        out_dir="results/demo_5133",
    )

    print("\n=== PIPELINE RESULT ===")
    from pprint import pprint
    pprint(result)


if __name__ == "__main__":
    main()

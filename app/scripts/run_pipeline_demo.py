import cv2

from app.models.vehicle.vehicle_detection import VehicleDetector
from app.models.unsafe_behavior.unsafe_classification import UnsafeBehaviorClassifier
from app.models.license_plate.license_plate import LicensePlateDetector
from app.models.ocr.ocr_net import OCRNet

from app.pipelines.tracking import VehicleTracker
from app.pipelines.detection_pipeline import DetectionPipeline


def main():
    # -----------------------
    # Load models
    # -----------------------
    vehicle_detector = VehicleDetector(
        weights_path="app/models/vehicle/weights/vehicle.pt"
    )

    unsafe_detector = UnsafeBehaviorClassifier(
        weights_path="app/models/unsafe_behavior/weights/unsafe.pt"
    )

    license_plate_detector = LicensePlateDetector(
        weights_path="app/models/license_plate/weights/lp.pt"
    )

    ocr_model = OCRNet(
        weights_path="app/models/ocr/weights/ocr.pt"
    )

    tracker = VehicleTracker(frame_rate=30)

    pipeline = DetectionPipeline(
        vehicle_detector=vehicle_detector,
        unsafe_behavior_detector=unsafe_detector,
        license_plate_detector=license_plate_detector,
        ocr_model=ocr_model,
        tracker=tracker,
        min_violation_frames=3,
    )

    # -----------------------
    # Load test input
    # -----------------------
    image_path = "data/samples/test.jpg"
    frame = cv2.imread(image_path)

    if frame is None:
        raise RuntimeError("Failed to load test image")

    # -----------------------
    # Run pipeline
    # -----------------------
    results = pipeline.process_frame(
        frame=frame,
        timestamp=0.0
    )

    # -----------------------
    # Print results
    # -----------------------
    print("\n=== PIPELINE OUTPUT ===")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()

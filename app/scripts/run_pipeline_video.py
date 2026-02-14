import cv2

from app.models.vehicle.vehicle_detection import VehicleNet
from app.models.vehicle.vehicle_detector import VehicleDetector
from app.models.unsafe_behavior.unsafe_classification import UnsafeBehaviorClassifier
from app.models.license_plate.license_plate import LicensePlateDetector
from app.models.ocr.ocr_net import OCRNet

from app.pipelines.frame_extractor import FrameExtractor
from app.pipelines.tracking import VehicleTracker
from app.pipelines.detection_pipeline import DetectionPipeline


def main():
    video_path = "data/1.mp4"

    # -----------------------
    # Load models
    # -----------------------
    vehicle_net = VehicleNet(
        weights_path="app/models/vehicle/weights/vehicle.pt"
    )

    vehicle_detector = VehicleDetector(vehicle_net=vehicle_net)

    unsafe_detector = UnsafeBehaviorClassifier(
        weights_path="app/models/unsafe_behavior/weights/passenger_cls.pth"
    )

    license_plate_detector = LicensePlateDetector(
        weights_path="app/models/license_plate/weights/plate.pt"
    )


    tracker = VehicleTracker(frame_rate=30)

    pipeline = DetectionPipeline(
        vehicle_detector=vehicle_detector,
        unsafe_behavior_detector=unsafe_detector,
        license_plate_detector=license_plate_detector,
        ocr_model=OCRNet(),
        tracker=tracker,
        min_violation_frames=3,  # adjust if needed
    )

    # -----------------------
    # Frame extractor
    # -----------------------
    extractor = FrameExtractor(sample_fps=2)

    # -----------------------
    # Run pipeline on video
    # -----------------------
    for frame_id, timestamp, frame in extractor.extract(video_path):
        results = pipeline.process_frame(
            frame=frame,
            timestamp=timestamp,
        )

        for r in results:
            print(
                f"[VIOLATION] "
                f"time={timestamp:.2f}s "
                f"id={r['track_id']} "
                f"type={r['unsafe_type']} "
                f"plate={r['license_plate']}"
            )

        # OPTIONAL: visualize
        for r in results:
            x1, y1, x2, y2 = r["bbox"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(
                frame,
                f"{r['license_plate']}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )

        cv2.imshow("SafeRide AI - Demo", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

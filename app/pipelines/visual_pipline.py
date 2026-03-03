import cv2
import time

from app.pipelines.frame_reader import VideoFrameReader
from app.models.vehicle.vehicle_detector import VehicleDetector
from app.services.tracking_state import TrackStateManger
from app.utils.image import crop_vehicle, resize_and_pad
from app.models.unsafe_behavior.efficientnet import UnsafeBehaviorClassifier
from app.services.violation_logic import ViolationLogic
from app.models.license_plate.lp_detector import LicensePlateDetector
from app.models.ocr.ocr_engine import OCRRecognizer
from app.services.detection_logger import DetectionLogger


class VisualPipeline:
    def __init__(self, config: dict):

        self.reader = VideoFrameReader(config["video_source"])

        self.detector = VehicleDetector(
            model_path=config["vehicle_model"],
            device=config["device"]
        )

        self.track_state = TrackStateManger(
            max_missing_frames=config.get("max_missing_frames", 30)
        )

        self.unsafe_classifier = UnsafeBehaviorClassifier(
            weights_path=config["unsafe_model"],
            device=config["device"],
            threshold=config.get("unsafe_threshold", 0.5)
        )

        self.violation_logic = ViolationLogic(
            unsafe_frame_threshold=config.get("unsafe_frame_threshold", 1)
        )

        self.lp_detector = LicensePlateDetector(
            model_path=config["lp_model"],
            device=config["device"]
        )

        self.ocr = OCRRecognizer(
            languages=["en"],
            gpu=config.get("device") == "cuda"
        )

        # 🔥 NEW LOGGER
        self.logger = DetectionLogger(
            base_dir=config.get("detection_dir", "data/detections")
        )

        # Display settings
        self.display_max_width = config.get("display_max_width", 1280)
        self.display_max_height = config.get("display_max_height", 720)


    # -----------------------------------------------------------
    # VISUALIZATION
    # -----------------------------------------------------------
    def draw_overlay(
        self,
        frame,
        bbox,
        track_id,
        result,
        plate_bbox=None,
        plate_text=None,
        violation_confirmed=False
    ):
        x1, y1, x2, y2 = bbox

        if violation_confirmed:
            color = (0, 0, 255)
        elif result["label"] == "unsafe":
            color = (0, 165, 255)
        else:
            color = (0, 255, 0)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        label = f"ID:{track_id} | {result['label']} | {result['confidence']:.2f}"
        cv2.putText(
            frame,
            label,
            (x1, max(0, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )

        if plate_bbox:
            px1, py1, px2, py2 = plate_bbox
            cv2.rectangle(frame, (px1, py1), (px2, py2), (255, 255, 0), 2)

            if plate_text:
                cv2.putText(
                    frame,
                    plate_text,
                    (px1, max(0, py1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 0),
                    2
                )

        return frame


    # -----------------------------------------------------------
    # MAIN LOOP
    # -----------------------------------------------------------
    def run(self):

        cv2.namedWindow("Vehicle Violation System", cv2.WINDOW_NORMAL)

        prev_time = time.time()

        for frame, meta in self.reader.frames():

            frame_index = meta["frame_index"]

            detections = self.detector.detect_and_track(frame)

            for det in detections:

                track_id = det["track_id"]
                bbox = det["bbox"]

                self.track_state.update(track_id, frame_index)

                vehicle_crop = crop_vehicle(frame, bbox)
                vehicle_crop = resize_and_pad(vehicle_crop, (224, 224))

                # --- Classification ---
                result = self.unsafe_classifier.predict(vehicle_crop)
                label = result["label"]
                confidence = result["confidence"]

                if label == "unsafe":
                    self.track_state.increament_unsafe(track_id)

                track = self.track_state.tracks.get(track_id)
                if track is None:
                    continue

                violation_confirmed = False
                plate_bbox_global = None
                plate_text = None
                plate_crop = None

                # --- License Plate Detection ---
                plate_result = self.lp_detector.detect(vehicle_crop)

                if plate_result:
                    px1, py1, px2, py2 = plate_result["bbox"]
                    x1, y1, x2, y2 = bbox

                    plate_bbox_global = (
                        x1 + px1,
                        y1 + py1,
                        x1 + px2,
                        y1 + py2
                    )

                    plate_crop = vehicle_crop[py1:py2, px1:px2]
                    plate_text = self.ocr.recognize(plate_crop)

                # --- SAVE EVERY DETECTION ---
                self.logger.save(
                    frame=frame,
                    vehicle_crop=vehicle_crop,
                    track_id=track_id,
                    frame_index=frame_index,
                    label=label,
                    confidence=confidence,
                    plate_text=plate_text,
                    plate_crop=plate_crop
                )

                # --- Violation confirmation ---
                if self.violation_logic.check_violation(track):
                    violation_confirmed = True
                    self.track_state.confirm_violation(track_id)

                frame = self.draw_overlay(
                    frame=frame,
                    bbox=bbox,
                    track_id=track_id,
                    result=result,
                    plate_bbox=plate_bbox_global,
                    plate_text=plate_text,
                    violation_confirmed=violation_confirmed
                )

            # FPS
            current_time = time.time()
            fps = 1.0 / (current_time - prev_time)
            prev_time = current_time

            cv2.putText(
                frame,
                f"FPS: {fps:.2f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            # --- Display scaling ---
            display_frame = frame.copy()
            h, w = display_frame.shape[:2]

            scale = min(
                self.display_max_width / w,
                self.display_max_height / h,
                1.0
            )

            if scale < 1.0:
                display_frame = cv2.resize(
                    display_frame,
                    (int(w * scale), int(h * scale))
                )

            cv2.imshow("Vehicle Violation System", display_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            self.track_state.cleanup(frame_index)

        cv2.destroyAllWindows()
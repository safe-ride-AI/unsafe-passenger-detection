from typing import List, Dict
import numpy as np

from app.pipelines.tracking import VehicleTracker
from app.utils.image_utils import safe_crop


class DetectionPipeline:
    """
    End-to-end detection pipeline:
    frame -> vehicles -> tracking -> unsafe behavior -> license plate -> OCR
    """

    def __init__(
        self,
        vehicle_detector,
        unsafe_behavior_detector,
        license_plate_detector,
        ocr_model,
        tracker: VehicleTracker,
        min_violation_frames: int = 3,
    ):
        self.vehicle_detector = vehicle_detector
        self.unsafe_detector = unsafe_behavior_detector
        self.license_plate_detector = license_plate_detector
        self.ocr_model = ocr_model
        self.tracker = tracker

        self.violation_counter = {}
        self.plate_cache = {}  # track_id -> plate string
        self.min_violation_frames = min_violation_frames

    def process_frame(
        self,
        frame: np.ndarray,
        timestamp: float,
    ) -> List[Dict]:

        results = []

        # 1. Vehicle detection
        detections = self.vehicle_detector.detect(frame)

        # 2. Tracking
        tracks = self.tracker.update(
            detections=detections,
            frame_shape=frame.shape[:2],
        )

        for track in tracks:
            track_id = track["track_id"]
            bbox = track["bbox"]

            vehicle_crop = safe_crop(frame, bbox)
            if vehicle_crop is None:
                continue

            # 3. Unsafe behavior detection
            unsafe_result = self.unsafe_detector.predict(vehicle_crop)
            is_unsafe = unsafe_result.get("unsafe", False)

            if is_unsafe:
                self.violation_counter[track_id] = (
                    self.violation_counter.get(track_id, 0) + 1
                )
            else:
                self.violation_counter.pop(track_id, None)
                continue

            # 4. Confirm violation temporally
            if self.violation_counter.get(track_id, 0) < self.min_violation_frames:
                continue

            # 5. License plate + OCR (ONCE per track)
            plate_text = self.plate_cache.get(track_id)

            if plate_text is None:
                lp_dets = self.license_plate_detector.detect(vehicle_crop)

                if lp_dets is not None and len(lp_dets) > 0:
                    lp_bbox = lp_dets[0][:4]  # best plate
                    plate_crop = safe_crop(vehicle_crop, lp_bbox)

                    if plate_crop is not None:
                        plate_text = self.ocr_model.predict(plate_crop)
                        self.plate_cache[track_id] = plate_text

            results.append(
                {
                    "track_id": track_id,
                    "timestamp": timestamp,
                    "bbox": bbox,
                    "unsafe_type": unsafe_result.get("type"),
                    "confidence": unsafe_result.get("confidence"),
                    "license_plate": plate_text,
                }
            )

        return results

# app/services/storage_service.py

import os
import cv2
import json
from datetime import datetime


class StorageService:
    def __init__(self, base_dir: str = "data/violations"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_violation(
        self,
        track_id: int,
        timestamp_sec: float,
        unsafe_confidence: float,
        vehicle_crop,
        plate_crop=None,
        plate_text: str | None = None
    ):
        """
        Saves violation evidence to disk.
        """

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

        violation_dir = os.path.join(
            self.base_dir,
            f"track_{track_id}_{timestamp}"
        )

        os.makedirs(violation_dir, exist_ok=True)

        # Save vehicle image
        vehicle_path = os.path.join(violation_dir, "vehicle.jpg")
        cv2.imwrite(vehicle_path, vehicle_crop)

        # Save plate image if available
        plate_path = None
        if plate_crop is not None:
            plate_path = os.path.join(violation_dir, "plate.jpg")
            cv2.imwrite(plate_path, plate_crop)

        # Save metadata
        metadata = {
            "track_id": track_id,
            "timestamp_sec": timestamp_sec,
            "unsafe_confidence": unsafe_confidence,
            "plate_text": plate_text,
            "vehicle_image": vehicle_path,
            "plate_image": plate_path
        }

        metadata_path = os.path.join(violation_dir, "metadata.json")

        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

        return metadata

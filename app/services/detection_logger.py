import cv2
from pathlib import Path


class DetectionLogger:
    def __init__(self, base_dir: str = "data/violations"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        frame,
        vehicle_crop,
        track_id,
        frame_index,
        label,
        confidence,
        plate_text=None,
        plate_crop=None
    ):
        """
        Save detection result (safe / unsafe)
        """

        # Folder based on label
        label_dir = self.base_dir / label
        label_dir.mkdir(parents=True, exist_ok=True)

        prefix = f"track_{track_id}_frame_{frame_index}"

        # Save full frame
        cv2.imwrite(str(label_dir / f"{prefix}_full.jpg"), frame)

        # Save vehicle crop
        cv2.imwrite(str(label_dir / f"{prefix}_vehicle.jpg"), vehicle_crop)

        # Save plate crop if available
        if plate_crop is not None:
            cv2.imwrite(str(label_dir / f"{prefix}_plate.jpg"), plate_crop)

        # Save metadata
        meta_path = label_dir / f"{prefix}_meta.txt"
        with open(meta_path, "w") as f:
            f.write(f"track_id: {track_id}\n")
            f.write(f"frame_index: {frame_index}\n")
            f.write(f"label: {label}\n")
            f.write(f"confidence: {confidence:.4f}\n")
            if plate_text:
                f.write(f"plate_text: {plate_text}\n")
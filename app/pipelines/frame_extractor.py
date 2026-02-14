import cv2
from typing import Generator, Tuple
import numpy as np


class FrameExtractor:
    """
    Extract frames from a video at a fixed FPS.
    """

    def __init__(self, sample_fps: int = 2):
        """
        Args:
            sample_fps (int): how many frames per second to extract
        """
        if sample_fps <= 0:
            raise ValueError("sample_fps must be > 0")

        self.sample_fps = sample_fps

    def extract(
        self, video_path: str
    ) -> Generator[Tuple[int, float, np.ndarray], None, None]:
        """
        Yields:
            frame_id (int): incremental id
            timestamp (float): seconds
            frame (np.ndarray): BGR image
        """

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {video_path}")

        video_fps = cap.get(cv2.CAP_PROP_FPS)
        if video_fps <= 0:
            raise RuntimeError("Invalid video FPS")

        frame_interval = int(round(video_fps / self.sample_fps))
        frame_interval = max(frame_interval, 1)

        frame_id = 0
        current_frame = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if current_frame % frame_interval == 0:
                timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                yield frame_id, timestamp, frame
                frame_id += 1

            current_frame += 1

        cap.release()

from typing import List, Dict
import numpy as np
from types import SimpleNamespace

from ultralytics.trackers.byte_tracker import BYTETracker


class VehicleTracker:
    """
    ByteTrack wrapper (Ultralytics-compatible)
    """

    def __init__(self, frame_rate: int = 30):
        args = SimpleNamespace(
            track_thresh=0.5,
            track_buffer=30,
            match_thresh=0.8,
            mot20=False,
        )

        self.tracker = BYTETracker(args, frame_rate)

    def update(
        self,
        detections: np.ndarray,
        frame_shape: tuple,
    ) -> List[Dict]:

        if detections is None or len(detections) == 0:
            online_targets = self.tracker.update(
                np.empty((0, 5)), frame_shape, frame_shape
            )
        else:
            dets = detections[:, :5]  # x1,y1,x2,y2,score
            online_targets = self.tracker.update(
                dets, frame_shape, frame_shape
            )

        tracks = []

        for t in online_targets:
            if not t.is_activated:
                continue

            tracks.append(
                {
                    "track_id": int(t.track_id),
                    "bbox": [
                        int(t.tlbr[0]),
                        int(t.tlbr[1]),
                        int(t.tlbr[2]),
                        int(t.tlbr[3]),
                    ],
                    "score": float(t.score),
                }
            )

        return tracks

import cv2
import os
from pathlib import Path

VIDEO_DIR = "data/raw/videos"
OUTPUT_DIR = "data/processed/frames"
FRAME_INTERVAL = 10  # extract 1 frame every 10 frames


def extract_frames(video_path: Path, output_dir: Path):
    cap = cv2.VideoCapture(str(video_path))
    frame_count = 0
    saved_count = 0

    video_name = video_path.stem
    out_dir = output_dir / video_name
    out_dir.mkdir(parents=True, exist_ok=True)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % FRAME_INTERVAL == 0:
            frame_name = f"{video_name}_{saved_count:06d}.jpg"
            cv2.imwrite(str(out_dir / frame_name), frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"[OK] {video_name}: {saved_count} frames saved")


if __name__ == "__main__":
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    for video_file in Path(VIDEO_DIR).glob("*.mp4"):
        extract_frames(video_file, output_dir)

import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# ========= CONFIG =========
VIDEO_DIR = "reels_downloads"   # folder where your .mp4 reels are stored
OUTPUT_DIR = "frames_output"    # folder where extracted frames will go
FRAME_INTERVAL = 10             # process every nth frame to save time
SSIM_THRESHOLD = 0.75           # lower = more sensitive to scene change
BRIGHTNESS_THRESHOLD = 25       # skip very dark/blank frames
# ==========================


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def is_useful_frame(prev_gray, current_gray):
    """Check if current frame differs enough from previous."""
    if prev_gray is None:
        return True
    try:
        score = ssim(prev_gray, current_gray)
        return score < SSIM_THRESHOLD  # lower similarity → more different
    except Exception:
        return True


def is_bright_enough(frame):
    """Avoid black or empty frames."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)
    return mean_brightness > BRIGHTNESS_THRESHOLD


def extract_useful_frames(video_path, output_subdir):
    """Extract only meaningful frames from one video."""
    ensure_dir(output_subdir)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f" Could not open {video_path}")
        return

    prev_gray = None
    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % FRAME_INTERVAL != 0:
            continue

        if not is_bright_enough(frame):
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if is_useful_frame(prev_gray, gray):
            frame_filename = os.path.join(output_subdir, f"frame_{saved_count+1:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
            prev_gray = gray

    cap.release()
    print(f" {os.path.basename(video_path)} → Saved {saved_count} useful frames.")


def main():
    ensure_dir(OUTPUT_DIR)
    videos = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith(".mp4")]

    if not videos:
        print(" No videos found in", VIDEO_DIR)
        return

    for vid in videos:
        video_path = os.path.join(VIDEO_DIR, vid)
        name = os.path.splitext(vid)[0]
        output_subdir = os.path.join(OUTPUT_DIR, name)
        extract_useful_frames(video_path, output_subdir)

    print("\n All videos processed. Useful frames saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()

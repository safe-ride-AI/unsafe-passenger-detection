from app.pipelines.frame_reader import VideoFrameReader
from app.models.vehicle.vehicle_detector import VehicleDetector
import cv2

reader = VideoFrameReader('data/1.mp4')
vehicle_model = VehicleDetector(model_path="app/models/vehicle/weights/vehicle.pt", device='cpu')

for frame, meta in reader.frames():

    detections = vehicle_model.detect_and_track(frame)

    # 1. Draw all boxes on the original High-Res frame
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        track_id = det['track_id']
        label = f"{det['class']} ID:{track_id}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 2. RESIZE FOR DISPLAY (The Fix)
    # We shrink the image to 1280x720 just so it fits your monitor
    # This does not affect detection accuracy because detections are already done.
    display_frame = cv2.resize(frame, (1280, 1280))

    # 3. Show the resized frame (MOVED OUTSIDE the detections loop)
    cv2.imshow("Vehicle Tracking", display_frame)

    # Press 'q' to quit, 'space' to step
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 4. Cleanup (MOVED OUTSIDE the main loop)
cv2.destroyAllWindows()
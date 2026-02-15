from fastapi import APIRouter, BackgroundTasks
from app.pipelines.video_pipeline import VideoPipeline

router = APIRouter()


@router.post("/detect/video")
def detect_video(
    video_source: str,
    background_tasks: BackgroundTasks
):
    """
    video_source:
    - local file path
    - OR RTSP URL
    """

    config = {
        "video_source": video_source,
        "vehicle_model": "yolov8n.pt",
        "unsafe_model": "app/models/unsafe_behavior/weights/passenger_cls.pth",
        "lp_model": "app/models/license_plate/weights/plate.pt",
        "device": "cpu",
        "unsafe_frame_threshold": 1,
        "evidence_dir": "data/violate"
    }

    pipeline = VideoPipeline(config)

    background_tasks.add_task(pipeline.run)

    return {
        "status": "processing_started",
        "source": video_source
    }

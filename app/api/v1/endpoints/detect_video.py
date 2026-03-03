from fastapi import APIRouter, BackgroundTasks
from app.pipelines.video_pipeline import VideoPipeline
from app.pipelines.visual_pipline import VisualPipeline
import torch


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
    

    device = "cuda" if torch.cuda.is_available() else "cpu"

    config = {
        "video_source": video_source,
        "vehicle_model": "app/models/vehicle/weights/vehicle.pt",
        "unsafe_model": "app/models/unsafe_behavior/weights/passenger_cls.pth",
        "lp_model": "app/models/license_plate/weights/plate.pt",
        "device": device,
        "unsafe_frame_threshold": 1,
        "evidence_dir": "data/violate"
    }

    pipeline = VideoPipeline(config)  ### this is real pipeline it does not show visulization
    ##pipeline = VisualPipeline(config)    ### checking visualization temperory for testing purpose

    background_tasks.add_task(pipeline.run)

    return {
        "status": "processing_started",
        "source": video_source
    }

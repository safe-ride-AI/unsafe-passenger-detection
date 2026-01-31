from typing import Dict


def get_camera_location(camera_id: str) -> Dict[str, float]:
    """
    Returns approximate camera location.
    Can be replaced with DB lookup later.
    """
    CAMERA_LOCATIONS = {
        "cam_01": {"lat": 33.6844, "lon": 73.0479},  # Islamabad
        "cam_02": {"lat": 31.5204, "lon": 74.3587},  # Lahore
    }

    return CAMERA_LOCATIONS.get(
        camera_id,
        {"lat": 0.0, "lon": 0.0}
    )

from typing import List, Tuple
from pydantic import BaseModel

class VehicleDetection(BaseModel):
    class_name: str               # e.g. "bus"
    confidence: float             # 0.0 - 1.0
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2


class VehicleNetOutput(BaseModel):
    vehicles: List[VehicleDetection]

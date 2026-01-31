from pydantic import BaseModel
from typing import Tuple


class LicensePlateOutput(BaseModel):
    found: bool
    bbox: Tuple[int, int, int, int] | None  # x1, y1, x2, y2
    confidence: float | None

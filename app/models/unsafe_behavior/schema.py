from pydantic import BaseModel


class UnsafeBehaviorOutput(BaseModel):
    is_unsafe: bool
    confidence: float

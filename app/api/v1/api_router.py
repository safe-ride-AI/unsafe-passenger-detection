from fastapi import APIRouter
from app.api.v1.endpoints import detect_video, health

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(detect_video.router, tags=["Detection"])
api_router.include_router(health.router, tags=["Health"])

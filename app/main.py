from fastapi import FastAPI
from .api.v1.api_router import api_router

app = FastAPI(
    title="SafeRide AI",
    description="CCTV-based unsafe passenger detection system",
    version="1.0.0"
)

app.include_router(api_router)

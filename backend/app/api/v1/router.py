from fastapi import APIRouter
from app.api.v1.endpoints import health, profiles, logs

api_router = APIRouter()

api_router.include_router(health.router, prefix="")
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
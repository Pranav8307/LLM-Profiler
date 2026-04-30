from fastapi import APIRouter
from app.api.v1.endpoints import health, profiles, logs, generate, analytics, history

api_router = APIRouter()

api_router.include_router(health.router, prefix="")
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
api_router.include_router(generate.router, prefix="/generate", tags=["Generate"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(history.router, prefix="/history", tags=["History"])
from fastapi import APIRouter
from app.schemas.health import HealthResponse
from app.services.health import get_health

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the status of the app and all downstream services.",
    tags=["system"],
)
def health_check() -> HealthResponse:
    return get_health()
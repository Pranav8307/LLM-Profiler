from pydantic import BaseModel
from typing import Dict


class ServiceStatus(BaseModel):
    status: str          # "ok" | "degraded" | "down"
    detail: str = ""


class HealthResponse(BaseModel):
    status: str          # "ok" | "degraded"
    version: str
    environment: str
    services: Dict[str, ServiceStatus]

    model_config = {"json_schema_extra": {
        "example": {
            "status": "ok",
            "version": "0.1.0",
            "environment": "development",
            "services": {
                "database": {"status": "ok"},
                "redis": {"status": "ok"},
            },
        }
    }}
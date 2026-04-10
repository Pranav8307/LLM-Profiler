from app.core.config import get_settings
from app.db.session import check_db_connection
from app.core.redis import check_redis_connection
from app.schemas.health import HealthResponse, ServiceStatus

settings = get_settings()


def get_health() -> HealthResponse:
    db_ok = check_db_connection()
    redis_ok = check_redis_connection()

    services = {
        "database": ServiceStatus(
            status="ok" if db_ok else "down",
            detail="" if db_ok else "Cannot reach PostgreSQL",
        ),
        "redis": ServiceStatus(
            status="ok" if redis_ok else "down",
            detail="" if redis_ok else "Cannot reach Redis",
        ),
    }

    overall = "ok" if all(s.status == "ok" for s in services.values()) else "degraded"

    return HealthResponse(
        status=overall,
        version=settings.app_version,
        environment=settings.app_env,
        services=services,
    )
# app/services/logging_service.py

from sqlalchemy.orm import Session
from app.models.request_log import RequestLog


class LoggingService:

    def log(self, db: Session, data: dict):
        log = RequestLog(
            prompt=data["prompt"],
            response=data["response"],
            latency_ms=data["latency_ms"],
            tokens=data["tokens"],
            cost=data["cost"],
            estimated_cost=data.get("estimated_cost", 0.0),
            cached=data["cached"]
        )

        db.add(log)
        db.commit()
        db.refresh(log)

        return log
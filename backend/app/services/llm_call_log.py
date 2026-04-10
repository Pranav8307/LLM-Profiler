from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.llm_call_log import LLMCallLog, CallStatus
from app.schemas.llm_call_log import LLMCallLogCreate


def log_call(db: Session, data: LLMCallLogCreate) -> LLMCallLog:
    """Persist a single LLM call record."""
    payload = data.model_dump(by_alias=False)
    # Rename metadata_ → metadata for the ORM column
    payload["metadata_"] = payload.pop("metadata_", None)
    log = LLMCallLog(**payload)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def list_logs(
    db: Session,
    profile_id: Optional[UUID] = None,
    status: Optional[CallStatus] = None,
    skip: int = 0,
    limit: int = 50,
) -> tuple[int, list[LLMCallLog]]:
    query = db.query(LLMCallLog)
    if profile_id:
        query = query.filter(LLMCallLog.profile_id == profile_id)
    if status:
        query = query.filter(LLMCallLog.status == status)
    total = query.count()
    items = query.order_by(LLMCallLog.created_at.desc()).offset(skip).limit(limit).all()
    return total, items


def get_log(db: Session, log_id: UUID) -> LLMCallLog:
    from fastapi import HTTPException, status as http_status
    log = db.query(LLMCallLog).filter(LLMCallLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND,
                            detail=f"Log {log_id} not found")
    return log


def get_profile_stats(db: Session, profile_id: UUID) -> dict:
    """
    Aggregate stats for a profile:
    total calls, success rate, avg latency, total tokens, total cost.
    """
    rows = (
        db.query(
            func.count(LLMCallLog.id).label("total_calls"),
            func.sum(
                (LLMCallLog.status == CallStatus.SUCCESS).cast(db.bind.dialect.INTEGER
                    if hasattr(db.bind, "dialect") else "integer")
            ).label("success_count"),
            func.avg(LLMCallLog.latency_ms).label("avg_latency_ms"),
            func.sum(LLMCallLog.total_tokens).label("total_tokens"),
            func.sum(LLMCallLog.estimated_cost_usd).label("total_cost_usd"),
        )
        .filter(LLMCallLog.profile_id == profile_id)
        .one()
    )
    total = rows.total_calls or 0
    return {
        "profile_id": str(profile_id),
        "total_calls": total,
        "success_rate": round((rows.success_count or 0) / total, 4) if total else 0,
        "avg_latency_ms": round(rows.avg_latency_ms or 0, 2),
        "total_tokens": rows.total_tokens or 0,
        "total_cost_usd": round(rows.total_cost_usd or 0, 6),
    }
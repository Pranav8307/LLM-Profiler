from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.llm_call_log import CallStatus
from app.schemas.llm_call_log import LLMCallLogCreate, LLMCallLogResponse, LLMCallLogListResponse
from app.services import llm_call_log as log_service

router = APIRouter()


@router.post(
    "/",
    response_model=LLMCallLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record an LLM call",
)
def create_log(data: LLMCallLogCreate, db: Session = Depends(get_db)):
    return log_service.log_call(db, data)


@router.get(
    "/",
    response_model=LLMCallLogListResponse,
    summary="List call logs (filterable)",
)
def list_logs(
    profile_id: Optional[UUID] = Query(None),
    status: Optional[CallStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    total, items = log_service.list_logs(db, profile_id=profile_id, status=status,
                                         skip=skip, limit=limit)
    return LLMCallLogListResponse(total=total, items=items)


@router.get(
    "/stats/{profile_id}",
    summary="Aggregate stats for a profile",
)
def profile_stats(profile_id: UUID, db: Session = Depends(get_db)):
    return log_service.get_profile_stats(db, profile_id)


@router.get(
    "/{log_id}",
    response_model=LLMCallLogResponse,
    summary="Get a single call log",
)
def get_log(log_id: UUID, db: Session = Depends(get_db)):
    return log_service.get_log(db, log_id)
# app/api/v1/endpoints/history.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.services.analytics_service import AnalyticsService
from app.schemas.log import LogResponse
from app.db.session import get_db

router = APIRouter()

analytics_service = AnalyticsService()


@router.get("/", response_model=List[LogResponse])
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    logs = analytics_service.get_recent_requests(db, limit)
    return logs
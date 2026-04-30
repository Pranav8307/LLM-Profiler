from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsResponse
from app.db.session import get_db

router = APIRouter()

analytics_service = AnalyticsService()


@router.get("/", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    return analytics_service.get_summary(db)
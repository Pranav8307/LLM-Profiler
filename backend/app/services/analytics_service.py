# app/services/analytics_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.request_log import RequestLog


class AnalyticsService:

    def get_summary(self, db: Session):
        total_requests = db.query(func.count(RequestLog.id)).scalar()
        avg_latency = db.query(func.avg(RequestLog.latency_ms)).scalar()
        total_tokens = db.query(func.sum(RequestLog.tokens)).scalar()
        total_cost = db.query(func.sum(RequestLog.cost))\
            .filter(RequestLog.cached == False)\
            .scalar() or 0

        cached_requests = db.query(func.count(RequestLog.id))\
            .filter(RequestLog.cached == True)\
            .scalar()

        cache_hit_rate = (
            (cached_requests / total_requests) * 100
            if total_requests else 0
        )

        cost_saved = db.query(
            func.sum(func.coalesce(RequestLog.estimated_cost, 0))
        ).filter(
            RequestLog.cached == True
        ).scalar() or 0

        return {
            "total_requests": total_requests or 0,
            "avg_latency": round(avg_latency or 0, 2),
            "total_tokens": total_tokens or 0,
            "total_cost": round(total_cost or 0, 6),
            "cache_hit_rate": round(cache_hit_rate, 2),
            "cost_saved": round(cost_saved, 6)
        }

    def get_recent_requests(self, db: Session, limit: int = 10):
        logs = db.query(RequestLog)\
            .order_by(RequestLog.created_at.desc())\
            .limit(limit)\
            .all()

        return logs
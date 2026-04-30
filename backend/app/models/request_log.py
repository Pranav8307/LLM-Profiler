from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from app.db.base import Base


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String)
    response = Column(String)

    latency_ms = Column(Float)
    tokens = Column(Integer)
    cost = Column(Float)
    estimated_cost = Column(Float, nullable=True)
    cached = Column(Boolean)

    created_at = Column(DateTime, default=datetime.utcnow)
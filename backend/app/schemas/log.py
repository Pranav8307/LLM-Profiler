# app/schemas/log.py

from pydantic import BaseModel
from datetime import datetime


class LogResponse(BaseModel):
    id: int
    prompt: str
    response: str
    latency_ms: float
    tokens: int
    cost: float
    cached: bool
    created_at: datetime

    class Config:
        from_attributes = True
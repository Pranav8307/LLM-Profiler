# app/schemas/analytics.py

from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    total_requests: int
    avg_latency: float
    total_tokens: int
    total_cost: float
    cache_hit_rate: float
    cost_saved: float
from pydantic import BaseModel
from typing import Optional


class GenerateRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = "anonymous"


class GenerateResponse(BaseModel):
    answer: str
    latency_ms: float
    tokens: int
    cost: float 
    cached: bool
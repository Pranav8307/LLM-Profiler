from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.llm_call_log import CallStatus


class LLMCallLogCreate(BaseModel):
    profile_id: Optional[UUID] = None
    prompt: str = Field(..., min_length=1)
    response: Optional[str] = None
    status: CallStatus = CallStatus.SUCCESS
    error_message: Optional[str] = None
    prompt_tokens: Optional[int] = Field(None, ge=0)
    completion_tokens: Optional[int] = Field(None, ge=0)
    total_tokens: Optional[int] = Field(None, ge=0)
    latency_ms: Optional[float] = Field(None, ge=0)
    estimated_cost_usd: Optional[float] = Field(None, ge=0)
    metadata_: Optional[Dict[str, Any]] = Field(None, alias="metadata")

    model_config = {"populate_by_name": True}


class LLMCallLogResponse(BaseModel):
    id: UUID
    profile_id: Optional[UUID]
    prompt: str
    response: Optional[str]
    status: CallStatus
    error_message: Optional[str]
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]
    cost: Optional[float] = 0
    latency_ms: Optional[float]
    metadata_: Optional[Dict[str, Any]] = Field(None, alias="metadata")
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}


class LLMCallLogListResponse(BaseModel):
    total: int
    items: list[LLMCallLogResponse]
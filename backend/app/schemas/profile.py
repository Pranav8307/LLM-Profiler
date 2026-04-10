from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


# ── Shared base ────────────────────────────────────────────────────────────────
class ProfileBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, examples=["gpt4-turbo-creative"])
    description: Optional[str] = Field(None, max_length=500)
    provider: str = Field(..., min_length=1, max_length=60, examples=["openai"])
    model: str = Field(..., min_length=1, max_length=120, examples=["gpt-4-turbo"])
    parameters: Dict[str, Any] = Field(default_factory=dict, examples=[{"temperature": 0.7}])
    is_active: bool = True

    @field_validator("provider")
    @classmethod
    def provider_lowercase(cls, v: str) -> str:
        return v.lower().strip()


# ── Create ─────────────────────────────────────────────────────────────────────
class ProfileCreate(ProfileBase):
    pass


# ── Update (all optional for PATCH) ───────────────────────────────────────────
class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = None
    provider: Optional[str] = Field(None, min_length=1, max_length=60)
    model: Optional[str] = Field(None, min_length=1, max_length=120)
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


# ── DB → Response ──────────────────────────────────────────────────────────────
class ProfileResponse(ProfileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── List response ──────────────────────────────────────────────────────────────
class ProfileListResponse(BaseModel):
    total: int
    items: list[ProfileResponse]
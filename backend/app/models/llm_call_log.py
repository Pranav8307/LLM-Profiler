import uuid
from sqlalchemy import Column, Text, Integer, Float, JSON, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base
from app.models.base import TimestampMixin


class CallStatus(str, enum.Enum):
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"


class LLMCallLog(Base, TimestampMixin):
    """
    One row per LLM API call made through the profiler.
    Captures latency, token usage, cost, and raw I/O.
    """
    __tablename__ = "llm_call_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    profile = relationship("Profile", back_populates="call_logs")

    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=True)

    status = Column(
        Enum(CallStatus, create_type=False),
        nullable=False,
        default=CallStatus.SUCCESS,
    )
    error_message = Column(Text, nullable=True)

    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)

    latency_ms = Column(Float, nullable=True)

    estimated_cost_usd = Column(Float, nullable=True)

    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    def __repr__(self):
        return f"<LLMCallLog {self.id} | {self.status} | {self.latency_ms}ms>"
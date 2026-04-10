import uuid
from sqlalchemy import Column, String, Boolean, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.base import TimestampMixin


class Profile(Base, TimestampMixin):
    """
    A named configuration for an LLM call:
    provider + model + parameters.
    e.g. "gpt4-turbo-creative", "claude-3-fast", etc.
    """
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(120), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Provider: "openai" | "anthropic" | "ollama" | etc.
    provider = Column(String(60), nullable=False)
    model = Column(String(120), nullable=False)

    # Model params stored as JSON for flexibility
    # e.g. {"temperature": 0.7, "max_tokens": 1024, "top_p": 0.9}
    parameters = Column(JSON, nullable=False, default=dict)

    is_active = Column(Boolean, default=True, nullable=False)

    # Relationship to call logs
    call_logs = relationship("LLMCallLog", back_populates="profile", lazy="dynamic")

    def __repr__(self):
        return f"<Profile {self.name} | {self.provider}/{self.model}>"
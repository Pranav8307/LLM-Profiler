from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from app.db.session import Base


def utcnow():
    return datetime.now(timezone.utc)


class TimestampMixin:
    """Adds created_at / updated_at to any model."""
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
# Import all models here so that Base.metadata has them registered
# Required for Alembic autogenerate to work correctly.
from app.models.profile import Profile
from app.models.llm_call_log import LLMCallLog, CallStatus

__all__ = ["Profile", "LLMCallLog", "CallStatus"]
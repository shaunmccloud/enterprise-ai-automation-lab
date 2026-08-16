from enum import Enum

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


class AutomationIntent(str, Enum):
    CREATE = "create"
    ADD_USER = "add_user"
    UPDATE = "update"
    DELETE = "delete"
    READ = "read"
    UNKNOWN = "unknown"


class AIRequestClassification(BaseModel):
    """Structured output produced by the AI classification layer."""

    intent: AutomationIntent
    resource: str = Field(min_length=1)
    risk: RiskLevel
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(min_length=1)

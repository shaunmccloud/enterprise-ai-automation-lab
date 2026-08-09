from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AutomationRequestStatus(str, Enum):
    SUBMITTED = "submitted"


class AutomationRequestCreate(BaseModel):
    request: str = Field(min_length=1, max_length=2000)


class AutomationRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    request: str
    status: AutomationRequestStatus = AutomationRequestStatus.SUBMITTED

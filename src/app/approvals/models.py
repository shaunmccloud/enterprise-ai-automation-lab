from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.policy.models import AutomationAction, RequesterRole


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ApprovalRequestCreate(BaseModel):
    requester_role: RequesterRole
    action: AutomationAction
    reason: str


class ApprovalRequest(BaseModel):
    id: UUID
    requester_role: RequesterRole
    action: AutomationAction
    reason: str
    status: ApprovalStatus = ApprovalStatus.PENDING

    @classmethod
    def create(
        cls,
        requester_role: RequesterRole,
        action: AutomationAction,
        reason: str,
    ) -> ApprovalRequest:
        return cls(
            id=uuid4(),
            requester_role=requester_role,
            action=action,
            reason=reason,
        )

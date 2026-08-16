from uuid import UUID

from app.approvals.models import ApprovalRequest, ApprovalStatus
from app.policy.models import AutomationAction, RequesterRole


class ApprovalService:
    def __init__(self) -> None:
        self._approvals: dict[UUID, ApprovalRequest] = {}

    def create_approval(
        self,
        requester_role: RequesterRole,
        action: AutomationAction,
        reason: str,
    ) -> ApprovalRequest:
        approval = ApprovalRequest.create(
            requester_role=requester_role,
            action=action,
            reason=reason,
        )

        self._approvals[approval.id] = approval
        return approval

    def get_approval(self, approval_id: UUID) -> ApprovalRequest | None:
        return self._approvals.get(approval_id)

    def approve(self, approval_id: UUID) -> ApprovalRequest | None:
        approval = self._approvals.get(approval_id)

        if approval is None:
            return None

        if approval.status != ApprovalStatus.PENDING:
            return approval

        approval.status = ApprovalStatus.APPROVED
        return approval

    def reject(self, approval_id: UUID) -> ApprovalRequest | None:
        approval = self._approvals.get(approval_id)

        if approval is None:
            return None

        if approval.status != ApprovalStatus.PENDING:
            return approval

        approval.status = ApprovalStatus.REJECTED
        return approval

from uuid import UUID

from app.approvals.models import (
    ApprovalRequest,
    ApprovalStatus,
)
from app.approvals.service import ApprovalService
from app.policy.models import AutomationAction, RequesterRole


def test_approval_request_defaults_to_pending():
    approval = ApprovalRequest.create(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.ADD_USER,
        reason="Adding a user requires approval.",
    )

    assert approval.status == ApprovalStatus.PENDING


def test_approval_request_preserves_request_details():
    approval = ApprovalRequest.create(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.DELETE_RESOURCE,
        reason="High-risk resource deletion requires approval.",
    )

    assert approval.requester_role == RequesterRole.EMPLOYEE
    assert approval.action == AutomationAction.DELETE_RESOURCE
    assert approval.reason == "High-risk resource deletion requires approval."


def test_approval_request_generates_unique_ids():
    first = ApprovalRequest.create(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.ADD_USER,
        reason="Approval required.",
    )

    second = ApprovalRequest.create(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.ADD_USER,
        reason="Approval required.",
    )

    assert first.id != second.id


def test_approval_service_creates_pending_approval():
    service = ApprovalService()

    approval = service.create_approval(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.ADD_USER,
        reason="Adding a user requires approval.",
    )

    assert approval.status == ApprovalStatus.PENDING
    assert service.get_approval(approval.id) == approval


def test_approval_service_approves_pending_approval():
    service = ApprovalService()

    approval = service.create_approval(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.ADD_USER,
        reason="Adding a user requires approval.",
    )

    result = service.approve(approval.id)

    assert result is not None
    assert result.status == ApprovalStatus.APPROVED


def test_approval_service_rejects_pending_approval():
    service = ApprovalService()

    approval = service.create_approval(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.ADD_USER,
        reason="Adding a user requires approval.",
    )

    result = service.reject(approval.id)

    assert result is not None
    assert result.status == ApprovalStatus.REJECTED


def test_approval_service_does_not_change_completed_approval():
    service = ApprovalService()

    approval = service.create_approval(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.ADD_USER,
        reason="Adding a user requires approval.",
    )

    service.approve(approval.id)
    result = service.reject(approval.id)

    assert result is not None
    assert result.status == ApprovalStatus.APPROVED


def test_approval_service_returns_none_for_unknown_approval():
    service = ApprovalService()

    result = service.get_approval(UUID("00000000-0000-0000-0000-000000000000"))

    assert result is None

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.approvals.models import ApprovalRequest, ApprovalRequestCreate
from app.approvals.service import ApprovalService

router = APIRouter(
    prefix="/api/v1/approvals",
    tags=["approvals"],
)

approval_service = ApprovalService()


@router.post(
    "",
    response_model=ApprovalRequest,
    status_code=status.HTTP_201_CREATED,
)
def create_approval(
    request: ApprovalRequestCreate,
) -> ApprovalRequest:
    return approval_service.create_approval(
        requester_role=request.requester_role,
        action=request.action,
        reason=request.reason,
    )


@router.get(
    "/{approval_id}",
    response_model=ApprovalRequest,
)
def get_approval(approval_id: UUID) -> ApprovalRequest:
    approval = approval_service.get_approval(approval_id)

    if approval is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found",
        )

    return approval


@router.post(
    "/{approval_id}/approve",
    response_model=ApprovalRequest,
)
def approve_approval(approval_id: UUID) -> ApprovalRequest:
    approval = approval_service.approve(approval_id)

    if approval is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found",
        )

    return approval


@router.post(
    "/{approval_id}/reject",
    response_model=ApprovalRequest,
)
def reject_approval(approval_id: UUID) -> ApprovalRequest:
    approval = approval_service.reject(approval_id)

    if approval is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found",
        )

    return approval

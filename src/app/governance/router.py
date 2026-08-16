from fastapi import APIRouter

from app.ai.governance import AIGovernanceService
from app.ai.policy_mapper import AIClassificationPolicyMapper
from app.ai.providers.mock import MockRequestClassifier
from app.governance.models import (
    GovernanceEvaluationRequest,
    GovernanceEvaluationResponse,
)
from app.policy.engine import PolicyEngine

router = APIRouter(
    prefix="/api/v1/governance",
    tags=["governance"],
)


governance_service = AIGovernanceService(
    classifier=MockRequestClassifier(),
    policy_engine=PolicyEngine(),
    policy_mapper=AIClassificationPolicyMapper(),
)


@router.post(
    "/evaluate",
    response_model=GovernanceEvaluationResponse,
)
def evaluate_governance(
    request: GovernanceEvaluationRequest,
) -> GovernanceEvaluationResponse:
    result = governance_service.evaluate_request(
        request=request.request,
        requester_role=request.requester_role,
    )

    return GovernanceEvaluationResponse(
        decision=result.decision,
        reason=result.reason,
    )

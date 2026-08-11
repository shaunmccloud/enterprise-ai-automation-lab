from app.ai.governance import AIGovernanceService
from app.ai.policy_mapper import AIClassificationPolicyMapper
from app.ai.providers.mock import MockRequestClassifier
from app.policy.engine import PolicyEngine
from app.policy.models import PolicyDecision, RequesterRole


def create_service() -> AIGovernanceService:
    return AIGovernanceService(
        classifier=MockRequestClassifier(),
        policy_engine=PolicyEngine(),
        policy_mapper=AIClassificationPolicyMapper(),
    )


def test_low_risk_workspace_request_is_allowed():
    service = create_service()

    result = service.evaluate_request(
        "Create a workspace for the project team.",
        RequesterRole.EMPLOYEE,
    )

    assert result.decision == PolicyDecision.ALLOW


def test_delete_request_requires_approval():
    service = create_service()

    result = service.evaluate_request(
        "Delete the production resource.",
        RequesterRole.EMPLOYEE,
    )

    assert result.decision == PolicyDecision.APPROVAL_REQUIRED


def test_unknown_request_is_denied():
    service = create_service()

    result = service.evaluate_request(
        "Tell me something interesting.",
        RequesterRole.EMPLOYEE,
    )

    assert result.decision == PolicyDecision.DENY

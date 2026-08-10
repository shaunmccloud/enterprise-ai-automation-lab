from app.policy.engine import PolicyEngine
from app.policy.models import (
    AutomationAction,
    PolicyDecision,
    PolicyEvaluationRequest,
    RequesterRole,
    RiskLevel,
)


def test_low_risk_workspace_creation_is_allowed():
    engine = PolicyEngine()

    request = PolicyEvaluationRequest(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.CREATE_WORKSPACE,
        risk=RiskLevel.LOW,
    )

    result = engine.evaluate(request)

    assert result.decision == PolicyDecision.ALLOW


def test_adding_user_requires_approval():
    engine = PolicyEngine()

    request = PolicyEvaluationRequest(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.ADD_USER,
        risk=RiskLevel.MEDIUM,
    )

    result = engine.evaluate(request)

    assert result.decision == PolicyDecision.APPROVAL_REQUIRED


def test_high_risk_resource_deletion_requires_approval():
    engine = PolicyEngine()

    request = PolicyEvaluationRequest(
        requester_role=RequesterRole.MANAGER,
        action=AutomationAction.DELETE_RESOURCE,
        risk=RiskLevel.HIGH,
    )

    result = engine.evaluate(request)

    assert result.decision == PolicyDecision.APPROVAL_REQUIRED


def test_prohibited_action_is_denied():
    engine = PolicyEngine()

    request = PolicyEvaluationRequest(
        requester_role=RequesterRole.ADMINISTRATOR,
        action=AutomationAction.PROHIBITED,
        risk=RiskLevel.LOW,
    )

    result = engine.evaluate(request)

    assert result.decision == PolicyDecision.DENY


def test_unapproved_action_defaults_to_deny():
    engine = PolicyEngine()

    request = PolicyEvaluationRequest(
        requester_role=RequesterRole.EMPLOYEE,
        action=AutomationAction.DELETE_RESOURCE,
        risk=RiskLevel.LOW,
    )

    result = engine.evaluate(request)

    assert result.decision == PolicyDecision.DENY


def test_administrator_can_delete_high_risk_resource():
    engine = PolicyEngine()

    request = PolicyEvaluationRequest(
        requester_role=RequesterRole.ADMINISTRATOR,
        action=AutomationAction.DELETE_RESOURCE,
        risk=RiskLevel.HIGH,
    )

    result = engine.evaluate(request)

    assert result.decision == PolicyDecision.ALLOW

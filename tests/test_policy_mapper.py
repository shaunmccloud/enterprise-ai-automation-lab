from app.ai.models import AIRequestClassification, AutomationIntent, RiskLevel
from app.ai.policy_mapper import AIClassificationPolicyMapper
from app.policy.models import AutomationAction, RequesterRole


def test_create_workspace_maps_to_create_workspace():
    mapper = AIClassificationPolicyMapper()

    classification = AIRequestClassification(
        intent=AutomationIntent.CREATE,
        resource="workspace",
        risk=RiskLevel.LOW,
        confidence=0.95,
        reasoning="The request describes creating a workspace.",
    )

    result = mapper.map_to_policy_request(
        classification,
        RequesterRole.EMPLOYEE,
    )

    assert result.action == AutomationAction.CREATE_WORKSPACE
    assert result.requester_role == RequesterRole.EMPLOYEE
    assert result.risk == RiskLevel.LOW


def test_delete_request_maps_to_delete_resource():
    mapper = AIClassificationPolicyMapper()

    classification = AIRequestClassification(
        intent=AutomationIntent.DELETE,
        resource="resource",
        risk=RiskLevel.HIGH,
        confidence=0.95,
        reasoning="The request describes deleting a resource.",
    )

    result = mapper.map_to_policy_request(
        classification,
        RequesterRole.EMPLOYEE,
    )

    assert result.action == AutomationAction.DELETE_RESOURCE
    assert result.risk == RiskLevel.HIGH


def test_unknown_classification_fails_closed():
    mapper = AIClassificationPolicyMapper()

    classification = AIRequestClassification(
        intent=AutomationIntent.UNKNOWN,
        resource="unknown",
        risk=RiskLevel.UNKNOWN,
        confidence=0.25,
        reasoning="The request could not be classified.",
    )

    result = mapper.map_to_policy_request(
        classification,
        RequesterRole.EMPLOYEE,
    )

    assert result.action == AutomationAction.PROHIBITED

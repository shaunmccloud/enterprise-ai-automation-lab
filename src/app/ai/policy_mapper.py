from app.ai.models import (
    AIRequestClassification,
    AutomationIntent,
)
from app.policy.models import (
    AutomationAction,
    PolicyEvaluationRequest,
    RequesterRole,
)
from app.policy.models import (
    RiskLevel as PolicyRiskLevel,
)


class AIClassificationPolicyMapper:
    """Maps AI classification results into deterministic policy inputs."""

    def map_to_policy_request(
        self,
        classification: AIRequestClassification,
        requester_role: RequesterRole,
    ) -> PolicyEvaluationRequest:
        action = self._map_action(classification)

        return PolicyEvaluationRequest(
            requester_role=requester_role,
            action=action,
            risk=PolicyRiskLevel(classification.risk.value),
        )

    def _map_action(
        self,
        classification: AIRequestClassification,
    ) -> AutomationAction:
        if (
            classification.intent == AutomationIntent.CREATE
            and classification.resource == "workspace"
        ):
            return AutomationAction.CREATE_WORKSPACE

        if classification.intent == AutomationIntent.ADD_USER:
            return AutomationAction.ADD_USER

        if classification.intent == AutomationIntent.DELETE:
            return AutomationAction.DELETE_RESOURCE

        return AutomationAction.PROHIBITED

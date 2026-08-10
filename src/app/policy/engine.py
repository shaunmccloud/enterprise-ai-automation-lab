from .models import (
    AutomationAction,
    PolicyDecision,
    PolicyEvaluation,
    PolicyEvaluationRequest,
    RequesterRole,
    RiskLevel,
)


class PolicyEngine:
    def evaluate(self, request: PolicyEvaluationRequest) -> PolicyEvaluation:
        if request.action == AutomationAction.PROHIBITED:
            return PolicyEvaluation(
                decision=PolicyDecision.DENY,
                reason="This action is prohibited by policy.",
            )

        if request.action == AutomationAction.CREATE_WORKSPACE:
            return PolicyEvaluation(
                decision=PolicyDecision.ALLOW,
                reason="Low-risk workspace creation is permitted.",
            )

        if request.action == AutomationAction.ADD_USER:
            return PolicyEvaluation(
                decision=PolicyDecision.APPROVAL_REQUIRED,
                reason="Adding users requires human approval.",
            )

        if (
            request.action == AutomationAction.DELETE_RESOURCE
            and request.risk == RiskLevel.HIGH
        ):
            if request.requester_role == RequesterRole.ADMINISTRATOR:
                return PolicyEvaluation(
                    decision=PolicyDecision.ALLOW,
                    reason=("Administrators may perform high-risk resource deletion."),
                )

            return PolicyEvaluation(
                decision=PolicyDecision.APPROVAL_REQUIRED,
                reason="High-risk resource deletion requires approval.",
            )

        return PolicyEvaluation(
            decision=PolicyDecision.DENY,
            reason="No policy explicitly permits this action.",
        )

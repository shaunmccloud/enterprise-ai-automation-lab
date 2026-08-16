from app.ai.classifier import RequestClassifier
from app.ai.policy_mapper import AIClassificationPolicyMapper
from app.approvals.service import ApprovalService
from app.policy.engine import PolicyEngine
from app.policy.models import PolicyDecision, PolicyEvaluation, RequesterRole


class AIGovernanceService:
    """Coordinates AI classification with deterministic policy evaluation."""

    def __init__(
        self,
        classifier: RequestClassifier,
        policy_engine: PolicyEngine,
        policy_mapper: AIClassificationPolicyMapper,
        approval_service: ApprovalService | None = None,
    ) -> None:
        self.classifier = classifier
        self.policy_engine = policy_engine
        self.policy_mapper = policy_mapper
        self.approval_service = approval_service

    def evaluate_request(
        self,
        request: str,
        requester_role: RequesterRole,
    ) -> PolicyEvaluation:
        classification = self.classifier.classify(request)

        policy_request = self.policy_mapper.map_to_policy_request(
            classification,
            requester_role,
        )

        result = self.policy_engine.evaluate(policy_request)

        if (
            result.decision == PolicyDecision.APPROVAL_REQUIRED
            and self.approval_service is not None
        ):
            self.approval_service.create_approval(
                requester_role=requester_role,
                action=policy_request.action,
                reason=result.reason,
            )

        return result

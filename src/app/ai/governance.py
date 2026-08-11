from app.ai.classifier import RequestClassifier
from app.ai.policy_mapper import AIClassificationPolicyMapper
from app.policy.engine import PolicyEngine
from app.policy.models import PolicyEvaluation, RequesterRole


class AIGovernanceService:
    """Coordinates AI classification with deterministic policy evaluation."""

    def __init__(
        self,
        classifier: RequestClassifier,
        policy_engine: PolicyEngine,
        policy_mapper: AIClassificationPolicyMapper,
    ) -> None:
        self.classifier = classifier
        self.policy_engine = policy_engine
        self.policy_mapper = policy_mapper

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

        return self.policy_engine.evaluate(policy_request)

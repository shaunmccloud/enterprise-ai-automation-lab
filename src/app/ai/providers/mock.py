from app.ai.classifier import RequestClassifier
from app.ai.models import (
    AIRequestClassification,
    AutomationIntent,
    RiskLevel,
)


class MockRequestClassifier(RequestClassifier):
    """Deterministic classifier used for development and testing."""

    def classify(self, request: str) -> AIRequestClassification:
        normalized_request = request.lower()

        if "delete" in normalized_request:
            return AIRequestClassification(
                intent=AutomationIntent.DELETE,
                resource="resource",
                risk=RiskLevel.HIGH,
                confidence=0.95,
                reasoning="The request contains a delete operation.",
            )
        if "add a user" in normalized_request or "add user" in normalized_request:
            return AIRequestClassification(
                intent=AutomationIntent.ADD_USER,
                resource="user",
                risk=RiskLevel.MEDIUM,
                confidence=0.95,
                reasoning="The request contains an add-user operation.",
            )

        if "create" in normalized_request:
            return AIRequestClassification(
                intent=AutomationIntent.CREATE,
                resource="workspace",
                risk=RiskLevel.LOW,
                confidence=0.95,
                reasoning="The request contains a create operation.",
            )

        return AIRequestClassification(
            intent=AutomationIntent.UNKNOWN,
            resource="unknown",
            risk=RiskLevel.UNKNOWN,
            confidence=0.25,
            reasoning="The request could not be classified.",
        )

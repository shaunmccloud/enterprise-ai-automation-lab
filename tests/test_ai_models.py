import pytest
from pydantic import ValidationError

from app.ai.models import (
    AIRequestClassification,
    AutomationIntent,
    RiskLevel,
)


def test_valid_classification():
    classification = AIRequestClassification(
        intent=AutomationIntent.CREATE,
        resource="workspace",
        risk=RiskLevel.LOW,
        confidence=0.94,
        reasoning="The request describes creating a workspace.",
    )

    assert classification.intent == AutomationIntent.CREATE
    assert classification.resource == "workspace"
    assert classification.risk == RiskLevel.LOW
    assert classification.confidence == 0.94


def test_confidence_must_be_between_zero_and_one():
    with pytest.raises(ValidationError):
        AIRequestClassification(
            intent=AutomationIntent.CREATE,
            resource="workspace",
            risk=RiskLevel.LOW,
            confidence=1.5,
            reasoning="Invalid confidence.",
        )


def test_unknown_values_are_supported():
    classification = AIRequestClassification(
        intent=AutomationIntent.UNKNOWN,
        resource="unknown",
        risk=RiskLevel.UNKNOWN,
        confidence=0.25,
        reasoning="The request could not be confidently classified.",
    )

    assert classification.intent == AutomationIntent.UNKNOWN
    assert classification.risk == RiskLevel.UNKNOWN

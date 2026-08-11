import pytest

from app.ai.classifier import RequestClassifier
from app.ai.models import AIRequestClassification


def test_request_classifier_is_abstract():
    with pytest.raises(TypeError):
        RequestClassifier()


def test_classifier_contract_requires_classify_method():
    assert hasattr(RequestClassifier, "classify")


def test_classifier_returns_expected_type():
    class TestClassifier(RequestClassifier):
        def classify(self, request: str) -> AIRequestClassification:
            return AIRequestClassification(
                intent="create",
                resource="workspace",
                risk="low",
                confidence=0.95,
                reasoning="The request describes creating a workspace.",
            )

    classifier = TestClassifier()

    result = classifier.classify("Create a workspace.")

    assert isinstance(result, AIRequestClassification)
    assert result.intent == "create"
    assert result.resource == "workspace"

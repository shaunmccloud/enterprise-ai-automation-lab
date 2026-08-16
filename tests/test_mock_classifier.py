from app.ai.models import AutomationIntent, RiskLevel
from app.ai.providers.mock import MockRequestClassifier


def test_mock_classifier_identifies_create_request():
    classifier = MockRequestClassifier()

    result = classifier.classify("Create a workspace for the project team.")

    assert result.intent == AutomationIntent.CREATE
    assert result.resource == "workspace"
    assert result.risk == RiskLevel.LOW
    assert result.confidence > 0.9


def test_mock_classifier_identifies_delete_request():
    classifier = MockRequestClassifier()

    result = classifier.classify("Delete the production resource.")

    assert result.intent == AutomationIntent.DELETE
    assert result.risk == RiskLevel.HIGH


def test_mock_classifier_handles_unknown_request():
    classifier = MockRequestClassifier()

    result = classifier.classify("Tell me something interesting.")

    assert result.intent == AutomationIntent.UNKNOWN
    assert result.resource == "unknown"
    assert result.risk == RiskLevel.UNKNOWN


def test_mock_classifier_classifies_add_user():
    classifier = MockRequestClassifier()

    result = classifier.classify("Add a user to the project workspace.")

    assert result.intent == AutomationIntent.ADD_USER
    assert result.resource == "user"

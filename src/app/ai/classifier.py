from abc import ABC, abstractmethod

from .models import AIRequestClassification


class RequestClassifier(ABC):
    """Interface for converting natural-language requests into structured classifications."""

    @abstractmethod
    def classify(self, request: str) -> AIRequestClassification:
        """Classify a natural-language automation request."""
        raise NotImplementedError

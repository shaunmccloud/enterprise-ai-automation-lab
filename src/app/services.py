from uuid import UUID

from .models import AutomationRequest, AutomationRequestCreate


class AutomationRequestService:
    def __init__(self) -> None:
        self._requests: dict[UUID, AutomationRequest] = {}

    def create_request(self, request: AutomationRequestCreate) -> AutomationRequest:
        automation_request = AutomationRequest(request=request.request)
        self._requests[automation_request.id] = automation_request
        return automation_request

    def get_request(self, request_id: UUID) -> AutomationRequest | None:
        return self._requests.get(request_id)

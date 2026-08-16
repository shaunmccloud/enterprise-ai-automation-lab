from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from .approvals.router import router as approvals_router
from .governance.router import router as governance_router
from .models import AutomationRequest, AutomationRequestCreate
from .policy.router import router as policy_router
from .services import AutomationRequestService

app = FastAPI(
    title="Enterprise AI Automation Lab",
    description="Secure, AI-assisted enterprise workflow automation.",
    version="0.1.0",
)
app.include_router(policy_router)
app.include_router(governance_router)
app.include_router(approvals_router)
request_service = AutomationRequestService()


@app.get("/")
def root():
    return {
        "name": "Enterprise AI Automation Lab",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post(
    "/api/v1/automation-requests",
    response_model=AutomationRequest,
    status_code=status.HTTP_201_CREATED,
)
def create_automation_request(
    request: AutomationRequestCreate,
) -> AutomationRequest:
    return request_service.create_request(request)


@app.get(
    "/api/v1/automation-requests/{request_id}",
    response_model=AutomationRequest,
)
def get_automation_request(request_id: UUID) -> AutomationRequest:
    automation_request = request_service.get_request(request_id)

    if automation_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation request not found",
        )

    return automation_request

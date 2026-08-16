from pydantic import BaseModel

from app.policy.models import PolicyDecision, RequesterRole


class GovernanceEvaluationRequest(BaseModel):
    request: str
    requester_role: RequesterRole


class GovernanceEvaluationResponse(BaseModel):
    decision: PolicyDecision
    reason: str

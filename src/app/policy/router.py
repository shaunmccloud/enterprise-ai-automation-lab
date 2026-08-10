from fastapi import APIRouter

from .engine import PolicyEngine
from .models import PolicyEvaluation, PolicyEvaluationRequest

router = APIRouter(prefix="/api/v1/policy", tags=["policy"])

policy_engine = PolicyEngine()


@router.post("/evaluate", response_model=PolicyEvaluation)
def evaluate_policy(
    request: PolicyEvaluationRequest,
) -> PolicyEvaluation:
    return policy_engine.evaluate(request)

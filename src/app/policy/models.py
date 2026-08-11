from enum import Enum

from pydantic import BaseModel


class RequesterRole(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMINISTRATOR = "administrator"


class AutomationAction(str, Enum):
    CREATE_WORKSPACE = "create_workspace"
    ADD_USER = "add_user"
    DELETE_RESOURCE = "delete_resource"
    PROHIBITED = "prohibited"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


class PolicyDecision(str, Enum):
    ALLOW = "allow"
    APPROVAL_REQUIRED = "approval_required"
    DENY = "deny"


class PolicyEvaluationRequest(BaseModel):
    requester_role: RequesterRole
    action: AutomationAction
    risk: RiskLevel


class PolicyEvaluation(BaseModel):
    decision: PolicyDecision
    reason: str

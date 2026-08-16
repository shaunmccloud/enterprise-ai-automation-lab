from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_root():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Enterprise AI Automation Lab",
        "status": "running",
        "version": "0.1.0",
    }


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_automation_request():
    payload = {
        "request": (
            "Create a Slack channel for the Acme project and add the project team."
        )
    }

    with TestClient(app) as client:
        response = client.post("/api/v1/automation-requests", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["request"] == payload["request"]
    assert data["status"] == "submitted"
    assert "id" in data


def test_get_automation_request():
    payload = {"request": "Create a project workspace for the Acme team."}

    with TestClient(app) as client:
        create_response = client.post(
            "/api/v1/automation-requests",
            json=payload,
        )

        request_id = create_response.json()["id"]

        response = client.get(f"/api/v1/automation-requests/{request_id}")

    assert response.status_code == 200
    assert response.json()["id"] == request_id
    assert response.json()["request"] == payload["request"]
    assert response.json()["status"] == "submitted"


def test_get_missing_automation_request():
    missing_id = uuid4()

    with TestClient(app) as client:
        response = client.get(f"/api/v1/automation-requests/{missing_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Automation request not found"}


def test_policy_evaluation_endpoint():
    payload = {
        "requester_role": "employee",
        "action": "create_workspace",
        "risk": "low",
    }

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/policy/evaluate",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json() == {
        "decision": "allow",
        "reason": "Low-risk workspace creation is permitted.",
    }


def test_governance_evaluate_allows_low_risk_workspace():
    payload = {
        "request": "Create a workspace for my project team.",
        "requester_role": "employee",
    }

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/governance/evaluate",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json()["decision"] == "allow"


def test_governance_evaluate_requires_approval_for_delete():
    payload = {
        "request": "Delete a resource from the project workspace.",
        "requester_role": "employee",
    }

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/governance/evaluate",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json()["decision"] == "approval_required"


def test_governance_evaluate_denies_unknown_request():
    payload = {
        "request": "Do something completely unknown.",
        "requester_role": "employee",
    }

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/governance/evaluate",
            json=payload,
        )

    assert response.status_code == 200
    assert response.json()["decision"] == "deny"

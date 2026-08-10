# Enterprise AI Automation Lab

### A reference architecture for secure, AI-assisted enterprise workflow automation.

Enterprise organizations have thousands of requests moving between employees, applications, IT teams, security teams, and business processes.

The technology to automate these workflows already exists. The harder problem is building automation that is **secure, auditable, explainable, and practical to operate at enterprise scale.**

The **Enterprise AI Automation Lab** is an open-source reference project exploring how AI, APIs, deterministic policy controls, and workflow automation can work together without allowing AI to bypass enterprise governance.

> **AI recommends. Policies decide. Automation executes.**

---

## 🎯 The Problem

Consider a request such as:

> "Create a workspace for my project team and add the project members."

In a traditional enterprise environment, that request may involve:

* Request intake
* Identity validation
* Application identification
* Risk assessment
* Policy evaluation
* Manager or security approval
* Automation
* User notification
* Audit documentation

The goal of this project is to demonstrate how much of that workflow can be intelligently automated **while preserving deterministic enterprise controls.**

---

## 🏗️ Current Architecture

The current implementation focuses on the request and policy layers.

```text
                     Automation Request
                              │
                              ▼
                     ┌─────────────────┐
                     │    FastAPI      │
                     │   Request API   │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Policy Router  │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Policy Engine  │
                     └────────┬────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
             ALLOW       APPROVAL       DENY
                              │
                              ▼
                       Future Workflow
                         Execution
```

The policy engine currently evaluates:

* Requester role
* Requested action
* Risk level

and produces one of three deterministic decisions:

```text
ALLOW
APPROVAL_REQUIRED
DENY
```

The engine follows a **fail-closed** approach: actions that are not explicitly permitted are denied.

---
## 📐 Architecture Decisions

Key architectural decisions are documented as Architecture Decision Records (ADRs).

- [ADR-001: AI Does Not Authorize Enterprise Actions](docs/adr/001-ai-does-not-authorize-actions.md) — Separates AI-assisted reasoning from deterministic enterprise authorization.

## 🔐 Core Architecture Principle

### AI should not be the policy engine.

Large language models are powerful reasoning and classification tools, but enterprise authorization decisions should remain deterministic and auditable.

The intended architecture is:

```text
User Request
     │
     ▼
AI / Intent Classification
     │
     ▼
Structured Automation Request
     │
     ▼
Deterministic Policy Engine
     │
     ├── ALLOW
     ├── APPROVAL_REQUIRED
     └── DENY
     │
     ▼
Workflow Execution
     │
     ▼
Audit Event
```

AI can interpret intent and recommend actions.

**Policy controls determine what is actually permitted.**

---

## ⚙️ Implemented

### Automation Request API

The application currently provides:

```text
GET  /
GET  /health

POST /api/v1/automation-requests
GET  /api/v1/automation-requests/{request_id}
```

### Policy Evaluation API

Policy decisions can be evaluated through:

```text
POST /api/v1/policy/evaluate
```

Example request:

```json
{
  "requester_role": "employee",
  "action": "create_workspace",
  "risk": "low"
}
```

Example response:

```json
{
  "decision": "allow",
  "reason": "Low-risk workspace creation is permitted."
}
```

### Policy Engine

The current policy model demonstrates:

| Scenario                                   | Decision          |
| ------------------------------------------ | ----------------- |
| Employee creates a low-risk workspace      | Allow             |
| Employee adds a user                       | Approval required |
| Employee deletes a high-risk resource      | Approval required |
| Manager deletes a high-risk resource       | Approval required |
| Administrator deletes a high-risk resource | Allow             |
| Prohibited action                          | Deny              |
| Unrecognized/unapproved scenario           | Deny              |

---

## 🧪 Engineering Practices

The project uses automated validation throughout development.

### Testing

* Pytest
* Unit tests for policy behavior
* API contract tests
* Fail-closed behavior tests

### Code Quality

* Ruff formatting
* Ruff linting
* Python type-aware models with Pydantic
* Feature branches
* Pull requests
* Code review

### Continuous Integration

GitHub Actions automatically validates:

```text
Checkout
   ↓
Python environment
   ↓
Dependency installation
   ↓
Format validation
   ↓
Lint validation
   ↓
Automated tests
```

The repository is designed so that changes must pass automated validation before being merged.

---

## 🧠 Design Philosophy

### 1. AI recommends. Policies decide.

AI systems should not independently authorize enterprise actions.

### 2. Fail closed.

If the system cannot determine that an action is permitted, it should not execute the action.

### 3. Human approval is a first-class capability.

Some actions should require human authorization rather than unrestricted automation.

### 4. Every automated action should be explainable.

The system should eventually be able to answer:

> What happened?

> Why did it happen?

> Which policy allowed it?

> Who requested it?

> What system performed the action?

### 5. Integrations should be replaceable.

The architecture should avoid coupling the core workflow to a single SaaS vendor or AI provider.

### 6. Security belongs in the architecture.

Identity, authorization, policy, auditability, and failure handling should be designed into the system rather than added later.

---

## 🔧 Technology

### Current

- Python 3.14
- FastAPI
- Pydantic
- Pytest
- Ruff
- GitHub Actions
- REST APIs

### Planned

- AI/LLM provider abstractions
- PostgreSQL
- Docker
- Enterprise SaaS APIs
- Workflow orchestration
- Observability

---

## 🗺️ Roadmap

### Phase 1 — Foundation ✅

* [x] Request intake API
* [x] Automation request service
* [x] Policy domain models
* [x] Policy evaluation engine
* [x] Policy evaluation API
* [x] Automated tests
* [x] GitHub Actions CI

### Phase 2 — Intelligence

* [ ] AI request classification
* [ ] Structured AI responses
* [ ] AI provider abstraction
* [ ] Entity extraction
* [ ] Confidence scoring

### Phase 3 — Governance

* [ ] Risk scoring
* [ ] Configurable policies
* [ ] Role-based authorization expansion
* [ ] Approval workflows
* [ ] Audit logging
* [ ] Policy decision history

### Phase 4 — Automation

* [ ] Workflow execution engine
* [ ] Idempotent operations
* [ ] Retry and failure handling
* [ ] External SaaS integrations
* [ ] Notification workflows

### Phase 5 — Enterprise Hardening

* [ ] PostgreSQL persistence
* [ ] Docker deployment
* [ ] Observability
* [ ] Security threat model
* [ ] Architecture decision records
* [ ] Deployment documentation
* [ ] Production-oriented security controls

---

## 🏢 Fictional Enterprise Environment

All examples in this project use a fictional organization.

No proprietary Logitech systems, data, credentials, architecture, or internal processes are used.

The fictional environment represents a modern enterprise using a mixture of:

* Microsoft 365
* Google Workspace
* Slack
* Zoom
* SaaS applications
* Identity providers
* AI services

The goal is to demonstrate **transferable enterprise architecture patterns**, not reproduce any proprietary environment.

---

## 👨‍💻 About

Built by **Shaun McCloud**, an enterprise technology leader focused on AI, automation, digital workplace architecture, security, and organizational transformation.

My work sits at the intersection of **technology, people, and business outcomes**.

This project explores a question I believe will become increasingly important as enterprise AI adoption accelerates:

> **How do we make AI capable of doing useful work without giving it uncontrolled authority?**

---

## 📜 License

This project is released under the MIT License.

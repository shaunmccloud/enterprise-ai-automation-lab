# ADR-001: AI Does Not Authorize Enterprise Actions

* **Status:** Accepted
* **Date:** 2026-08-09
* **Decision Owners:** Enterprise AI Automation Lab
* **Scope:** Authorization and policy evaluation

## Context

Enterprise automation increasingly uses AI systems to interpret natural-language requests, classify intent, extract entities, and recommend actions.

For example, an employee might submit:

> "Create a workspace for my project team and add the project members."

An AI system can be useful for determining that the request represents a workspace-creation operation and extracting the relevant information.

However, allowing an AI model to make the final authorization decision introduces significant risks.

AI model behavior can be probabilistic, difficult to reproduce exactly, sensitive to prompt and context changes, and affected by ambiguous or adversarial input.

Enterprise authorization decisions, by contrast, need to be:

* Deterministic
* Auditable
* Explainable
* Testable
* Consistent
* Governed by explicit organizational policy

The system therefore needs a clear boundary between **AI-assisted reasoning** and **enterprise authorization**.

## Decision

AI systems will **not** be responsible for authorizing enterprise actions.

The architecture separates AI reasoning from deterministic policy enforcement.

The intended flow is:

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

The AI layer may:

* Interpret natural-language requests
* Classify intent
* Extract entities
* Recommend an action
* Provide confidence information
* Identify information that may be missing

The policy layer is responsible for:

* Determining whether an action is permitted
* Applying requester roles and permissions
* Evaluating policy conditions
* Requiring human approval when appropriate
* Denying actions that are not explicitly permitted

The policy engine follows a **fail-closed** model.

If an action cannot be established as permitted by policy, the system denies or routes the request for explicit human approval rather than allowing the AI layer to authorize it.

## Rationale

This separation provides several important properties.

### Determinism

Given the same policy inputs, the policy engine should produce the same decision.

### Auditability

A policy decision can be recorded with the relevant inputs, policy rules, decision, and reason.

### Testability

Authorization behavior can be covered with conventional automated tests without depending on model behavior.

### Security

The AI system cannot grant itself additional authority through a prompt, generated response, or interpretation of a request.

### Replaceability

The AI provider can be changed without redesigning the authorization model.

### Human Oversight

High-risk or ambiguous operations can be routed to a human approval workflow.

## Consequences

### Positive

* Clear security boundary between AI and authorization
* Deterministic policy enforcement
* Easier security review
* Easier automated testing
* Improved auditability
* AI providers can be replaced independently
* Human approval can be incorporated without changing the AI layer
* Policy behavior can evolve independently of AI models

### Negative

* The architecture contains an additional policy layer.
* Some workflows require explicit policy definitions before they can be automated.
* AI cannot independently complete every requested workflow.
* Policy maintenance becomes an ongoing operational responsibility.

These tradeoffs are intentional.

The objective is not maximum automation.

The objective is **safe, governed automation that can operate at enterprise scale.**

## Security Considerations

The policy engine is treated as a security boundary.

AI-generated output must be treated as untrusted input to the policy layer.

The system must not assume that:

* An AI recommendation is authorized.
* A model's confidence represents security approval.
* Natural-language intent implies permission.
* A model can safely interpret organizational policy without deterministic enforcement.

Authorization decisions should be based on structured inputs and explicit policy rules.

## Future Implications

Future AI capabilities will be designed around this boundary.

Potential future components include:

* LLM-based intent classification
* Structured output validation
* Confidence thresholds
* Retrieval-augmented policy context
* Human approval workflows
* Policy decision logging
* Risk scoring
* External identity and SaaS integrations

These capabilities may improve the quality and efficiency of automation, but they must not bypass the authorization boundary established by this decision.

## Related Principles

This ADR establishes the following project principle:

> **AI recommends. Policies decide. Automation executes.**

This principle should guide future architecture and implementation decisions.

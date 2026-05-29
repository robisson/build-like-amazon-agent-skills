---
name: Design Review
description: Review a technical design before specs or implementation. Evaluate problem clarity, requirements, alternatives, trade-offs, architecture, dependency behavior, security, operations, cost, testability, and simplicity.
leadership_principles:
  - Insist on the Highest Standards
  - Are Right, A Lot
  - Learn and Be Curious
  - Have Backbone; Disagree and Commit
  - Earn Trust
---

# Design Review

## Overview

Design Review is a quality gate before `spec-driven-implementation` and `/build`. Its purpose is to catch design flaws while they are still cheap to fix in a document instead of expensive to fix in code or production.

This is not a meeting format, SLA, or panel process. For an agent, the job is straightforward: evaluate whether the design is clear, complete, simple, operable, and safe enough to become executable specs. If the design does not meet the bar, block progression and explain exactly what must change.

## When to Use

- Before creating implementation specs from a design document
- Before implementing a new service, major component, public API, shared library, infrastructure change, or data model change
- When the design introduces new external dependencies, queues, caches, databases, third-party APIs, or cross-service calls
- When the design changes security boundaries, access models, customer data handling, or operational blast radius
- When a decision is a one-way door or would be expensive to reverse after implementation

## Amazon Context

Amazon-style design review raises the bar by forcing written reasoning before implementation. The reviewer evaluates the design on behalf of the customer and the long-term operators of the system, not on behalf of delivery pressure.

A strong review does not try to prove the author wrong. It makes the design better by surfacing missing assumptions, weak trade-offs, hidden failure modes, operational gaps, and unnecessary complexity.

## The Process

Before reviewing, load `agents/design-bar-raiser.md` and apply that persona's review lens. If the design contains a one-way door decision, also load `agents/principal-engineer.md` and apply that persona to the irreversible decision, blast-radius, and long-term architecture trade-off review.

### 1. Context Assessment

Before reviewing, classify the design:

- [ ] Is this a one-way door? Public API, data migration, security model, data deletion, service split/merge, or irreversible infrastructure change.
- [ ] Does it introduce or change external dependencies? Services, databases, caches, queues, config systems, or third-party APIs.
- [ ] Does it handle customer, Confidential, or Restricted data?
- [ ] Does it affect other teams, shared infrastructure, or public consumers?
- [ ] Does it add operational burden, new alarms, new runbooks, or new on-call failure modes?

If any answer is yes, review at full depth. If all answers are no, perform a lightweight review but still verify clarity, correctness, simplicity, and testability.

### 2. Review Dimensions

#### Problem And Requirements

- [ ] The problem statement links to customer value or an approved Working Backwards artifact.
- [ ] Requirements are specific, testable, and avoid vague terms like "fast", "scalable", or "reasonable".
- [ ] Success metrics and non-functional requirements have numeric targets.
- [ ] Scope boundaries are explicit: what is included, what is excluded, and what is deferred.

#### Alternatives And Trade-Offs

- [ ] At least two real alternatives are considered.
- [ ] Rejected alternatives are plausible, not strawmen.
- [ ] When a pattern from `patterns/INDEX.md` plausibly fits the workload (per its criteria), it appears as a real alternative or is the chosen approach — not silently skipped.
- [ ] If a pattern is adopted, its Skill Impact Map is reflected in Architecture, Operational Concerns, and Testing.
- [ ] Trade-offs are explicit: "choosing X over Y because Z, accepting W."
- [ ] The design explains why the simplest viable option is sufficient or why extra complexity is necessary.

#### Architecture And Data

- [ ] Component boundaries are clear.
- [ ] Data ownership, schema evolution, and migration strategy are defined.
- [ ] Backward compatibility is preserved or a versioned migration path exists.
- [ ] Failure domains and blast radius are understood.
- [ ] The design works at expected scale and has a credible path to 10x scale.

#### Dependency Behavior

- [ ] Every external dependency is listed and classified as critical or non-critical.
- [ ] Timeout, retry, backoff, jitter, circuit breaker, and bulkhead strategies are defined where relevant.
- [ ] Non-critical dependencies degrade gracefully.
- [ ] Dependency health is observable through metrics, logs, traces, and alarms.
- [ ] The design does not couple this system's availability unnecessarily to a weaker dependency.

#### Security And Privacy

- [ ] Data classification is stated.
- [ ] Authentication and authorization paths are clear.
- [ ] IAM, roles, policies, and secrets follow least privilege.
- [ ] Threat model risks are addressed or explicitly deferred with rationale.
- [ ] Sensitive data is protected in transit, at rest, and in logs.

#### Operations

- [ ] Deployment and rollback strategy are described.
- [ ] Feature flags or safe defaults protect incomplete or risky behavior.
- [ ] Metrics, logs, traces, dashboards, and alarms cover new failure modes.
- [ ] Runbooks are planned for likely failures.
- [ ] The system can be debugged by an on-call engineer without the original author present.

#### Cost And Capacity

- [ ] Cost estimate includes build and run cost.
- [ ] Cost scales predictably with traffic, storage, and dependency usage.
- [ ] Capacity assumptions are backed by numbers.
- [ ] Load, soak, or failure testing is planned for high-risk paths.

#### Testability

- [ ] Unit, integration, contract, and end-to-end test boundaries are clear.
- [ ] Property-based tests or invariants are defined for complex logic.
- [ ] Dependency failure scenarios are testable.
- [ ] Acceptance criteria can be verified from the eventual implementation.

### 3. Blocking Criteria

Block progression to specs or build if any of these are true:

- [ ] Problem or requirements are ambiguous.
- [ ] The design has no real alternatives or trade-off analysis.
- [ ] A pattern from `patterns/INDEX.md` plausibly fits the workload but was not considered as an alternative or as the chosen approach.
- [ ] A one-way door decision lacks explicit sign-off criteria.
- [ ] External dependencies are introduced without failure behavior.
- [ ] Security-sensitive flows lack a threat model or mitigation plan.
- [ ] Data migration, schema evolution, or rollback is undefined.
- [ ] Operational readiness is missing for new failure modes.
- [ ] The design is too complex to explain clearly and succinctly.
- [ ] Acceptance criteria cannot be tested.

## Feedback Format

Use concise, evidence-backed findings:

| Prefix | Meaning | Required Action |
|--------|---------|-----------------|
| `[BLOCKING]` | Must be resolved before specs or build. | Revise the design. |
| `[IMPORTANT]` | Should be resolved unless there is a documented reason not to. | Fix or justify. |
| `[QUESTION]` | Clarification needed; may reveal a blocker. | Answer in the design. |
| `[NOTE]` | Non-blocking observation or future consideration. | Optional. |

Write feedback like this:

```markdown
[BLOCKING] Dependency failure behavior is undefined.
The design adds synchronous calls to PaymentService but does not define timeout,
retry, circuit breaker, fallback behavior, or customer impact when PaymentService
is unavailable. Add dependency classification and failure handling before specs.
```

## Review Outcome

Return one of these outcomes:

| Outcome | Meaning | Next Step |
|---------|---------|-----------|
| **APPROVED** | Design meets the bar. | Proceed to `spec-driven-implementation`. |
| **APPROVED WITH NOTES** | Design is sound; notes are non-blocking. | Proceed, carrying notes into specs if relevant. |
| **NEEDS REVISION** | One or more blocking issues exist. | Revise design and re-run review before specs. |
| **RE-DESIGN** | Core approach is flawed or too complex. | Rework the approach before continuing. |

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "We'll think through trade-offs" | Require alternatives and explicit trade-off statements in the design doc |
| "We'll handle dependency failures" | Require dependency classification and failure behavior before specs |
| "We'll make it operable" | Require metrics, alarms, rollback, and runbook plans in the design |
| "We'll keep it simple" | Require simpler alternatives and a clear complexity justification |
| "We'll verify it later" | Require test strategy and acceptance criteria before implementation |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|----------------|-------------------|
| "We'll figure this out during build" | Build should execute approved decisions, not discover architecture. | Decide in the design doc, then preserve the decision in specs. |
| "The happy path is enough for now" | Most production incidents happen in failure paths, not happy paths. | Add failure modes, fallback behavior, and operational signals. |
| "This dependency is reliable" | Every dependency fails, slows down, or returns bad data eventually. | Define timeout, retry, circuit breaker, fallback, and observability. |
| "This is just an internal API" | Internal APIs become dependencies and create coupling. | Define contract, compatibility expectations, and migration path. |
| "A simpler design might not scale someday" | Future scale does not justify current unnecessary complexity. | Build the simplest design with a credible evolution path. |

## Red Flags

- Alternatives are missing or obviously weak.
- Requirements use vague terms without numeric targets.
- The design assumes dependencies are always available.
- Retry logic exists without backoff, jitter, or circuit breaking.
- Data migration or rollback is described as "manual" without steps.
- Security is deferred without risk classification.
- Observability is planned "after launch".
- The design introduces a new service when a module, library, or existing service would work.
- The document needs verbal explanation to make sense.
- The review finds the same missing sections across multiple designs.

## Verification

Before approving the design, verify:

- [ ] Problem, requirements, and success metrics are clear.
- [ ] Alternatives and trade-offs are real and explicit.
- [ ] One-way door decisions are identified.
- [ ] Dependency-management decisions are present when dependency boundaries exist.
- [ ] Security and privacy risks are addressed.
- [ ] Operational readiness is designed, not deferred.
- [ ] Cost and capacity assumptions are backed by numbers.
- [ ] Test strategy covers behavior, contracts, and failure modes.
- [ ] The design is simple enough for a new engineer to understand.
- [ ] Blocking findings are resolved or the outcome is `NEEDS REVISION` / `RE-DESIGN`.

## Tenets

1. **The design must stand alone.** If it needs verbal explanation to make sense, the document is incomplete.
2. **Paper is cheaper than code.** A design issue fixed now prevents rework later.
3. **Trade-offs are the design.** A design without trade-offs is just a preference.
4. **Failure modes are first-class.** Happy-path architecture is not production architecture.
5. **The bar exists for customers and operators.** Reliability, security, cost, and operability are customer-impacting concerns.
6. **Simplicity wins unless complexity earns its place.** Every extra concept must pay rent.

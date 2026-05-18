# [Project Name] — Design Document

**Author(s):** [Name(s)]
**Date:** [YYYY-MM-DD]
**Status:** Draft | In Review | Approved | Superseded
**Reviewers:** [Names and roles]
**Design Bar Raiser:** [Name]
**Last Updated:** [YYYY-MM-DD]

---

## 1. Problem Statement

### 1.1 Working Backwards Reference

| Field | Value |
|-------|-------|
| WB Artifact | [Link to PR/FAQ or PRFAQ] |
| Customer | [Who is the customer?] |
| Customer Problem | [1-2 sentence problem from WB] |
| Success Metric | [How we'll know this is working] |

### 1.2 Background

[2-3 paragraphs of context. What exists today? Why is the current state insufficient? What has changed that makes this work necessary now? Include relevant metrics about the current state.]

### 1.3 Scope

**In scope:**
- [Specific capability 1]
- [Specific capability 2]
- [Specific capability 3]

**Out of scope:**
- [Thing we're explicitly NOT doing and why]
- [Another thing we're deferring and when we'll revisit]

---

## 2. Requirements

### 2.1 Functional Requirements

| ID | Priority | Requirement | Acceptance Criteria |
|----|----------|-------------|-------------------|
| FR-1 | P0 | [What the system must do] | [How to verify it does it] |
| FR-2 | P0 | [What the system must do] | [How to verify it does it] |
| FR-3 | P1 | [What the system must do] | [How to verify it does it] |
| FR-4 | P2 | [What the system must do] | [How to verify it does it] |

### 2.2 Non-Functional Requirements

| Category | Requirement | Target | Measurement Method |
|----------|-------------|--------|-------------------|
| Latency | p50 response time | [X] ms | [CloudWatch metric / Load test] |
| Latency | p99 response time | [X] ms | [CloudWatch metric / Load test] |
| Throughput | Sustained TPS | [X] TPS | [Load test] |
| Throughput | Peak TPS | [X] TPS (for [duration]) | [Load test] |
| Availability | Uptime | [99.9X]% | [Synthetic monitoring] |
| Durability | Data loss tolerance | [RPO = X] | [Backup verification] |
| Scalability | Growth ceiling | [X]x current without re-architecture | [Capacity model] |
| Security | Data classification | [Public / Internal / Confidential / Restricted] | [Security review] |
| Cost | Per-unit cost | $[X] per [unit] at steady state | [Cost monitoring] |

### 2.3 Constraints

- [Technical constraint: e.g., must run on existing infrastructure]
- [Business constraint: e.g., must launch before Q4]
- [Compliance constraint: e.g., must be GDPR compliant]
- [Organizational constraint: e.g., team size is 4 engineers]

---

## 3. Proposed Architecture

### 3.1 High-Level Architecture

```
[ASCII diagram or description of diagram location]

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API GW    │────▶│   Service   │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                                    ┌───────────┼───────────┐
                                    ▼           ▼           ▼
                              ┌──────────┐ ┌──────────┐ ┌──────────┐
                              │  Cache   │ │ Database │ │  Queue   │
                              └──────────┘ └──────────┘ └──────────┘
```

[Narrative description of the architecture. Explain the diagram. Cover:
- Why these boundaries exist
- What protocol is used between components
- Where data is stored and why
- What is synchronous vs. asynchronous and why]

### 3.2 Component Design

#### 3.2.1 [Component A Name]

| Aspect | Detail |
|--------|--------|
| Responsibility | [Single-sentence purpose] |
| Input | [What triggers this component] |
| Output | [What it produces] |
| State | [Stateless / Stateful — if stateful, where is state stored] |
| Scaling | [How it scales: horizontal, vertical, auto-scaling trigger] |
| Failure mode | [What happens when this component fails] |
| Recovery | [How it recovers: restart, retry, failover] |

[Additional design details for this component. Include algorithms, data structures, or protocols that are non-obvious.]

#### 3.2.2 [Component B Name]

[Same structure as above]

#### 3.2.3 [Component C Name]

[Same structure as above]

### 3.3 Data Model

#### 3.3.1 Schema Design

```
[Table/collection definitions with types and constraints]

Table: [table_name]
├── partition_key: [type] — [description]
├── sort_key: [type] — [description]
├── attribute_1: [type] — [description]
├── attribute_2: [type] — [description]
└── GSI-1: [partition_key, sort_key] — [access pattern it serves]
```

#### 3.3.2 Access Patterns

| # | Access Pattern | Key Condition | Frequency | Latency Target |
|---|---------------|--------------|-----------|---------------|
| 1 | [Get user by ID] | [PK = user_id] | [X TPS] | [X ms] |
| 2 | [List orders by user] | [GSI-1: PK = user_id, SK > date] | [X TPS] | [X ms] |
| 3 | [Query by status] | [GSI-2: PK = status] | [X TPS] | [X ms] |

#### 3.3.3 Data Growth

| Time Horizon | Record Count | Storage Size | Monthly Cost |
|-------------|-------------|-------------|-------------|
| Launch | [X] | [X GB] | $[X] |
| 6 months | [X] | [X GB] | $[X] |
| 1 year | [X] | [X GB] | $[X] |
| 3 years | [X] | [X GB] | $[X] |

#### 3.3.4 Migration Strategy

[If migrating from existing system:]
- **Phase 1**: [Dual-write to both old and new]
- **Phase 2**: [Read from new, verify against old]
- **Phase 3**: [Cut over reads to new]
- **Phase 4**: [Decommission old]
- **Rollback**: [How to revert at each phase]

### 3.4 API Design

[Key API contracts. Full API spec should be a separate document, but include the most important endpoints here.]

```
POST /v1/[resource]
Request:
{
  "field_1": "string (required)",
  "field_2": 123,
  "idempotency_key": "uuid (required)"
}

Response (201 Created):
{
  "id": "string",
  "field_1": "string",
  "field_2": 123,
  "created_at": "ISO-8601",
  "version": 1
}

Error (4xx/5xx):
{
  "error_code": "RESOURCE_CONFLICT",
  "message": "Human-readable description",
  "request_id": "uuid",
  "retry_after_ms": 1000
}
```

### 3.5 Security Design

- **Authentication**: [How clients authenticate]
- **Authorization**: [How permissions are enforced; IAM roles, policies]
- **Encryption at rest**: [KMS key management, what's encrypted]
- **Encryption in transit**: [TLS version, certificate management]
- **Data classification**: [What data is stored, its classification level]
- **Audit logging**: [What actions are logged, retention period]
- **Network boundaries**: [VPC design, security groups, NACLs]

---

## 4. Alternatives Considered

> When generating alternatives, scan `patterns/*/PATTERN.md` for any pattern whose `applies_when:` plausibly matches this workload. A matching pattern competes here as a real alternative (or is the chosen approach if the user/WB asked for it). Patterns that don't fit do not appear — quality of thought, not quantity of dismissals.
>
> If a pattern is adopted, copy its Skill Impact Map into the relevant later sections (Architecture, Operational Concerns, Testing).

### 4.1 [Alternative A Name]

**Description:** [Clear description of this approach — enough for someone to implement it]

**Pros:**
- [Genuine advantage 1]
- [Genuine advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Why rejected:** [The specific requirement or constraint that made this inferior to the proposed approach]

### 4.2 [Alternative B Name]

**Description:** [Clear description]

**Pros:**
- [Genuine advantage 1]
- [Genuine advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Why rejected:** [Specific reason]

### 4.3 Comparison Matrix

| Criterion | Proposed | Alternative A | Alternative B |
|-----------|----------|--------------|--------------|
| Meets latency target | ✅ | ✅ | ❌ |
| Meets cost target | ✅ | ❌ | ✅ |
| Operational complexity | Medium | High | Low |
| Time to implement | [X weeks] | [X weeks] | [X weeks] |
| Scales to 10x | ✅ | ✅ | ❌ |

---

## 5. Trade-offs

[State each trade-off explicitly using this format:]

### Trade-off 1: [Short Name]

> **We are choosing** [X] **over** [Y] **because** [Z], **accepting that** [W].

**Impact of acceptance:** [What does this mean in practice? How will we mitigate?]

**Reversibility:** [Can we change our mind later? At what cost?]

### Trade-off 2: [Short Name]

> **We are choosing** [X] **over** [Y] **because** [Z], **accepting that** [W].

**Impact of acceptance:** [Practical consequences]

**Reversibility:** [Cost to reverse]

### Trade-off 3: [Short Name]

> **We are choosing** [X] **over** [Y] **because** [Z], **accepting that** [W].

**Impact of acceptance:** [Practical consequences]

**Reversibility:** [Cost to reverse]

---

## 6. Cost Estimation

### 6.1 Infrastructure Cost (Monthly)

| Resource | Configuration | Steady State | Peak | At 10x Growth |
|----------|--------------|-------------|------|---------------|
| Compute | [Instance type × count] | $[X] | $[X] | $[X] |
| Database | [Type, storage, IOPS] | $[X] | $[X] | $[X] |
| Cache | [Type, size] | $[X] | $[X] | $[X] |
| Queue/Stream | [Type, throughput] | $[X] | $[X] | $[X] |
| Network | [Data transfer] | $[X] | $[X] | $[X] |
| Monitoring | [Metrics, logs, traces] | $[X] | $[X] | $[X] |
| **Total** | | **$[X]** | **$[X]** | **$[X]** |

### 6.2 Unit Economics

| Metric | Value |
|--------|-------|
| Cost per request | $[X] |
| Cost per active user/month | $[X] |
| Cost per GB stored | $[X] |
| Break-even point | [X users / X TPS] |

### 6.3 Development Cost

| Phase | Engineers | Duration | Engineer-Weeks |
|-------|-----------|----------|---------------|
| Design & Review | [X] | [X weeks] | [X] |
| Core Implementation | [X] | [X weeks] | [X] |
| Testing & Hardening | [X] | [X weeks] | [X] |
| Deployment & Bake | [X] | [X weeks] | [X] |
| **Total** | | | **[X]** |

### 6.4 Comparison to Alternatives

| | Proposed | Alternative A | Alternative B |
|--|----------|--------------|--------------|
| Monthly infra cost | $[X] | $[X] | $[X] |
| Development cost | [X] eng-weeks | [X] eng-weeks | [X] eng-weeks |
| Ongoing ops cost | [X] hrs/week | [X] hrs/week | [X] hrs/week |

---

## 7. Operational Concerns

### 7.1 Deployment

- **Strategy**: [Blue/green, canary, rolling, progressive]
- **Rollback trigger**: [What metric/alarm triggers automatic rollback]
- **Rollback time**: [Target time from detection to full rollback]
- **Feature flags**: [What's behind flags for gradual rollout]
- **Data migration**: [How schema changes are deployed; backward compatible?]

### 7.2 Monitoring & Alerting

| Metric | Alarm Threshold | Severity | Action |
|--------|----------------|----------|--------|
| p99 latency | > [X] ms for 5 min | P2 (High) | [Auto-scale / Page on-call] |
| Error rate | > [X]% for 3 min | P2 (High) | [Auto-rollback / Page on-call] |
| Queue depth | > [X] messages for 10 min | P3 (Medium) | [Scale consumers / Investigate] |
| Disk usage | > 80% | P3 (Medium) | [Expand storage / Archive] |
| [Custom metric] | [Threshold] | [Severity] | [Action] |

### 7.3 Dependency Failure Handling

| Dependency | Failure Mode | Impact | Mitigation |
|-----------|-------------|--------|-----------|
| [Database] | Unavailable | [Total outage] | [Retry with backoff, circuit breaker, cached reads] |
| [Cache] | Unavailable | [Increased latency] | [Fall through to database, degrade gracefully] |
| [External API] | Timeout | [Feature degraded] | [Circuit breaker, fallback response, queue for retry] |
| [Queue] | Backpressure | [Delayed processing] | [Shed load, alert, scale consumers] |

### 7.4 Runbooks

[List runbooks that must be written before launch:]

- [ ] **Runbook: High latency** — Steps to diagnose and mitigate latency spikes
- [ ] **Runbook: Data inconsistency** — How to detect and repair data inconsistencies
- [ ] **Runbook: Dependency failure** — Steps for each dependency failure scenario
- [ ] **Runbook: Capacity emergency** — How to quickly add capacity
- [ ] **Runbook: Rollback procedure** — Step-by-step rollback including data

### 7.5 On-Call Impact

- **Expected pages/week**: [X] (based on similar services)
- **New dashboards needed**: [List]
- **Training required**: [What on-call engineers need to learn]
- **Escalation path**: [Primary → Secondary → Manager → VP]

### 7.6 Disaster Recovery

| Scenario | RTO | RPO | Recovery Procedure |
|----------|-----|-----|-------------------|
| Single AZ failure | [X min] | [0 / X min] | [Automatic failover] |
| Region failure | [X hrs] | [X min] | [Manual failover to DR region] |
| Data corruption | [X hrs] | [X min] | [Restore from backup] |
| Service compromise | [X hrs] | [X min] | [Isolate, rotate creds, restore] |

---

## 8. Testing Strategy

### 8.1 Testing Pyramid

| Level | Scope | Count (est.) | Run Time | When |
|-------|-------|-------------|----------|------|
| Unit | Individual functions/classes | [X] | [X sec] | Every commit |
| Integration | Service + dependencies | [X] | [X min] | Every PR |
| Contract | API compatibility | [X] | [X min] | Every PR |
| Load | Performance at scale | [X scenarios] | [X min] | Pre-deploy |
| Chaos | Failure injection | [X scenarios] | [X min] | Weekly |
| E2E | Full customer journey | [X flows] | [X min] | Pre-deploy |

### 8.2 Load Testing Plan

| Scenario | TPS | Duration | Success Criteria |
|----------|-----|----------|-----------------|
| Steady state | [X] | 30 min | p99 < [X]ms, errors < 0.1% |
| Peak load | [X] | 15 min | p99 < [X]ms, errors < 0.5% |
| Sustained peak | [X] | 2 hrs | No degradation over time |
| Spike (cold start) | [X] | 5 min ramp | Recovery < 2 min |

### 8.3 Chaos Testing Plan

| Failure Scenario | Expected Behavior | Verification |
|-----------------|-------------------|-------------|
| Database failover | Automatic failover, <30s impact | Synthetic tests pass within 30s |
| Cache failure | Graceful degradation, higher latency | All requests succeed, latency < 2x |
| AZ failure | No customer impact | Synthetic tests never fail |
| Poison pill message | Message sent to DLQ, processing continues | Queue depth doesn't grow |

---

## 9. Implementation Plan

### 9.1 Milestones

| # | Milestone | Description | Target Date | Exit Criteria |
|---|-----------|-------------|-------------|--------------|
| 1 | Foundation | [Core infrastructure, CI/CD, monitoring] | [Date] | [Pipeline deploys to dev] |
| 2 | Core Logic | [Primary business logic implemented] | [Date] | [Unit tests pass, integration tests pass] |
| 3 | Integration | [Connected to dependencies, E2E working] | [Date] | [E2E tests pass in staging] |
| 4 | Hardening | [Load testing, chaos testing, security review] | [Date] | [All NFRs verified] |
| 5 | Launch | [Production deployment, monitoring verified] | [Date] | [Bake period complete, metrics green] |

### 9.2 Dependencies & Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [External team dependency delays] | Medium | High | [Start integration early, have fallback] |
| [New technology learning curve] | Medium | Medium | [Spike first, pair programming] |
| [Scope creep from stakeholders] | High | Medium | [Strict scope doc, change process] |

---

## 10. Open Questions

[Questions that need resolution before or during implementation:]

| # | Question | Owner | Due Date | Resolution |
|---|----------|-------|----------|-----------|
| 1 | [Question about design choice] | [Name] | [Date] | [Pending / Resolved: answer] |
| 2 | [Question about requirement] | [Name] | [Date] | [Pending / Resolved: answer] |

---

## Appendix

### A. Glossary

| Term | Definition |
|------|-----------|
| [Term 1] | [Definition] |
| [Term 2] | [Definition] |

### B. References

- [Link to Working Backwards document]
- [Link to related design documents]
- [Link to relevant RFCs or standards]
- [Link to similar systems for reference]

### C. Revision History

| Date | Author | Change |
|------|--------|--------|
| [YYYY-MM-DD] | [Name] | Initial draft |
| [YYYY-MM-DD] | [Name] | Incorporated review feedback |

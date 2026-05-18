# Operational Readiness Review Checklist

**Service Name:** ___________________________  
**Team:** ___________________________  
**Target Launch Date:** ___________________________  
**ORR Reviewer:** ___________________________  
**Assessment Date:** ___________________________  

---

## Scoring Legend

| Status | Symbol | Meaning |
|--------|--------|---------|
| Pass | ✅ | Complete with evidence |
| Conditional | ⚠️ | Partially complete, risk accepted with mitigation |
| Fail | ❌ | Not addressed — must fix before launch |
| Not Applicable | N/A | Doesn't apply (justification required) |

**Launch Criteria:** Zero ❌ items. Maximum 3 ⚠️ items with documented mitigations.

---

## A. Monitoring and Observability

| # | Item | Status | Evidence / Notes |
|---|------|--------|-----------------|
| A1 | Service-level dashboard exists showing overall health at a glance | | |
| A2 | Dashboard shows latency (p50, p90, p99) for every API operation | | |
| A3 | Dashboard shows error rate (4xx, 5xx) for every API operation | | |
| A4 | Dashboard shows throughput (TPS/RPM) for every API operation | | |
| A5 | Dependency health metrics visible (latency + errors per dependency) | | |
| A6 | Business metrics tracked (items processed, events handled, etc.) | | |
| A7 | Distributed tracing enabled and propagating across service boundaries | | |
| A8 | Structured JSON logging configured with request_id, trace_id fields | | |
| A9 | Log aggregation configured and queryable (CloudWatch Logs Insights or equivalent) | | |
| A10 | Custom metrics for feature-specific critical behavior | | |
| A11 | Dashboard accessible to entire team (not just author) | | |

---

## B. Alarming

| # | Item | Status | Evidence / Notes |
|---|------|--------|-----------------|
| B1 | Alarm for high error rate (5xx > threshold for N minutes) | | |
| B2 | Alarm for high latency (p99 > SLA for N minutes) | | |
| B3 | Alarm for low throughput / traffic drop (potential silent failure) | | |
| B4 | Alarm for each critical dependency failure rate | | |
| B5 | Alarm severity levels defined | | |
| B6 | Every alarm has a linked runbook in its description | | |
| B7 | Alarms tested and proven to fire (test alarm event in history) | | |
| B8 | Canary/synthetic monitoring alarm (external check fails → page) | | |
| B9 | Alarm for resource exhaustion (disk, memory, connections, queue depth) | | |
| B10 | Alarm escalation path defined (on-call → senior → manager) | | |
| B11 | No alarm fatigue — each alarm is actionable (< 5 pages/week baseline) | | |

---

## C. Runbooks

| # | Item | Status | Evidence / Notes |
|---|------|--------|-----------------|
| C1 | Runbook exists for every alarm (diagnosis + remediation steps) | | |
| C2 | Runbook for service restart/recovery procedure | | |
| C3 | Runbook for scaling up (manual, if auto-scaling insufficient) | | |
| C4 | Runbook for failover to secondary region (if applicable) | | |
| C5 | Runbook for dependency failure (what to do when X is down) | | |
| C6 | Runbook includes "what does healthy look like?" baseline metrics | | |
| C7 | Runbooks tested by engineer who didn't write them | | |
| C8 | Runbooks stored in team-accessible, durable location | | |
| C9 | Runbook for data recovery / backup restoration | | |
| C10 | Runbook for emergency feature flag toggle (disable new feature) | | |

---

## D. On-Call Readiness

| # | Item | Status | Evidence / Notes |
|---|------|--------|-----------------|
| D1 | On-call rotation established with minimum 2 people | | |
| D2 | All rotation members have shadowed on-call at least once | | |
| D3 | On-call engineer has production access (deploy, restart, scale permissions) | | |
| D4 | Escalation path documented (who to contact for each severity) | | |
| D5 | On-call handoff process defined (shift change procedures) | | |
| D6 | On-call has access to all dashboards, logs, and deployment tools | | |
| D7 | No single point of failure — at least 2 people fully operational | | |
| D8 | On-call response time SLA defined (e.g., acknowledge within 15 min) | | |
| D9 | Pager/notification system tested and working | | |
| D10 | On-call schedule published and visible to the team | | |

---

## E. Scaling and Performance

| # | Item | Status | Evidence / Notes |
|---|------|--------|-----------------|
| E1 | Load testing completed at 2x expected peak traffic | | |
| E2 | Auto-scaling configured with appropriate min/max boundaries | | |
| E3 | Auto-scaling tested — observed scaling up under load | | |
| E4 | Time to scale documented (how long from trigger to capacity) | | |
| E5 | Known scaling limits documented with early-warning alarms | | |
| E6 | Rate limiting / throttling configured to protect service | | |
| E7 | Backpressure mechanisms in place (queue depth limits, shedding) | | |
| E8 | Database scaling strategy documented (read replicas, sharding plan) | | |
| E9 | Capacity planning documented (expected growth, review cadence) | | |
| E10 | Performance regression testing in CI/CD pipeline | | |
| E11 | Hot partition / hot key analysis completed (DynamoDB, etc.) | | |

---

## F. Security

| # | Item | Status | Evidence / Notes |
|---|------|--------|-----------------|
| F1 | Authentication implemented for all external-facing endpoints | | |
| F2 | Authorization enforced (users can only access their own data) | | |
| F3 | Input validation on all external inputs (API parameters, headers, body) | | |
| F4 | Secrets stored in secrets manager (not in code, env vars, or config files) | | |
| F5 | Secret rotation configured and tested | | |
| F6 | Encryption at rest for all persistent data stores | | |
| F7 | Encryption in transit (TLS 1.2+) for all network communication | | |
| F8 | Network security groups restrict access to minimum required | | |
| F9 | IAM roles follow least-privilege principle | | |
| F10 | Dependency vulnerability scanning enabled and blocking in pipeline | | |
| F11 | No PII logged or exposed in error messages | | |
| F12 | Threat model completed and reviewed | | |
| F13 | OWASP Top 10 risks assessed and mitigated | | |

---

## G. Deployment Safety

| # | Item | Status | Evidence / Notes |
|---|------|--------|-----------------|
| G1 | Fully automated deployment pipeline (no manual steps) | | |
| G2 | Canary/staged deployment with automatic rollback on alarm | | |
| G3 | Deployment alarms configured (error rate spike during deploy → rollback) | | |
| G4 | Rollback tested and verified to complete within SLA (< 15 min) | | |
| G5 | Blue-green or rolling deployment strategy documented | | |
| G6 | Database migrations are backward-compatible (no breaking changes) | | |
| G7 | Feature flags used for behavioral changes (deploy ≠ release) | | |
| G8 | Deployment bake time configured between stages | | |
| G9 | One-box / canary stage before full fleet deployment | | |
| G10 | Deploy cadence established (at least weekly during active dev) | | |
| G11 | Pipeline has pre-deployment integration tests | | |
| G12 | Deployment cannot proceed if pre-prod tests fail | | |

---

## H. Cost Management

| # | Item | Status | Evidence / Notes |
|---|------|--------|-----------------|
| H1 | Expected monthly cost estimated with calculation methodology | | |
| H2 | Cost alarm at 80% of monthly budget (notify team) | | |
| H3 | Cost alarm at 120% of monthly budget (page on-call) | | |
| H4 | All resources tagged for cost attribution | | |
| H5 | No unbounded resources (TTLs, auto-scaling limits, storage lifecycle) | | |
| H6 | Cost per transaction/request calculated and tracked | | |
| H7 | Reserved capacity or savings plans evaluated | | |
| H8 | Cost reviewed monthly in operational review | | |
| H9 | Data retention policy defined (when is data deleted/archived?) | | |
| H10 | Idle resource cleanup automated or scheduled | | |

---

## I. Dependency Management

| # | Item | Status | Evidence / Notes |
|---|------|--------|-----------------|
| I1 | All external dependencies documented with owner team contact | | |
| I2 | Dependency SLOs documented (expected availability, latency) | | |
| I3 | Circuit breakers configured on all external service calls | | |
| I4 | Explicit timeouts on every network call (no defaults) | | |
| I5 | Retries configured with exponential backoff and jitter | | |
| I6 | Non-critical dependencies degrade gracefully (not error) | | |
| I7 | Dependency failure tested — verified degradation behavior | | |
| I8 | No circular dependencies | | |
| I9 | Dependency version pinning (no "latest" in production) | | |
| I10 | Fallback values/cached data available when dependency unavailable | | |

---

## Summary

| Category | Pass | Conditional | Fail | N/A |
|----------|------|-------------|------|-----|
| A. Monitoring | | | | |
| B. Alarming | | | | |
| C. Runbooks | | | | |
| D. On-Call | | | | |
| E. Scaling | | | | |
| F. Security | | | | |
| G. Deployment | | | | |
| H. Cost | | | | |
| I. Dependencies | | | | |
| **TOTAL** | | | | |

---

## Conditional Items — Mitigation and Timeline

| Item # | Mitigation | Resolution Owner | Target Date |
|--------|-----------|-----------------|-------------|
| | | | |
| | | | |
| | | | |

---

## Reviewer Decision

- [ ] **APPROVED** — Service meets operational readiness bar. Launch may proceed.
- [ ] **APPROVED WITH CONDITIONS** — Launch may proceed. Conditional items must be resolved within 2 weeks post-launch.
- [ ] **NOT APPROVED** — Gaps must be addressed before launch. Re-review required.

**Reviewer Comments:**

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

**Reviewer Signature:** ___________________________ **Date:** ___________

---

## Post-Launch Follow-up (Due: 2 weeks after launch)

| # | Item | Status | Notes |
|---|------|--------|-------|
| PL1 | All CONDITIONAL items resolved to PASS | | |
| PL2 | Actual metrics reviewed vs. estimated metrics | | |
| PL3 | Actual cost reviewed vs. estimated cost | | |
| PL4 | On-call has handled at least one alarm (synthetic or real) | | |
| PL5 | Any new operational learnings captured in runbooks | | |
| PL6 | Scaling behavior observed under real traffic | | |
| PL7 | Next ORR re-assessment date scheduled | | |

# COE: [Title — Brief Description of the Incident]

## Summary

| Field | Value |
|-------|-------|
| **Date of Incident** | YYYY-MM-DD |
| **Duration of Impact** | X hours Y minutes |
| **Severity** | Yourr company's classification |
| **Services Affected** | [Service names] |
| **Customers Affected** | [Number or percentage] |
| **Revenue Impact** | [$X or "No direct revenue impact"] |
| **Incident Commander** | [Name] |
| **COE Author** | [Name] |
| **COE Review Date** | YYYY-MM-DD |

### One-Paragraph Summary

[In 3-4 sentences: What happened, when, what customers experienced, how long it lasted, and how it was resolved. Write this so someone with no context understands the incident.]

---

## Customer Impact

### What Customers Experienced

[Describe what customers saw/felt. Be specific: "Customers received 500 errors when attempting to place orders" not "service was degraded."]

### Scope of Impact

- **Affected customers**: [number or percentage of total traffic]
- **Affected regions**: [list regions]
- **Affected functionality**: [specific features/APIs]
- **Data impact**: [any data loss, inconsistency, or corruption? If none, state "No data impact confirmed"]

### Detection Method

- [ ] Automated alarm
- [ ] Synthetic canary
- [ ] Customer contact/complaint
- [ ] Internal report
- [ ] Other: ___

**Time from impact start to detection**: [X minutes]

---

## Timeline

All times in UTC (or specify timezone).

| Time | Event | Actor |
|------|-------|-------|
| HH:MM | [First sign of trouble — what metric moved, what alarm fired] | [System/Person] |
| HH:MM | [On-call acknowledged page] | [Name] |
| HH:MM | [First investigation action taken] | [Name] |
| HH:MM | [Escalation decision made — who was engaged] | [Name] |
| HH:MM | [Incident bridge opened] | [Name] |
| HH:MM | [Mitigation action taken — what was done] | [Name] |
| HH:MM | [Customer impact resolved — metrics returned to normal] | [System] |
| HH:MM | [Root cause identified] | [Name] |
| HH:MM | [Permanent fix deployed] | [Name] |
| HH:MM | [Incident closed] | [Name] |

---

## Root Cause Analysis

### 5 Whys

**Why #1**: Why were customers affected?
→ [Answer: Direct technical cause of customer impact]

**Why #2**: Why did [answer from #1] happen?
→ [Answer: What allowed the direct cause]

**Why #3**: Why did [answer from #2] happen?
→ [Answer: Deeper systemic cause]

**Why #4**: Why did [answer from #3] happen?
→ [Answer: Process or design gap]

**Why #5**: Why did [answer from #4] happen?
→ [Answer: Organizational or cultural root]

### Contributing Factors

List all factors that contributed to the incident (not root causes, but made it worse or delayed detection/recovery):

1. [Factor 1 — e.g., "Alarm threshold was too lenient, delaying detection by 8 minutes"]
2. [Factor 2 — e.g., "Runbook for this alarm was outdated and referenced a deprecated tool"]
3. [Factor 3 — e.g., "Incident occurred during a deployment freeze, so team was less alert"]

### Root Cause Summary

[2-3 sentences stating the root cause in terms of SYSTEMS, not PEOPLE. "The deployment pipeline lacked a check for X" not "Engineer Y forgot to check X."]

---

## What Went Well

[Acknowledge things that worked correctly — this encourages continued good behavior]

1. [e.g., "Alarm fired within 3 minutes of impact — detection was fast"]
2. [e.g., "On-call acknowledged within 2 minutes and began investigation immediately"]
3. [e.g., "Rollback was executed cleanly and resolved impact within 5 minutes of decision"]
4. [e.g., "Communication to customers was timely and accurate"]

---

## What Could Be Improved

[Identify gaps without blaming individuals]

1. [e.g., "Detection time: 12 minutes elapsed before alarm fired. Threshold was too lenient"]
2. [e.g., "Mitigation: Took 45 minutes because runbook didn't cover this scenario"]
3. [e.g., "Communication: Status page not updated until 25 minutes after detection"]
4. [e.g., "Testing: This failure mode was not covered by integration tests"]

---

## Action Items

### Immediate (Complete within 7 days)

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 | [Specific, actionable item — e.g., "Add alarm on connection pool utilization with threshold at 80%"] | [Name] | YYYY-MM-DD | Open |
| 2 | [e.g., "Update runbook for DatabaseConnectionAlarm with new mitigation steps"] | [Name] | YYYY-MM-DD | Open |
| 3 | [e.g., "Rollback the specific code change that introduced the bug"] | [Name] | YYYY-MM-DD | Open |

### Short-term (Complete within 30 days)

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 4 | [e.g., "Add integration test that verifies connection pool is properly released after request handling"] | [Name] | YYYY-MM-DD | Open |
| 5 | [e.g., "Implement circuit breaker for database connections with fallback behavior"] | [Name] | YYYY-MM-DD | Open |
| 6 | [e.g., "Add pre-deploy gate that checks connection pool behavior under load test"] | [Name] | YYYY-MM-DD | Open |

### Long-term (Complete within 90 days)

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 7 | [e.g., "Implement connection pool auto-scaling with dynamic limits based on traffic"] | [Name] | YYYY-MM-DD | Open |
| 8 | [e.g., "Add static analysis rule to detect unclosed connections in code review"] | [Name] | YYYY-MM-DD | Open |

---

## Lessons Learned

### For This Team

[What should this team internalize from this incident?]

1. [e.g., "Resource cleanup patterns must be verified in integration tests, not just unit tests"]
2. [e.g., "Alarms on internal resource utilization are as important as customer-facing metrics"]

### For the Organization

[What can other teams learn from this COE?]

1. [e.g., "Connection pool exhaustion is a common failure mode — all services should alarm on pool utilization"]
2. [e.g., "Static analysis can catch resource leaks automatically — consider adding to shared pipeline"]

---

## Review Sign-off

| Reviewer | Role | Date | Approved |
|----------|------|------|----------|
| [Name] | Team Lead | YYYY-MM-DD | ☐ |
| [Name] | Manager | YYYY-MM-DD | ☐ |
| [Name] | Senior Leadership | YYYY-MM-DD | ☐ |

---

## Appendix

### Related Incidents

- [Link to similar past incidents, if any]
- [Link to previous COEs with similar root causes]

### Supporting Data

- [Link to dashboard showing the incident metrics]
- [Link to deployment that triggered the incident]
- [Link to the specific code change, if applicable]
- [Link to incident bridge recording/notes, if available]

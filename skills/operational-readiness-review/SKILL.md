---
name: Operational Readiness Review
description: The ORR process — a self-assessment checklist covering monitoring, alarming, runbooks, on-call, scaling, security, deployment safety, cost, and dependencies. Must pass before launch.
leadership_principles:
  - Ownership
  - Insist on the Highest Standards
  - Think Big
---

## Overview

An [Operational Readiness Review (ORR)](https://docs.aws.amazon.com/wellarchitected/latest/operational-readiness-reviews/wa-operational-readiness-reviews.html) is a structured self-assessment that a team completes before launching a new service, feature, or significant change to production. It is a mandatory gate—nothing ships to production without a passing ORR.

The ORR is not a meeting with approvers. It is a checklist of operational requirements that the team fills out, providing evidence for each item. A senior engineer or principal reviews the completed ORR and either approves or identifies gaps. The ORR does not test whether the feature works—it tests whether the team can operate the feature in production when things go wrong.

The philosophy: **if you can't operate it, you can't launch it.** Writing code is 10% of the job. Operating it for years is the other 90%.

## When to Use

- Before launching a new service or microservice
- Before enabling a feature flag for general availability
- Before major architectural changes (new database, new dependency, new region)
- Before migrating traffic from one system to another
- Before accepting production traffic in a new AWS region
- Before any change that significantly alters operational characteristics

## Agent Persona

Load `agents/ops-bar-raiser.md` when reviewing ORR evidence. Use it to verify observability, alarms, runbooks, deployment safety, rollback capability, capacity, dependencies, and whether the team can operate the system under pressure.

## Amazon Context

The ORR originated from Amazon's experience launching services that "worked" but couldn't be operated. Teams would build features, demonstrate them in dev, and ship to production—only to discover at 2 AM that nobody knew how to restart the service, what constituted "healthy," or who to contact when the database filled up.

Amazon's ORR process has prevented thousands of operational incidents by catching gaps before they become 2 AM pages. The checklist has evolved over 15+ years from hard-won lessons. Each item exists because a team skipped it and suffered the consequences.

The ORR is owned by the team, not by a central authority. This reflects Amazon's ownership model: the team that builds it operates it. The ORR is their promise that they're ready to operate what they've built.

## The Process

### 1. ORR Timeline

```
Feature Implementation ──────────────────────────────────────────→ Launch
         │                                                          │
         │   Start ORR self-assessment                              │
         │   (2-4 weeks before target launch)                       │
         │         │                                                │
         │         ▼                                                │
         │   Team fills out checklist                               │
         │   (identifies gaps, creates tickets for fixes)           │
         │         │                                                │
         │         ▼                                                │
         │   Gaps resolved                                          │
         │   (dashboards built, alarms set, runbooks written)       │
         │         │                                                │
         │         ▼                                                │
         │   Senior/Principal review                                │
         │   (evidence verified, concerns raised)                   │
         │         │                                                │
         │         ├── Pass → Launch approved                       │
         │         └── Fail → Fix gaps → Re-review                 │
         │                                                          │
         └──────────────────────────────────────────────────────────┘
```

### 2. ORR Categories

The ORR covers nine categories, each with specific items:

#### A. Monitoring and Observability
- Service-level dashboard showing health at a glance
- Metrics for every API operation (latency p50/p90/p99, error rates, TPS)
- Dependency health metrics (for each external dependency)
- Business metrics (orders processed, events handled, etc.)
- Distributed tracing enabled and propagating across boundaries
- Log aggregation configured with structured JSON logging
- Custom metrics for feature-specific behavior

#### B. Alarming
- Alarms for every critical metric (error rate, latency, availability)
- Alarm severity levels defined
- Alarm thresholds tested (proven to fire before customer impact)
- No alarm without a runbook (alarm description links to runbook)
- Composite alarms for complex failure conditions
- Canary alarms (synthetic tests running continuously)
- Alarm escalation paths defined and tested

#### C. Runbooks
- Runbook for every alarm (diagnosis steps + remediation actions)
- Runbook for common operational tasks (scale up, restart, failover)
- Runbook for disaster recovery
- Runbooks tested by someone other than the author
- Runbooks include "what does this look like when healthy?"
- Runbooks are in a team-accessible location (wiki, runbook tool)

#### D. On-Call
- On-call rotation established with sufficient coverage
- On-call engineer has permissions to act (deploy, restart, scale)
- On-call training completed (every rotation member has shadowed)
- Escalation path defined (who to call for each severity)
- On-call handoff process documented
- No single point of failure (at least 2 people can operate the service)

#### E. Scaling
- Load testing completed at 2x expected peak traffic
- Auto-scaling configured with appropriate min/max
- Scaling behavior tested (time to scale, stability)
- Capacity planning documented (expected growth, when to add capacity)
- Known scaling limits documented with early-warning alarms
- Backpressure mechanisms in place (queue depth limits, rate limiting)
- Database scaling strategy defined (sharding plan, read replicas)

#### F. Security
- Authentication and authorization implemented correctly
- Input validation on all external inputs
- Secrets stored in secrets manager (not in code or config files)
- Network security groups restrict access appropriately
- Encryption at rest and in transit
- Dependency vulnerabilities scanned (automated, blocking)
- IAM roles follow least-privilege principle
- Penetration testing or threat modeling completed

#### G. Deployment Safety
- Automated deployment pipeline (no manual steps)
- Canary deployments with automatic rollback
- Deployment alarms that block rollout on failure
- Rollback tested and verified to complete within SLA
- Blue-green or rolling deployment strategy documented
- Database migrations are backward-compatible
- Feature flags for behavioral changes
- Deploy cadence established (at least weekly during active development)

#### H. Cost
- Expected cost estimated and budgeted
- Cost alarms set (alert at 80% of budget, page at 120%)
- Resource tagging for cost attribution
- No unbounded resources (TTLs on data, auto-scaling limits)
- Cost per transaction/request understood
- Cost optimization opportunities identified (reserved capacity, spot, etc.)

#### I. Dependencies
- All dependencies documented with SLOs
- Circuit breakers on all external calls
- Timeouts configured for every network call
- Graceful degradation for non-critical dependencies
- Dependency failure tested (what happens when X is unavailable?)
- No circular dependencies
- Dependency team contacts documented for escalation

### 3. Evidence Requirements

Each ORR item requires evidence, not just a checkbox:

| Item Type | Acceptable Evidence |
|-----------|-------------------|
| Dashboard exists | Screenshot or URL showing real data |
| Alarm configured | Alarm ARN + proof it fires (test alarm history) |
| Runbook written | URL to runbook + name of person who tested it |
| Load test completed | Report showing results at 2x expected traffic |
| Rollback tested | Date of last rollback test + time to complete |
| On-call trained | Names of rotation members + shadowing dates |
| Security reviewed | Threat model document + review sign-off |
| Cost estimated | Spreadsheet with per-unit costs + projected volume |

### 4. ORR Scoring

| Status | Meaning | Required for Launch |
|--------|---------|-------------------|
| ✅ PASS | Item complete with evidence | — |
| ⚠️ CONDITIONAL | Item partially complete, acceptable risk with mitigation | Mitigation documented |
| ❌ FAIL | Item not addressed | Must fix before launch |
| N/A | Item doesn't apply to this service (with justification) | Justification documented |

Launch criteria:
- **Zero** ❌ FAIL items
- **Maximum 3** ⚠️ CONDITIONAL items (with documented mitigation and timeline to resolve)
- Reviewer sign-off on all N/A justifications

### 5. The ORR Review Meeting

Format: 60-minute meeting with the team and a senior/principal reviewer

Agenda:
1. (5 min) Team presents service overview and launch scope
2. (10 min) Walk through any CONDITIONAL items and mitigations
3. (30 min) Reviewer asks questions about specific items, examines evidence
4. (10 min) Reviewer deliberates and provides decision
5. (5 min) If gaps identified, team creates action items with owners and dates

### 6. Post-Launch ORR Follow-up

Within 2 weeks of launch:
- [ ] All CONDITIONAL items resolved to PASS
- [ ] Post-launch metrics reviewed (did reality match estimates?)
- [ ] Any new operational insights added to runbooks
- [ ] On-call has handled at least one alarm (even if synthetic)
- [ ] Cost actuals compared to estimates

## Mechanisms Over Good Intentions

| Mechanism | What It Enforces | How |
|-----------|-----------------|-----|
| Pipeline launch gate | No deployment to prod without ORR | Deployment system checks for approved ORR ticket |
| ORR template in team wiki | Consistent coverage | Team can't "forget" categories—template lists them all |
| Quarterly ORR re-assessment | Operational standards maintained over time | Calendar reminder triggers re-review of existing services |
| Reviewer rotation | Fresh eyes on operational readiness | Different reviewer each ORR prevents groupthink |
| ORR failure postmortem | Learning from gaps | If a launch incident maps to an ORR gap, team writes COE |

## Common Rationalizations

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|----------------|-------------------|
| "We'll finish the ORR after launch, it's blocking our deadline" | The ORR exists because post-launch is when you need operational readiness. Launching without it is launching without a parachute. | Start the ORR 4 weeks before target launch. If it's not passing, move the launch date. |
| "We have monitoring, just not for everything yet" | Partial monitoring means you'll detect some failures and miss others. The ones you miss are the ones that become critical incidents. | Complete monitoring for all operations before launch. Use the checklist—every item exists because someone missed it and paid the price. |
| "The team is too small for on-call rotation" | If the team is too small for on-call, it's too small to own a production service. Two-person rotations work. | Establish rotation with at least 2 people. Cross-train aggressively. If truly single-threaded, escalation path to partner team required. |
| "Load testing is too expensive/complex for this service" | The production load is coming whether you test for it or not. Discovering your limits during peak traffic is not a strategy. | Use synthetic load testing tools. Even basic load tests (2x expected QPS for 30 minutes) catch most scaling issues. |
| "This is a low-traffic internal service, it doesn't need full ORR" | Internal services become critical dependencies for other teams. Low traffic doesn't mean low impact—batch jobs and cron jobs run at critical times. | Every production service gets an ORR. Scale the depth to the risk, but never skip it entirely. |

## Red Flags

- Team says "we're operationally ready" but can't show a dashboard
- Alarms exist but nobody on the team has ever been paged by them
- Runbooks reference infrastructure that has since changed
- On-call rotation has one person (single point of failure)
- No load test has been run since the initial launch
- Cost estimates are "we'll see what it costs in production"
- Deployment requires manual steps or manual approval
- Team cannot demonstrate rollback in under 15 minutes
- Security review was "we followed best practices" without evidence
- Dependencies listed but no circuit breakers or fallbacks exist

## Verification

After completing the ORR, verify:

- [ ] All nine categories have been addressed with evidence
- [ ] Zero FAIL items remain
- [ ] CONDITIONAL items have documented mitigation and resolution timeline
- [ ] A senior/principal engineer has reviewed and signed off
- [ ] The ORR is stored in a durable, team-accessible location
- [ ] Post-launch follow-up is scheduled (2 weeks after launch)
- [ ] All action items from review have owners and due dates
- [ ] The service has been operating under canary traffic without issues
- [ ] On-call rotation members have confirmed readiness
- [ ] The team can answer "is the service healthy?" in under 30 seconds

## Tenets

1. **Operability before launch.** If you can't demonstrate you can operate it, you can't ship it. No exceptions, no deadline overrides this gate.
2. **Evidence over assertion.** "We have monitoring" means nothing without a dashboard URL showing real data. Every item requires proof.
3. **The checklist is the minimum.** The ORR template covers known failure modes. Your service may have unique operational requirements—add them to your ORR.
4. **Ownership means operating.** The team that writes the code operates the code. The ORR is your promise that you're prepared to do so, 24/7/365.
5. **Prevention over detection.** The best incident is the one that never happens. ORR catches the gaps that become 2 AM pages before they become 2 AM pages.
6. **Living document.** The ORR is not a one-time exercise. Re-assess quarterly. Services evolve; operational requirements evolve with them.
7. **Start early, not late.** Begin the ORR 4 weeks before launch. Discovering gaps 2 days before launch creates impossible choices between quality and deadlines.

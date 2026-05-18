---
name: Operational Excellence
description: Dashboards, alarms, and runbooks that make a service operable. Covers latency, error rate, availability, throughput, and severity-based alarming.
leadership_principles:
  - Customer Obsession
  - Ownership
  - Insist on the Highest Standards
  - Dive Deep
---

# Operational Excellence

## Overview

Operational excellence means your service is observable, alarmed, and documented such that any on-call engineer can understand its health and respond to problems—even at 3 AM without the original author available. This requires dashboards that show the right metrics at the right granularity, alarms that fire at the right thresholds with the right severity, and runbooks that provide actionable steps for each alarm.

## When to Use

- Building a new service (operational readiness before launch)
- Reviewing an existing service's operational posture
- After any incident where detection or response was slower than expected
- When onboarding a new team member to on-call
- During operational readiness reviews (ORR)
- When service metrics indicate degradation trends

## Agent Persona

Load `agents/ops-bar-raiser.md` when evaluating dashboards, alarms, runbooks, and operational burden. Use it to challenge whether the service can be diagnosed, mitigated, and rolled back by someone who did not write the code.

## Amazon Context

At Amazon, you build it, you own it, you operate it. There is no separate operations team that runs your service. The team that writes the code carries the pager. This means operational excellence is not an afterthought—it's a core competency of every engineer. A service without proper alarms is a service where customers discover problems before you do. A service without runbooks is a service where every incident requires the original author, creating a single point of failure.

## The Process

### Dashboards

Every service needs three dashboard levels:

**Level 1: Customer Experience Dashboard (primary)**
- Availability: successful requests / total requests (target: 99.9%+ or per-SLA)
- Latency: p50, p90, p99, p99.9 (separate graphs, not averaged)
- Error rate: 5xx rate, client error rate (4xx), timeout rate
- Throughput: requests per second (to detect traffic anomalies)
- Business metrics: orders/sec, messages delivered/sec, etc.

**Level 2: Service Health Dashboard**
- Host health: CPU, memory, disk, network across fleet
- Dependency health: latency and error rate to each downstream
- Queue depths, thread pool utilization, connection pool usage
- Cache hit rates, database connection counts
- Deployment markers (vertical lines showing when deploys happened)

**Level 3: Deep Dive Dashboard**
- Per-endpoint breakdown (latency, errors, throughput)
- Per-customer/tenant breakdown (for multi-tenant services)
- Per-AZ and per-region breakdown
- Garbage collection pauses, JVM metrics (if applicable)
- Detailed dependency call patterns

### Alarms

Alarms are categorized by severity and mapped to response actions:

**P1: Critical — Customer-facing impact, immediate page**
- Availability drops below SLA threshold
- p99 latency exceeds 5x normal for >3 minutes
- Error rate exceeds 5% for >2 minutes
- Complete loss of a dependency
- Response: Immediate page, incident bridge opened within 15 minutes

**P2: High — Significant degradation, urgent page**
- Availability drops below target but above SLA
- p99 latency exceeds 2x normal for >5 minutes
- Error rate exceeds 1% for >5 minutes
- Single AZ degradation
- Response: Page on-call, response within 15 minutes, escalation within 30 if not mitigated

**P3: Medium — Degradation detected, ticket created**
- p99 latency trending up (>20% above baseline)
- Error rate above normal but below 1%
- Host health issues (high CPU, disk filling)
- Capacity approaching limits (>80% utilization)
- Response: Ticket created, addressed within business hours, same day

**P4: Low — Informational, review during business hours**
- Metric anomalies that don't yet impact customers
- Capacity forecasting alerts (weeks out)
- Dependency deprecation warnings
- Stale configuration detected
- Response: Ticket created, addressed within 1 week

### Alarm Design Principles

- **Alarm on customer impact, not internal state.** High CPU is not a customer problem until latency increases.
- **Alarm on rate of change, not just thresholds.** A sudden spike from 1ms to 50ms p99 matters even if 50ms is "acceptable."
- **Every alarm has a runbook.** An alarm without a runbook is just noise.
- **Tune regularly.** An alarm that fires weekly without action is worse than no alarm (alert fatigue).
- **Use composite alarms.** Combine signals to reduce false positives (e.g., high latency AND high error rate).

### Runbooks

Every alarm links to a runbook that contains:

1. **What this alarm means**: Plain English description of what triggered
2. **Customer impact**: What customers are experiencing right now
3. **Immediate actions**: Steps to mitigate (not debug) within first 5 minutes
4. **Diagnosis steps**: How to determine root cause
5. **Escalation path**: Who to contact if you can't resolve
6. **Recent changes**: How to check what changed recently (deploys, configs)
7. **Known causes**: List of past incidents with this alarm and their resolutions
8. **Rollback instructions**: How to undo the most recent change

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "I'll add dashboards before launch" | Operational readiness review blocks launch without dashboards |
| "I'll write runbooks when I have time" | Every alarm creation requires a runbook link. No link = alarm rejected |
| "I'll tune alarms when they get noisy" | Monthly alarm review meeting. Alarms that fire >5x without action are auto-escalated to manager |
| "I'll monitor after deployment" | Deployment dashboard auto-opens on deploy. Bake time requires green metrics |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "We'll add monitoring after MVP" | If you can't tell if MVP is working, you can't iterate on it | Monitoring is part of MVP. Ship metrics before features if you must prioritize |
| "Our error rate is fine at 0.5%" | 0.5% of 10M requests/day = 50,000 customer failures | Set targets based on absolute customer impact, not just percentages |
| "The alarm is too noisy, I'll suppress it" | Noisy alarms are a sign of a real problem (either the alarm or the service) | Fix the alarm threshold or fix the underlying issue. Never suppress without investigation |
| "We don't need p99.9, p99 is enough" | Your worst-affected customers live at p99.9. They're often your biggest customers | Monitor p99.9. Alert on p99. Dashboard shows p99.9 for awareness |

## Red Flags

- No dashboard exists for the service
- Dashboard exists but no one looks at it regularly
- Alarms fire but no one responds (alert fatigue)
- Alarms have no runbooks
- Runbooks say "contact [specific person]" as the only action
- No alarm coverage for a critical dependency
- p99 latency not monitored (only average)
- No business metrics on the dashboard
- Alarm thresholds haven't been reviewed in 6+ months
- On-call doesn't know which dashboard to look at first

## Verification

- [ ] Customer Experience Dashboard exists with availability, latency (p50/p99), errors, throughput
- [ ] Service Health Dashboard exists with host metrics, dependency health, resource utilization
- [ ] P1 and P2 alarms defined for availability and latency
- [ ] Every alarm links to a runbook with actionable steps
- [ ] Alarms tested (confirmed they fire when conditions are met)
- [ ] Runbooks reviewed and updated within last 90 days
- [ ] On-call engineer can find the right dashboard within 30 seconds
- [ ] Alert fatigue score: <2 false-positive pages per on-call rotation
- [ ] Business metrics represented on dashboard
- [ ] Alarm thresholds reviewed quarterly

## Tenets

1. **If you can't measure it, you can't operate it.** Every behavior that matters to customers must have a metric.
2. **Customers should never discover problems before you do.** Alarms must fire before customer complaints arrive.
3. **Dashboards are for understanding, not decoration.** If no one looks at it during incidents, it's not useful.
4. **Every alarm is a contract with the on-call engineer.** It promises: "this is worth waking you up, and here's what to do about it."
5. **Operational excellence is not optional for launch.** A service without observability is a service you're operating blind.

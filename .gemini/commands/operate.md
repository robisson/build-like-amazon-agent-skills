<!-- MIRROR: This file mirrors .claude/commands/operate.md. Do not edit directly — sync from the Claude version. -->

# Operate — Operational Excellence

Activate the **operate** skill chain: `skills/operational-excellence/` → `skills/operational-readiness-review/`.

## Instructions

Help the user establish practices for running the service in production.

### Step 1: Operational Excellence
- **Dashboards**: Latency p50/p99, error rate, throughput, saturation.
- **Alarms**: P2 (High) pages on-call, P3 (Medium) notifies business hours.
- **Weekly review**: Team reviews operational health every week.
- **Toil tracking**: Measure and automate repetitive tasks.
- **Capacity planning**: Forecast growth, provision ahead of demand.
- **Dependency health**: Monitor upstream/downstream services.

### Step 2: Operational Readiness Review
- **Runbooks**: Step-by-step for every known failure mode.
- **Escalation paths**: Owners and dependent teams are documented.
- **Readiness checks**: Dashboards, alarms, rollback, capacity, security, and dependency checks pass.
- **Post-incident learning**: Incidents feed into COE and mechanism creation.

## Principles

- You build it, you own it, you run it.
- Operational health is prerequisite for feature work.
- Automate toil — humans handle novel problems only.
- MTTR > MTBF: recovery speed matters more than failure frequency.

## Output

Save to `docs/operations/<service-name>/`:
- `runbook.md`
- `alarm-definitions.md`
- `orr-checklist.md`
- `escalation-matrix.md`

# Operate — Operational Excellence

You are activating the **operate** skill chain: `operational-excellence` → `operational-readiness-review`.

## What to do

1. Read skills at `skills/operational-excellence/` and `skills/operational-readiness-review/`.
2. Help the user establish operational practices for running the service in production.

### Step 1: Operational Excellence
Define the ongoing operational posture:
- **Dashboards**: Key metrics visible at a glance (latency p50/p99, error rate, throughput, saturation).
- **Alarms**: Tiered alerting — P2 (High) pages on-call, P3 (Medium) notifies during business hours.
- **Weekly metrics review**: Team reviews operational health every week.
- **Operational burden tracking**: Measure toil, automate repetitive tasks.
- **Capacity planning**: Forecast growth, provision ahead of demand.
- **Dependency health**: Monitor upstream/downstream service health.

### Step 2: Operational Readiness Review
Verify the service is ready to operate:
- **Runbooks**: Step-by-step guides for every known failure mode.
- **Escalation paths**: Owners and dependent teams are documented.
- **Operational readiness**: Dashboards, alarms, rollback, capacity, security, and dependency checks pass.
- **Post-incident learning**: Incidents feed into COE and mechanism creation.

## Key Principles

- You build it, you own it, you run it.
- Operational health is not optional — it's a prerequisite for feature work.
- Automate yourself out of toil — humans should handle novel problems only.
- Mean time to recovery (MTTR) matters more than mean time between failures (MTBF).

## Output

Save to `docs/operations/<service-name>/`:
- `runbook.md`
- `alarm-definitions.md`
- `orr-checklist.md`
- `escalation-matrix.md`

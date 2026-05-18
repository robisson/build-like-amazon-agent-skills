---
name: Progressive Deployment
description: Deploy changes incrementally through expanding blast radius stages with bake time and automatic rollback on alarm.
leadership_principles:
  - Customer Obsession
  - Bias for Action
  - Insist on the Highest Standards
  - Ownership
---

# Progressive Deployment

## Overview

Every production change follows a staged rollout that expands blast radius gradually: One-Box → One-AZ → Regional → Global. Each stage has mandatory bake time during which alarms are monitored. Any alarm breach triggers automatic rollback to the last known-good state. The goal is to detect problems when they affect the fewest customers possible.

## When to Use

- Every code deployment to production
- Configuration changes that affect runtime behavior
- Infrastructure changes (new instance types, scaling policies)
- Database schema migrations with application-level changes
- Any change that could impact customer-facing behavior

## Amazon Context

At Amazon, no service deploys to all hosts simultaneously. The pipeline enforces progressive deployment because the cost of a bad deployment to 100% of hosts is measured in customer trust and revenue. A 1-box deployment that catches a bug costs almost nothing. A full-fleet deployment that causes a critical incident costs millions and erodes customer confidence. Teams that skip stages eventually cause high-severity events—this is not theoretical, it is observed repeatedly.

## The Process

### Stage 1: One-Box (Canary)

1. Deploy to a single host in the lowest-traffic availability zone
2. Route a small percentage of traffic (typically <1%) to this host
3. Monitor for 30-60 minutes minimum (bake time)
4. Compare metrics against the rest of the fleet:
   - Latency p50, p99, p99.9
   - Error rate (5xx, 4xx anomalies)
   - CPU, memory, GC pauses
   - Business metrics (conversion, success rate)
5. Automated gate: proceed only if all metrics are within threshold

### Stage 2: One-AZ

1. Deploy to all hosts in one Availability Zone (~33% in a 3-AZ setup)
2. Bake time: 60-120 minutes
3. Monitor the same metrics at AZ level
4. Watch for cross-AZ dependency issues
5. Verify the AZ can handle full load if others need to absorb traffic during rollback

### Stage 3: Regional

1. Deploy to all hosts in one region
2. Bake time: 2-4 hours (longer for low-traffic regions: 4-8 hours)
3. Verify region-level metrics and cross-region replication
4. Monitor for subtle issues that only appear at higher traffic volumes
5. Choose initial region carefully: not the largest, not the smallest

### Stage 4: Global

1. Deploy to remaining regions in waves (not all at once)
2. Stagger by region size: small regions first, largest last
3. Bake time between region waves: 30-60 minutes
4. Final bake after all regions: 2-4 hours before marking deployment complete

### Rollback Triggers

Automatic rollback fires when any of these conditions are met:
- Error rate exceeds baseline + 0.1% for 3 consecutive minutes
- p99 latency exceeds baseline + 20% for 5 consecutive minutes
- Any P1 or P2 alarm fires
- Dependency health check failures exceed threshold
- Deployment health monitor (synthetic canary) fails

### Rollback Execution

1. Stop forward deployment immediately
2. Revert to previous code/config on affected hosts
3. Verify rollback success with synthetic tests
4. Page on-call if rollback fails or metrics don't recover within 5 minutes
5. Create ticket for investigation regardless of auto-recovery

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "I'll watch the metrics after deploy" | Pipeline blocks progression until bake time completes with green metrics |
| "This change is too small to cause issues" | Every change, regardless of size, goes through all stages |
| "We need this out fast" | Emergency pipeline still has one-box + reduced bake, never zero stages |
| "I'll rollback manually if something breaks" | Rollback is automatic on alarm—human speed is too slow for customers |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "It's just a config change" | Config changes cause more outages than code changes at Amazon | Same pipeline, same stages, same bake times |
| "We're blocking on this for a launch" | A failed launch is worse than a delayed launch | Use the emergency pipeline (reduced bake, not zero bake) |
| "The change was already tested in staging" | Staging doesn't have production traffic patterns, data volumes, or dependency behavior | Staging reduces risk; it doesn't eliminate it. Pipeline stages are still required |
| "It's Friday afternoon but this is urgent" | Weekend deploys have longer detection time due to reduced monitoring attention | Deploy Monday, or accept extended bake times (2x) for off-hours |

## Red Flags

- Skipping one-box because "it's a small change"
- Bake time set to 5 minutes ("just to get through the gate")
- Manual rollback as the only rollback mechanism
- No synthetic canary validating the deployment
- Same bake time for all regions regardless of traffic volume
- Deploying to the largest region first
- No alarm covering the specific functionality being changed
- "We'll add the alarm after we deploy this"

## Verification

Before marking a deployment complete, confirm:

- [ ] One-box stage completed with full bake time
- [ ] One-AZ stage completed with full bake time
- [ ] Regional deployment completed with full bake time
- [ ] All automated rollback triggers are active and tested
- [ ] Metrics dashboard shows no degradation at any percentile
- [ ] Synthetic canary passed at every stage
- [ ] Business metrics (if applicable) show no negative movement
- [ ] Rollback was tested (either actually triggered or dry-run verified within the last 30 days)

## Tenets

1. **Blast radius minimization is not optional.** Every change starts small and grows. No exceptions for "simple" changes.
2. **Bake time is not idle time.** It is active verification that the change behaves correctly under real traffic.
3. **Automatic rollback is faster than any human.** By the time you notice, diagnose, and decide to rollback, thousands of customers have been impacted.
4. **The pipeline is the authority, not the developer.** No individual should be able to bypass safety stages without VP-level approval and a documented reason.
5. **Speed comes from confidence, not from skipping steps.** Teams that invest in deployment safety deploy more frequently because they trust their pipeline.

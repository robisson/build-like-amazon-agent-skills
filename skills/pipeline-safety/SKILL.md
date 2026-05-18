---
name: Pipeline Safety
description: CI/CD pipeline safety with automated gates, deployment blockers, alarm checks, and one-click rollback.
leadership_principles:
  - Customer Obsession
  - Insist on the Highest Standards
  - Ownership
  - Dive Deep
---

# Pipeline Safety

## Overview

A safe pipeline is one that makes it harder to deploy bad code than good code. It enforces automated quality gates at every stage, blocks deployments when alarms are firing, provides one-click rollback, and creates an audit trail of every production change. The pipeline is not a convenience tool—it is a safety system that protects customers.

## When to Use

- Setting up a new service's CI/CD pipeline
- Adding safety gates to an existing pipeline
- Reviewing pipeline configuration for operational readiness
- After any incident caused by a deployment that should have been caught
- When a team is deploying less frequently due to fear of breaking things (symptom of insufficient safety)

## Amazon Context

Amazon's deployment philosophy: the pipeline should be the safest, fastest path to production. If developers feel tempted to bypass the pipeline, the pipeline is broken—either too slow or too fragile. A good pipeline deploys hundreds of times per day across a large organization while catching the handful of changes that would have caused customer impact. The investment in pipeline safety is what enables high deployment velocity.

## The Process

### Pre-Commit Gates

1. **Static analysis**: Linting, type checking, security scanning (SAST)
2. **Unit tests**: Must pass 100%. No "known failures" or skipped tests without expiration dates
3. **Dependency check**: No known vulnerabilities in dependencies above configured severity
4. **Commit message format**: Structured messages that link to tickets/tasks

### Pre-Merge Gates

1. **Integration tests**: Service-level integration test suite
2. **Code coverage**: Cannot decrease. New code must meet minimum threshold (e.g., 80%)
3. **Code review approval**: At least one approval from a qualified reviewer
4. **Design review link**: For changes above a size threshold, link to approved design

### Pre-Deploy Gates

1. **Alarm check**: No active alarms on the target service (P1, P2 block; P3 warn)
2. **Deployment window**: Respect maintenance windows and blackout periods
3. **Active incident check**: No ongoing incidents for this service or critical dependencies
4. **Rollback verification**: Confirm rollback target exists and is healthy
5. **Capacity check**: Sufficient capacity to handle deployment (rolling deploy won't reduce capacity below safe minimum)

### During-Deploy Gates

1. **Health check**: New instances must pass health checks before receiving traffic
2. **Metric comparison**: Real-time comparison against baseline (previous deployment metrics)
3. **Synthetic canary**: Automated customer-journey tests running continuously
4. **Dependency health**: Verify downstream services are healthy
5. **Automatic pause**: Stop deployment if any metric breaches threshold

### Post-Deploy Gates

1. **Bake time enforcement**: Pipeline doesn't mark "complete" until bake time passes with green metrics
2. **Smoke tests**: Automated verification of critical paths
3. **Alarm check (again)**: Verify no new alarms fired during bake period
4. **Audit log**: Record who deployed what, when, and the metrics observed

### One-Click Rollback

Every deployment must support instant rollback:
- Previous known-good artifact is always retained
- Rollback is a single action (button, command, or automatic trigger)
- Rollback does not require a new build or new tests
- Rollback is tested regularly (at least monthly via actual rollback or chaos exercise)
- Rollback time target: <5 minutes from decision to full rollback

### Deployment Blockers

The pipeline MUST block deployment when:
- Active P1 or P2 alarm on the service
- Active incident bridge for the service
- Outside deployment window (configurable per-team)
- Required approvals not obtained
- Test suite has failures
- Security scan has critical findings
- Previous deployment is still baking

Override requires: documented justification + senior engineer approval + post-deploy review within 24 hours.

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "I'll check alarms before deploying" | Pipeline automatically blocks on active alarms |
| "I'll rollback quickly if something goes wrong" | Automatic rollback on alarm, not human decision |
| "I'll make sure tests pass" | Pipeline blocks merge on any test failure |
| "I won't deploy during incidents" | Pipeline queries incident system and blocks |
| "I'll deploy during business hours" | Deployment windows enforced by pipeline |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "The pipeline is too slow" | A pipeline that catches bugs before production saves more time than it costs | Optimize the pipeline (parallel tests, caching) rather than removing gates |
| "This fix is urgent, I need to skip gates" | Urgent fixes are exactly when you make mistakes under pressure | Use the emergency pipeline—fewer gates but never zero |
| "Tests are flaky, we have to ignore them" | Flaky tests mask real failures. Fix them. | Mark flaky tests with expiration dates; fix or delete within 2 weeks |
| "The alarm is a false positive" | You don't know that until you investigate | Fix the alarm signal, don't deploy over it |

## Red Flags

- Developers routinely skip or override pipeline gates
- "Emergency" deployments happen more than once per quarter
- Rollback requires building and deploying a new artifact
- No alarm check before deployment
- Test results are advisory rather than blocking
- No deployment windows or blackout periods
- Pipeline takes >60 minutes for a standard deployment
- No audit trail of who deployed what and when
- Rollback hasn't been tested in the last 30 days

## Verification

- [ ] All pre-commit gates are automated and blocking
- [ ] All pre-merge gates are automated and blocking
- [ ] Alarm check runs before every deployment
- [ ] Deployment blockers are enforced (not advisory)
- [ ] One-click rollback exists and has been tested in the last 30 days
- [ ] Pipeline creates an audit log for every deployment
- [ ] Emergency pipeline exists with reduced (not zero) gates
- [ ] Pipeline completes in <30 minutes for standard changes
- [ ] Override requires documented justification and senior approval
- [ ] Deployment windows are configured and enforced

## Tenets

1. **The pipeline protects customers, not developers' convenience.** Every gate exists because a real incident happened without it.
2. **Fast and safe are not opposites.** A well-designed pipeline is both. If yours isn't, fix the pipeline, don't remove safety.
3. **Blocking is better than warning.** Warnings are ignored under pressure. Gates must block.
4. **Every override is a data point.** Track overrides. If they happen often, the pipeline needs improvement.
5. **Rollback is not failure; inability to rollback is failure.** Design every deployment to be reversible.

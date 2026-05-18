---
name: Feature Flag Lifecycle
description: Complete lifecycle of feature flags from creation through gradual rollout to cleanup, including kill switches and A/B testing.
leadership_principles:
  - Customer Obsession
  - Bias for Action
  - Invent and Simplify
  - Ownership
---

# Feature Flag Lifecycle

## Overview

Feature flags decouple deployment from release. Code ships dark (behind a flag), then is gradually exposed to increasing percentages of traffic. Every flag has a defined lifecycle: creation → gradual rollout → full rollout → cleanup. Flags that live forever become tech debt that obscures code paths and creates combinatorial testing nightmares. Kill switches provide instant off-switches for new features without requiring deployment.

## When to Use

- Launching any customer-facing feature
- Deploying code that changes behavior for existing functionality
- Running A/B tests or experiments
- Providing a kill switch for risky changes
- Migrating between systems (old path vs. new path)
- Enabling features for internal testing before customer exposure

## Amazon Context

Amazon treats feature flags as first-class operational controls. A feature without a kill switch is a feature you can't turn off at 3 AM when it's causing problems. The gradual rollout pattern (1% → 5% → 25% → 50% → 100%) is not arbitrary—each stage allows you to detect different classes of problems. 1% catches crashes and obvious errors. 5% catches performance issues. 25% catches capacity problems. 50% catches subtle behavioral differences. Flags that outlive their purpose are aggressively cleaned up because stale flags are a source of both confusion and incidents.

## The Process

### Flag Creation

1. **Name**: Descriptive, follows naming convention (e.g., `feature.payment.new-checkout-flow`)
2. **Owner**: Individual engineer responsible for the flag's lifecycle
3. **Expiration date**: When this flag should be removed (max 90 days for launch flags, 30 days for experiments)
4. **Type**: Launch flag, experiment flag, ops kill switch, or permission gate
5. **Default state**: Off (new features start dark)
6. **Kill switch behavior**: What happens when toggled off mid-traffic (graceful degradation, not crash)
7. **Metrics**: What metrics indicate success/failure at each rollout stage

### Gradual Rollout

**Stage 1: Internal (dogfooding) — 0% external**
- Enable for internal users/accounts only
- Duration: 2-5 days
- Validate basic functionality with real (internal) usage
- Fix any issues found before external exposure

**Stage 2: 1% of external traffic**
- Duration: 24-48 hours minimum
- Watch for: crashes, exceptions, error rates, latency spikes
- Success criteria: no increase in error rate, no p99 latency degradation >10%

**Stage 3: 5% of external traffic**
- Duration: 48-72 hours
- Watch for: performance under slightly higher load, edge cases in diverse traffic
- Success criteria: same as Stage 2 + no customer contacts about new behavior

**Stage 4: 25% of external traffic**
- Duration: 3-5 days
- Watch for: capacity issues, downstream dependency strain, business metric impact
- Success criteria: business metrics neutral or positive, no capacity alarms

**Stage 5: 50% of external traffic**
- Duration: 5-7 days
- Watch for: A/B comparison stabilization, subtle behavioral regressions
- Success criteria: statistically significant positive or neutral business impact

**Stage 6: 100% of external traffic**
- Duration: 7-14 days (stabilization period)
- Confirm all metrics stable at full rollout
- Begin flag cleanup process

### Kill Switches

Every feature flag serves as a kill switch:
- Toggle off must take effect within 60 seconds globally
- Toggle off must not cause errors (graceful fallback to previous behavior)
- Kill switch must work without a deployment
- Kill switch must be documented in the service runbook
- On-call must know which flags can be toggled and what effect each has

### A/B Testing

When using flags for experimentation:
1. Define hypothesis before creating the flag
2. Define primary metric and guardrail metrics
3. Calculate required sample size for statistical significance
4. Run for the minimum required duration (typically 1-2 weeks)
5. Do not peek and make decisions before reaching significance
6. Document results regardless of outcome
7. Clean up losing variants immediately after decision

### Flag Cleanup

Flags MUST be removed after reaching 100% rollout + stabilization:
1. Remove flag checks from code (both sides of the conditional)
2. Remove flag from configuration system
3. Remove flag-specific tests (keep the behavior tests)
4. Update documentation to reflect the feature as permanent
5. Close the flag's tracking ticket

**Cleanup timeline**: 
- Launch flags: Remove within 14 days of reaching 100%
- Experiment flags: Remove within 7 days of decision
- Kill switches for permanent features: May remain if actively used for operational control (reviewed quarterly)

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "I'll clean up the flag after launch" | Automated alerts when flags pass expiration date. Stale flag report in weekly operational review |
| "I'll monitor the rollout carefully" | Automated rollout gates that block progression without green metrics |
| "The kill switch will work if we need it" | Kill switch tested monthly as part of operational drills |
| "I'll define success criteria before launch" | Flag creation template requires metrics and criteria fields—pipeline blocks without them |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "This flag is simple, it doesn't need gradual rollout" | Simple flags gate complex behavior. You don't know what breaks until real traffic hits it | Every customer-facing flag follows the rollout stages. No exceptions. |
| "We'll clean up flags next sprint" | Next sprint never comes. Flags accumulate and interact in unexpected ways | Set expiration at creation. Automated ticket creation on expiry. Block new flags if team has >10 stale flags |
| "We can't remove this flag, someone might need it" | If it's been at 100% for 30+ days and no one has toggled it, no one needs it | Remove it. If you need the capability again, create a new flag with a new lifecycle |
| "Let's leave the flag so we can rollback" | Rollback via flag beyond 30 days means you haven't committed to the feature | Commit or revert. Long-lived flags are not a substitute for deployment rollback |

## Red Flags

- Flags older than 90 days that haven't been cleaned up
- More than 20 active flags in a single service
- Flags with no owner or an owner who has left the team
- No expiration date on a launch flag
- Kill switch never tested since creation
- Jumping from 1% directly to 100% ("it looked fine at 1%")
- A/B tests running longer than 30 days without a decision
- Flag interactions not documented (Flag A + Flag B = undefined behavior)
- No monitoring specific to the flagged behavior

## Verification

- [ ] Flag has an owner, expiration date, and type
- [ ] Kill switch behavior defined and tested
- [ ] Success metrics defined for each rollout stage
- [ ] Rollout follows the staged percentage plan
- [ ] Metrics monitored at each stage before progression
- [ ] A/B tests have hypothesis, required sample size, and duration
- [ ] Cleanup completed within 14 days of full rollout
- [ ] No flags past their expiration date
- [ ] Kill switch works without deployment
- [ ] Stale flag report reviewed weekly

## Tenets

1. **Flags are temporary by default.** A flag without an expiration date is tech debt waiting to happen.
2. **Gradual rollout catches what testing cannot.** Real traffic at scale reveals problems that no test environment can replicate.
3. **Kill switches must work at 3 AM.** If you can't turn it off without a deploy, it's not a real kill switch.
4. **Clean up is part of the feature work.** The feature isn't done when it reaches 100%—it's done when the flag is removed.
5. **Flag interactions multiply complexity.** Every new flag doubles the number of possible system states. Keep the active count low.

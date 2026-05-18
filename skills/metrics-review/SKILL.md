---
name: Metrics Review
description: Reviewing operational and business metrics for continuous improvement, trend analysis, and proactive issue detection.
leadership_principles:
  - Dive Deep
  - Insist on the Highest Standards
  - Customer Obsession
  - Ownership
---

# Metrics Review

## Overview

Metrics review is the practice of regularly examining operational and business metrics to identify trends, detect degradation early, validate improvements, and drive data-informed decisions. Unlike incident response (reactive), metrics review is proactive—you're looking for problems before they become incidents and confirming that improvements are having the desired effect. Good metrics review distinguishes signal from noise and leads to concrete actions.

## When to Use

- Weekly or monthly as a recurring service health review
- After deploying a significant change (did it improve what we expected?)
- When planning capacity or architecture changes
- When evaluating the effectiveness of past improvements
- When investigating customer experience trends
- When preparing for a launch or traffic event

## Amazon Context

Amazon is deeply metrics-driven. The phrase "in God we trust, all others bring data" captures the culture. Anecdotes and opinions don't drive decisions—metrics do. But metrics can also mislead if you look at the wrong ones, use the wrong aggregation, or ignore confounding factors. A skilled metrics review requires understanding what the metric actually measures, what can influence it, and what actions the metric should trigger. Amazon engineers are expected to know their service's metrics cold and explain any movement.

## The Process

### Metric Categories

**Customer Experience Metrics (primary — these matter most)**
- Availability: percentage of requests served successfully
- Latency: p50, p90, p99, p99.9 — each tells a different story
- Error rate: 5xx (your fault), 4xx anomalies (possibly your fault)
- Throughput: requests per second (traffic health)
- Business success rate: conversions, completions, deliveries

**Operational Health Metrics**
- MTTD: Mean Time to Detect problems
- MTTR: Mean Time to Recover from problems
- Deployment frequency: How often you deploy (higher = smaller, safer changes)
- Rollback rate: What percentage of deploys rollback (lower = better pipeline)
- Change failure rate: Deploys that cause incidents
- On-call page count: Toil indicator

**Resource Metrics**
- CPU, memory, disk utilization across fleet
- Connection pool usage (database, HTTP clients)
- Queue depths and processing lag
- Cache hit rates
- Cost per request (efficiency)

**Business Metrics**
- Conversion rate, order rate, message delivery rate
- Customer contacts and complaint rate
- Feature adoption rate
- Revenue per request (where applicable)

### Review Methodology

**Step 1: Establish baselines**
- What is "normal" for each metric? Use 4-week rolling average
- Account for daily patterns (peak hours), weekly patterns (weekdays vs weekends)
- Account for seasonal patterns (holiday traffic, end-of-month)

**Step 2: Identify anomalies**
- Spikes or dips outside 2 standard deviations from baseline
- Trend changes: gradual degradation over weeks
- Correlation between metrics (latency up AND error rate up = different from latency up alone)
- Missing data (gaps in metrics are a problem themselves)

**Step 3: Classify the signal**
- Is this a known event? (Deploy, traffic spike, downstream issue)
- Is this a new pattern requiring investigation?
- Is this noise? (Single point, already recovered, explained by external factor)

**Step 4: Determine action**
- No action needed (noise, already resolved)
- Create ticket for investigation (unclear signal, needs deeper analysis)
- Immediate action (clear degradation requiring intervention)
- Update alarm thresholds (metric moved but alarms didn't fire when they should have)

**Step 5: Track over time**
- Did the action item improve the metric?
- Is the improvement sustained or temporary?
- Are there second-order effects (improving one metric degrading another)?

### What Good Metrics Review Looks Like

**Looking at latency:**
- DON'T: "p99 is 200ms, that seems fine"
- DO: "p99 is 200ms, which is 15% higher than 4 weeks ago. The increase started on March 3, which correlates with the deployment of feature X. This is within SLA but trending in the wrong direction. Action: investigate whether feature X added an unnecessary network call."

**Looking at availability:**
- DON'T: "We had 99.95% availability this week"
- DO: "Availability was 99.95%, which is above our 99.9% SLA. However, we had two 5-minute windows below 99% that affected approximately 2,000 customers. Both correlated with deployment bake periods. Action: Review bake time alarm sensitivity."

**Looking at deployment frequency:**
- DON'T: "We deployed 8 times this week"
- DO: "Deployment frequency dropped from 15/week to 8/week. This correlates with 3 rollbacks in the past 2 weeks. The team is likely deploying more cautiously due to recent failures. Action: Address the root cause of rollbacks to restore confidence, don't just accept lower velocity."

### Metrics Anti-Patterns

1. **Vanity metrics**: Numbers that look good but don't indicate customer health (e.g., "uptime" that excludes maintenance windows)
2. **Average-only thinking**: Averages hide outliers. A p99 of 5s with p50 of 50ms means some customers are suffering badly
3. **Metric fixation**: Optimizing one metric at the expense of others (e.g., reducing latency by returning cached stale data)
4. **Measurement bias**: Only measuring happy path, not error paths or edge cases
5. **Ignoring rate of change**: 200ms p99 is fine; going from 100ms to 200ms in one week is not fine

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "I'll keep an eye on metrics" | Automated weekly metrics report generated and reviewed on a fixed cadence |
| "I'll notice if something degrades" | Anomaly detection alarms that fire on trend changes, not just absolute thresholds |
| "I'll investigate when things look off" | Degradation triggers automatic ticket creation with investigation template |
| "I'll track whether improvements worked" | Before/after metrics comparison required for closing improvement tickets |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "The metric is within SLA" | Within SLA doesn't mean optimal. Trending toward SLA breach means action is needed now | Track trend direction. Action triggers at 80% of SLA threshold, not 100% |
| "It's just noise" | Repeated "noise" is a pattern. Three noisy data points in a month is a signal | Track "noise" events. If the same anomaly repeats 3x, investigate systematically |
| "We don't have time for deep analysis" | Shallow analysis misses the root cause. You'll spend more time on repeated incidents | Invest 30 minutes in deep analysis now to avoid hours of incident response later |
| "Our metrics are green, we're good" | Green means meeting minimum bar. It doesn't mean you can't improve | Use metrics to drive improvement, not just pass/fail. Set stretch targets |

## Red Flags

- No one can explain why a metric moved in the last week
- Metrics reviewed only during incidents, not proactively
- Only averages reviewed (no percentile analysis)
- Metrics not compared against baseline or trend
- Business metrics completely disconnected from operational metrics
- Metric degradation accepted without investigation ("it's always been like that")
- No automated anomaly detection — relying on humans to notice gradual changes
- Metrics dashboard hasn't been updated in 6+ months (stale)
- Cost metrics not tracked (operational spending growing without awareness)

## Verification

- [ ] Weekly metrics review happens with documented findings
- [ ] Both customer experience and operational metrics are reviewed
- [ ] Percentile latency (p50, p99, p99.9) reviewed, not just averages
- [ ] Trend analysis compares current week to 4-week baseline
- [ ] Anomalies are classified and actioned (not ignored)
- [ ] Metrics improvement tracked after deploying changes
- [ ] Automated anomaly detection configured for key metrics
- [ ] Business metrics correlated with operational metrics
- [ ] Metrics targets defined and tracked (not just SLA minimum)
- [ ] Metrics review produces at least one insight or action per week

## Tenets

1. **Metrics tell stories, not just numbers.** A number without context is meaningless. Always compare against baseline, trend, and target.
2. **Proactive beats reactive.** Finding degradation in metrics review is cheaper than finding it in an incident.
3. **Percentiles reveal truth.** The average hides the suffering of your worst-affected customers. Always check p99.
4. **Every metric needs an owner.** A metric no one watches is a metric no one will act on.
5. **Improvement must be measured.** If you can't measure whether your fix worked, you don't know if it worked.

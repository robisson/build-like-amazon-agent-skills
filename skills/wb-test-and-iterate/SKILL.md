---
name: wb-test-and-iterate
description: "Stage 5 of Working Backwards: Define how success will be measured using input and output metrics, set specific numeric targets, design experiments to validate assumptions, and plan iteration cycles based on data feedback."
leadership_principles:
  - Customer Obsession
  - Dive Deep
  - Insist on the Highest Standards
  - Deliver Results
  - Bias for Action
---

# WB-Test & Iterate: How Will We Measure Success?

## Overview

Test & Iterate defines HOW you'll know whether the product delivers on the promise made in the PR/FAQ. It establishes metrics, targets, and experiments BEFORE building — not after. This prevents the failure mode where teams build something, find metrics that make it look good in retrospect, and declare victory regardless of actual customer impact.

The key distinction in this stage: **input metrics** (what you control and do) vs **output metrics** (what customers experience and value). Input metrics are leading indicators — they move first. Output metrics are lagging indicators — they move later as a consequence of input metrics moving.

Your job is to identify the input metrics you can drive, predict which output metrics should respond, set specific numeric targets for both, and design experiments to validate the causal chain.

## When to Use

- After PR/FAQ is approved (Stage 4) and before engineering begins
- When defining success criteria for a product or feature launch
- During annual planning to set measurable goals for initiatives
- When re-evaluating an existing product that isn't meeting expectations
- When leadership asks "how will you know this is working?"

## Amazon Context

At Amazon, every significant initiative has a **metrics deck** that is reviewed weekly. Metrics are not chosen after launch to make the team look good — they are committed to before building, published in the PR/FAQ's Internal FAQ ("How will we measure success?"), and reviewed rigorously after launch.

Amazon's metrics philosophy:
- **Input metrics over output metrics for operational control.** You can't directly control "customer satisfaction" but you can control "page load time" which drives satisfaction.
- **Controllable metrics over vanity metrics.** "Total signups" is vanity if most users sign up and never return. "Weekly active users doing core action" is controllable.
- **Leading indicators over lagging indicators.** By the time revenue moves, it's too late to course-correct. Watch the metrics that predict revenue movement.

Amazon also distinguishes between:
- **Guardrail metrics:** Must NOT degrade (e.g., latency, error rate, security incidents)
- **Success metrics:** Must IMPROVE to validate the investment (e.g., task completion rate, time-to-value)
- **Counter-metrics:** Measure unintended negative consequences (e.g., if you optimize for speed, counter-metric might be accuracy)

The Weekly Business Review (WBR) mechanism enforces accountability: metrics are reviewed every week, deviations from target trigger investigation, and teams must explain why inputs aren't producing expected outputs.

## The Process

### Step 1: Define the Input-Output Metric Chain

Map the causal chain from what you DO (inputs) to what customers EXPERIENCE (outputs):

```
INPUT METRICS                    OUTPUT METRICS
(You control these)              (Customers experience these)
─────────────────────────────    ──────────────────────────────
Actions your team takes    ───▶  Direct customer outcomes
                                        │
                                        ▼
                                 Business results
                                 (Revenue, retention, NPS)
```

**Example causal chain:**

```
INPUT METRICS                         OUTPUT METRICS
─────────────────────────────         ──────────────────────────
Feature availability (ship date)  ──▶ Customer adoption rate
Documentation completeness        ──▶ Time-to-first-value
API response time (p99)           ──▶ Customer task completion rate
Bug fix response time             ──▶ Customer satisfaction (CSAT)
                                           │
                                           ▼
                                      Retention rate
                                      Revenue per customer
                                      Net Promoter Score
```

For YOUR initiative, identify:
1. **3-5 input metrics** you can directly influence through your team's work
2. **2-3 output metrics** that should respond if your inputs are effective
3. **1-2 business metrics** that are the ultimate measure of value (but lag significantly)

### Step 2: Set Specific Numeric Targets

Every metric needs a target. Without targets, metrics are just monitoring — you can't declare success or failure.

**Target-setting framework:**

| Metric | Current Baseline | Target (90-day) | Target (6-month) | Target (12-month) | Source of Target |
|--------|-----------------|-----------------|-------------------|--------------------|----|
| [Metric 1] | [Current value] | [90-day target] | [6-mo target] | [12-mo target] | [Why this number] |
| [Metric 2] | [Current value] | [90-day target] | [6-mo target] | [12-mo target] | [Why this number] |

**Sources for targets:**
- **Problem statement:** "Reduce from 4.2 hours to <30 minutes" (from Stage 2)
- **Competitive benchmark:** Best-in-class competitor achieves X; we target X or better
- **Customer expectation:** Interviews revealed customers consider Y the acceptable threshold
- **Statistical significance:** Minimum detectable effect for our experiment sample size
- **Step-function improvement:** 10x improvement (not 10%) — if you can't set a 10x target, the solution might not be transformative enough

**Anti-patterns in target-setting:**
- "Improve by 20%" — Why 20%? What does the customer notice?
- "Best in class" — Undefined. Put a number on it
- "Statistically significant improvement" — This is a methodology, not a target
- No baseline documented — You can't measure improvement without a starting point

### Step 3: Define Guardrail and Counter-Metrics

For every success metric, identify what could go wrong:

```
SUCCESS METRIC              GUARDRAIL METRIC            COUNTER-METRIC
(Must improve)              (Must not degrade)          (Watch for unintended harm)
────────────────────        ──────────────────────      ────────────────────────────
Task completion speed   →   Error rate                  Accuracy of completed tasks
User adoption rate      →   System reliability          Performance for existing users
Feature usage frequency →   Page load time              Support ticket volume
New customer acquisition →  Existing customer retention Cost per acquisition
```

**Rule:** You cannot declare success if a guardrail metric degrades, even if the success metric improves. A 50% speed improvement that introduces 5x more errors is not a success.

### Step 4: Design Validation Experiments

Before building the full product, design experiments to validate your riskiest assumptions:

**Experiment Design Template:**

```
EXPERIMENT: [Name]
==================
Hypothesis: "If we [action], then [predicted outcome] because [rationale]"
Riskiest Assumption Being Tested: [What this experiment validates]
Success Criteria: [Specific metric + threshold that confirms hypothesis]
Failure Criteria: [Specific metric + threshold that rejects hypothesis]
Duration: [How long to run for statistical confidence]
Sample Size: [Minimum N for statistical significance]
Methodology: [A/B test / before-after / cohort / prototype test / wizard of oz]

DECISION FRAMEWORK:
- If success criteria met → Proceed to full build
- If failure criteria met → Pivot to alternative approach or kill
- If inconclusive → Extend duration or increase sample size (define limit)
```

**Experiment types by stage:**

| Product Stage | Experiment Type | What It Validates |
|---------------|----------------|-------------------|
| Pre-build | Fake door test | Demand exists (customers click) |
| Pre-build | Wizard of Oz | Solution concept works (manual simulation) |
| Pre-build | Concierge MVP | Customers get value (hands-on with small N) |
| Alpha | Prototype usability test | Customers can use it (task completion) |
| Beta | Limited release A/B test | Metrics improve with real usage |
| GA | Full rollout with holdback | Causal impact at scale |

### Step 5: Plan Iteration Cycles

Define when and how you'll review metrics and make decisions:

**Weekly rhythm:**
- Review input metrics every week in team standup
- Flag any metric trending 20%+ below target as "at risk"
- Identify specific actions to correct trajectory (not just "try harder")

**Monthly rhythm:**
- Review output metrics monthly (they move slower)
- Compare actual metric movement to predicted movement
- If output isn't responding to input improvement, investigate the causal chain

**Decision points:**
- **Week 4 after launch:** Are early indicators positive? If not, what do we adjust?
- **Week 8 after launch:** Is the causal chain working? Inputs moving but outputs flat = broken chain
- **Week 12 after launch:** Are we on track for 6-month targets? If not, is this a timing issue or a fundamental issue?

**Pivot/persevere framework:**
```
METRIC ASSESSMENT AT DECISION POINT
====================================
Inputs improving AND Outputs improving → PERSEVERE (scaling)
Inputs improving AND Outputs flat      → INVESTIGATE (broken chain)
Inputs flat AND Outputs flat           → PIVOT (approach isn't working)
Inputs degrading AND Outputs degrading → KILL or RESTART (fundamental problem)
```

### Step 6: Write the Success Framework

```
SUCCESS FRAMEWORK
=================

Initiative: [Name from PR/FAQ]
Problem Solved: [One-line from Stage 2]
Solution: [One-line from Stage 3]

INPUT METRICS (Team Controls)
| Metric | Baseline | 90-Day Target | 6-Month Target | Owner |
|--------|----------|---------------|----------------|-------|
| [Metric 1] | [Value] | [Target] | [Target] | [Name] |
| [Metric 2] | [Value] | [Target] | [Target] | [Name] |
| [Metric 3] | [Value] | [Target] | [Target] | [Name] |

OUTPUT METRICS (Customer Experiences)
| Metric | Baseline | 90-Day Target | 6-Month Target | Measurement Method |
|--------|----------|---------------|----------------|--------------------|
| [Metric 1] | [Value] | [Target] | [Target] | [How measured] |
| [Metric 2] | [Value] | [Target] | [Target] | [How measured] |

GUARDRAIL METRICS (Must Not Degrade)
| Metric | Current Value | Maximum Acceptable Degradation |
|--------|---------------|-------------------------------|
| [Metric 1] | [Value] | [Threshold] |
| [Metric 2] | [Value] | [Threshold] |

COUNTER-METRICS (Watch for Harm)
| Metric | Current Value | Alert Threshold |
|--------|---------------|-----------------|
| [Metric 1] | [Value] | [Threshold] |

VALIDATION EXPERIMENTS (Pre-build)
| Experiment | Hypothesis | Success Criteria | Duration | Start Date |
|------------|-----------|-----------------|----------|-----------|
| [Exp 1] | [If/then] | [Metric > X] | [Weeks] | [Date] |
| [Exp 2] | [If/then] | [Metric > X] | [Weeks] | [Date] |

DECISION CADENCE
- Weekly: Input metric review (team)
- Monthly: Output metric review (team + PM)
- Quarterly: Business metric review (team + leadership)

DECISION POINTS
| Date | Decision | Criteria |
|------|----------|----------|
| [Launch + 4 weeks] | Continue/Adjust | [Specific criteria] |
| [Launch + 8 weeks] | Investigate/Persist | [Specific criteria] |
| [Launch + 12 weeks] | Scale/Pivot/Kill | [Specific criteria] |

KILL CRITERIA (When to stop):
- [Specific condition that triggers stopping the initiative]
- [Specific condition that triggers stopping the initiative]
```

### Final Step: Present and Wait for Approval

Present your complete Success Framework to the user. Ask:
- "Here's what I have for the Test & Iterate stage. Are these success metrics, guardrails, and experiment designs right?"
- "Anything you'd like to adjust before we finalize the Working Backwards process?"

Wait for the user to respond with explicit approval or requested changes.

- If they request changes → revise the Success Framework → re-present → ask again.
- If they approve → the Working Backwards process is complete and ready for execution planning.

⛔ DO NOT finalize the Working Backwards process until the user explicitly approves or says to continue.

## Example Output

```
SUCCESS FRAMEWORK
=================

Initiative: Deployment Telescope
Problem Solved: Platform engineers spend 4.2 hours diagnosing pipeline failures
Solution: Automated correlation of deployment events with root cause ranking

INPUT METRICS (Team Controls)
| Metric | Baseline | 90-Day Target | 6-Month Target | Owner |
|--------|----------|---------------|----------------|-------|
| Root cause accuracy (top-3) | N/A (new) | 70% | 85% | ML Team |
| Correlation coverage (% of failure types) | N/A | 60% | 90% | Platform Team |
| Time to display correlated timeline | N/A | <30 seconds | <10 seconds | Backend Team |
| CI/CD integrations supported | 0 | 3 (Jenkins, GHA, GitLab) | 7 | Integrations |

OUTPUT METRICS (Customer Experiences)
| Metric | Baseline | 90-Day Target | 6-Month Target | Measurement |
|--------|----------|---------------|----------------|-------------|
| Median time-to-root-cause | 4.2 hours | 45 minutes | 15 minutes | In-product timer |
| % of failures resolved without escalation | 34% | 60% | 80% | Resolution tracking |
| Engineer satisfaction with debugging (1-10) | 3.2 | 6.0 | 8.0 | Monthly survey |

GUARDRAIL METRICS (Must Not Degrade)
| Metric | Current Value | Maximum Acceptable Degradation |
|--------|---------------|-------------------------------|
| Pipeline execution time (added overhead) | 0ms | +500ms (0.5 second max added latency) |
| False positive rate (incorrect root cause in top-1) | N/A | <30% (must not erode trust) |
| Data security (no credential exposure) | 0 incidents | 0 incidents (zero tolerance) |

COUNTER-METRICS (Watch for Harm)
| Metric | Current Value | Alert Threshold |
|--------|---------------|-----------------|
| Engineers skipping manual investigation (over-relying on tool) | N/A | >20% of cases where tool is wrong AND engineer doesn't verify |
| Alert fatigue from correlation notifications | 0 | >3 non-actionable notifications per engineer per day |

VALIDATION EXPERIMENTS (Pre-build)
| Experiment | Hypothesis | Success Criteria | Duration | Start |
|------------|-----------|-----------------|----------|-------|
| Retrospective correlation | If we run correlation algorithm against 50 historical failures, we can identify correct root cause in top-3 for >60% | Accuracy ≥60% on 50 historical cases | 3 weeks | Week 1 |
| Wizard of Oz (manual analysis) | If we manually provide correlated timelines to 5 engineers during real failures, they resolve >50% faster | Time-to-resolution <2 hours for 4/5 cases | 4 weeks | Week 2 |

DECISION CADENCE
- Weekly: Root cause accuracy and coverage metrics (team standup)
- Monthly: Customer time-to-resolution and satisfaction (PM review)
- Quarterly: Retention impact and expansion metrics (leadership review)

DECISION POINTS
| Date | Decision | Criteria |
|------|----------|----------|
| Launch + 4 weeks | Continue / Adjust algorithm | Accuracy ≥50% on live failures AND 10+ active teams |
| Launch + 8 weeks | Invest in V2 / Investigate stall | Time-to-resolution ≤1 hour for median user |
| Launch + 12 weeks | Scale to GA / Pivot approach | 3+ integrations stable AND NPS ≥ 7 from active users |

KILL CRITERIA:
- Root cause accuracy plateaus below 50% after 8 weeks of iteration (algorithm approach fundamentally flawed)
- Fewer than 5 teams actively using after 90 days despite free access (value prop not compelling)
- Security incident involving customer pipeline data (trust destroyed, must rebuild from scratch)
```

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "We'll track metrics after launch" | Success Framework written and approved BEFORE engineering begins. Metrics instrumented in sprint 1 |
| "We'll know success when we see it" | Specific numeric targets committed in writing. No retroactive redefinition of success |
| "We'll iterate based on feedback" | Decision points with specific dates and criteria. Not vague "we'll see how it goes" |
| "We won't let the metrics game us" | Counter-metrics and guardrail metrics defined alongside success metrics |
| "We'll pivot if it's not working" | Kill criteria explicitly defined. Prevents sunk-cost fallacy from keeping a failing initiative alive |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "It's too early to set targets — we don't know enough" | You know the problem statement (Stage 2) and the current baseline. That's enough to set a directional target | Set targets with confidence ranges. "We expect 60-80% improvement" is better than no target. Refine as you learn |
| "Our metrics won't be statistically significant with small N" | Small N means you need larger effect sizes to detect. If your product can't produce a large observable effect with early adopters, the value prop is weak | Design for large effect detection first. If you need 10,000 users to see a difference, the per-user value may be too small |
| "Vanity metrics are fine for early stage — we need traction" | Vanity metrics (signups, page views) don't predict business success. Teams that optimize for vanity metrics build popular-but-unprofitable products | Track vanity metrics for momentum, but DECIDE based on value metrics (retention, engagement depth, task completion) |
| "We can't measure customer satisfaction quantitatively" | You can always find proxies: repeat usage, support ticket reduction, time-on-task improvement, NPS, feature-specific CSAT | Pick 2-3 proxy metrics. Imperfect measurement > no measurement. Triangulate across multiple imperfect signals |
| "Setting kill criteria is defeatist" | Kill criteria are the opposite of defeatist — they're courageous. They commit you to intellectual honesty over sunk-cost rationalization | Define kill criteria as a sign of rigor. Teams that can't name their failure conditions can't recognize failure when it arrives |

## Red Flags

- No baseline measurement for current state (can't measure improvement without starting point)
- Success metrics chosen after seeing data (cherry-picking metrics that look good)
- No guardrail metrics (optimizing one thing at the expense of everything else)
- No counter-metrics (willful blindness to potential negative consequences)
- Targets set so low they're guaranteed to be achieved (sandbagging)
- Targets set so high they're obviously aspirational, not operational
- No decision points with specific dates (perpetual "we're still learning")
- Kill criteria so extreme they'd never trigger ("cancel if the product causes a PR crisis")
- Only output metrics tracked (can't diagnose why things aren't working)
- Only input metrics tracked (can't tell if customer outcomes are actually improving)
- "We'll add metrics in the next sprint" (metrics instrumentation should be sprint 1)

## Verification

Before beginning engineering/execution:

- [ ] 3-5 input metrics identified with clear causal link to customer outcomes
- [ ] 2-3 output metrics identified that reflect actual customer experience
- [ ] Baselines documented for all metrics (or plan to establish baselines in week 1)
- [ ] Specific numeric targets set for 90-day, 6-month, and 12-month horizons
- [ ] Guardrail metrics defined (what must NOT degrade)
- [ ] Counter-metrics defined (watching for unintended negative consequences)
- [ ] At least one validation experiment designed with success/failure criteria
- [ ] Decision points scheduled with specific dates and criteria
- [ ] Kill criteria defined honestly (conditions that would stop the initiative)
- [ ] Metrics instrumentation planned for sprint 1 (not deferred)
- [ ] Weekly/monthly review cadence committed with specific owners
- [ ] Leadership aligned on what "success" means (preventing retroactive redefinition)

## Tenets

1. **Measure what matters to the customer, not what's easy to measure.** The most important metrics are often the hardest to instrument. Do the hard work. Easy metrics (page views, signups) are comforting but rarely decisive.
2. **Input metrics for operators, output metrics for judgment.** The team operates on input metrics daily (they can act on them). Output metrics are for evaluating whether the strategy is working (they judge whether inputs are the right inputs).
3. **Targets before data, not after.** Set success criteria when you're intellectually honest (before building). Retroactive targets are corrupted by the desire to declare success.
4. **Every optimization has a cost — name it.** If you're improving speed, what might you sacrifice in accuracy? If you're increasing coverage, what might you sacrifice in depth? Counter-metrics keep you honest.
5. **Kill criteria are a sign of courage, not pessimism.** The willingness to define failure conditions demonstrates intellectual honesty and prevents the sunk-cost fallacy from consuming resources on losing initiatives.

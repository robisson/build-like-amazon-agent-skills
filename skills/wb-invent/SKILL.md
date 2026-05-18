---
name: wb-invent
description: "Stage 3 of Working Backwards: Generate multiple solution approaches, classify decisions as one-way vs two-way doors, evaluate alternatives against customer benefit and feasibility, and select the recommended solution with clear rationale."
leadership_principles:
  - Invent and Simplify
  - Bias for Action
  - Think Big
  - Are Right, A Lot
  - Frugality
---

# WB-Invent: What Is the Solution? Why This One Over Alternatives?

## Overview

Invent is where creative problem-solving happens — but within disciplined constraints. The input is a validated problem statement (from Stage 2). The output is a recommended solution with a clear explanation of why this approach was chosen over alternatives.

The key discipline: you must generate and evaluate **at least 3 meaningfully different approaches** before selecting one. This prevents the team from anchoring on the first idea (which is usually the most obvious, not the best). Each alternative must be genuinely viable — not a strawman created to make the preferred option look good.

Additionally, every major decision is classified as either a **one-way door** (irreversible, high-consequence) or a **two-way door** (reversible, lower-consequence). This classification determines how much analysis and approval is required before proceeding.

## When to Use

- After completing Stage 2 (Define) with a validated problem statement
- When the team has jumped to a solution without considering alternatives
- When there's internal disagreement about the right approach
- When evaluating build vs. buy vs. partner decisions
- When a proposed solution feels over-engineered or under-ambitious

## Amazon Context

Amazon's Leadership Principle "Invent and Simplify" is paired with Jeff Bezos's concept of Type 1 vs Type 2 decisions:

**Type 1 (One-Way Door):** Irreversible or nearly irreversible. Consequences are severe if wrong. Examples: choosing a database architecture that data will be locked into, public pricing commitments, acquiring a company, launching a new brand.

**Type 2 (Two-Way Door):** Reversible at low cost. If wrong, you can walk it back. Examples: UI changes behind a feature flag, A/B tests, internal tool choices, pricing experiments on a small segment.

The failure mode Amazon guards against: treating every decision like a Type 1 decision (analysis paralysis) or treating every decision like a Type 2 decision (reckless speed). Most decisions are Type 2 and should be made quickly by small groups. Type 1 decisions deserve the full rigor of Working Backwards.

Amazon also emphasizes "disagree and commit" — once a solution is chosen through rigorous evaluation, the team commits fully even if individuals preferred a different option. The time for debate is during Invent, not during execution.

## The Process

### Step 1: Diverge — Generate Solution Approaches

Produce at least 3 meaningfully different approaches. Use these prompts:

**Approach generation techniques:**
1. **The obvious solution:** What would a senior engineer suggest in 5 minutes?
2. **The radical simplification:** What if we could only build 1/10th of what we initially imagined?
3. **The "what if money/time were no object" solution:** Dream big, then work backwards to feasibility
4. **The platform play:** What if we solved this once for many teams/customers?
5. **The buy/partner option:** Who else already solves this? Can we leverage existing solutions?
6. **The "do nothing" option:** What happens if we consciously choose not to solve this? (Baseline)

**For each approach, document:**
```
APPROACH [N]: [Name]
==================
Summary: [2-3 sentence description]
How it works: [Key technical/operational mechanism]
Customer experience: [What the customer sees/does differently]
Key assumptions: [What must be true for this to work]
Biggest risk: [Single biggest reason this might fail]
Effort estimate: [T-shirt size: S/M/L/XL with rationale]
Time to first value: [How long before customers benefit]
```

### Step 2: Classify Decisions as One-Way vs Two-Way Doors

For each major decision within the approaches:

```
┌─────────────────────────────────────────────────────────┐
│              DOOR CLASSIFICATION FRAMEWORK                │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Can we reverse this decision at low cost?               │
│  ├── Yes → TWO-WAY DOOR                                 │
│  │   • Decide quickly (days, not weeks)                  │
│  │   • Small group can decide (2-3 people)               │
│  │   • Optimize for speed of learning                    │
│  │   • Accept 70% confidence threshold                   │
│  │                                                       │
│  └── No → ONE-WAY DOOR                                  │
│      • Full analysis required                            │
│      • Senior leadership review                          │
│      • 90%+ confidence threshold                         │
│      • Consider: Can we restructure to make it two-way?  │
│                                                           │
│  CONVERSION TECHNIQUES (One-Way → Two-Way):              │
│  • Feature flags (ship but don't expose)                 │
│  • Parallel systems (run both, switch traffic)           │
│  • Contracts/APIs (isolate behind interface)             │
│  • Time-limited experiments (try before committing)      │
│  • Partial rollouts (limit blast radius)                 │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

**Common one-way doors:**
- Public API contracts (once external developers depend on them)
- Data model choices (migration cost grows with data volume)
- Pricing structures (customers budget based on published pricing)
- Brand/positioning (market perception is slow to change)
- Team structure decisions (reorgs are expensive and disruptive)

**Common two-way doors (treated erroneously as one-way):**
- UI/UX changes (A/B testable, revertible)
- Internal tooling choices (swap later if wrong)
- Feature scope for v1 (launch small, expand based on data)
- Marketing messaging (test different framings cheaply)
- Internal process changes (try for 2 weeks, revert if worse)

### Step 3: Evaluate Approaches

Score each approach against these criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Customer benefit | 30% | How completely does this solve the problem defined in Stage 2? |
| Time to value | 20% | How quickly can customers start benefiting? |
| Feasibility | 20% | Can we build this with available skills, technology, and resources? |
| Scalability | 15% | Does this approach work at 10x and 100x current scale? |
| Reversibility | 15% | If we're wrong, how easily can we change course? |

**Scoring rubric (1-5):**
- 5: Exceptional — best possible outcome on this dimension
- 4: Strong — clearly above the bar, minor gaps
- 3: Adequate — meets the minimum, no more
- 2: Weak — significant gaps that require mitigation
- 1: Unacceptable — disqualifying on this dimension alone

**Evaluation table example:**
```
| Criterion (Weight)      | Approach A | Approach B | Approach C |
|-------------------------|-----------|-----------|-----------|
| Customer benefit (30%)  |     4     |     5     |     3     |
| Time to value (20%)     |     5     |     2     |     4     |
| Feasibility (20%)       |     4     |     3     |     5     |
| Scalability (15%)       |     3     |     5     |     3     |
| Reversibility (15%)     |     4     |     4     |     2     |
| WEIGHTED SCORE          |   4.05    |   3.85    |   3.45    |
```

### Step 4: Stress-Test the Leading Approach

For the top-scoring approach, conduct a pre-mortem:

1. **Assume it failed.** Write 5 reasons why.
2. **Identify the riskiest assumption.** What single thing, if wrong, kills this approach?
3. **Define the kill criteria.** What evidence would make you abandon this approach?
4. **Plan the de-risking experiment.** What's the smallest thing you can do to validate the riskiest assumption?
5. **Identify the "plan B" trigger.** At what point do you switch to the second-ranked approach?

### Step 5: Write the Solution Recommendation

```
SOLUTION RECOMMENDATION
=======================

Problem Being Solved: [One-line from Stage 2]

Recommended Approach: [Name]
Summary: [3-5 sentences describing the solution and key mechanism]

Why This Approach:
- [Reason 1 with evidence/score reference]
- [Reason 2 with evidence/score reference]
- [Reason 3 with evidence/score reference]

Why Not the Alternatives:
- [Alternative A]: [Specific reason for rejection, not just "lower score"]
- [Alternative B]: [Specific reason for rejection]

Key Decisions:
| Decision | Classification | Rationale |
|----------|---------------|-----------|
| [Decision 1] | One-way door | [Why irreversible, what analysis was done] |
| [Decision 2] | Two-way door | [Why reversible, what speed is appropriate] |
| [Decision 3] | Two-way door | [Conversion technique if applicable] |

Riskiest Assumption: [Statement]
De-risking Plan: [How we'll validate before full commitment]
Kill Criteria: [What would make us stop and switch approaches]

Effort Estimate: [Range with confidence level]
Time to First Customer Value: [Date or sprint count]
Full Solution Timeline: [Date or sprint count]
```

### Final Step: Present and Wait for Approval

Present your complete Solution Recommendation (including the alternatives analysis) to the user. Ask:
- "Here's what I have for the Invent stage. Do these alternatives make sense? Are you happy with the recommended solution?"
- "Anything you'd like to adjust before we move to Refine (PR/FAQ writing)?"

Wait for the user to respond with explicit approval or requested changes.

- If they request changes → revise the Solution Recommendation → re-present → ask again.
- If they approve → proceed to Stage 4 (Refine).

⛔ DO NOT proceed to the Refine stage (PR/FAQ) until the user explicitly approves or says to continue.

## Example Output

```
SOLUTION RECOMMENDATION
=======================

Problem Being Solved: Platform engineers spend 4.2 hours diagnosing
each deployment failure because root cause information is scattered
across 5+ tools with no unified timeline.

Recommended Approach: "Deployment Telescope"
An observability layer that automatically correlates deployment events
with infrastructure changes, log anomalies, and metric shifts into a
single causal timeline. Runs as a sidecar to existing CI/CD tools
(not replacing them). Uses change-correlation algorithms to rank
probable root causes by likelihood.

Why This Approach:
- Highest customer benefit (5/5): Directly addresses the 4.2-hour
  diagnosis time by surfacing probable root cause within 5 minutes
- Strong reversibility (4/5): Runs alongside existing tools as a
  read-only observer. Can be removed with zero impact on pipelines
- Incremental value delivery: First useful output (correlated timeline)
  delivered in 4 weeks. Full root-cause ranking in 12 weeks

Why Not the Alternatives:
- "Pipeline Overhaul" (replace existing CI/CD with integrated platform):
  Scored highest on customer benefit (5) and scalability (5), but
  lowest on feasibility (2) and time-to-value (1). Requires 9-month
  migration that customers won't tolerate. One-way door with
  catastrophic failure mode.
- "Runbook Automation" (auto-generate and execute diagnosis runbooks):
  Fast to deliver (4 weeks) but only solves known failure patterns.
  Novel failures (which cause the longest diagnosis times) are
  unaddressed. Ceiling on customer benefit is 3/5.

Key Decisions:
| Decision | Classification | Rationale |
|----------|---------------|-----------|
| Data correlation algorithm choice | Two-way door | Can swap algorithms behind API; customers see ranked results regardless of implementation |
| Integration approach (agent vs API) | Two-way door | Start with API polling; switch to agent-based push if latency is unacceptable |
| Pricing model (per-deployment vs per-seat) | One-way door | Once published, customers budget against it. Requires pricing experiment with 50 customers before committing |
| Data retention period (7 vs 30 vs 90 days) | Two-way door | Start at 30 days; adjust based on actual usage patterns. Storage cost is linear and reversible |

Riskiest Assumption: That deployment failures can be correlated with
root cause using only observational data (logs, metrics, change events)
without requiring instrumentation changes to the customer's pipeline.

De-risking Plan: Build a prototype correlator against 3 customer
environments (with permission). Manually validate correlation accuracy
against their incident post-mortems. Target: >70% of failures have
correct root cause in top-3 suggestions.

Kill Criteria: If correlation accuracy is <50% after 6 weeks of
iteration, switch to Approach B (Runbook Automation) which has lower
ceiling but higher floor.

Effort Estimate: 3-4 engineers for 12 weeks (high confidence for MVP)
Time to First Customer Value: 4 weeks (correlated timeline, no ranking)
Full Solution Timeline: 12 weeks to GA-quality root cause ranking
```

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "We'll consider alternatives" | Minimum 3 approaches documented with full evaluation. Reviewer checks that alternatives are genuinely viable, not strawmen |
| "We'll move fast on this" | Two-way door decisions must be classified explicitly. Only true two-way doors get the speed treatment |
| "We'll de-risk as we go" | Riskiest assumption identified upfront with explicit de-risking experiment designed BEFORE committing |
| "If it doesn't work, we'll pivot" | Kill criteria defined in writing before starting. Prevents sunk-cost fallacy from keeping a failing approach alive |
| "The team agrees on the approach" | Evaluation table with scores forces explicit tradeoff discussion. Disagreements surface in the scoring, not after launch |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "We don't need alternatives — the solution is obvious" | The "obvious" solution is usually the most familiar one, not the best one. Familiarity masquerades as correctness | Generate alternatives anyway. If the obvious solution truly is best, the evaluation will confirm it in 2 hours |
| "All our alternatives would take too long" | Time-to-value is ONE criterion, not the only one. A fast solution to the wrong problem is worthless | Score alternatives honestly. If all options are slow, that's a sign the problem needs re-scoping, not that you should skip evaluation |
| "This is a two-way door, we don't need analysis" | Two-way door means faster decisions, not zero analysis. You still need to know WHAT you're deciding and WHY | Classify the door type, then match the analysis level. Two-way doors get 1-2 days of evaluation, not zero |
| "We need to move fast — competitors are ahead" | Panic-driven decisions are the most expensive. If a competitor has a 6-month lead, 2 weeks of analysis won't close or widen that gap | Speed comes from clarity, not from skipping thinking. A clear solution recommendation accelerates execution |
| "We should build the platform play from day one" | Premature generalization is the root of over-engineering. You don't know what the platform needs until you've solved 2-3 specific cases | Solve one specific problem well first. Extract the platform from successful specific solutions |

## Red Flags

- Only one solution was seriously considered (the rest are strawmen)
- No explicit classification of one-way vs two-way doors
- The "riskiest assumption" is something easily verified — suggests the real risk is being avoided
- Evaluation criteria are customized to make the preferred solution win
- No kill criteria defined ("we'll make it work no matter what")
- The do-nothing option wasn't considered (sometimes the right answer is "not now")
- Solution is described in technology terms but not customer experience terms
- Effort estimate has no range (single-point estimates are always wrong)
- No de-risking experiment planned for the highest-risk assumption
- The team can't articulate why Alternative B was rejected in one sentence

## Verification

Before advancing to Stage 4 (Refine / PR/FAQ):

- [ ] Minimum 3 genuinely viable approaches documented
- [ ] Each approach has: summary, mechanism, customer experience, assumptions, risks, effort
- [ ] Evaluation table completed with scores and weights
- [ ] All major decisions classified as one-way or two-way doors
- [ ] One-way doors have explicit analysis and senior review planned
- [ ] Two-way doors identified for fast execution (don't over-analyze)
- [ ] Pre-mortem completed for the leading approach (5 failure reasons)
- [ ] Riskiest assumption identified with de-risking experiment designed
- [ ] Kill criteria defined in writing
- [ ] Solution described in customer experience terms (not just technical terms)
- [ ] "Do nothing" option explicitly considered and rejected with reasoning

## Tenets

1. **Alternatives are mandatory, not optional.** You cannot claim you've chosen the best approach without evaluating others. Minimum three. No strawmen. No pre-determined winners.
2. **Classify the door before walking through it.** One-way doors get full analysis. Two-way doors get speed. Confusing the two wastes time (over-analyzing reversible choices) or creates catastrophes (rushing irreversible ones).
3. **Name the riskiest assumption out loud.** Every approach has a "if this isn't true, nothing works" assumption. Identify it. Test it. Plan for what happens if it's wrong.
4. **Simplicity is a feature, not a compromise.** The best solutions are the simplest ones that fully address the problem. Complexity should be added only when simplicity provably fails.
5. **Commit fully once decided.** After rigorous evaluation, the chosen approach gets 100% of the team's energy. Second-guessing during execution is more expensive than making the "wrong" choice with full commitment.

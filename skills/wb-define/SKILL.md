---
name: wb-define
description: "Stage 2 of Working Backwards: Articulate the customer's problem or opportunity with precision, using data to quantify impact and framing it in the customer's language — not engineering jargon."
leadership_principles:
  - Customer Obsession
  - Dive Deep
  - Insist on the Highest Standards
  - Ownership
---

# WB-Define: What Is the Customer's Problem or Opportunity?

## Overview

Define transforms customer insights into a precise, data-backed problem statement. The goal is to articulate the problem so clearly that anyone — engineer, designer, executive, or new team member — can read it and immediately understand: what's broken, for whom, how badly, and why it matters now.

A good problem statement is the single most valuable artifact in product development. It constrains the solution space (preventing scope creep), aligns the team (preventing debates about what we're solving), and provides evaluation criteria (any proposed solution must address THIS problem for THESE customers).

The canonical template:

> **"Today, [customers] have to [problem/painful activity] when [situation/trigger], which causes [quantified negative impact]."**

## When to Use

- After completing Stage 1 (Listen) and having a validated Customer Insight Summary
- When the team has customer data but hasn't converged on what specific problem to solve
- When multiple stakeholders have different interpretations of "the problem"
- When a team is jumping to solutions without clearly defining what they're solving
- When reviewing an existing problem statement that feels vague or too broad

## Amazon Context

At Amazon, the problem statement appears in the PR/FAQ as the "current state" paragraph — the section that describes what life looks like today WITHOUT the proposed solution. This paragraph must make the reader feel the pain. If leadership reads it and shrugs ("so what?"), the PR/FAQ will not be approved.

Common feedback from Amazon leadership on weak problem statements:
- "So what? Why should we care about this?" — Impact not quantified
- "This is a solution masquerading as a problem" — Leading the witness
- "Who specifically has this problem?" — Customer too vague
- "Is this getting worse? Why now?" — No urgency established
- "How do you know this?" — No data cited

The problem statement discipline prevents a failure mode Amazon observed repeatedly in its early days: teams would fall in love with a technical approach and then search for a problem it might solve. The results were technically elegant products that nobody needed.

## The Process

### Step 1: Review Customer Insights

Pull forward the key findings from Stage 1 (Listen):
- Which insight themes represent the biggest opportunity?
- Which problems affect the most customers most frequently?
- Which problems are getting worse over time (growing urgency)?
- Which problems do customers currently have no good workaround for?

Prioritization matrix:
```
                    HIGH FREQUENCY
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         │  Important    │  Critical     │
         │  but niche    │  (start here) │
         │               │               │
LOW ─────┼───────────────┼───────────────┼───── HIGH
SEVERITY │               │               │ SEVERITY
         │  Monitor      │  Painful but  │
         │  (not now)    │  infrequent   │
         │               │               │
         └───────────────┼───────────────┘
                         │
                    LOW FREQUENCY
```

### Step 2: Frame the Problem (Not the Solution)

Write the problem statement using the template. Critical rules:

**DO:** Describe the current state from the customer's perspective
**DON'T:** Imply a specific solution in the problem framing

| Problem Framing (Good) | Solution Disguised as Problem (Bad) |
|------------------------|-------------------------------------|
| "Engineers spend 3 hours/day context-switching between monitoring tools" | "Engineers need a unified monitoring dashboard" |
| "New hires take 6 weeks to make their first production commit" | "The onboarding system lacks automated environment setup" |
| "Customers abandon checkout when shipping cost is revealed late" | "We need to show shipping costs earlier in the flow" |

The test: if your "problem" contains a verb like "need," "lack," or "should have," you've embedded a solution. Rewrite.

### Step 3: Quantify the Impact

Every problem statement must include measurable impact. Without numbers, problems are opinions.

**Impact dimensions to quantify:**

1. **Time cost:** Hours/week wasted, days delayed, time-to-value increased
2. **Money cost:** Revenue lost, extra spend on workarounds, opportunity cost
3. **Frequency:** How often does this happen? Per day? Per week? Per transaction?
4. **Breadth:** How many customers are affected? What % of the segment?
5. **Trend:** Is this getting better or worse? At what rate?
6. **Emotional cost:** Frustration score, NPS impact, support ticket sentiment

Format: "This affects [X customers], happening [frequency], costing [quantified impact], and is [trending direction]."

### Step 4: Establish Urgency (Why Now?)

A problem that has existed for 5 years without action needs a "why now" argument:

- **Market shift:** Competitor solved it, customer expectations changed
- **Scale inflection:** Problem grows super-linearly with usage/customers
- **Technology enabler:** Something is now possible that wasn't before
- **Regulatory pressure:** Compliance deadline, policy change
- **Strategic alignment:** Connects to company priorities this year
- **Compounding cost:** Every month we wait, the problem gets X% worse

### Step 5: Validate with Customers

Before finalizing, verify your problem statement with 3-5 customers:
- Read it to them verbatim
- Ask: "Does this describe your experience? What would you change?"
- Listen for: "Yes, exactly!" vs "Well, sort of, but actually..."
- If >1 customer corrects your framing, rewrite

### Step 6: Write the Complete Problem Definition

```
PROBLEM DEFINITION
==================

Problem Statement:
"Today, [specific customers] have to [painful activity] when [situation/trigger],
which causes [quantified negative impact]."

Customer Segment: [From Stage 1]
Customers Affected: [Number and %]
Frequency: [How often this occurs]
Impact Per Occurrence: [Time/money/frustration per instance]
Annual Aggregate Impact: [Total cost across all customers]
Trend: [Getting better/worse, at what rate]
Why Now: [What makes this urgent today vs. 6 months ago]

Evidence Base:
- [Data point 1 with source]
- [Data point 2 with source]
- [Data point 3 with source]
- [Customer quote that validates the framing]

What Success Looks Like (Without Specifying a Solution):
"In the future state, [customers] will be able to [desired outcome]
in [timeframe/effort], compared to [current timeframe/effort] today."

Constraints:
- [What the solution must NOT do — e.g., must not require migration]
- [What the solution must preserve — e.g., must maintain security posture]
- [Non-negotiable requirements from customers]
```

### Final Step: Present and Wait for Approval

Present your complete Problem Definition to the user. Ask:
- "Here's what I have for the Define stage. Does this problem statement capture the customer's pain accurately?"
- "Anything you'd like to refine before we move to Invent (solution alternatives)?"

Wait for the user to respond with explicit approval or requested changes.

- If they request changes → revise the Problem Definition → re-present → ask again.
- If they approve → proceed to Stage 3 (Invent).

⛔ DO NOT proceed to the Invent stage until the user explicitly approves or says to continue.

## Example Output

```
PROBLEM DEFINITION
==================

Problem Statement:
"Today, backend engineers at mid-size SaaS companies have to manually
investigate and resolve deployment pipeline failures when automated
tests pass but production deployments fail, which causes an average of
4.2 hours of unplanned work per failure and blocks an average of 3
downstream teams for 6+ hours."

Customer Segment: Backend engineers at SaaS companies (100-1000 employees)
who own deployment pipelines serving 20-100 development teams.

Customers Affected: ~12,000 engineers in the US (27% of segment)
experiencing this monthly

Frequency: 3.4 times per month per engineer (average across segment)

Impact Per Occurrence: 4.2 engineer-hours investigating + 18 blocked
engineer-hours across downstream teams = 22.2 engineer-hours total cost

Annual Aggregate Impact: 12,000 engineers × 3.4 occurrences/month × 12
months × 22.2 hours = ~10.9M engineer-hours/year across the segment
(approximately $1.6B in loaded engineering cost)

Trend: Growing 40% YoY as deployment frequency increases but pipeline
complexity grows faster than tooling maturity

Why Now: The shift to microservices and daily deployments (from monthly)
has increased pipeline complexity 5x in 3 years, but debugging tools
remain designed for monolithic, infrequent deployment patterns. Customer
interviews reveal this crossed the "unacceptable" threshold ~8 months ago.

Evidence Base:
- Product analytics: 73% of deployment failures require >2 hours to
  diagnose (Jan-Mar 2026, N=2,847 failure events)
- Customer interviews: 11 of 12 interviewees ranked "deployment debugging"
  in their top 3 time sinks
- Support tickets: 340 tickets in Q1 2026 related to "pipeline failure
  diagnosis" — up 52% from Q1 2025
- "Every time a deploy breaks, I lose my whole afternoon. And I know 3
  teams are sitting there waiting on me." — Platform engineer, Series C
  fintech company

What Success Looks Like (Without Specifying a Solution):
"In the future state, platform engineers will be able to identify the
root cause of a deployment failure and remediate it in under 30 minutes,
compared to 4.2 hours today, without requiring tribal knowledge about
pipeline internals."

Constraints:
- Must work with existing CI/CD tools (not rip-and-replace)
- Must not require full access to production environments
- Must maintain SOC2 compliance for audit trails
- Must work without changing the deployment pipeline architecture
```

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "The problem is obvious to everyone" | Written problem statement required, reviewed by someone outside the team |
| "We'll refine the problem as we build" | Problem statement locked before Stage 3. Changes require re-review |
| "The numbers are roughly right" | Every quantification must cite a source. No unsourced estimates |
| "Customers validated this in passing" | Explicit validation step: read the statement to 3-5 customers verbatim |
| "The problem is too complex for one statement" | If it can't fit the template, you're conflating multiple problems. Split them |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "The problem is self-evident" | Self-evident to you ≠ self-evident to leadership, new team members, or partner teams. And "self-evident" often means "unexamined" | Write it down. If it's truly obvious, writing takes 30 minutes. If writing is hard, the problem wasn't as clear as you thought |
| "We can't quantify this — it's a quality/experience issue" | Every experience problem has measurable proxies: time-on-task, error rate, retry rate, abandonment rate, support contacts | Find the proxy metric. "Frustration" isn't measurable, but "users who rage-click the refresh button 5+ times" is |
| "The problem statement is too narrow — we'll miss opportunities" | A narrow problem is a solvable problem. Broad problems lead to unfocused solutions that half-solve everything and fully-solve nothing | Start narrow. Solve it completely. Expand later if data supports it |
| "We need to keep options open for the solution" | Keeping options open for the solution is fine. Keeping options open for the PROBLEM means you haven't done the work of Listen | A clear problem doesn't constrain solutions — it constrains scope, which is the point |
| "Our execs already defined the problem for us" | Executive framing may reflect a business problem, not a customer problem. "Revenue is declining" is a business observation, not a customer problem statement | Translate the exec framing into customer language. What customer behavior causes the revenue decline? |

## Red Flags

- Problem statement contains a specific solution ("we need to build X")
- Impact is stated without numbers ("it's very frustrating for customers")
- No "Why Now" rationale (if this has been true for years, why prioritize today?)
- Problem validated only internally (no actual customer confirmation)
- Problem affects "everyone" (no segmentation = no focus)
- Multiple unrelated problems crammed into one statement
- Problem framing suspiciously aligns with a technology the team already has
- No constraints defined (suggests the team hasn't thought about what WON'T work)
- Impact quantification uses only best-case assumptions

## Verification

Before advancing to Stage 3 (Invent):

- [ ] Problem statement follows the template: "Today, [who] have to [what] when [when], which causes [impact]"
- [ ] Customer segment is consistent with Stage 1 Customer Insight Summary
- [ ] Impact is quantified with at least 3 measurable dimensions
- [ ] All numbers cite sources (no unsourced estimates)
- [ ] "Why Now" argument is explicit and compelling
- [ ] Problem validated with 3+ customers (they recognize their experience in the statement)
- [ ] Statement does NOT embed a specific solution
- [ ] Success state is defined without prescribing HOW to get there
- [ ] Constraints are documented (what solution must NOT do)
- [ ] Reviewed by at least one person outside the team who confirms clarity

## Tenets

1. **A problem well-stated is half-solved.** Invest disproportionate time in getting the problem statement right. Rushing past this stage is the #1 cause of building the wrong thing.
2. **Customer language, not engineer language.** If the problem statement uses words the customer wouldn't use, rewrite it. Jargon is a hiding place for unclear thinking.
3. **Numbers are non-negotiable.** Unquantified problems are opinions. Opinions don't survive leadership review, and they shouldn't — because they can't be evaluated against alternatives.
4. **One problem, one statement.** If you're solving multiple problems, write multiple statements and prioritize explicitly. Bundling problems obscures tradeoffs.
5. **The problem is stable; solutions are not.** A well-defined problem should remain valid even if you change your solution approach entirely. If your problem statement "breaks" when you consider a different solution, it was solution-shaped all along.

---
name: working-backwards
description: Entry point for developing new products, features, or initiatives using Amazon's Working Backwards process. Orchestrates 5 stages from customer insight to measurable success, starting with the 5 Customer Questions as a lightweight on-ramp before committing to a full PR/FAQ.
leadership_principles:
  - Customer Obsession
  - Invent and Simplify
  - Think Big
  - Have Backbone; Disagree and Commit
  - Bias for Action
---

# Working Backwards

## Overview

Working Backwards is Amazon's signature product development methodology. Instead of starting with a technology or business idea and finding customers for it, you start with the customer and work backwards to the technology. The output is a PR/FAQ document that describes the finished product as if it already exists, written from the customer's perspective. If you can't write a compelling press release, you don't yet understand what you're building or why it matters.

The process has 5 stages, each with a clear deliverable that must pass review before advancing:

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKING BACKWARDS FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  LISTEN  │───▶│  DEFINE  │───▶│  INVENT  │───▶│  REFINE  │  │
│  │          │    │          │    │          │    │  (PR/FAQ) │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       │               │               │               │          │
│       ▼               ▼               ▼               ▼          │
│  Customer        Problem          Solution        PR/FAQ         │
│  Insights        Statement        Selection       Document       │
│                                                       │          │
│                                                       ▼          │
│                                              ┌──────────────┐    │
│                                              │ TEST &       │    │
│                                              │ ITERATE      │    │
│                                              └──────────────┘    │
│                                                       │          │
│                                                       ▼          │
│                                              Success Metrics     │
│                                              & Experiments       │
└─────────────────────────────────────────────────────────────────┘
```

## The 5 Customer Questions (5CQ) — Lightweight Starting Point

Before committing to a full PR/FAQ, answer these 5 questions in 1-2 sentences each. This takes 30 minutes, not 3 weeks, and tells you whether the idea has enough substance to invest in a full Working Backwards cycle.

1. **Who is the customer?** — Name a specific, observable customer segment (not "everyone" or "developers")
2. **What is the customer's problem or opportunity?** — State it in the customer's words, not your technical framing
3. **What is the most important customer benefit?** — Single benefit, stated clearly enough for a press release headline
4. **How do you know what the customer needs?** — Cite data: interviews, support tickets, usage metrics, market research
5. **What does the customer experience look like?** — Describe the end-to-end experience in concrete steps

### When to Use 5CQ vs Full PR/FAQ

| Situation | Start With |
|-----------|-----------|
| Brainstorming session, exploring multiple ideas | 5CQ for each idea, then pick 1-2 for full WB |
| Clear mandate from leadership with defined customer | Jump to Stage 1 (Listen) with full process |
| Hack-a-thon or innovation sprint | 5CQ → rapid PR (no FAQ yet) |
| Annual planning, new product line | Full WB process, all 5 stages |
| Feature addition to existing product | 5CQ to validate, then abbreviated Refine stage |
| Cross-team initiative needing alignment | Full WB process — the PR/FAQ is the alignment mechanism |

## When to Use

- Starting a new product or service from scratch
- Adding a significant feature to an existing product (>2 weeks of work)
- Deciding between multiple competing ideas (use 5CQ to screen, then WB for finalists)
- Annual planning and roadmap creation
- Any initiative where the customer benefit is unclear or disputed
- When a team is "solution-first" and needs to be redirected to customer-first thinking
- Cross-organization initiatives that need a shared understanding of what we're building

## Amazon Context

At Amazon, no significant product investment begins without a Working Backwards document. The PR/FAQ is not a formality — it is the decision artifact. Leadership reviews the document (not a slide deck, not a verbal pitch) and makes investment decisions based on it. A PR/FAQ goes through multiple revisions (often 10-20 drafts) before it is approved. This is intentional: the writing process forces clarity of thought that slides and verbal discussions never achieve.

The mechanism works because:
- Writing full sentences and paragraphs requires rigorous thinking (you can't hide behind bullet points)
- The press release format forces customer-centric framing (you can't lead with technology)
- The FAQ section forces you to confront hard questions early (not after you've already built it)
- The iterative review process ensures the idea is stress-tested before a single line of code is written

Jeff Bezos: "If you can't write a clear press release, you can't think clearly about what you're building."

## Approval Gates Between Stages

Each stage of Working Backwards has a **mandatory human approval gate**. The agent MUST NOT advance to the next stage without explicit user confirmation.

### How Gates Work

After completing each stage, the agent:
1. Presents the full output of that stage to the user
2. Asks the user to review: "Here's what I have for [Stage Name]. Does this look right? Anything you'd like to adjust before we move to [Next Stage]?"
3. **Waits** for the user to explicitly approve or request changes
4. If the user requests changes → revises and re-presents → waits again
5. Only after explicit approval (e.g., "looks good", "let's move on", "approved") → proceeds to the next stage

### Gate Sequence

| Stage | Output Presented | Approval Question |
|-------|-----------------|-------------------|
| Listen | Customer Insight Summary | "Does this customer profile look right? Want to adjust?" |
| Define | Problem Statement | "Does this problem statement capture it? Want to refine?" |
| Invent | Solution Recommendation | "Do these alternatives make sense? Happy with the chosen solution?" |
| Refine | PR/FAQ Document | "Review this PR/FAQ. What needs changing?" |
| Test & Iterate | Success Framework | "Are these success metrics right?" |

### Non-Negotiable Rules

- **Never skip stages.** Even if the user "seems to know what they want," complete each stage sequentially.
- **Never combine stages.** Each stage produces its own distinct output that gets its own review.
- **Never proceed on silence.** If the user hasn't explicitly confirmed, ask again. Do not interpret lack of objection as approval.
- **Never jump to PR/FAQ.** The PR/FAQ is Stage 4. It requires Stages 1-3 to be completed and approved first. There are no shortcuts.

⛔ **An agent that produces a PR/FAQ without showing Listen, Define, and Invent outputs first has violated the process.**

## The Process

### Stage 1: Listen (wb-listen)

**Question:** "Who is the customer and what insights do we have?"

- Identify and segment the target customer
- Gather qualitative and quantitative data about their current experience
- Build customer empathy through direct engagement
- Deliverable: Customer Insight Summary (1-2 pages)

### Stage 2: Define (wb-define)

**Question:** "What is the customer's problem or opportunity?"

- Articulate the problem in the customer's language
- Quantify the impact (time lost, money wasted, frustration caused)
- Establish that this problem is worth solving at scale
- Deliverable: Problem Statement using the template: "Today, [customers] have to [problem] when [situation], which causes [impact]."

### Stage 3: Invent (wb-invent)

**Question:** "What is the solution? Why this one over alternatives?"

- Generate multiple solution approaches (minimum 3)
- Classify decisions as one-way doors vs two-way doors
- Evaluate against customer benefit, feasibility, and business viability
- Deliverable: Solution Recommendation with alternatives analysis

### Stage 4: Refine (wb-refine)

**Question:** "How do we describe this so clearly that any reader understands the customer value?"

- Write the Press Release (customer announcement)
- Write the FAQ (Internal + External questions)
- Create supporting visuals (mockups, architecture diagrams)
- Submit for Doc Bar Raiser review
- Deliverable: Complete PR/FAQ document (typically 6-12 pages)

### Stage 5: Test & Iterate (wb-test-and-iterate)

**Question:** "How will we measure success?"

- Define input metrics (what we control) and output metrics (what customers experience)
- Set success criteria before building
- Design experiments to validate assumptions
- Plan iteration cycles based on metric feedback
- Deliverable: Success Framework with metrics, targets, and experiment design

## Routing Decision: Which Stage to Start?

```
Do you have a clear customer segment with data?
├── No → Start at Stage 1 (Listen)
├── Yes
│   Do you have a validated problem statement?
│   ├── No → Start at Stage 2 (Define)
│   ├── Yes
│   │   Do you have a recommended solution with alternatives analysis?
│   │   ├── No → Start at Stage 3 (Invent)
│   │   ├── Yes
│   │   │   Do you have a reviewed PR/FAQ?
│   │   │   ├── No → Start at Stage 4 (Refine)
│   │   │   └── Yes → Start at Stage 5 (Test & Iterate)
```

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "We'll talk to customers eventually" | Stage 1 requires documented customer conversations or data before Stage 2 begins |
| "Everyone knows what the problem is" | Stage 2 requires a written problem statement reviewed by someone outside the team |
| "We'll figure out the details as we build" | Stage 4 PR/FAQ must be approved before engineering begins |
| "We'll add metrics later" | Stage 5 success criteria are defined before any code is written |
| "Leadership already approved this verbally" | No investment without a written PR/FAQ — verbal approvals are not commitments |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "We don't have time for a full PR/FAQ" | A PR/FAQ takes 2-4 weeks; building the wrong thing takes 6-12 months | Start with 5CQ (30 min). If the idea survives, invest in the full document |
| "The technology is ready, we just need to ship it" | Technology-first thinking is how you build features nobody wants | Write the press release first. If it's not compelling, the technology doesn't matter |
| "Our customers can't articulate what they want" | Customers can't design solutions, but they absolutely can describe their problems | Focus Stage 1 on observing behavior and pain points, not asking for feature requests |
| "The user seems to know what they want, I'll skip to PR/FAQ" | Skipping stages is how you build the wrong thing faster. Every stage exists to surface assumptions and force rigor. Even experts benefit from disciplined sequencing | Complete every stage in order. Present each output. Wait for approval. No shortcuts |
| "This is an internal tool, we don't need WB" | Internal users are customers too. They have the same need for clarity on value | Use the same process with internal customers. The press release is an internal announcement |
| "We already know this will work — [competitor] did it" | Copy-paste from competitors is not customer obsession. Their customers ≠ your customers | Validate that YOUR customers have this problem. Then solve it better, not the same |

## Red Flags

- PR/FAQ written after the product is already built (retro-fitting the narrative)
- No customer quotes, data, or references in the document
- Press release leads with technology instead of customer benefit
- FAQ section has no hard questions (only softballs)
- Single draft submitted for review (no iteration)
- "Customer" is defined as "everyone" or an internal team's convenience
- Success metrics are purely business metrics (revenue, adoption) with no customer experience metrics
- The team can't explain why a customer would choose this over doing nothing
- Document written by one person without cross-functional input
- Agent produced a PR/FAQ without showing Listen, Define, and Invent outputs first
- Agent advanced to the next stage without explicit user approval at the gate

## Verification

Before approving a Working Backwards initiative to proceed to engineering:

- [ ] 5CQ answered clearly and validated with data
- [ ] Customer segment is specific, observable, and large enough to matter
- [ ] Problem statement is written in customer language (not engineering jargon)
- [ ] At least 3 solution alternatives were evaluated with pros/cons
- [ ] PR/FAQ has been through ≥3 revisions with substantive feedback incorporated
- [ ] FAQ section includes at least 5 hard questions (the ones you hope nobody asks)
- [ ] Success metrics include both input and output metrics
- [ ] Success criteria are defined with specific numeric targets
- [ ] A Doc Bar Raiser (or equivalent senior reviewer) has approved the document
- [ ] The team can articulate why NOW is the right time (not just why this is a good idea)

## Tenets

1. **The customer is the starting point, not the technology.** Every sentence in the PR/FAQ must connect back to a real customer need supported by evidence. Technology is the how, never the why.
2. **Writing is thinking.** The PR/FAQ process is not documentation — it is the thinking process itself. If the writing is muddled, the thinking is muddled. Rewrite until it's clear.
3. **Iterate the document, not the product.** It is 100x cheaper to iterate on a 6-page document than on a shipped product. Spend the time upfront.
4. **Mechanisms enforce the process.** No verbal approvals. No skipping stages. No "we'll write it up later." The document is the decision, and the process is the safeguard.
5. **Disagree and commit happens at the document stage.** Debate during PR/FAQ review. Once approved, commit fully. Don't relitigate during execution.
6. **Customer experience is delivered by an API.** The PR/FAQ describes *what the customer experiences*. The Design Document and the API Contract describe *how that experience is exposed*. Every customer-facing capability becomes an API at the design stage, and every client (UI, CLI, SDK, MCP, AI agent, partner integration) consumes that API. The API may be REST (OpenAPI), GraphQL (SDL), gRPC (`.proto`), async / events (AsyncAPI), data (ODCS), MCP, or agent tools — pick the standard that matches the protocol, not OpenAPI by default. This is the bridge between Working Backwards and API First — the customer outcome is the *why*, the API is the contract that delivers it.

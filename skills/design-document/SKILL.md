---
name: Design Document
description: Writing a technical design document that translates a Working Backwards output into a concrete, reviewable engineering plan with architecture, trade-offs, cost estimation, and operational concerns.
leadership_principles:
  - Think Big
  - Dive Deep
  - Invent and Simplify
  - Are Right, A Lot
  - Insist on the Highest Standards
---

# Design Document

## Overview

A design document is the bridge between "what we're building" (Working Backwards output) and "how we're building it." It forces the author to think deeply before writing code, surface trade-offs explicitly, consider operational reality, and invite scrutiny from peers. The document is not documentation—it is a thinking tool. If writing the design document doesn't change your approach at least once, you didn't think deeply enough.

A good design document answers: What problem are we solving? Why this approach over alternatives? What are we trading away? How will we know it's working? How will we operate it at scale?

## When to Use

- Before starting implementation of any project estimated at more than 2 engineer-weeks
- When introducing a new service, API, or significant data store
- When making architectural changes that affect other teams
- When changing system boundaries (splitting or merging services)
- When the blast radius of failure includes customer-facing impact
- When multiple valid approaches exist and the choice isn't obvious
- Before any project that will require a Design Bar Raiser review

## Amazon Context

At Amazon, writing is thinking. A design document is a 6-page narrative (not PowerPoint) that forces clarity of thought. The design document ties directly to the Working Backwards process: the PR/FAQ and PRFAQ define *what* and *why* for customers; the design document defines *how* for engineers. The Design Bar Raiser (DBR) review process ensures the document meets a high bar before implementation begins.

Design documents are living artifacts during the design phase but become historical records once approved. They capture the reasoning at a point in time—including constraints, assumptions, and rejected alternatives—so future engineers can understand *why* decisions were made, not just *what* was decided.

The standard flow: Working Backwards → Design Document → Design Bar Raiser Review → Implementation Plan → Code.

## The Process

### 1. Link to Working Backwards Output

Every design document starts by referencing the approved Working Backwards artifact (PR/FAQ, PRFAQ, or one-pager). This section answers:

- What customer problem are we solving? (1-2 sentences, pulled from WB)
- Who is the customer? (Internal team, external customer, or both)
- What does success look like from the customer's perspective?
- What constraints were established during Working Backwards?

Do NOT re-argue the "what" or "why." That was settled in WB. If you find yourself re-litigating the problem statement, go back and update the WB document first.

### 2. Requirements

#### Functional Requirements

List what the system must do. Each requirement should be:
- Testable (you can write a verification for it)
- Prioritized (P0 = launch blocker, P1 = needed within 30 days of launch, P2 = future)
- Traced to a customer need from the WB output

Example format:
- **FR-1 (P0)**: The system shall process payment transactions within 500ms at p99.
- **FR-2 (P0)**: The system shall support idempotent retries for all write operations.

#### Non-Functional Requirements

Cover these categories explicitly:
- **Latency**: p50, p95, p99 targets for key operations
- **Throughput**: Expected TPS at launch, at 10x, and peak
- **Availability**: Target (e.g., 99.95%) and what "available" means precisely
- **Durability**: Data loss tolerance (zero? RPO of X minutes?)
- **Scalability**: How does the system scale? Horizontally? What's the ceiling?
- **Security**: Data classification, encryption requirements, access control
- **Cost**: Per-unit economics at steady state and at 10x growth
- **Compliance**: Regulatory requirements (GDPR, PCI, SOC2, etc.)

### 3. Proposed Architecture

#### High-Level Architecture

Describe the system using a clear diagram and narrative. Cover:
- Service boundaries and responsibilities
- Data flows (read path and write path separately)
- External dependencies and how you handle their failure
- Storage choices and why
- Async vs. sync boundaries and why

#### Detailed Design

For each major component:
- Input/output contract
- State management approach
- Failure modes and recovery
- Scaling characteristics

#### Data Model

- Schema design with rationale
- Access patterns that drove the design
- Migration strategy from current state (if applicable)
- Growth projections and storage cost implications

### 4. Alternatives Considered

For each rejected alternative:
- **What**: Describe the approach clearly enough that a reader could implement it
- **Pros**: Genuine advantages (not strawmen)
- **Cons**: Why it was ultimately rejected
- **Decision driver**: The specific requirement or constraint that made this inferior

You must include at least 2 alternatives. If you can only think of one approach, you haven't explored the design space enough.

Common alternatives to address:
- Build vs. buy
- Single service vs. multiple services
- Synchronous vs. asynchronous
- SQL vs. NoSQL vs. purpose-built
- Push vs. pull architecture
- Architectural patterns from the `patterns/` catalog when applicable (see below)

#### Using `patterns/` as a source of alternatives

The `patterns/` directory carries architectural patterns whose adoption propagates across the entire system (e.g., cell-based architecture, shuffle-sharding, static stability). Patterns are not a separate mandatory section — they enter the design as alternatives, evaluated against the data and the workload's actual requirements.

When generating alternatives, read `patterns/INDEX.md` (the lightweight catalog) and identify any pattern whose `applies_when` criteria plausibly match the workload's characteristics. Only then load the full `patterns/<name>/PATTERN.md` for matching patterns. A matching pattern becomes a real alternative — it competes with the baseline and other options on its own merits, with concrete pros/cons, cost, and operational impact.

Two important cases:

1. **The user already chose a pattern.** If the user (or the WB output) is asking to implement cell-based, shuffle-sharding, or any other pattern explicitly, the pattern is the starting point. The design then explores alternatives *to* the pattern (e.g., "cell-based with Single-AZ cells" vs "cell-based with Multi-AZ cells" vs "the simpler bulkhead approach within a single instance"), not whether to adopt it at all.
2. **No pattern fits.** If, after scanning the catalog, none of the patterns is a credible match for the workload, do not list patterns just to reject them. Patterns that don't fit don't appear in the design. Quality of thought, not quantity of dismissals.

When a pattern is adopted, copy its `Skill Impact Map` into the relevant later sections (Architecture, Operational Concerns, Testing) — the map is the contract for how the pattern propagates through the rest of the design and into the specs.

### 5. Trade-offs

State trade-offs explicitly using this format:

> **We are choosing X over Y because Z, accepting the consequence that W.**

Examples:
- "We are choosing eventual consistency over strong consistency because our read throughput requirement of 100K TPS cannot be met with a single-leader model, accepting that users may see stale data for up to 5 seconds after a write."
- "We are choosing DynamoDB over Aurora because our access patterns are key-value lookups with predictable latency requirements, accepting that ad-hoc queries will require a separate analytics pipeline."

Every non-trivial design has trade-offs. If your document has none, you're hiding them.

### 6. Cost Estimation

- **Infrastructure cost**: Compute, storage, network, managed services
- **Operational cost**: On-call burden, maintenance time, monitoring
- **Development cost**: Engineer-weeks to build, timeline
- **Cost at scale**: What happens to unit economics at 10x current projection?
- **Cost comparison**: How does this compare to alternatives from Section 4?

Use the AWS pricing calculator or equivalent. Show your math. Include both steady-state and peak costs.

### 7. Operational Concerns

- **Deployment strategy**: How will this be deployed? (Progressive, blue/green, etc.)
- **Rollback plan**: How do you undo a bad deployment? What about data migrations?
- **Monitoring**: What metrics will you emit? What dashboards exist?
- **Alarming**: What conditions trigger alarms? Who gets paged?
- **Runbooks**: What manual interventions might be needed? Document them.
- **On-call burden**: How does this change the on-call experience?
- **Dependency management**: What happens when each dependency fails?
- **Capacity planning**: How do you know when to scale? Is it automatic?
- **Disaster recovery**: RTO and RPO. How do you recover from region failure?

### 8. Testing Strategy

- **Unit tests**: What components are unit-testable? Coverage target?
- **Integration tests**: How do you test service interactions?
- **Load tests**: How do you verify the system meets throughput/latency requirements?
- **Chaos tests**: What failure scenarios will you inject?
- **Security tests**: Penetration testing, SAST/DAST, dependency scanning
- **Acceptance tests**: How do you verify customer-facing requirements from WB?
- **Migration tests**: If migrating, how do you verify correctness during transition?

### 9. Design Bar Raiser Review

Before submitting for Design BR review:
- Ensure all sections above are complete (no TBD or placeholders)
- Have at least one peer pre-review the document
- Prepare a 2-sentence summary of your biggest open question
- Identify which sections you expect the most pushback on
- Schedule the review with adequate lead time (minimum 3 business days for reviewers to read)

See the `design-review` skill for the full review process.

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "I'll think about alternatives" | Document requires at least 2 alternatives with genuine pros for each. When generating alternatives, read `patterns/INDEX.md` and pull in any pattern whose criteria plausibly fit the workload. |
| "I'll consider operational impact" | Mandatory operational concerns section with specific runbook references |
| "I'll come back and add cost estimates" | Cost section is a launch blocker for Design BR review |
| "I'll make sure it's secure" | Threat model section required for any system handling customer data |
| "I'll keep it up to date" | Design doc is frozen after approval; amendments require explicit addendum |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "The design is simple enough; we don't need a document" | Simple designs still have trade-offs, failure modes, and operational concerns. The document forces you to find the non-obvious complexity. | Write the document. If it's truly simple, it will be short. Short is fine. Missing is not. |
| "We'll figure out the details during implementation" | Implementation is too late to discover fundamental architecture issues. Changing direction after code is written costs 10x more. | Identify the unknowns now. Write a spike plan for things you genuinely can't decide without code. |
| "I've built this before, I know how to do it" | Your experience is valuable but not infallible. The document lets others verify your assumptions and catch blind spots. | Write it anyway. Your experience will make it faster to write, and the review will either validate or improve your approach. |
| "The timeline is too tight for a design doc" | A design doc takes 2-5 days. A wrong architecture takes months to fix. The timeline is too tight to NOT write one. | Timebox the document to 3 days. Focus on trade-offs and alternatives. Skip polish, keep substance. |
| "We already discussed this in meetings" | Meetings don't create artifacts. No one can review your meeting. Decisions made verbally are forgotten or remembered differently. | Write it down. If you truly discussed it well, the document will write itself quickly. |

## Red Flags

- Design document has no alternatives considered (author didn't explore the space)
- All alternatives are strawmen with obvious flaws (rigged comparison)
- For a high-criticality workload (≥ 99.99% availability target, RPO < 5s, RTO < 30s, FSI/regulated, ultra-scale, multi-tenant), the alternatives list does not include any pattern from `patterns/INDEX.md` despite plausibly matching criteria — the author skipped the catalog
- An adopted pattern's Skill Impact Map is not reflected in Architecture, Operational Concerns, or Testing
- No explicit trade-offs stated (author is hiding complexity)
- Non-functional requirements are missing or vague ("high availability," "fast")
- Cost section says "TBD" or is missing entirely
- No operational concerns section (author hasn't thought about running this in production)
- Document was written after implementation started (post-hoc justification, not design)
- No link to Working Backwards output (solving an unvalidated problem)
- Testing strategy only mentions unit tests (no integration, load, or chaos)
- Architecture diagram is a single box labeled "Service" (insufficient detail)
- Document is over 20 pages (scope is too large; break into smaller designs)

## Verification

- [ ] Document links to an approved Working Backwards artifact
- [ ] Functional requirements are testable and prioritized (P0/P1/P2)
- [ ] Non-functional requirements include specific numeric targets
- [ ] Architecture section includes both high-level and detailed component design
- [ ] Data model covers access patterns and growth projections
- [ ] At least 2 genuine alternatives are described with real pros/cons
- [ ] When `patterns/INDEX.md` contains a pattern that plausibly fits the workload, it appears as a real alternative (or is the chosen approach) — not silently skipped
- [ ] If a pattern is adopted, its Skill Impact Map is reflected in Architecture, Operational Concerns, and Testing
- [ ] Trade-offs are explicit ("choosing X over Y because Z, accepting W")
- [ ] Cost estimation includes infrastructure, operational, and development costs
- [ ] Operational concerns cover deployment, rollback, monitoring, and on-call
- [ ] Testing strategy covers unit, integration, load, and chaos testing
- [ ] Document has been pre-reviewed by at least one peer before BR review
- [ ] No sections contain "TBD" or placeholder text

## Tenets

1. **Writing is thinking.** The document is not overhead; it IS the design work. If you skip the document, you skip the thinking.
2. **Explicit trade-offs over implicit assumptions.** Every choice has a cost. Name it. If you can't articulate what you're giving up, you don't understand your design.
3. **Alternatives are not decorative.** You must genuinely consider other approaches. If your alternative section reads like a formality, you've failed to explore the space.
4. **Operational reality over architectural elegance.** A beautiful design that can't be operated at 3am by an on-call engineer is a bad design.
5. **The document serves future engineers.** Six months from now, someone will ask "why did we do it this way?" Your document is the answer. Write for them.

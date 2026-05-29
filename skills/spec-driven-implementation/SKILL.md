---
name: Spec-Driven Implementation
description: Bridge between an approved Design Document and code. Decompose the system-level blueprint into N vertical specs (requirements → design → tasks), each independently deliverable. Fail fast by ordering hardest-first. Execute wave-by-wave with approval gates.
leadership_principles:
  - Bias for Action
  - Deliver Results
  - Dive Deep
  - Insist on the Highest Standards
---

# Spec-Driven Implementation

## Overview

After a Design Document is approved by the Design Bar Raiser, you do NOT jump directly to code. Instead, you decompose the macro design into **N vertical specs**—each representing an independently deliverable unit of customer value. Each spec follows the Kiro IDE trio format:

```
requirements.md → design.md → tasks.md
```

This intermediate layer exists because macro designs are too coarse for implementation and too abstract for task tracking. A spec bridges the gap: it is precise enough to code against, small enough to deliver in 1–2 weeks, and traceable back to the approved design.

The flow:

```
Design Document (approved) → Spec 1 → Spec 2 → ... → Spec N → Done
                                 ↓         ↓              ↓
                            Implement  Implement      Implement
                                 ↓         ↓              ↓
                             Deploy     Deploy         Deploy
```

Each spec is a complete vertical slice: from customer-facing behavior at the top to infrastructure at the bottom. No spec depends on "the rest being finished" to deliver observable value.

## When to Use

> **Important:** This skill is invoked as the **final phase of the design command** (`/design`), after the system Design Document is approved. It is NOT part of `/build`. By the time `/build` starts, all specs must already exist with approved requirements, design, and tasks.

- After the Design Document has been **approved** by the Design Bar Raiser
- Before `incremental-implementation` begins on any slice
- When the approved design covers more than a single deployable unit of work
- When multiple engineers will work in parallel on different parts of the system
- When requirements need to be formalized into testable acceptance criteria
- As the **last step of `/design`** — creating the specs that `/build` will execute

**Do NOT use for:**
- Trivial changes (< 2 hours of work)—go directly to implementation
- Bug fixes with clear root cause—use incremental-implementation directly
- Changes already covered by an existing spec
- Prototype/spike work (use `wb-test-and-iterate` instead)

## Amazon Context

> **Flow Clarification:** This skill is the LAST STEP of `/design`. The `/design` command sequence is: design-document → api-contract-first → threat-modeling → design-review → **spec-driven-implementation**. Once specs are created and approved here, `/build` picks them up and executes the tasks. `/build` does NOT create specs — it only reads and executes them.

This skill is the **bridge** in Amazon's engineering workflow:

| Layer | Artifact | Scope | Audience | Approved By |
|-------|----------|-------|----------|-------------|
| Macro | Design Document | System-level blueprint | All engineers, stakeholders | Design Bar Raiser |
| **Micro** | **Spec (trio)** | **Single vertical slice** | **Implementing engineer(s)** | **Tech Lead / Peer** |
| Execution | PR / Commit | Individual code change | Reviewer | Code Review Bar Raiser |

The Design Bar Raiser approved the **macro**—the overall architecture, trade-offs, cost model, and operational plan. Now you plan each slice at **micro** level before coding. This prevents:

1. **Implementation drift**: Code diverges from the approved design because engineers interpret ambiguity differently
2. **Integration hell**: Slices built in isolation don't compose correctly
3. **Missing edge cases**: Requirements not formalized means edge cases discovered in production
4. **Parallelization failure**: Without explicit dependency graphs, parallel work creates merge conflicts and rework

At Amazon, this maps to the practice of writing implementation plans after design approval but before sprint planning. The spec trio formalizes what many senior engineers do informally in their heads—making the reasoning explicit, reviewable, and traceable.

## Template Enforcement (Non-Negotiable)

When generating spec artifacts, you MUST follow the templates EXACTLY:

1. **requirements.md** → Copy structure from `skills/spec-driven-implementation/templates/requirements-template.md`
   - MUST have: Introduction, Glossary, Requirements sections
   - Each requirement MUST have: User Story + Acceptance Criteria
   - Acceptance Criteria MUST use EARS notation: "THE [Subject] SHALL [behavior]", "WHEN [condition] THE [Subject] SHALL [action]"
   - MUST use modal verbs: SHALL, SHALL NOT, MUST, MAY
   - Each criterion must be individually testable and referenceable (e.g., "1.3.a")

2. **design.md** → Copy structure from `skills/spec-driven-implementation/templates/design-template.md`
   - MUST have: Overview, Architecture (with Mermaid diagrams), Components & Interfaces (with code signatures), Data Models, Error Handling, Properties (PBT), Testing Strategy, Security, Open Questions
   - MUST include at least one Mermaid sequence diagram
   - MUST reference requirements by number (traceability)

3. **tasks.md** → Copy structure from `skills/spec-driven-implementation/templates/tasks-template.md`
   - MUST have: Legend, Phases with green-build gates, Tasks with sub-tasks
   - Each task MUST have: size estimate (S/M/L/XL), traceability annotations (_Requirements: X.Y_, _Design: §N.N_, _Depends on: Task X.Y_), Wave assignment
   - MUST end with Dependency Graph JSON showing waves
   - MUST use status markers: `- [ ]` pending, `- [-]` in progress, `- [x]` done, `- [!]` blocked

⛔ RED FLAG: If your spec output does NOT have these sections, STOP and redo it following the template.
⛔ RED FLAG: If your requirements don't use EARS notation (SHALL/WHEN/IF), STOP and rewrite them.
⛔ RED FLAG: If your tasks.md doesn't have a dependency graph with waves, STOP and add it.

## The Process

### 1. Identify Vertical Slices from the Design Document

Read the approved Design Document and identify slices that:

| Criteria | Good Slice | Bad Slice |
|----------|-----------|-----------|
| Delivers observable value | User can see/use something new | Only adds internal plumbing |
| Vertical completeness | API → Logic → Storage → Observability | Only a database migration |
| Independent deployability | Works without other slices being done | Requires slice 3 to function |
| Bounded scope | 1–2 weeks of implementation | Multi-month effort |
| Testable in isolation | Has clear acceptance criteria | "Works when everything else works" |

**Outputs**: A numbered list of slices with one-line descriptions and estimated effort.

### 2. Order Slices by Risk, API First, and Dependency

Apply the **hardest-first** principle (fail fast), **with API First as the dominant ordering rule**:

- **Tier 1 — Foundation**: Infrastructure, schemas, control plane, shared interfaces that others depend on. Only present when an adopted pattern (e.g., cell-based) demands it, or when a one-way door decision (e.g., partition key) must be locked first.
- **Tier 2 — API**: The API spec(s) implementing the customer-value contract end-to-end (handler → logic → storage → observability for that API surface). The API is the only customer-facing contract. **No client spec is created before the API it consumes is specified and frozen.**
- **Tier 3 — Clients**: UI, CLI, SDK, MCP server, AI agent, partner integration, batch job — each is its own spec, built on the now-stable API. A "client" is anything that consumes an API; the word "frontend" is too narrow.
- **Tier 4 — Hardening**: Edge case handling, degraded modes, performance optimization, operational polish, documentation.

Within each tier, order by dependency: if Slice B imports from Slice A, A comes first.

#### API First — the non-negotiable ordering rule

**API specs precede client specs.** When a feature involves both an API and one or more clients (UI, CLI, SDK, MCP, AI agent, batch job, partner integration), the API spec is created and approved first. Client specs are created only after the API contract is stable. This is not negotiable — it prevents the client from leaking implementation assumptions into a not-yet-frozen API surface, and it keeps every client equivalent from the contract's point of view.

The API may be REST, gRPC, an event schema, a data contract, an MCP tool surface, or an agent tool definition. The protocol does not change the rule.

If you find yourself ordering a UI spec before its API spec, stop — you have inverted the dependency. The UI cannot exist without a stable API, and any work done before the API is stable will need to be redone when the API is finalized.

**Rationale**: If the hardest part is impossible or needs redesign, you discover that in week 1, not week 8. Two-way door decisions (reversible) can be reordered; one-way door decisions (schema migrations, public APIs, partition keys) are sequenced carefully — and almost always live in Tier 1 or Tier 2.

### 3. Create a Spec for Each Slice (The Trio)

**⛔ MANDATORY HUMAN REVIEW GATES: Each artifact (requirements → design → tasks) has a mandatory pause for user review. Do NOT generate the next artifact until the previous one is explicitly approved by the user.**

For each slice, create three files in `specs/<slice-name>/`:

#### 3.1 requirements.md

Extract and formalize requirements **for this slice only** from the Design Document.

- Use the EARS (Easy Approach to Requirements Syntax) format
- Each requirement has a User Story and Acceptance Criteria
- Acceptance Criteria use SHALL/MUST/MAY with WHEN/IF/WHERE conditions
- Cross-reference the Design Document section that drives each requirement

**Agent**: Load `agents/requirements-analyzer.md` and apply the `requirements-analyzer` persona to review the requirements for:
- Logical inconsistencies across requirements
- Ambiguous terms ("fast", "large scale", "reasonable")
- Conflicting constraints
- Unstated assumptions
- Missing edge cases and boundary conditions

The agent asks clarifying questions with suggested fixes and updates the requirements.

**🚦 GATE: Present requirements.md to the user. Ask: "Review these requirements. Anything missing, ambiguous, or wrong?" Wait for explicit approval. Do NOT generate design.md until requirements are approved.**

#### 3.2 design.md

Detailed technical design **for this slice only**:

- Architecture specific to this slice (Mermaid diagrams)
- Component interfaces with code signatures
- Data models (schema, types, validations)
- Error handling strategy (retry, circuit breaker, fallback)
- Dependency behavior inherited from the approved Design Document (classification, timeout/retry policy, circuit breakers, bulkheads, fallback behavior, observability)
- Feature flag behavior inherited from the approved Design Document (flag type, safe default, OFF behavior, kill switch behavior, rollout metrics, cleanup)
- Operational behavior inherited from the approved Design Document (customer experience metrics, service health metrics, dashboards, alarms, runbooks, severity expectations, operational burden)
- Properties for property-based testing (PBT)
- Testing strategy (unit, integration, contract)
- Security considerations specific to this slice

This is NOT a repeat of the macro design. It adds implementation detail: exact function signatures, error codes, retry policies, concurrency handling, dependency failure behavior, feature flag behavior, operational behavior, and test properties that the macro design intentionally omits. Specs must preserve dependency-management, feature-flag lifecycle, and operational-excellence decisions from the approved Design Document rather than rediscovering them during `/build`.

**🚦 GATE: Present design.md to the user. Ask: "Review this design. Trade-offs make sense? Anything to adjust?" Wait for explicit approval. Do NOT generate tasks.md until design is approved.**

#### 3.3 tasks.md

Decompose the design into executable tasks:

- Organized in phases with green-build gates between them
- Tasks grouped into parallelizable waves
- Each task has sub-tasks, size estimates, and traceability
- Dependency annotations link tasks to each other
- Requirement traceability links tasks to requirements
- Design references link tasks to design sections
- A dependency graph JSON at the end enables tooling

**Agent**: Load `agents/task-planner.md` and apply the `task-planner` persona to generate the dependency graph, identify the critical path, group tasks into waves, and flag one-way door decisions that need extra review.

**🚦 GATE: Present tasks.md to the user. Ask: "Review this task plan. Dependencies correct? Sizing makes sense?" Wait for explicit approval. The spec is only ready for /build after tasks are approved.**

### 4. Approval Gates

Each spec goes through review before execution:

| Gate | Reviewer | Focus |
|------|----------|-------|
| Requirements Review | Product/Tech Lead | Completeness, correctness, priority |
| Design Review | Peer Engineer | Feasibility, interface contracts, testability |
| Task Review | Tech Lead | Ordering, parallelization, risk |

A spec can be rejected back to any previous stage. Rejection is cheap at this stage—it's just markdown. Rejection after coding is expensive (throwaway code, morale damage).

### 5. Execute Tasks Wave-by-Wave

Once a spec is approved:

1. Execute Wave 1 tasks (these have no dependencies)
2. Verify green-build gate passes (all tests green, no regressions)
3. Execute Wave 2 tasks (depend on Wave 1 outputs)
4. Continue until all waves are complete
5. Load `agents/implementation-verifier.md` and apply the `implementation-verifier` persona to validate PBT properties

Parallel execution within a wave is safe by construction—the `task-planner` guarantees no intra-wave dependencies.

### 6. Post-Spec Completion

After each spec is fully implemented:

1. Run `code-review-bar-raising` on the aggregate changes
2. Deploy using `progressive-deployment` (or batch multiple specs before deploying)
3. Verify acceptance criteria pass in production (canary)
4. Mark the spec as DONE and proceed to the next spec

### 7. Spec Coherence Review (Pre-Build Gate)

After all 3 spec artifacts are approved (requirements.md, design.md, tasks.md) and BEFORE the spec is handed to `/build`, run a coherence review to catch drift between the spec and the approved Design Document.

**Reviewers**: Load `agents/design-bar-raiser.md` and apply the `design-bar-raiser` persona. For one-way door decisions, also load `agents/principal-engineer.md` and apply the `principal-engineer` persona.

**What they check**:
1. Does the spec contradict any decision from the System Design Document?
2. Are all requirements traceable to sections in the Design Doc?
3. Are there new architectural decisions in the spec that weren't in the Design Doc? (scope creep)
4. Is the tasks.md dependency graph achievable within the architecture described?
5. Are one-way door decisions in the spec consistent with the ones identified at design level?
6. Are dependency-management decisions from the Design Document preserved in requirements, slice design, and tasks?
7. Are feature-flag lifecycle decisions from the Design Document preserved in requirements, slice design, and tasks?
8. Are operational-excellence decisions from the Design Document preserved in requirements, slice design, and tasks?

**Output format** (structured so the build agent can consume it directly):

```markdown
## Spec Coherence Review — [Spec Name]

### Verdict: APPROVED | APPROVED WITH NOTES | NEEDS REVISION

### Coherence Matrix
| Requirement | Design Doc Section | Status | Note |
|---|---|---|---|
| Req 1.1 | §3.2 Architecture | ✅ Aligned | — |
| Req 1.2 | §3.2 Architecture | ✅ Aligned | — |
| Req 2.3 | §4.1 Data Model | ⚠️ Divergence | Spec uses DynamoDB but Design Doc specified PostgreSQL |
| Req 3.1 | §5.1 Integration | ❌ No traceability | Requirement not found in Design Doc |

### Findings
- [BLOCKING] Description of blocking issue (must fix before /build proceeds)
- [WARNING] Description of non-blocking concern (proceed with awareness)
- [NOTE] Observation or context for the implementing agent

### Action Items for Build Agent
- [ ] When implementing Req 2.3, use PostgreSQL as specified in Design Doc §4.1 (not DynamoDB as written in spec)
- [ ] Req 3.1 references a service that doesn't exist yet — implement stub first (see Task 1.2)
- [ ] One-way door in Task 2.3 (schema migration) — confirm index strategy matches Design Doc §4.3 before executing
```

The **"Action Items for Build Agent"** section is the KEY deliverable — it becomes an addendum that the build agent reads alongside tasks.md. Save the review output to `specs/<slice-name>/coherence-review.md`.

**🚦 GATE:**
- If verdict is **APPROVED**: Proceed to `/build`. The build agent reads `coherence-review.md` alongside `tasks.md`.
- If verdict is **APPROVED WITH NOTES**: Proceed to `/build`. The "Action Items for Build Agent" section is mandatory reading for the build agent.
- If verdict is **NEEDS REVISION**: Go back and fix the spec artifacts. Do NOT proceed to `/build` until re-reviewed.

**How the build agent uses this**:
When `/build` starts on a spec, it checks for `specs/<slice-name>/coherence-review.md`. If present, the "Action Items for Build Agent" section is treated as binding constraints — equivalent to additional requirements that override or clarify what's in the spec. If an action item conflicts with tasks.md, the action item wins.

## The Spec Format

### requirements.md Format

```markdown
# Requirements: [Slice Name]

## 1. Introduction

### 1.1 Context
[What part of the system this slice addresses]

### 1.2 Scope
[What is IN scope for this spec]

### 1.3 Non-Goals
[What is explicitly OUT of scope]

### 1.4 Design Document Reference
[Link to the approved Design Document section(s)]

## 2. Glossary

| Term | Definition |
|------|-----------|
| ... | ... |

## 3. Requirements

### 3.1 [Feature Area]

#### Requirement 3.1.1: [Short Name]

**User Story**: As a [role], I want [action] so that [benefit].

**Acceptance Criteria**:
1. WHEN [trigger] the system SHALL [behavior] — [rationale]
2. IF [condition] THEN the system MUST [behavior] — [rationale]
3. WHERE [context] the system MAY [behavior] — [rationale]

**Priority**: P0 | P1 | P2
**Design Ref**: §[section number] of Design Document
```

### design.md Format

```markdown
# Design: [Slice Name]

## 1. Overview
[What this slice implements and why this design approach]

## 2. Architecture

```mermaid
[Component/sequence diagram specific to this slice]
```

## 3. Components & Interfaces

### 3.1 [Component Name]

```typescript
interface ComponentName {
  method(param: Type): ReturnType;
}
```

**Responsibilities**: ...
**Error Contract**: ...

## 4. Data Models

[Schema definitions, type definitions, validations]

## 5. Error Handling

| Error | Detection | Response | Recovery |
|-------|-----------|----------|----------|
| ... | ... | ... | ... |

## 6. Properties (PBT)

| Property | Formal Statement | Generator Strategy |
|----------|-----------------|-------------------|
| Idempotency | f(f(x)) = f(x) for all x | Random valid inputs |
| Monotonicity | if a ≤ b then f(a) ≤ f(b) | Ordered pairs |

## 7. Testing Strategy

| Level | What | How | Coverage Target |
|-------|------|-----|----------------|
| Unit | Pure logic | PBT + example-based | 90%+ |
| Integration | Component boundaries | Contract tests | All interfaces |
| E2E | User-facing flows | Acceptance criteria | All P0 requirements |

## 8. Security

[Authentication, authorization, data protection for this slice]

## 9. Open Questions

[Unresolved decisions to discuss during review]
```

### tasks.md Format

```markdown
# Tasks: [Slice Name]

## Legend

- 🏗️ Infrastructure / Setup
- 🔧 Implementation
- 🧪 Testing
- 📖 Documentation
- 🚀 Deployment
- 🔒 One-way door (irreversible — needs explicit approval)
- 🔓 Two-way door (reversible — bias for action)
- ✅ Green-build gate

## Phase 1: Foundation

✅ **Green-build gate**: All existing tests pass. CI pipeline green.

### Task 1.1: [Task Name] 🏗️ 🔓

_Size: S | Requirements: 3.1.1 | Design: §3.1_
_Depends on: None (Wave 1)_

- [ ] Sub-task A
- [ ] Sub-task B
- [ ] Sub-task C

### Task 1.2: [Task Name] 🔧 🔓

_Size: M | Requirements: 3.1.2, 3.2.1 | Design: §3.2_
_Depends on: Task 1.1_

- [ ] Sub-task A
- [ ] Sub-task B

## Phase 2: Core Logic

✅ **Green-build gate**: Phase 1 tests pass. New interfaces compile. No regressions.

### Task 2.1: [Task Name] 🔧 🔓

_Size: L | Requirements: 3.2.1 | Design: §4.1_
_Depends on: Task 1.2 (Wave 2)_

- [ ] Sub-task A
- [ ] Sub-task B
- [ ] Sub-task C
- [ ] Sub-task D

## Dependency Graph

```json
{
  "tasks": {
    "1.1": { "depends_on": [], "wave": 1, "size": "S" },
    "1.2": { "depends_on": ["1.1"], "wave": 1, "size": "M" },
    "2.1": { "depends_on": ["1.2"], "wave": 2, "size": "L" }
  },
  "critical_path": ["1.1", "1.2", "2.1"],
  "waves": {
    "1": ["1.1", "1.2"],
    "2": ["2.1"]
  }
}
```
```

## Three Specialized Sub-Agents

### requirements-analyzer

Load `agents/requirements-analyzer.md` before performing this review.

**Purpose**: Cross-requirement consistency checking. Does NOT analyze requirements in isolation—reasons across ALL requirements simultaneously.

**What it catches**:
- Logical inconsistencies: Requirement A says "at most 5 seconds" but Requirement B says "real-time response"
- Ambiguities: "large scale", "fast enough", "reasonable timeout", "appropriate level"
- Conflicting constraints: Requirement A demands strong consistency; Requirement B demands sub-10ms latency for the same operation
- Unstated assumptions: Requirements assume a database exists but no requirement specifies its creation
- Missing edge cases: Happy path defined but no requirement for timeout, partial failure, or concurrent access

**How it works**: Reads all requirements, builds a constraint graph, identifies contradictions and gaps, asks clarifying questions with suggested resolutions, then updates requirements.md with the resolved version.

### task-planner

Load `agents/task-planner.md` before generating tasks or dependency graphs.

**Purpose**: Decompose design into executable tasks with optimal ordering.

**What it does**:
- Identifies natural phases (foundation → core → edge cases → observability)
- Creates a dependency graph with explicit edges
- Groups independent tasks into parallelizable waves
- Identifies the critical path (longest dependency chain)
- Assigns size estimates (S/M/L/XL) based on complexity and risk
- Flags one-way door decisions that need explicit approval before execution
- Marks two-way door decisions where bias for action applies

**How it works**: Reads design.md, extracts components and their relationships, generates tasks that build components bottom-up, validates that every requirement has at least one task covering it, and produces the tasks.md with dependency graph JSON.

### implementation-verifier

Load `agents/implementation-verifier.md` before validating properties or implementation/design conformance.

**Purpose**: Validate that implementation satisfies the spec's properties and requirements.

**What it does**:
- Extracts PBT properties from design.md
- Generates property-based tests from EARS requirements
- Runs tests against the implementation
- Detects regressions when later specs break earlier specs
- Flags implementation divergence from design (e.g., interface mismatch, missing error handling)

**How it works**: After each task wave completes, runs the verification suite. Reports pass/fail per property with counterexamples on failure. Compares actual interfaces against design.md signatures. Alerts when implementation deviates from the spec.

## Mechanisms Over Good Intentions

| Intention | Mechanism | Why the Mechanism |
|-----------|-----------|-------------------|
| "We'll make sure requirements are consistent" | `requirements-analyzer` agent runs cross-check | Humans miss contradictions across 20+ requirements |
| "We'll implement in the right order" | Dependency graph JSON + wave grouping | Ad hoc ordering leads to blocked developers |
| "We'll test thoroughly" | PBT properties extracted from EARS → auto-generated tests | Manual test selection has coverage blind spots |
| "We won't break existing features" | Green-build gates between phases | Without gates, regressions accumulate silently |
| "We'll keep design and code in sync" | `implementation-verifier` compares signatures | Drift happens gradually and is invisible until production |
| "We'll review before coding" | Approval gates between spec phases | Without gates, "I'll get review later" becomes never |
| "We'll parallelize safely" | Wave grouping guarantees no intra-wave deps | Informal "this should be safe" causes merge conflicts |

## Common Rationalizations

| Rationalization | Why It's Wrong | The Mechanism |
|-----------------|---------------|---------------|
| "The design doc is detailed enough—we don't need specs" | Design docs describe the system; specs describe the work. They serve different audiences and timescales. | Require specs for any slice > 2 days of work |
| "Writing specs slows us down" | Writing specs takes hours; debugging integration failures takes days. Specs are faster. | Track rework hours pre-spec vs post-spec adoption |
| "We'll figure out the order as we go" | Ad hoc ordering causes blocked engineers, context-switching, and idle time. | task-planner generates optimal order upfront |
| "Requirements are obvious from the design" | 73% of production bugs trace to ambiguous or missing requirements, not logic errors. | requirements-analyzer forces explicit formalization |
| "We can skip the approval gate for this one" | The one you skip is the one that fails. Gates are cheap; rollbacks are expensive. | Tooling enforces gates—no skip without explicit override |
| "The template is too heavy for this simple feature" | Every spec follows the same format regardless of size. Consistency enables tooling, parallelization, and resumability. A small spec just has fewer requirements and tasks — but the structure is identical. | Template enforcement via format validation |

## Red Flags

Watch for these signals that the spec process is being short-circuited:

- 🚩 **Spec with zero open questions** — Either trivially simple (shouldn't need a spec) or the author hasn't thought deeply enough
- 🚩 **Tasks with no dependency annotations** — Means ordering hasn't been analyzed; parallelization will be wrong
- 🚩 **Requirements without acceptance criteria** — Untestable requirements are wishes, not specifications
- 🚩 **Design that repeats the macro design** — The spec should ADD detail, not copy it. If it's a copy, the spec is waste.
- 🚩 **All tasks in a single wave** — Either the slice is too small for a spec or dependencies haven't been identified
- 🚩 **No PBT properties in design** — Properties are how you verify correctness beyond example-based tests
- 🚩 **Spec covering more than 2 weeks of work** — Slice further. Large specs lose the benefits of incremental delivery.
- 🚩 **Client spec (UI, CLI, SDK, MCP, AI agent, partner) ordered before its API spec** — API First is non-negotiable. The client cannot be specified before the contract it consumes is stable. Re-order.
- 🚩 **Logic embedded in a client spec to work around a missing API capability** — Evolve the API instead. Client-side workarounds leak implementation details and trap the API in its current shape.
- 🚩 **Feature has a UI/CLI/agent in the design but no API spec exists** — Every customer-facing surface is an API. If you cannot identify the API, the design is incomplete; go back to `/design`.
- 🚩 **`/build` stopped at the end of a spec to ask "proceed to the next?"** — That is not a valid stop reason. PASSED verdict means continue automatically. The user opts into pausing only by saying so explicitly.
- 🚩 **`/build` declared "done" while `specs/` still has unstarted specs** — `/build` is complete only when every spec is in a terminal state, not when one spec finishes.
- 🚩 **Agent generated all three spec files (requirements, design, tasks) without pausing for user review between them** — Each artifact has a mandatory human approval gate. Generating all three in one pass means the user had no opportunity to course-correct.
- 🚩 **Spec output missing EARS notation in acceptance criteria** — Requirements without SHALL/WHEN/IF are informal wishes, not testable specifications. Rewrite using the EARS template.
- 🚩 **tasks.md without dependency graph or wave assignments** — Without the JSON dependency graph and wave grouping, parallelization is guesswork and ordering is arbitrary.
- 🚩 **design.md without Mermaid diagrams or requirement traceability** — A design that doesn't reference requirement numbers and doesn't visualize architecture is disconnected from the spec chain.
- 🚩 **Agent generated all spec files without reading the templates first** — The templates at `skills/spec-driven-implementation/templates/` define the required structure. Generating from memory produces inconsistent, incomplete specs.

## Verification

Before marking the spec process complete for a slice:

- [ ] Every requirement in requirements.md traces to a Design Document section
- [ ] Every requirement has testable acceptance criteria in EARS format
- [ ] `requirements-analyzer` has run and all issues are resolved
- [ ] design.md adds implementation detail beyond the macro design
- [ ] design.md includes PBT properties for all critical behaviors
- [ ] tasks.md has a valid dependency graph (no cycles, no orphans)
- [ ] Every task traces to at least one requirement
- [ ] Every requirement has at least one task covering it
- [ ] Green-build gates are defined between all phases
- [ ] One-way door decisions are explicitly marked and have approval
- [ ] Wave grouping has no intra-wave dependencies
- [ ] Critical path is identified and estimated
- [ ] Approval gates have been passed for all three documents
- [ ] `implementation-verifier` passes after final wave
- [ ] At spec completion, every entry in `tasks.md` is `[x]` (done) or `[!]` (blocked, with documented reason). No task remains `[ ]` or `[-]`. The orchestrator (the agent running `/build`) is responsible for keeping this file truthful throughout execution — sub-agents never edit `tasks.md` directly.

## Tenets

1. **Specs are thinking tools, not bureaucracy.** If writing the spec doesn't change your implementation plan, you either didn't think deeply enough or the work is too trivial for a spec.

2. **Fail fast, fail cheap.** Order by risk. If the hardest slice is infeasible, discover that before building the easy slices that depend on it.

3. **Every slice delivers value.** A spec that requires "the other 5 specs to be done first" is not a vertical slice—it's a horizontal layer. Slice differently.

4. **Mechanisms enforce what intentions forget.** Approval gates, dependency graphs, and automated verification exist because "we'll be careful" doesn't scale.

5. **The spec is not the design doc.** The design doc says "the system SHALL have an authentication module." The spec says "the authentication module SHALL use PKCE flow with 5-minute code expiry, return HTTP 401 with error body `{code: 'TOKEN_EXPIRED', retry_after: seconds}`, and satisfy the property: `for all valid tokens t, verify(sign(t)) == true`."

6. **Parallelism is earned, not assumed.** Tasks run in parallel only when the dependency graph proves they are independent. "I think these are independent" is not proof.

7. **Traceability is non-negotiable.** Every task links to a requirement. Every requirement links to the design. Every design section links to the Design Document. If you can't trace it, you can't verify it.

8. **API First.** Every customer-facing surface is an API. UI, CLI, SDK, MCP server, AI agent, partner integration, batch job — all clients of an API. The API spec is created and frozen before any client spec. A client never bypasses its API; if a client needs new behavior, the API evolves. This is the direct application of Amazon's 2002 API Mandate to the spec layer.

9. **`/build` runs to completion, not to the end of one spec.** Approval gates happened during `/design`. Once `/build` is invoked, the agent executes every spec in `specs/` end-to-end, without pausing between waves, specs, or post-implementation reviews (when verdict is PASSED). Stopping at the end of one spec to ask "should I proceed?" is not a checkpoint — it is a process failure. The default is **autonomous to feature completion**; the user opts into a paused mode only by saying so explicitly in the prompt.

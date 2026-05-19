---
name: Using Amazon Skills
description: Meta-skill for navigating and applying the complete skills library. Routing flow chart, core operating behaviors, and skill discovery logic.
leadership_principles:
  - Customer Obsession
  - Ownership
  - Insist on the Highest Standards
  - Bias for Action
---

# Using Amazon Skills

## Overview

This is the meta-skill: it describes how to navigate, select, and combine the other skills in this library. Use this when you're unsure which skill applies, when you need to understand how skills interact, or when you want to establish core operating behaviors that underpin all other skills. Think of this as the operating system on which individual skills run.

## When to Use

- Starting a new project and wondering "what's the Amazon way?"
- Unsure which skill applies to your current situation
- Onboarding new team members to this way of working
- Wanting to establish core behaviors before diving into specific practices
- Assessing whether your team is following the overall system, not just individual parts

## Amazon Context

Amazon doesn't have a single monolithic process—it has a collection of mechanisms, principles, and practices that compose together. The power comes from the composition: progressive deployment is effective because pipelines enforce safety gates, which work because alarms are set up correctly, which matter because the team operates the service they build. Remove one piece and the others weaken. This meta-skill helps you see the whole system.

## Skill Routing Flow Chart

### "I'm starting a new project"

```
Start → Working Backwards (define what customer needs)
      → Dependency Management (if external/system dependencies exist)
      → Feature Flag Lifecycle (if controlled exposure or kill switch is needed)
      → Operational Excellence (operational signals and runbooks)
      → Design Document (technical approach)
      → API Contract First (define interfaces)
      → Infrastructure as Code (define resources)
      → Operational Excellence (set up monitoring)
      → Progressive Deployment (ship safely)
```

### "I'm writing/reviewing code"

```
Code change → Code Review Bar Raising (quality)
            → Test-Driven Development (coverage)
            → Pipeline Safety (automated gates)
            → Progressive Deployment (ship it)
```

### "I'm deploying a change"

```
Ready to deploy → Feature Flag Lifecycle (if a flag gates release)
               → Pipeline Safety (gates passing?)
               → Progressive Deployment (staged rollout)
               → Operational Excellence (monitoring ready?)
               → Operational Readiness Review (prepared to launch?)
```

### "Something is broken"

```
Incident → Correction of Errors (learn from it)
         → Mechanism Creation (prevent recurrence)
         → Metrics Review (track improvement)
```

### "I want to improve how we work"

```
Improvement → Metrics Review (identify gaps and measure current state)
            → Mechanism Creation (automate improvements)
```

## Core Operating Behaviors

These behaviors underpin all skills and should be followed regardless of which specific skill you're applying:

### 1. Customer Backwards

Every decision starts with: "What's the customer impact?" Not "what's easiest for us" or "what's technically elegant." The customer's experience is the measure of success.

### 2. Data Over Opinions

When someone says "I think..." ask "What does the data say?" Opinions are hypotheses. Data is evidence. Make decisions on evidence.

### 3. Bias for Action with Reversible Decisions

Most decisions are reversible (Type 2). Make them quickly. Use progressive deployment, feature flags, and rollback to make decisions reversible. Reserve extensive deliberation for irreversible decisions (Type 1).

### 4. Mechanisms Over Good Intentions

Whenever you find yourself saying "we should..." or "we need to remember to...", stop and build a mechanism. Automate the safeguard. Remove the human from the critical path.

### 5. Ownership Without Boundaries

You own the entire experience, not just your component. If a customer problem crosses team boundaries, you own driving it to resolution even if the fix is in someone else's code. You can't say "that's not my team's service."

### 6. High Standards Are Contagious

What you accept becomes the new normal. If you accept flaky tests, you'll get more flaky tests. If you accept missing alarms, you'll get more services without alarms. Hold the bar on everything.

### 7. Simplicity Is a Feature

The simplest solution that meets requirements is almost always the best. Complexity is not a sign of quality—it's a sign of insufficient thinking. Every line of code is a liability.

### 8. Written Thought Over Verbal Discussion

Write things down. Written documents force clarity that verbal discussions don't. Ambiguity hides in conversation but is exposed on paper.

### 9. API First

Every customer-facing surface is an API. The API is the contract; everything behind it is private implementation. Design and ship the API before any of its clients.

A **client** is anything that consumes an API: a web UI, a mobile app, a CLI, an SDK, an MCP server, an AI agent, another internal service, a partner integration, a batch job. They are all clients of the same API and follow the same rules. The word "frontend" is too narrow — use "client" or "API consumer".

The API may be REST, GraphQL, gRPC, an async / event surface, a data contract, an MCP tool surface, an agent tool definition, a webhook, a CLI, or an SDK. The protocol does not change the rule: **the contract is designed, frozen, and shipped before the clients that depend on it.**

**Pick the right standard for the protocol** — OpenAPI is *not* the universal answer. Use OpenAPI for REST, GraphQL SDL for GraphQL, `.proto` for gRPC, AsyncAPI (with JSON Schema / Avro / Protobuf payloads) for async events, ODCS for data contracts, MCP manifest for MCP tools, provider-native tool spec for AI agents. See `skills/api-contract-first/SKILL.md` for the full mapping.

If a client needs behavior the API doesn't expose, evolve the API. Do not embed logic in the client to work around a missing API capability. Doing so leaks implementation details into the client and makes the API impossible to evolve later.

This rule is the direct descendant of Amazon's 2002 API Mandate: every team exposes its functionality only through APIs, and there is no other way to consume what another team built.

## Architectural Patterns

Alongside skills, this repository carries a catalog of **architectural patterns** in `patterns/`. Patterns are different in nature from skills:

- **Skills** = how to *execute* a phase (workflows with gates).
- **Patterns** = what to *decide* (architectural choices that propagate across the system).

A pattern, once adopted, changes how almost every skill is applied — partition keys leak into APIs, deploy strategy changes, observability changes, on-call changes. Each `patterns/<name>/PATTERN.md` declares its applicability in `applies_when:` and carries a `Skill Impact Map` listing exactly which skills change.

**How patterns enter design (Amazon-style):** patterns are not a separate mandatory checklist. They feed **Alternatives Considered** in the Design Doc. When generating alternatives, read `patterns/INDEX.md` (lightweight catalog) and identify any pattern whose `applies_when` criteria plausibly match the workload. Only then load the full `patterns/<name>/PATTERN.md` for matching patterns. That pattern becomes a real alternative, evaluated with data and trade-offs against the other options. If the user (or the WB output) is asking for a specific pattern (e.g., "implement cell-based"), the pattern is the chosen approach and alternatives are explored *within* it. Patterns that don't fit don't appear — quality of thought, not quantity of dismissals.

When a pattern is adopted, its `Skill Impact Map` becomes a constraint on the rest of the design and on the specs that follow.

## Match the Ceremony to the Change (Proportionality Ladder)

The Build Like Amazon flow is designed for change of every size — from a one-line fix to a brand-new product. The full ceremony (`/wb` → `/design` → `/spec` → `/build`) is appropriate for **a small fraction** of changes; applying it everywhere is over-engineering and makes the agent feel slow.

**The agent's job is to choose the right ceremony level automatically — never the user's job.** The user describes the change; the agent classifies and proposes 2-3 concrete options when there is genuine ambiguity. The user picks an outcome (time, scope, traceability), not a process step.

### The ladder

| Change size | Examples | Recommended path | Artifacts produced |
|---|---|---|---|
| **Trivial** (< 2h, no customer impact) | Typo fix, dependency bump, comment cleanup, internal helper rename, dev-only logging tweak | Direct to code with Code Quality Bar from `incremental-implementation`. No spec, no Design Doc, no PR/FAQ. | Code + tests |
| **Small** (2h-1d, customer-facing but local) | Add a button, change copy, add a field to an existing API response (additive, backward-compatible), add an alarm, fix a known bug with clear root cause | Direct to code OR a single lightweight spec without a separate Design Doc. Apply TDD + operational-code + Code Quality Bar. | Code + tests, optionally `specs/<slice>/tasks.md` |
| **Medium** (1d-1wk, feature in existing product) | New endpoint with new logic, new screen with new interactions, integrating a new external dependency, adding a feature flag and rolling out a new behavior | `/spec` (anchored on existing code or a reverse-engineered design — see `/onboard`) → `/build`. No `/wb`; the customer is already known. Mini design section if architectural decisions arise. | Full spec trio + code + tests |
| **Large** (1wk+, feature changing architecture or new service) | New service, new public API surface, new pattern adoption (e.g., move to cell-based), schema migration, multi-region rollout, security model change | Full flow: `/wb` (or 5CQ if customer is known) → `/design` (Design Doc + API Contract + Threat Model + Review) → `/spec` per slice → `/build` | Full flow artifacts |
| **New product** (months, novel customer value) | A new product, a new business line, a major rewrite | Full `/wb` cycle: `/listen` → `/define` → `/invent` → `/refine` → `/test-idea` → `/design` → ... | Full flow artifacts |

### Signals the agent uses to classify

- **Code-impact size** — lines of code, files touched, blast radius. Read the request literally; "add a button" is small, "rebuild auth" is large.
- **Customer impact** — does this change behavior the customer sees or depends on? Trivial = no, Small = yes-but-additive, Medium = yes-changing, Large = new surface.
- **Reversibility** — one-way doors (schema, public API, partition key, security model) lift the ceremony level even when the code change is small.
- **Repository state** — is this a project with existing artifacts (`docs/design/`, `docs/working-backwards/`) or an unstructured project? Affects which path is *available*, not which is *appropriate*.

### When to ask the user (and when not to)

The agent decides silently and proceeds **when the right level is unambiguous**. It asks only when:

1. The classification is genuinely ambiguous (e.g., "add caching" — could be Small or Medium depending on consistency requirements)
2. There is a mismatch between the command invoked and the repo state (e.g., `/build` invoked but no `specs/` exists — see Step 0 in the command files)
3. The user asked for a heavyweight path on what looks like a lightweight change, or vice versa

When asking, present **2-3 options framed by outcome**, not by process: time, scope, traceability. Names like "Tier 1" or "Spec-Driven Implementation" do not appear in the question to the user.

### Greenfield vs brownfield

- **Greenfield** (new product, fresh repo, or user explicitly invokes `/wb`/`/listen`/`/define`/`/invent`/`/refine`/`/test-idea`): the ladder above maps directly onto the canonical flow. Do not infer brownfield context from existing code.
- **Brownfield** (mutation in a project with code but no BLA artifacts): for *trivial* and *small* changes, apply the ladder directly. For *medium* and *large* changes, the agent should consider proposing `/onboard` first — it reverse-engineers a Design Doc, API Contracts, and Threat Model from the existing code so subsequent specs are anchored in reality. See `skills/brownfield-discovery/SKILL.md`.

These two modes are mutually exclusive per invocation. The trigger (which command was invoked, which artifacts exist) decides which mode applies.

## Skill Discovery Logic

### Routing rule 0 — Brownfield discovery before medium/large changes

Before answering any of the questions below, check repo state:

- If the user invoked `/wb`, `/listen`, `/define`, `/invent`, `/refine`, `/test-idea` → **greenfield in progress**. Do not infer brownfield context. Skip this rule.
- If the user invoked `/build` and `specs/` exists → execute as normal. Skip this rule.
- If the project has significant code/IaC/CI but **no BLA artifacts** (`docs/design/`, `docs/working-backwards/`):
  - For a **trivial / small** change (per the proportionality ladder): proceed via the lightweight path; do not propose `/onboard`.
  - For a **medium / large** change: proactively offer `/onboard` as one of the options. Use `AskUserQuestion`:
    > [A] Run `/onboard` first (~15-30min) to reverse-engineer the project. All subsequent specs use these as anchors. *Recommended.*
    > [B] Skip onboarding and proceed without it. The agent will infer context per-change (slower, may miss constraints).
    > [C] Cancel.

If `/onboard` was previously run (artifacts in `docs/design/<service>/` with the **REVERSE-ENGINEERED** banner), do not re-run unless the project has drifted significantly. Use those artifacts as the anchor exactly like canonical Design Doc artifacts.

### Phase / risk / scale routing

When facing a situation, ask yourself:

1. **What phase am I in?**
   - Planning/Design → Working Backwards, Dependency Management, Feature Flag Lifecycle, Operational Excellence, Design Document, API Contract First
   - Building → Code Review, Test-Driven Development, Incremental Implementation
   - Deploying → Pipeline Safety, Progressive Deployment, Feature Flags
   - Operating → Operational Excellence, Operational Readiness Review, Metrics Review
   - Learning → COE, Metrics Review, Mechanism Creation

2. **What's the risk?**
   - Customer-facing change → Progressive Deployment + Feature Flags
   - External dependency or service boundary → Dependency Management before writing the design doc
   - Behavior change needing controlled exposure or kill switch → Feature Flag Lifecycle before writing the design doc
   - New operational signals, alarms, dashboards, or runbooks → Operational Excellence before writing the design doc
   - Infrastructure change → Infrastructure as Code + Pipeline Safety
   - New service launch → Operational Excellence + Operational Readiness Review
   - High-criticality workload (≥ 99.99% availability target, RPO < 5s, RTO < 30s, FSI, ultra-scale, multi-tenant) → read `patterns/INDEX.md` while generating alternatives in the design doc; load full PATTERN.md for any whose criteria match
   - Post-incident → COE + Mechanism Creation

3. **What's the scale?**
   - Individual task → Code Review, TDD
   - Team process → Metrics Review, Mechanism Creation
   - Cross-team coordination → Design Review, Operational Readiness Review
   - Organizational learning → COE sharing, Mechanism Creation

## The Process

### For New Team Members

1. Read this meta-skill first
2. Read the Leadership Principles reference
3. Read Operational Excellence (understand how you'll operate)
4. Read Operational Readiness Review (understand launch readiness)
5. Read 5 COEs from your team to understand past failures

### For Existing Teams Adopting These Skills

1. Start with Operational Excellence (get monitoring right)
2. Add Pipeline Safety (get deployment gates right)
3. Add Progressive Deployment (deploy safely)
4. Establish Metrics Review (recurring data-driven inspection)
5. Adopt COE process (learn from failures)
6. Add Mechanism Creation (prevent recurrence)
7. Layer in remaining skills as appropriate

### For Assessing Maturity

**Level 1 — Foundational**: Monitoring exists, deployments are automated, on-call rotation works
**Level 2 — Practiced**: Pipeline has safety gates, progressive deployment enforced, metrics are reviewed regularly
**Level 3 — Advanced**: COE process produces mechanisms, metrics drive decisions, feature flags enable safe experimentation
**Level 4 — Excellent**: All skills composing together seamlessly, team rarely gets paged, deployment velocity is high, learning is continuous

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "The team will follow the skills" | Skills referenced in design reviews, ORRs, and code reviews as checklists |
| "We'll remember to use the right skill" | IDE/tool integration that suggests relevant skills based on context |
| "New hires will learn the skills" | Onboarding checklist includes reading specific skills. Shadowing requirements enforced |
| "We'll maintain high standards" | Bar raisers in design review, code review, and operational review enforce standards |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "We're too small for all this process" | Small teams have fewer people to catch mistakes. Process compensates for fewer eyeballs | Start with the highest-impact skills (Pipeline Safety, Operational Excellence) and add incrementally |
| "We're moving too fast to follow all these" | You're moving too fast to NOT follow these. Speed without safety leads to incidents that slow you down more | These skills enable speed by giving you confidence. Fast and safe, not fast or safe |
| "This is too Amazon-specific" | The principles are universal. Rename them if the terminology bothers you, but don't skip them | Adapt the language to your culture. Keep the mechanisms |
| "We'll adopt these later when we're bigger" | Habits set early compound. Bad habits set early also compound | Start simple, grow with your team. Perfect is the enemy of good |

## Red Flags

- Team doesn't know which skills exist or when to use them
- Skills are known but not practiced ("we know about COEs but never write them")
- Skills are followed mechanically without understanding the purpose
- Only one person on the team understands the system
- Skills are treated as documentation rather than living practices
- No connection between skills (e.g., COE findings don't feed into mechanism creation)
- Team adopts the language but not the behavior ("we say 'mechanisms' but don't build them")

## Verification

- [ ] Team can name the relevant skill for any given situation
- [ ] Skills are actively used (evidence in documents, reviews, tickets)
- [ ] New team members are onboarded to the skill system
- [ ] Skills reinforce each other (COE → Mechanism → Pipeline Gate)
- [ ] Regular reflection on whether skills are being applied effectively
- [ ] Skills evolve based on team learning (not static documents)
- [ ] Bar raisers reference skills during reviews
- [ ] Metrics Review feeds concrete actions into mechanisms, COEs, and pipeline gates

## Tenets

1. **The system is greater than its parts.** Individual skills are useful; the composition of all skills is transformative.
2. **Start anywhere, but start.** Don't wait until you can adopt everything. Each skill provides value independently.
3. **Practice makes permanent.** Skills become reflexive through repetition, not through reading.
4. **Adapt but don't dilute.** Adjust to your context, but don't remove the hard parts because they're inconvenient.
5. **Teach by doing.** The best way to spread these practices is to model them, not to lecture about them.
6. **API First, always.** Every customer-facing surface is an API. UI, CLI, SDK, MCP, AI agent, partner — all clients. The contract precedes the client. No exceptions.

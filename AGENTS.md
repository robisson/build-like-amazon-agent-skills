# Instructions for AI Agents

This document defines how AI agents should discover, load, and execute skills from this repository. Follow these instructions precisely — they are the operating contract between this skill library and any agent that uses it.

## Discovering Skills

Skills are located in the `skills/` directory. Each skill is a standalone markdown file with YAML frontmatter containing metadata.

### How to Find the Right Skill

1. **Check the command**: If the user invokes a slash command (e.g., `/wb`, `/design`, `/deploy`), load the corresponding skill file directly.
2. **Use the meta-skill when no command is clear**: If there is no slash command and the right workflow is unclear, read `skills/using-amazon-skills/SKILL.md` first. Use it to route the request to the correct lifecycle phase and skill chain.
3. **Check triggers**: Each skill's frontmatter contains `triggers` — natural language phrases that indicate the skill should be activated.
4. **Check the phase**: If you know what lifecycle phase the work is in, browse skills in that phase.
5. **When in doubt, ask**: If multiple skills could apply after consulting the meta-skill, ask the user which workflow they want to follow rather than guessing.

### Skill Loading Protocol

When a skill is activated:

1. Read the full skill file
2. Execute the **Context Assessment** section to determine if the skill applies
3. If it applies, follow the **Process** section step by step
4. At each **Verification Checkpoint**, evaluate the criteria before proceeding
5. If a blocking checkpoint fails, stop and surface the issue to the user
6. When complete, confirm all verification checkpoints have been met

## Operating Behaviors

These behaviors apply whenever you are operating under this skill library. They are non-negotiable.

### 0. Respect Approval Gates

**When a skill specifies a human approval gate, you MUST pause and present your work.** Do not proceed until the user explicitly approves. This applies to:
- **Working Backwards (/wb):** Each of the 5 stages (Listen → Define → Invent → Refine → Test) has a mandatory gate. Complete one stage, present the output, ask the user to review, and wait for explicit approval before advancing.
- **Spec creation (/design):** Each artifact (requirements.md → design.md → tasks.md) has a mandatory gate. Present each document for review before generating the next.
- **The only exception is /build task execution.** Once specs are approved, /build executes tasks autonomously following the dependency graph — no pause needed between tasks.

Violating an approval gate (e.g., jumping from Listen to PR/FAQ, or generating all spec files without pauses) is a critical process failure. If you notice yourself about to skip a gate, stop and present your work to the user.

### 1. Surface Assumptions

Never proceed on an unstated assumption. If you find yourself thinking "I assume the user means X," stop and ask.

**Do this:**
```
I'm about to design the API assuming REST over HTTP. The skill allows for 
GraphQL or gRPC as well. Which protocol fits your context?
```

**Not this:**
```
Here's the REST API design...
(proceeds without confirming the assumption)
```

### 2. Manage Confusion Budget

Complexity is a budget, not a feature. Every architectural decision has a "confusion cost" — the cognitive load it imposes on the next engineer who encounters it.

When implementing:
- Choose the approach that a new team member could understand in under 5 minutes
- If you can't explain why something is complex in one sentence, simplify it
- Prefer boring technology over clever technology
- Count the number of concepts someone needs to hold in their head simultaneously — keep it under 7

### 3. Push Back When Warranted

You are not a yes-machine. If a user's request conflicts with a skill's guidance, say so clearly and explain why.

**Push back when:**
- A request would skip a blocking verification checkpoint
- A design introduces unnecessary complexity
- A deployment plan lacks rollback capability
- A solution doesn't address the stated customer problem
- Technical debt is being introduced without acknowledgment

**How to push back:**
```
I want to flag a concern before proceeding. The skill requires [X] at this 
stage because [rationale]. Your request would skip this, which historically 
leads to [consequence]. Would you like to:
1. Address [X] first, then proceed
2. Explicitly acknowledge the risk and proceed anyway (two-way door only)
3. Take a different approach that satisfies both goals
```

### 4. Enforce Simplicity

The Simplicity Bar Raiser is always active. At every decision point, ask:

- Is this the simplest solution that solves the problem?
- Am I adding this because it's needed now, or because it might be needed later?
- Could I explain this architecture to a new hire in 5 minutes?
- What can I remove?

**YAGNI (You Ain't Gonna Need It)** is a first-class principle. If a feature or abstraction isn't needed for the current iteration, don't build it. Document it in a "Future Considerations" section if you want to preserve the idea.

### 5. Verify, Don't Assume

Never mark a verification checkpoint as "passed" based on assumption. Actually verify:

- **"Tests pass"** → Run the tests, don't assume they pass
- **"API contract is stable"** → Check for breaking changes against the previous version
- **"Rollback works"** → Describe the specific rollback procedure and confirm it's tested
- **"Customer problem validated"** → Point to the specific data or feedback

If you can't verify something, say so explicitly:
```
I cannot verify checkpoint "Load test completed" because no load testing 
infrastructure is configured. Options:
1. Set up load testing (I can help with this)
2. Defer this checkpoint with documented risk acceptance
3. Use traffic estimation as a proxy
```

### 6. API First (the 2002 API Mandate, applied)

Every customer-facing surface is an API. The API is the contract; everything behind it is private implementation.

- A **client** is anything that consumes an API: web UI, mobile app, CLI, SDK, MCP server, AI agent, another internal service, partner integration, batch ETL job. **All clients are equivalent from the contract's point of view.** Use "client" or "API consumer" — never "frontend" alone.
- The API may be REST, GraphQL, gRPC, an async / event surface, a data contract, an MCP tool surface, an AI agent tool definition, a webhook, a CLI, or an SDK. The protocol does not change the rule.
- **Pick the right contract standard for the protocol.** OpenAPI is not the universal answer. REST → OpenAPI; GraphQL → SDL; gRPC → `.proto`; async/events → AsyncAPI + JSON Schema / Avro / Protobuf; data → ODCS (or store-native); MCP → MCP manifest; AI agent tools → provider-native tool spec. See `skills/api-contract-first/SKILL.md` for the full mapping.
- During `/design`, Step 2 (API Contract) is **mandatory** — every design has an API. If you cannot identify the API, the design is not finished.
- During `/spec` and `/build`, **API specs precede client specs.** No client spec is created or implemented before the API it consumes is specified and frozen.
- If a client needs behavior the API doesn't expose, evolve the API. Do not embed logic in the client to work around a missing API capability.

For the full guidance, see `skills/using-amazon-skills/SKILL.md` (Operating Behavior 9) and `skills/api-contract-first/SKILL.md`.

### 7. Match the Ceremony to the Change

The agent picks the right ceremony level — never the user.

- **Trivial** (< 2h, no customer impact): direct to code with Code Quality Bar. No spec.
- **Small** (2h-1d, customer-facing but local): direct to code OR a single lightweight spec.
- **Medium** (1d-1wk, feature in existing product): `/spec` → `/build`.
- **Large** (1wk+, architectural change or new service): full `/design` → `/spec` → `/build`.
- **New product**: `/wb` → `/design` → `/spec` → `/build`.

Each command (`/build`, `/spec`, `/design`) starts with **Step 0: State Detection + Proportionality Check**. When ambiguity requires a choice, the agent uses outcome-framed options (time, scope, traceability), never process names ("Tier 1", "PR/FAQ" do not appear in the question).

For **brownfield projects** (existing code without BLA artifacts), the agent proactively offers **`/onboard`** for medium/large changes. `/onboard` has 3 paths the user picks from:
- **(A) Anchor only** — Design Doc + API contracts + Threat Model from existing code (~15–30min)
- **(B) Validate the *why*** — Path A + inferred PR/FAQ + hard questions from `doc-bar-raiser` where code can't answer (~30–45min)
- **(C) Forward WB + Gap Analysis** — full `/wb` from scratch with gates + Path A + gap-analysis.md comparing "what we'd build today" vs "what exists" (~1–2h)

Greenfield invocations (`/wb` and friends) are isolated by trigger and never invoke `/onboard`.

Full ladder in `skills/using-amazon-skills/SKILL.md` → "Match the Ceremony to the Change". Brownfield discovery process in `skills/brownfield-discovery/SKILL.md`.

### 8. /build Is Fully Autonomous by Default — Run to Feature Completion

Approval gates happen during `/design` (when specs are created). Once `/build` starts, the agent runs **all specs end-to-end without asking for permission between them**. "Done" means every spec in `specs/` is in a terminal state, not "I finished one spec, should I continue?"

The agent stops only for one of these four reasons:
1. **Hard blocker** — sub-agent reports `[!]` and resolution requires human input
2. **FAILED Post-Implementation Review** — fundamental gap (not minor fixes)
3. **Green-build gate cannot self-recover** — tests broken in a way the agent cannot fix within scope
4. **User explicitly asked to pause** — e.g., *"build spec by spec, ask me before each one"* in the original prompt

⛔ Anti-patterns: stopping at end of a spec to ask "proceed?", presenting status with implicit "continue?", declaring "done" while `tasks.md` has `[ ]` or while there are subsequent specs. None of these are valid stop reasons.

### 9. Track Tasks During /build

The orchestrator (the agent running `/build`) owns `tasks.md`. Sub-agents do not edit it.

- Before dispatching a wave: flip every task in the wave from `[ ]` to `[-]` and save the file.
- As each sub-agent reports back: flip its task to `[x]` (success) or `[!]` (blocked, with reason).
- Before declaring the wave complete: re-read `tasks.md` and verify no task is still `[ ]` or `[-]`.
- A spec is only complete when every task is `[x]` or `[!]`.

For the full state-transition protocol and resume rules, see `.claude/commands/build.md`.

### 10. Code Quality Bar (during writing, not after)

While writing code in `/build`:

- **Pick the paradigm by context.** Functional core, imperative shell as default. SOLID where entities have lifecycle. Procedural for short scripts.
- **Naming carries the design.** No `process`, `handle`, `data`, `info`, `temp` in production code.
- **Functions do one thing at one level of abstraction.** Small and shallow.
- **Cyclomatic complexity is a smell, not a metric.** High branching means decomposition, not tolerance.
- **No comments that describe *what*; only *why*.** Rename and extract until comments are unnecessary.
- **No dead code, no premature abstractions, no `any`/`unknown` escape hatches, no mutable globals.**
- **Errors are values at boundaries, exceptions inside.** Provider exceptions don't leak into business logic.

For the full bar, see `skills/incremental-implementation/SKILL.md` → "Code Quality Bar".

## Decision Framework: Two-Way vs One-Way Doors

This classification determines how much process rigor to apply:

### One-Way Doors (Irreversible or Very Costly to Reverse)

- Public API contracts
- Database schema migrations (especially column drops)
- Data deletion
- Security model changes
- Service decomposition / merging
- Pricing model changes

**Process**: Full skill execution, all bar raisers, explicit sign-off required.

### Two-Way Doors (Easily Reversible)

- Internal implementation details
- UI changes behind feature flags
- Configuration changes with rollback
- A/B tests
- Internal API changes with single consumer
- Documentation updates

**Process**: Lightweight skill execution, bias for action, iterate quickly.

### How to Classify

Ask these questions:
1. If this is wrong, can we undo it within 1 hour? → Two-way door
2. Does this affect external consumers who we don't control? → One-way door
3. Does this involve data loss or corruption risk? → One-way door
4. Can we put this behind a feature flag? → Likely two-way door
5. Would reverting require coordination across teams? → One-way door

## Bar Raiser Interaction Protocol

When a skill specifies bar raiser review:

1. **Activate the persona** — Shift into the bar raiser's perspective
2. **Ask the questions** — Present bar raiser questions to the user
3. **Evaluate honestly** — Don't rubber-stamp; if something doesn't meet the bar, say so
4. **Block if necessary** — For blocking checkpoints, refuse to proceed until criteria are met
5. **Document the decision** — Record what was reviewed, what passed, and any conditions

### When Multiple Bar Raisers Apply

Execute them in this order:
1. Customer Obsession (is this solving the right problem?)
2. Simplicity (is this the simplest approach?)
3. Security (is this safe?)
4. Architecture (is this well-designed?)
5. Code Quality (is this well-implemented?)
6. Operations (is this operable?)
7. Learning (are we capturing lessons?)

If any bar raiser blocks, resolve their concern before proceeding to the next.

## Error Handling

### When a Skill Doesn't Fit

If you've loaded a skill and the Context Assessment reveals it doesn't apply:

```
I loaded the [skill name] skill, but after assessing the context, it doesn't 
apply here because [reason]. A better fit might be [alternative skill] or 
we could proceed without a specific skill framework. What would you prefer?
```

### When Steps Are Ambiguous

If a skill's instructions are ambiguous in your specific context:

1. State what you understand
2. State what's ambiguous
3. Propose your interpretation
4. Ask for confirmation before proceeding

### When User Requests Conflict with Skills

The user always has final authority. But your job is to ensure they make **informed** decisions:

1. Clearly state the conflict
2. Explain the rationale behind the skill's recommendation
3. Describe the risk of deviating
4. If the user decides to deviate, document it and proceed

## Continuous Improvement

If you notice a skill is:
- Missing a step that caused issues
- Including a step that's consistently unnecessary
- Ambiguous in a way that required clarification
- Missing a verification checkpoint that would have caught a problem

Surface this to the user and suggest they open an issue or contribute an improvement.

---

*These operating behaviors are mechanisms, not suggestions. Follow them consistently — that's how quality compounds over time.*

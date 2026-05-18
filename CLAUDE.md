# CLAUDE.md

You are operating in a project that uses **Build Like Amazon Agent Skills** — a structured set of engineering workflows based on Amazon's Working Backwards methodology and operational excellence culture.

## Skills Directory

All skills are located in `skills/`. Each skill is a directory with a `SKILL.md` file (and optionally `templates/`). Agent personas are in `agents/`.

Use `skills/using-amazon-skills/SKILL.md` as the meta-skill when the user does not invoke a slash command and the right workflow is unclear. It routes ambiguous requests to the correct lifecycle phase and skill chain.

## Slash Commands

When the user invokes a slash command, read the corresponding command file in `.claude/commands/` and follow it:

| Command | Command File | What It Does |
|---------|-------------|--------------|
| `/onboard` | `.claude/commands/onboard.md` | Reverse-engineer an existing project — produce Design Doc, API contracts, baseline Threat Model from existing code, IaC, observability. Run once per brownfield project. 3 paths: anchor only / validate the *why* (inferred PR/FAQ + bar-raiser questions) / forward WB + gap analysis. |
| `/wb` | `.claude/commands/wb.md` | Full Working Backwards cycle (5 stages with approval gates) |
| `/listen` | `.claude/commands/listen.md` | Stage 1: Who is the customer? |
| `/define` | `.claude/commands/define.md` | Stage 2: What is the problem? |
| `/invent` | `.claude/commands/invent.md` | Stage 3: What is the solution? |
| `/refine` | `.claude/commands/refine.md` | Stage 4: Write the PR/FAQ |
| `/test-idea` | `.claude/commands/test-idea.md` | Stage 5: How will we measure success? |
| `/design` | `.claude/commands/design.md` | Full design flow (Dependency/Flag/Ops Context → Design Doc → API → Threat Model → Review → Specs) |
| `/spec` | `.claude/commands/spec.md` | Create a single new spec (when design already exists) |
| `/build` | `.claude/commands/build.md` | Execute spec tasks (wave-by-wave, parallel, autonomous) |
| `/review` | `.claude/commands/review.md` | Code review with bar raiser mentality |
| `/deploy` | `.claude/commands/deploy.md` | Progressive deployment with auto-rollback |
| `/operate` | `.claude/commands/operate.md` | Operational readiness and runbook generation |
| `/learn` | `.claude/commands/learn.md` | COE — blameless post-incident analysis |

## Critical Rules

### 1. Approval Gates (Non-Negotiable)

- **During /wb**: STOP after each of the 5 stages. Present output. Wait for user approval before proceeding.
- **During /design**: STOP after each gated step (Design Doc → API → Threat Model → Review → each spec artifact). Never skip steps. Dependency, feature flag, and operational context are assessed before the Design Doc and incorporated into it.
- **During /spec**: STOP after each artifact (requirements → design → tasks). Never generate all three without approval between them.
- **During /build**: Execute autonomously **end-to-end across all specs**. NO approval gates between tasks, between waves, between specs, or after the Post-Implementation Review when verdict is PASSED / PASSED WITH FIXES NEEDED. Run all specs in `specs/` to terminal state in a single invocation. Stop only for: a hard blocker requiring user input, a FAILED review verdict, an unrecoverable green-build failure, or an explicit user request to pause (e.g., *"build spec by spec, ask me before each"*). See `.claude/commands/build.md` for the four valid stop reasons and the end-of-build summary format.

### 2. Template Enforcement

When generating spec artifacts (requirements.md, design.md, tasks.md):
- Read templates in `skills/spec-driven-implementation/templates/` FIRST
- Follow the template structure EXACTLY — do not invent your own format
- requirements.md MUST use EARS notation (SHALL/WHEN/IF)
- design.md MUST include Mermaid diagrams
- tasks.md MUST include dependency graph JSON with waves at the bottom

### 3. Parallelization During /build

Tasks within the same wave MUST be executed IN PARALLEL (sub-agents). Do NOT execute them sequentially.
Each sub-agent MUST receive full context: task description, relevant requirements, design sections, file paths, and constraints from previous waves.

### 4. Task Status Markers

```
- [ ] Pending
- [-] In Progress (resume point if interrupted)
- [x] Done
- [!] Blocked (include reason)
```

During `/build`, `tasks.md` must be kept in sync with reality at all times. The orchestrator (the agent running `/build`) is the **only** writer of `tasks.md` — sub-agents do not edit it. Before dispatching a wave, flip every task in the wave from `[ ]` to `[-]`. As each sub-agent reports back, flip its task to `[x]` (success) or `[!]` (blocked). A spec is only complete when every task is `[x]` or `[!]`. See `.claude/commands/build.md` for the full state-transition protocol.

### 5. Operating Behaviors

Always follow `AGENTS.md`:
1. **Respect approval gates** — When a skill specifies a gate, STOP and present work
2. **Surface assumptions** — Never proceed on unstated assumptions
3. **Push back when warranted** — You are not a yes-machine
4. **Enforce simplicity** — Prefer the boring, obvious solution
5. **Verify, don't assume** — Check with evidence, not intuition

### 6. Bar Raisers

Bar Raisers are Amazon's mechanism for ensuring quality never regresses. They exist at **every stage** of the lifecycle — not just code review. When a skill specifies bar raiser review:

1. Load the relevant agent persona from `agents/` (e.g., `agents/doc-bar-raiser.md` for PR/FAQ, `agents/design-bar-raiser.md` for design docs, `agents/code-review-bar-raiser.md` for code)
2. Review the artifact through that persona's lens — ask the hard questions it specifies
3. **Block progression** if the quality bar isn't met. A Bar Raiser's job is to say "no" when something isn't ready, even if it's uncomfortable
4. Provide specific, actionable feedback (not vague "improve this")

Bar Raisers are NOT optional reviewers — they are **gates**. Their purpose is to ensure that every artifact (PR/FAQ, design doc, spec, code, COE) meets the standard before it moves forward. Without them, quality erodes gradually and silently.

Available personas: `doc-bar-raiser`, `design-bar-raiser`, `principal-engineer`, `code-review-bar-raiser`, `security-guardian`, `ops-bar-raiser`, `coe-reviewer`, `requirements-analyzer`, `task-planner`, `implementation-verifier`.

### 7. Decision Classification

Every significant decision is either:
- 🔒 **One-way door** (irreversible) → Full process, explicit sign-off
- 🚪 **Two-way door** (reversible) → Bias for action, iterate quickly

### 8. Match the Ceremony to the Change (Proportionality)

The agent picks the right ceremony level — the user never has to think about it.

- **Trivial** (< 2h, no customer impact): direct to code with Code Quality Bar. No spec, no Design Doc.
- **Small** (2h-1d, customer-facing but local): direct to code OR a single lightweight spec. No separate Design Doc.
- **Medium** (1d-1wk, feature in existing product): `/spec` → `/build`. Anchored on existing code or a reverse-engineered Design Doc (run `/onboard` first if brownfield without artifacts).
- **Large** (1wk+, architectural change or new service): full `/design` → `/spec` → `/build`.
- **New product**: `/wb` → `/design` → `/spec` → `/build`.

Each command (`/build`, `/spec`, `/design`) starts with **Step 0: State Detection + Proportionality Check** — when there is genuine ambiguity (e.g., `/build` without specs), the command uses `AskUserQuestion` with **outcome-framed options** (time, scope, traceability), never process names ("Tier 1", "spec", "PR/FAQ" do not appear in the question to the user).

For brownfield projects (existing code without BLA artifacts), the agent proactively offers `/onboard` for medium/large changes — runs once, produces reverse-engineered Design Doc + API contracts + Threat Model that anchor every subsequent `/spec` and `/build`. Full ladder in `skills/using-amazon-skills/SKILL.md` → "Match the Ceremony to the Change".

### 9. API First (the 2002 API Mandate, applied)

Every customer-facing surface is an API. The API is the contract; everything behind it is private implementation.

- A **client** is anything that consumes an API: web UI, mobile app, CLI, SDK, MCP server, AI agent, another internal service, partner integration, batch ETL job. **All clients are equivalent from the contract's point of view.** Use "client" or "API consumer" — never "frontend" alone.
- The API may be REST, GraphQL, gRPC, an async / event surface, a data contract, an MCP tool surface, an AI agent tool definition, a webhook, a CLI, or an SDK. The protocol does not change the rule.
- **Pick the right contract standard for the protocol.** OpenAPI is not the universal answer. REST → OpenAPI; GraphQL → SDL; gRPC → `.proto`; async/events → AsyncAPI + JSON Schema/Avro/Protobuf; data → ODCS (or store-native); MCP → MCP manifest; AI agent tools → provider-native tool spec. Full mapping in `skills/api-contract-first/SKILL.md`.
- During `/design`, Step 2 (API Contract) is **mandatory** — every design has an API. If you cannot identify the API, the design is not finished.
- During `/spec` and `/build`, **API specs precede client specs.** No client spec is created or implemented before the API it consumes is specified and frozen.
- If a client needs behavior the API doesn't expose, evolve the API. Do not embed logic in the client to work around a missing API capability.

## Automatic Activation

Even without explicit slash commands, activate relevant skills when:
- User starts discussing a new feature → `/wb` or `/listen`
- User asks for architecture input → `/design`
- User wants to add a feature to existing system → `/spec`
- User is ready to implement → `/build`
- User mentions deployment → `/deploy`
- User reports an incident → `/learn`
- User asks about production readiness → `/operate`

## Key Files

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Core operating behaviors + approval gate rules |
| `skills/` | 27 workflow skills organized by lifecycle phase |
| `agents/` | 10 bar raiser personas for specialized review |
| `patterns/` | Architectural decisions that propagate across skills (e.g., cell-based architecture) |
| `.claude/commands/` | 14 slash command definitions |
| `docs/` | Getting started, skill anatomy, philosophy |

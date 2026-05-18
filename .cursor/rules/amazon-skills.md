# Amazon Engineering Skills — Cursor Rules

> **Source of truth.** This file is a thin router. The actual content lives in `skills/`, `agents/`, `patterns/`, and `.claude/commands/`. Do not duplicate guidance here — point to it.

This project uses Amazon-style engineering practices. When working in this codebase:

1. **Identify the lifecycle phase** (Working Backwards / Design / Build / Deploy / Operate / Learn).
2. **Load the relevant skill(s)** from `skills/` for that phase.
3. **Follow the skill's Process section step by step**, including approval gates.
4. **When in doubt about which skill applies**, read `skills/using-amazon-skills/SKILL.md` first — it is the meta-skill that routes ambiguous requests.

## Skill Index

### Meta

| Skill | Directory |
|-------|-----------|
| using-amazon-skills | `skills/using-amazon-skills/` |
| brownfield-discovery | `skills/brownfield-discovery/` (reverse-engineer existing project) |

### Working Backwards

| Skill | Directory |
|-------|-----------|
| working-backwards | `skills/working-backwards/` |
| wb-listen | `skills/wb-listen/` |
| wb-define | `skills/wb-define/` |
| wb-invent | `skills/wb-invent/` |
| wb-refine | `skills/wb-refine/` |
| wb-test-and-iterate | `skills/wb-test-and-iterate/` |

### Design

| Skill | Directory |
|-------|-----------|
| design-document | `skills/design-document/` |
| dependency-management | `skills/dependency-management/` |
| feature-flag-lifecycle | `skills/feature-flag-lifecycle/` |
| operational-excellence | `skills/operational-excellence/` |
| api-contract-first | `skills/api-contract-first/` |
| threat-modeling | `skills/threat-modeling/` |
| design-review | `skills/design-review/` |
| spec-driven-implementation | `skills/spec-driven-implementation/` |

### Build

| Skill | Directory |
|-------|-----------|
| incremental-implementation | `skills/incremental-implementation/` |
| test-driven-development | `skills/test-driven-development/` |
| operational-code | `skills/operational-code/` |
| infrastructure-as-code | `skills/infrastructure-as-code/` |
| code-review-bar-raising | `skills/code-review-bar-raising/` |

### Deploy

| Skill | Directory |
|-------|-----------|
| progressive-deployment | `skills/progressive-deployment/` |
| pipeline-safety | `skills/pipeline-safety/` |

### Operate

| Skill | Directory |
|-------|-----------|
| operational-readiness-review | `skills/operational-readiness-review/` |
| metrics-review | `skills/metrics-review/` |

### Learn

| Skill | Directory |
|-------|-----------|
| correction-of-errors | `skills/correction-of-errors/` |
| mechanism-creation | `skills/mechanism-creation/` |

## Architectural Patterns

Patterns live in `patterns/`. Each `patterns/<name>/PATTERN.md` declares its applicability in `applies_when:` frontmatter. During design, scan the catalog and pull in any pattern whose `applies_when:` plausibly matches the workload — it becomes a candidate alternative in the Design Doc.

## Bar Raiser Personas

Personas live in `agents/`. When a skill specifies bar raiser review, load the persona and apply its lens.

## Slash Command Definitions

Slash command flows are defined in `.claude/commands/` (canonical) and mirrored in `.gemini/commands/`. Each command file lists steps, gates, and output artifacts. When the user invokes a command, follow the corresponding file.

## Operating Behaviors (the contract)

Read `AGENTS.md` for the full operating contract. The non-negotiable behaviors are:

1. **Respect approval gates.** During `/wb`, `/design`, `/spec`, stop at each gate and present work.
2. **Match the ceremony to the change.** Trivial → direct to code; Small → direct or lightweight spec; Medium → `/spec` + `/build`; Large → full `/design` flow; New product → `/wb` first. The agent picks; the user only sees outcome-framed options when there is genuine ambiguity. For brownfield projects without BLA artifacts, propose `/onboard` (3 paths: anchor only / validate-the-why with inferred PR/FAQ / forward WB + gap analysis). See `skills/using-amazon-skills/SKILL.md` → "Match the Ceremony to the Change" and `skills/brownfield-discovery/SKILL.md` for details.
3. **API First.** Every customer-facing surface is an API. UI / CLI / SDK / MCP / agent / partner are all clients. The API spec is created before any client spec. **Pick the right contract standard per protocol** — OpenAPI for REST, GraphQL SDL for GraphQL, `.proto` for gRPC, AsyncAPI + JSON Schema/Avro/Protobuf for async events, ODCS for data contracts, MCP manifest for MCP tools, provider-native spec for AI agent tools. See `skills/api-contract-first/SKILL.md`.
4. **Patterns enter design as alternatives.** Scan `patterns/` while generating alternatives in the Design Doc.
5. **Track tasks during `/build`.** The orchestrator owns `tasks.md`. Flip `[ ] → [-]` before dispatching a wave; `[-] → [x]` as sub-agents report success; `[!]` for blockers. No spec is "done" while any task is `[ ]` or `[-]`.
6. **`/build` is autonomous to feature completion.** Approval gates happened in `/design`. `/build` runs all specs end-to-end without asking between specs/waves/PASSED reviews. Stops only for hard blockers, FAILED review, unrecoverable green-build failure, or explicit user pause request.
7. **Code Quality Bar.** While writing code, apply paradigm-by-context (functional core, imperative shell), SOLID where it pays, clean naming, no dead code. See `skills/incremental-implementation/SKILL.md` → "Code Quality Bar".
8. **Surface assumptions.** Never proceed on an unstated assumption. Ask.
9. **Push back when warranted.** Not a yes-machine.
10. **Verify, don't assume.** Run the tests; check the file; don't claim something works without evidence.

## Lifecycle Flow

```
/wb → /listen → /define → /invent → /refine → /test-idea
                                                    ↓
                            /design → (specs) → /build → /review → /deploy
                                                                       ↓
                                                            /operate → /learn ↺
```

Each phase produces artifacts that feed the next.

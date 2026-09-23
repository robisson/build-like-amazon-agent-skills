# Artifact Catalog

Every artifact the Build Like Amazon flow produces, where it lives, whether it is mandatory, which
template shapes it, which command produces it and who consumes it afterwards.

This catalog was derived by reading the `## Output` section of each of the 14 commands in
`.claude/commands/` and the `## IO Contract` of each of the 10 personas in `agents/`. It renames nothing
and numbers nothing: the names here are the names those files already use. When a command's `## Output`
changes, this file changes in the same commit — `AGENTS.md` → *Keep the Documentation Truthful in the Same
Commit* applies to it like to any other cross-reference.

Two reading rules:

- **`Canonical path`** uses `<feature-name>`, `<service-name>`, `<slice-name>` and `<incident-name>`
  exactly as the commands do. The placeholder is part of the path, not a suggestion.
- **`Template`** names a file under `skills/*/templates/` when one exists. A `—` means the artifact's
  shape is defined by the prose of its skill, **not** that the artifact is freeform.

## Working Backwards

| Artifact | Canonical path | Mandatory/Optional | Template | Produced by (command) | Consumed by |
|---|---|---|---|---|---|
| 5CQ screen | `docs/working-backwards/<feature-name>/5cq.md` | Optional — the 30-minute screen before committing to a PR/FAQ | `skills/wb-refine/templates/5cq-template.md` | `/wb` | `/design` Step 0, `/refine` |
| Customer profile | `docs/working-backwards/<feature-name>/customer-profile.md` | Mandatory | — | `/listen`, `/wb` | `/define`, `/invent`, `/design` Step 0 |
| Problem statement | `docs/working-backwards/<feature-name>/problem-statement.md` | Mandatory | — | `/define`, `/wb` | `/invent`, `/refine` |
| Solution sketch | `docs/working-backwards/<feature-name>/solution-sketch.md` | Mandatory | — | `/invent`, `/wb` | `/refine`, `/design` Step 1 |
| PR/FAQ | `docs/working-backwards/<feature-name>/prfaq.md` | Mandatory | `skills/wb-refine/templates/prfaq-template.md` | `/refine`, `/wb` | `/test-idea`, `/design` Step 0, `agents/doc-bar-raiser.md` |
| Dear Customer Letter | `docs/working-backwards/<feature-name>/dear-customer-letter.md` | Optional — replaces the PR/FAQ for an incremental change to an existing product | `skills/wb-refine/templates/dear-customer-letter-template.md` | `/refine` | `/test-idea`, `/design` Step 0 |
| Success metrics | `docs/working-backwards/<feature-name>/success-metrics.md` | Mandatory | — | `/test-idea`, `/wb` | `/design`, `/deploy`, `/operate` |

A `—` in `Template` means the shape comes from the skill's prose: these four narrative documents are
shaped by `skills/working-backwards/SKILL.md` and its stage skills, which prescribe their sections.

## Design

| Artifact | Canonical path | Mandatory/Optional | Template | Produced by (command) | Consumed by |
|---|---|---|---|---|---|
| Design document | `docs/design/<feature-name>/design-doc.md` | Mandatory | `skills/design-document/templates/design-doc-template.md` | `/design` Step 1 | `/spec`, `/build`, `agents/design-bar-raiser.md`, `agents/security-guardian.md`, `agents/principal-engineer.md` |
| Contract artefact, one per protocol | `docs/design/<feature-name>/openapi.yaml`, `schema.graphql`, `service.proto`, `asyncapi.yaml` with `schemas/<event-name>.json` or `.avsc` or `.proto`, `data-contract.yaml`, `mcp-tools.json`, `tools.json` | Mandatory — every design has an API | — the standard is protocol-native, never markdown | `/design` Step 2 | every client, `/build`, `agents/implementation-verifier.md` |
| API contracts index | `docs/design/<feature-name>/api-contracts.md` | Mandatory | `skills/api-contract-first/templates/api-contracts-template.md` | `/design` Step 2, `/onboard` Path A | `/build`, `agents/implementation-verifier.md`, client teams |
| Threat model | `docs/design/<feature-name>/threat-model.md` | Mandatory when the change is security-sensitive; skipped with a stated note otherwise | `skills/threat-modeling/templates/threat-model-template.md` | `/design` Step 3, written by `agents/security-guardian.md` | `/design` Step 4, `/review`, `/deploy` |
| Design review checklist | `docs/design/<feature-name>/review-checklist.md` | Mandatory for a Medium or Large change; inline for Trivial and Small | — | `/design` Step 4, written by `agents/design-bar-raiser.md` | `/design` Step 5, `/spec` |

A `—` in `Template` means the shape comes from the skill's prose: `review-checklist.md` is shaped by
`skills/design-review/SKILL.md`, and the contract artefacts are shaped by the standard each one uses,
which is why no markdown template can stand in for them.

## Spec

| Artifact | Canonical path | Mandatory/Optional | Template | Produced by (command) | Consumed by |
|---|---|---|---|---|---|
| Requirements | `specs/<slice-name>/requirements.md` | Mandatory | `skills/spec-driven-implementation/templates/requirements-template.md` | `/spec`, `/design` Step 5 | `agents/requirements-analyzer.md`, `agents/task-planner.md`, `/build`, `agents/implementation-verifier.md` |
| Spec design | `specs/<slice-name>/design.md` | Mandatory | `skills/spec-driven-implementation/templates/design-template.md` | `/spec`, `/design` Step 5 | `agents/task-planner.md`, `/build`, `agents/implementation-verifier.md` |
| Tasks | `specs/<slice-name>/tasks.md` | Mandatory | `skills/spec-driven-implementation/templates/tasks-template.md` | `/spec`, written by `agents/task-planner.md` | `/build`, `agents/implementation-verifier.md`, `tools/bla-check tasks` |
| Requirements analysis | `specs/<slice-name>/requirements-analysis.md` | Mandatory | — | `/spec`, written by `agents/requirements-analyzer.md` | the producer of `requirements.md`, `/build` |
| Spec coherence review | `specs/<slice-name>/coherence-review.md` | Mandatory | — | `/spec` Step 7, `/design` Step 5b | `/build`, which treats its action items as binding |

A `—` in `Template` means the shape comes from the skill's prose: `requirements-analysis.md` is the
Requirements Analysis Report defined in `agents/requirements-analyzer.md`, including its terminal verdict
block, and `coherence-review.md` is defined in `skills/spec-driven-implementation/SKILL.md` Step 7.

## Build

| Artifact | Canonical path | Mandatory/Optional | Template | Produced by (command) | Consumed by |
|---|---|---|---|---|---|
| Implementation code and tests | the project's own source tree | Mandatory | — | `/build` | `/review`, `agents/implementation-verifier.md` |
| Task completion evidence | `specs/<slice-name>/.reports/<task-id>.md` | Mandatory at Medium/Large | — | `/build`, written by the task's sub-agent before it reports back | `/build` wave close, `python3 tools/bla-check tasks` |
| Post-implementation review | `specs/<slice-name>/implementation-review.md` | Mandatory | — | `/build`, written by `agents/implementation-verifier.md` | `/build` review-fix phase, `/review`, `docs/implementation-memory.md` |
| Code review | `docs/reviews/<feature-name>/code-review.md` | Mandatory | — | `/review`, written by `agents/code-review-bar-raiser.md` | the author, `/build`, `docs/implementation-memory.md` |
| Operational readiness checklist, review-time | `docs/reviews/<feature-name>/orr-checklist.md` | Mandatory | `skills/operational-readiness-review/templates/orr-checklist.md` | `/review`, written by `agents/ops-bar-raiser.md` | `/deploy`, `/operate` |

A `—` in `Template` means the shape comes from the skill's prose: both review reports are shaped by their
agent's `## IO Contract` and terminal verdict block, and `skills/code-review-bar-raising/SKILL.md` owns
the finding format they share. The per-task evidence file is shaped by `.claude/commands/build.md`, which
fixes its first line — `**Agent:** <task-id>` — because that line is what the wave close matches on.

## Deploy

| Artifact | Canonical path | Mandatory/Optional | Template | Produced by (command) | Consumed by |
|---|---|---|---|---|---|
| Rollout plan | `docs/deployment/<feature-name>/rollout-plan.md` | Mandatory | — | `/deploy` | `/operate`, `agents/ops-bar-raiser.md` |
| Pipeline configuration | `docs/deployment/<feature-name>/pipeline-config.md` | Mandatory | — | `/deploy` | `/operate`, `/learn` |

A `—` in `Template` means the shape comes from the skill's prose: both are shaped by
`skills/progressive-deployment/SKILL.md` and `skills/infrastructure-as-code/SKILL.md`.

## Operate

| Artifact | Canonical path | Mandatory/Optional | Template | Produced by (command) | Consumed by |
|---|---|---|---|---|---|
| Runbook | `docs/operations/<service-name>/runbook.md` | Mandatory | — | `/operate` | on-call, `/learn` |
| Alarm definitions | `docs/operations/<service-name>/alarm-definitions.md` | Mandatory | — | `/operate` | `/deploy`, `/learn` |
| Operational readiness checklist, launch-time | `docs/operations/<service-name>/orr-checklist.md` | Mandatory before launch | `skills/operational-readiness-review/templates/orr-checklist.md` | `/operate` | the launch decision, `/learn` |
| Escalation matrix | `docs/operations/<service-name>/escalation-matrix.md` | Mandatory | — | `/operate` | on-call, `/learn` |

A `—` in `Template` means the shape comes from the skill's prose: these three are shaped by
`skills/operational-excellence/SKILL.md`. The launch-time and review-time ORR checklists share one
template and are two distinct artifacts at two distinct paths — neither replaces the other.

## Learn

| Artifact | Canonical path | Mandatory/Optional | Template | Produced by (command) | Consumed by |
|---|---|---|---|---|---|
| COE report | `docs/coe/<incident-name>/coe-report.md` | Mandatory | `skills/correction-of-errors/templates/coe-template.md` | `/learn` Step 1 | `agents/coe-reviewer.md`, `docs/implementation-memory.md` |
| Action items | `docs/coe/<incident-name>/action-items.md` | Mandatory | — | `/learn` Step 1 | `agents/coe-reviewer.md`, `/operate`, `/build` |
| Mechanisms | `docs/coe/<incident-name>/mechanisms.md` | Mandatory | — | `/learn` Step 2 | `agents/coe-reviewer.md`, `/operate`, `/build` |

A `—` in `Template` means the shape comes from the skill's prose: `action-items.md` is shaped by
`skills/correction-of-errors/SKILL.md` and `mechanisms.md` by `skills/mechanism-creation/SKILL.md`, which
is also where the rule that an action item must be a mechanism and not a heroic lives.

## Onboarding

| Artifact | Canonical path | Mandatory/Optional | Template | Produced by (command) | Consumed by |
|---|---|---|---|---|---|
| Reverse-engineered design document | `docs/design/<service-name>/design-doc.md` | Mandatory in Paths A, B and C | `skills/design-document/templates/design-doc-template.md` | `/onboard` Path A | `/design`, `/spec`, `/build` |
| API contracts index | `docs/design/<service-name>/api-contracts.md` | Mandatory in Paths A, B and C | `skills/api-contract-first/templates/api-contracts-template.md` | `/onboard` Path A | `/design` Step 2, client teams |
| Contract artefacts read off the code | `docs/design/<service-name>/openapi.yaml` or `.proto`, `.graphql`, `asyncapi.yaml`, one per protocol | Mandatory in Paths A, B and C | — the standard is protocol-native | `/onboard` Path A | `/design` Step 2, `/build` |
| Baseline threat model | `docs/design/<service-name>/threat-model.md` | Mandatory in Paths A, B and C, baseline only | `skills/threat-modeling/templates/threat-model-template.md` | `/onboard` Path A | `/design` Step 3 |
| Patterns observed | `docs/design/<service-name>/patterns-observed.md` | Mandatory in Paths A, B and C | — | `/onboard` Path A | `/design` Step 0d |
| Inferred Working Backwards set | `docs/working-backwards/<service-name>/customer-profile.md`, `problem-statement.md`, `solution-sketch.md`, `prfaq.md` | Mandatory in Path B, each carrying the INFERRED banner | as in the Working Backwards table above | `/onboard` Path B | `agents/doc-bar-raiser.md`, `/design` |
| Bar raiser questions | `docs/working-backwards/<service-name>/bar-raiser-questions.md` | Mandatory in Path B | — | `/onboard` Path B, written by `agents/doc-bar-raiser.md` | the user, who answers them with real customer evidence |
| Canonical Working Backwards set | `docs/working-backwards/<service-name>/` — the same five documents as the Working Backwards table, produced through the full flow | Mandatory in Path C | as in the Working Backwards table above | `/onboard` Path C | `/design` |
| Gap analysis | `docs/design/<service-name>/gap-analysis.md` | Mandatory in Path C | — | `/onboard` Path C | `/design`, `/spec` |

A `—` in `Template` means the shape comes from the skill's prose: `patterns-observed.md`,
`bar-raiser-questions.md` and `gap-analysis.md` are all shaped by
`skills/brownfield-discovery/SKILL.md`, and `bar-raiser-questions.md` additionally by the terminal verdict
block in `agents/doc-bar-raiser.md`, which in Path B is always INCOMPLETE by construction.

## Cross-phase

| Artifact | Canonical path | Mandatory/Optional | Template | Produced by (command) | Consumed by |
|---|---|---|---|---|---|
| Implementation memory | `docs/implementation-memory.md` | Optional until the first rule is accepted; then it is read before every build | — | `/build`, and fed by `/review` and `/learn` | `/build` pre-build selection, `/design`, `/spec` |
| Accepted-risk rows | no file of its own: a row in the review artifact of the phase where the risk was accepted | Mandatory whenever a finding is accepted instead of fixed | `skills/operational-readiness-review/templates/orr-checklist.md`, whose *Conditional Items* table defines the four columns | whoever accepts the risk, in that phase | the next review of that artifact, the owner named in the row |
| Artifact catalog | `docs/artifact-catalog.md` | Mandatory — this file | — | maintained by hand, in the same commit as any change to a command's `## Output` | every command and every agent, as the index of what to produce and where |

A `—` in `Template` means the shape comes from the skill's prose: `docs/implementation-memory.md` is
shaped by `skills/implementation-memory/SKILL.md` → *Active Rule Format*, whose *Memory Limits* section
also caps it at 12 active rules.

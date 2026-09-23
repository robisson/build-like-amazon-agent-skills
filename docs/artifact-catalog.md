# Artifact Catalog

Every artifact the Build Like Amazon flow produces, where it lives, whether it is mandatory, which
template shapes it, which command produces it and who consumes it afterwards.

This catalog was derived by reading the `## Output` section of each of the 14 commands in
`.claude/commands/` and the `## IO Contract` of each of the 10 personas in `agents/`. It renames nothing
and numbers nothing: the names here are the names those files already use. When a command's `## Output`
changes, this file changes in the same commit — `AGENTS.md` → *Keep the Documentation Truthful in the Same
Commit* applies to it like to any other cross-reference.

Two reading rules:

- **`Caminho canônico`** uses `<feature-name>`, `<service-name>`, `<slice-name>` and `<incident-name>`
  exactly as the commands do. The placeholder is part of the path, not a suggestion.
- **`Template`** names a file under `skills/*/templates/` when one exists. A `—` means the artifact's
  shape is defined by the prose of its skill, **not** that the artifact is freeform.

## Working Backwards

| Artefato | Caminho canônico | Obrigatório/Opcional | Template | Produzido por (comando) | Consumido por |
|---|---|---|---|---|---|
| 5CQ screen | `docs/working-backwards/<feature-name>/5cq.md` | Opcional — the 30-minute screen before committing to a PR/FAQ | `skills/wb-refine/templates/5cq-template.md` | `/wb` | `/design` Step 0, `/refine` |
| Customer profile | `docs/working-backwards/<feature-name>/customer-profile.md` | Obrigatório | — | `/listen`, `/wb` | `/define`, `/invent`, `/design` Step 0 |
| Problem statement | `docs/working-backwards/<feature-name>/problem-statement.md` | Obrigatório | — | `/define`, `/wb` | `/invent`, `/refine` |
| Solution sketch | `docs/working-backwards/<feature-name>/solution-sketch.md` | Obrigatório | — | `/invent`, `/wb` | `/refine`, `/design` Step 1 |
| PR/FAQ | `docs/working-backwards/<feature-name>/prfaq.md` | Obrigatório | `skills/wb-refine/templates/prfaq-template.md` | `/refine`, `/wb` | `/test-idea`, `/design` Step 0, `agents/doc-bar-raiser.md` |
| Dear Customer Letter | `docs/working-backwards/<feature-name>/dear-customer-letter.md` | Opcional — replaces the PR/FAQ for an incremental change to an existing product | `skills/wb-refine/templates/dear-customer-letter-template.md` | `/refine` | `/test-idea`, `/design` Step 0 |
| Success metrics | `docs/working-backwards/<feature-name>/success-metrics.md` | Obrigatório | — | `/test-idea`, `/wb` | `/design`, `/deploy`, `/operate` |

A `—` in `Template` means the shape comes from the skill's prose: these four narrative documents are
shaped by `skills/working-backwards/SKILL.md` and its stage skills, which prescribe their sections.

## Design

| Artefato | Caminho canônico | Obrigatório/Opcional | Template | Produzido por (comando) | Consumido por |
|---|---|---|---|---|---|
| Design document | `docs/design/<feature-name>/design-doc.md` | Obrigatório | `skills/design-document/templates/design-doc-template.md` | `/design` Step 1 | `/spec`, `/build`, `agents/design-bar-raiser.md`, `agents/security-guardian.md`, `agents/principal-engineer.md` |
| Contract artefact, one per protocol | `docs/design/<feature-name>/openapi.yaml`, `schema.graphql`, `service.proto`, `asyncapi.yaml` with `schemas/<event-name>.json` or `.avsc` or `.proto`, `data-contract.yaml`, `mcp-tools.json`, `tools.json` | Obrigatório — every design has an API | — the standard is protocol-native, never markdown | `/design` Step 2 | every client, `/build`, `agents/implementation-verifier.md` |
| API contracts index | `docs/design/<feature-name>/api-contracts.md` | Obrigatório | `skills/api-contract-first/templates/api-contracts-template.md` | `/design` Step 2, `/onboard` Path A | `/build`, `agents/implementation-verifier.md`, client teams |
| Threat model | `docs/design/<feature-name>/threat-model.md` | Obrigatório when the change is security-sensitive; skipped with a stated note otherwise | `skills/threat-modeling/templates/threat-model-template.md` | `/design` Step 3, written by `agents/security-guardian.md` | `/design` Step 4, `/review`, `/deploy` |
| Design review checklist | `docs/design/<feature-name>/review-checklist.md` | Obrigatório for a Medium or Large change; inline for Trivial and Small | — | `/design` Step 4, written by `agents/design-bar-raiser.md` | `/design` Step 5, `/spec` |

A `—` in `Template` means the shape comes from the skill's prose: `review-checklist.md` is shaped by
`skills/design-review/SKILL.md`, and the contract artefacts are shaped by the standard each one uses,
which is why no markdown template can stand in for them.

## Spec

| Artefato | Caminho canônico | Obrigatório/Opcional | Template | Produzido por (comando) | Consumido por |
|---|---|---|---|---|---|
| Requirements | `specs/<slice-name>/requirements.md` | Obrigatório | `skills/spec-driven-implementation/templates/requirements-template.md` | `/spec`, `/design` Step 5 | `agents/requirements-analyzer.md`, `agents/task-planner.md`, `/build`, `agents/implementation-verifier.md` |
| Spec design | `specs/<slice-name>/design.md` | Obrigatório | `skills/spec-driven-implementation/templates/design-template.md` | `/spec`, `/design` Step 5 | `agents/task-planner.md`, `/build`, `agents/implementation-verifier.md` |
| Tasks | `specs/<slice-name>/tasks.md` | Obrigatório | `skills/spec-driven-implementation/templates/tasks-template.md` | `/spec`, written by `agents/task-planner.md` | `/build`, `agents/implementation-verifier.md`, `tools/bla-check tasks` |
| Requirements analysis | `specs/<slice-name>/requirements-analysis.md` | Obrigatório | — | `/spec`, written by `agents/requirements-analyzer.md` | the producer of `requirements.md`, `/build` |
| Spec coherence review | `specs/<slice-name>/coherence-review.md` | Obrigatório | — | `/spec` Step 7, `/design` Step 5b | `/build`, which treats its action items as binding |

A `—` in `Template` means the shape comes from the skill's prose: `requirements-analysis.md` is the
Requirements Analysis Report defined in `agents/requirements-analyzer.md`, including its terminal verdict
block, and `coherence-review.md` is defined in `skills/spec-driven-implementation/SKILL.md` Step 7.

## Build

| Artefato | Caminho canônico | Obrigatório/Opcional | Template | Produzido por (comando) | Consumido por |
|---|---|---|---|---|---|
| Implementation code and tests | the project's own source tree | Obrigatório | — | `/build` | `/review`, `agents/implementation-verifier.md` |
| Task completion evidence | `specs/<slice-name>/.reports/<task-id>.md` | Obrigatório at Medium/Large | — | `/build`, written by the task's sub-agent before it reports back | `/build` wave close, `python3 tools/bla-check tasks` |
| Post-implementation review | `specs/<slice-name>/implementation-review.md` | Obrigatório | — | `/build`, written by `agents/implementation-verifier.md` | `/build` review-fix phase, `/review`, `docs/implementation-memory.md` |
| Code review | `docs/reviews/<feature-name>/code-review.md` | Obrigatório | — | `/review`, written by `agents/code-review-bar-raiser.md` | the author, `/build`, `docs/implementation-memory.md` |
| Operational readiness checklist, review-time | `docs/reviews/<feature-name>/orr-checklist.md` | Obrigatório | `skills/operational-readiness-review/templates/orr-checklist.md` | `/review`, written by `agents/ops-bar-raiser.md` | `/deploy`, `/operate` |

A `—` in `Template` means the shape comes from the skill's prose: both review reports are shaped by their
agent's `## IO Contract` and terminal verdict block, and `skills/code-review-bar-raising/SKILL.md` owns
the finding format they share. The per-task evidence file is shaped by `.claude/commands/build.md`, which
fixes its first line — `**Agent:** <task-id>` — because that line is what the wave close matches on.

## Deploy

| Artefato | Caminho canônico | Obrigatório/Opcional | Template | Produzido por (comando) | Consumido por |
|---|---|---|---|---|---|
| Rollout plan | `docs/deployment/<feature-name>/rollout-plan.md` | Obrigatório | — | `/deploy` | `/operate`, `agents/ops-bar-raiser.md` |
| Pipeline configuration | `docs/deployment/<feature-name>/pipeline-config.md` | Obrigatório | — | `/deploy` | `/operate`, `/learn` |

A `—` in `Template` means the shape comes from the skill's prose: both are shaped by
`skills/progressive-deployment/SKILL.md` and `skills/infrastructure-as-code/SKILL.md`.

## Operate

| Artefato | Caminho canônico | Obrigatório/Opcional | Template | Produzido por (comando) | Consumido por |
|---|---|---|---|---|---|
| Runbook | `docs/operations/<service-name>/runbook.md` | Obrigatório | — | `/operate` | on-call, `/learn` |
| Alarm definitions | `docs/operations/<service-name>/alarm-definitions.md` | Obrigatório | — | `/operate` | `/deploy`, `/learn` |
| Operational readiness checklist, launch-time | `docs/operations/<service-name>/orr-checklist.md` | Obrigatório before launch | `skills/operational-readiness-review/templates/orr-checklist.md` | `/operate` | the launch decision, `/learn` |
| Escalation matrix | `docs/operations/<service-name>/escalation-matrix.md` | Obrigatório | — | `/operate` | on-call, `/learn` |

A `—` in `Template` means the shape comes from the skill's prose: these three are shaped by
`skills/operational-excellence/SKILL.md`. The launch-time and review-time ORR checklists share one
template and are two distinct artifacts at two distinct paths — neither replaces the other.

## Learn

| Artefato | Caminho canônico | Obrigatório/Opcional | Template | Produzido por (comando) | Consumido por |
|---|---|---|---|---|---|
| COE report | `docs/coe/<incident-name>/coe-report.md` | Obrigatório | `skills/correction-of-errors/templates/coe-template.md` | `/learn` Step 1 | `agents/coe-reviewer.md`, `docs/implementation-memory.md` |
| Action items | `docs/coe/<incident-name>/action-items.md` | Obrigatório | — | `/learn` Step 1 | `agents/coe-reviewer.md`, `/operate`, `/build` |
| Mechanisms | `docs/coe/<incident-name>/mechanisms.md` | Obrigatório | — | `/learn` Step 2 | `agents/coe-reviewer.md`, `/operate`, `/build` |

A `—` in `Template` means the shape comes from the skill's prose: `action-items.md` is shaped by
`skills/correction-of-errors/SKILL.md` and `mechanisms.md` by `skills/mechanism-creation/SKILL.md`, which
is also where the rule that an action item must be a mechanism and not a heroic lives.

## Onboarding

| Artefato | Caminho canônico | Obrigatório/Opcional | Template | Produzido por (comando) | Consumido por |
|---|---|---|---|---|---|
| Reverse-engineered design document | `docs/design/<service-name>/design-doc.md` | Obrigatório in Paths A, B and C | `skills/design-document/templates/design-doc-template.md` | `/onboard` Path A | `/design`, `/spec`, `/build` |
| API contracts index | `docs/design/<service-name>/api-contracts.md` | Obrigatório in Paths A, B and C | `skills/api-contract-first/templates/api-contracts-template.md` | `/onboard` Path A | `/design` Step 2, client teams |
| Contract artefacts read off the code | `docs/design/<service-name>/openapi.yaml` or `.proto`, `.graphql`, `asyncapi.yaml`, one per protocol | Obrigatório in Paths A, B and C | — the standard is protocol-native | `/onboard` Path A | `/design` Step 2, `/build` |
| Baseline threat model | `docs/design/<service-name>/threat-model.md` | Obrigatório in Paths A, B and C, baseline only | `skills/threat-modeling/templates/threat-model-template.md` | `/onboard` Path A | `/design` Step 3 |
| Patterns observed | `docs/design/<service-name>/patterns-observed.md` | Obrigatório in Paths A, B and C | — | `/onboard` Path A | `/design` Step 0d |
| Inferred Working Backwards set | `docs/working-backwards/<service-name>/customer-profile.md`, `problem-statement.md`, `solution-sketch.md`, `prfaq.md` | Obrigatório in Path B, each carrying the INFERRED banner | as in the Working Backwards table above | `/onboard` Path B | `agents/doc-bar-raiser.md`, `/design` |
| Bar raiser questions | `docs/working-backwards/<service-name>/bar-raiser-questions.md` | Obrigatório in Path B | — | `/onboard` Path B, written by `agents/doc-bar-raiser.md` | the user, who answers them with real customer evidence |
| Canonical Working Backwards set | `docs/working-backwards/<service-name>/` — the same five documents as the Working Backwards table, produced through the full flow | Obrigatório in Path C | as in the Working Backwards table above | `/onboard` Path C | `/design` |
| Gap analysis | `docs/design/<service-name>/gap-analysis.md` | Obrigatório in Path C | — | `/onboard` Path C | `/design`, `/spec` |

A `—` in `Template` means the shape comes from the skill's prose: `patterns-observed.md`,
`bar-raiser-questions.md` and `gap-analysis.md` are all shaped by
`skills/brownfield-discovery/SKILL.md`, and `bar-raiser-questions.md` additionally by the terminal verdict
block in `agents/doc-bar-raiser.md`, which in Path B is always INCOMPLETE by construction.

## Cross-phase

| Artefato | Caminho canônico | Obrigatório/Opcional | Template | Produzido por (comando) | Consumido por |
|---|---|---|---|---|---|
| Implementation memory | `docs/implementation-memory.md` | Opcional until the first rule is accepted; then it is read before every build | — | `/build`, and fed by `/review` and `/learn` | `/build` pre-build selection, `/design`, `/spec` |
| Accepted-risk rows | no file of its own: a row in the review artifact of the phase where the risk was accepted | Obrigatório whenever a finding is accepted instead of fixed | `skills/operational-readiness-review/templates/orr-checklist.md`, whose *Conditional Items* table defines the four columns | whoever accepts the risk, in that phase | the next review of that artifact, the owner named in the row |
| Artifact catalog | `docs/artifact-catalog.md` | Obrigatório — this file | — | maintained by hand, in the same commit as any change to a command's `## Output` | every command and every agent, as the index of what to produce and where |

A `—` in `Template` means the shape comes from the skill's prose: `docs/implementation-memory.md` is
shaped by `skills/implementation-memory/SKILL.md` → *Active Rule Format*, whose *Memory Limits* section
also caps it at 12 active rules.

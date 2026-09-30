---
name: bla
description: >-
  Build Like Amazon — the entry point for the BLA engineering flow. Routes a request to the right
  phase: Working Backwards discovery (wb, listen, define, invent, refine, test-idea), brownfield
  onboarding (onboard), design (design, spec), implementation (build, review), release (deploy,
  operate) and post-incident learning (learn). Use when the user types /bla, names a BLA phase or
  command, asks which phase or skill applies, starts a new product or feature, onboards an existing
  codebase, plans or reviews a design, implements from specs, reviews code against the bar, plans a
  progressive deployment, prepares an operational readiness review, or runs a Correction of Errors.
---

# Build Like Amazon

`/bla` routes a request to one of fourteen phases. Read the phase keyword from the text that follows
the command, activate the skills in the row, and run that phase. Any text after the keyword is the
request itself — treat it as the description of the work.

## Before you route

Two documents govern *how* you run a phase, and neither is restated here:

- **`AGENTS.md`** at the project root is the operating contract — the approval gates, the assumption
  rule, the severity and verdict scales, the accepted-risk table, the ceremony ladder. Kiro loads it
  as steering automatically. Follow it as written; do not paraphrase it.
- The **`using-amazon-skills`** skill decides how much ceremony a change deserves before any phase
  starts. Activate it first whenever the request does not already name a phase.

Every artifact path below is the one the phase's own skill declares. Write artifacts there and
nowhere else.

## Routing table

| `/bla …` | Phase | Skills to activate | Artifacts |
|---|---|---|---|
| `wb` | Working Backwards, all five stages with their gates | `working-backwards` | `.bla/working-backwards/<feature-name>/` |
| `listen` | Stage 1 — who is the customer, what do we know | `wb-listen` | `.bla/working-backwards/<feature-name>/` |
| `define` | Stage 2 — the problem, stated crisply | `wb-define` | `.bla/working-backwards/<feature-name>/` |
| `invent` | Stage 3 — the solution and the alternatives rejected | `wb-invent` | `.bla/working-backwards/<feature-name>/` |
| `refine` | Stage 4 — the PR/FAQ | `wb-refine` | `.bla/working-backwards/<feature-name>/` |
| `test-idea` | Stage 5 — how success will be measured | `wb-test-and-iterate` | `.bla/working-backwards/<feature-name>/` |
| `onboard` | Brownfield discovery, run once per project | `brownfield-discovery` | `.bla/design/<service-name>/` |
| `design` | Design, in the command's declared order | `dependency-management`, `feature-flag-lifecycle`, `operational-excellence`, `design-document`, `api-contract-first`, `threat-modeling`, `design-review`, `spec-driven-implementation` | `.bla/design/<feature-name>/` |
| `spec` | One new spec for one vertical slice | `spec-driven-implementation`, `implementation-memory` | `.bla/specs/<slice-name>/` |
| `build` | Implementation, then the post-implementation review | `incremental-implementation`, `test-driven-development`, `operational-code`, `implementation-memory`, `code-review-bar-raising` | `.bla/specs/<slice-name>/` |
| `review` | Code review against the bar | `code-review-bar-raising`, `operational-readiness-review`, `implementation-memory` | `.bla/reviews/<feature-name>/` |
| `deploy` | Progressive release | `feature-flag-lifecycle`, `progressive-deployment`, `pipeline-safety` | `.bla/deployment/<feature-name>/` |
| `operate` | Running it in production | `operational-excellence`, `operational-readiness-review` | `.bla/operations/<service-name>/` |
| `learn` | Post-incident learning | `correction-of-errors`, `mechanism-creation`, `implementation-memory` | `.bla/coe/<incident-name>/` |

The skill names in that table are Kiro skills installed under `.kiro/skills/`, so each is also a
slash command of its own: `/working-backwards`, `/design-review`, `/code-review-bar-raising`, and so
on. Activate them by name — never by file path, because in an adopter's project they do not sit
where they sit in this library.

Two skills are not routed by any phase because no phase chain declares them:
`infrastructure-as-code` and `metrics-review`. Reach them directly — Kiro also activates them on its
own when a request matches their description.

## When no keyword is recognised

Ask which phase the user wants. Do not guess, and do not start the phase that looks closest — the
phases have gates, and entering the wrong one skips someone else's approval. `AGENTS.md` states the
rule: never proceed on an unstated assumption.

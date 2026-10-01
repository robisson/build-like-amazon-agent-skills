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

`/bla` runs one of fourteen phases. Read the phase keyword from the text that follows the command,
then read that phase's procedure file from the table below **in full** and follow it step by step. It is
the same procedure the phase command runs in Claude Code — every step, gate and artifact path included.
Any text after the keyword is the request itself — treat it as the description of the work.

## Before you route

Three things govern *how* you run a phase, and none is restated here:

- **`AGENTS.md`** at the project root is the operating contract — the approval gates, the assumption
  rule, the severity and verdict scales, the accepted-risk table, the ceremony ladder. Kiro loads it
  as steering automatically. Follow it as written; do not paraphrase it.
- The **`using-amazon-skills`** skill decides how much ceremony a change deserves before any phase
  starts. Activate it first whenever the request does not already name a phase.
- **`.kiro/steering/bla.md`** is always in context. The procedures cite `skills/…`, `agents/…`,
  `patterns/…` and `.claude/commands/…` as they sit in the library; that map says where each one was
  installed in this project. Resolve every cited path through it before opening the file.

## Routing table

| `/bla …` | Phase | Read and follow |
|---|---|---|
| `wb` | Working Backwards, all five stages with their gates | `references/wb.md` |
| `listen` | Stage 1 — who is the customer, what do we know | `references/listen.md` |
| `define` | Stage 2 — the problem, stated crisply | `references/define.md` |
| `invent` | Stage 3 — the solution and the alternatives rejected | `references/invent.md` |
| `refine` | Stage 4 — the PR/FAQ | `references/refine.md` |
| `test-idea` | Stage 5 — how success will be measured | `references/test-idea.md` |
| `onboard` | Brownfield discovery, run once per project | `references/onboard.md` |
| `design` | Design — the design document through the spec breakdown | `references/design.md` |
| `spec` | One new spec for one vertical slice | `references/spec.md` |
| `build` | Implementation, then the post-implementation review | `references/build.md` |
| `review` | Code review against the bar | `references/review.md` |
| `deploy` | Progressive release | `references/deploy.md` |
| `operate` | Running it in production | `references/operate.md` |
| `learn` | Post-incident learning | `references/learn.md` |

Each path is relative to this skill's folder, `.kiro/skills/bla/`. A procedure file is the whole
phase: do not act on a summary of it, and do not skip a step or a gate it declares.

Two skills are not routed by any phase because no procedure declares them: `infrastructure-as-code`
and `metrics-review`. Reach them directly — Kiro also activates them on its own when a request matches
their description.

## When no keyword is recognised

Ask which phase the user wants. Do not guess, and do not start the phase that looks closest — the
phases have gates, and entering the wrong one skips someone else's approval. `AGENTS.md` states the
rule: never proceed on an unstated assumption.

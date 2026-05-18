# Amazon Working Backwards

## Description
Router skill for the Working Backwards lifecycle phase. Routes to the canonical skill files under `.kiro/skills/amazon/`.

## When to Use
- Starting a new product or feature from scratch
- Pivoting an existing feature based on customer feedback
- Validating whether an idea is worth building
- Aligning a team on what to build and why

## When NOT to Use (use a different path)

- **Existing project with code but no BLA artifacts** → use **`/onboard`** instead. It offers 3 paths: (A) anchor only — Design Doc + contracts + threat model; (B) validate the *why* — inferred PR/FAQ + hard questions from the doc-bar-raiser; (C) forward WB + gap analysis — full `/wb` from scratch, then compare against what exists. Working Backwards *as greenfield* (`/wb`) is for new-product discovery; `/onboard` Path B or C serve the "validate existing product" need. See `.kiro/skills/amazon-build-and-deploy.md` for the build-side skills.
- **Trivial or small change** to an existing product → skip Working Backwards entirely; describe the change directly and the agent applies the proportionality ladder. See `.kiro/skills/amazon/using-amazon-skills/SKILL.md` → "Match the Ceremony to the Change".

## Source of Truth

This skill is a thin router. Read these directly for the actual guidance:

| Phase | Skill | Path |
|-------|-------|------|
| Meta | Working Backwards Full Cycle | `.kiro/skills/amazon/working-backwards/SKILL.md` |
| 1 — Listen | Customer Discovery | `.kiro/skills/amazon/wb-listen/SKILL.md` |
| 2 — Define | Problem Statement | `.kiro/skills/amazon/wb-define/SKILL.md` |
| 3 — Invent | Solution Sketch | `.kiro/skills/amazon/wb-invent/SKILL.md` |
| 4 — Refine | PR/FAQ | `.kiro/skills/amazon/wb-refine/SKILL.md` |
| 5 — Test and Iterate | Success Metrics | `.kiro/skills/amazon/wb-test-and-iterate/SKILL.md` |

## Workflow

When the user asks to start a Working Backwards cycle:

1. Read `.kiro/skills/amazon/working-backwards/SKILL.md` for the full process
2. Execute each stage sequentially with approval gates between them
3. Use the individual stage skills above for detailed guidance at each step

## Approval Gates (non-negotiable)

Each of the five Working Backwards stages has a mandatory human approval gate. Complete one stage, present the output, ask the user to review, and wait for explicit approval before advancing. See `.kiro/steering/amazon-engineering.md` for the full gate protocol.

## Bar Raiser Personas

When a skill specifies bar raiser review, the persona guidance is embedded in the skill files and in the steering file (`.kiro/steering/amazon-engineering.md`).

## Bridge to Design

Working Backwards output (PR/FAQ + success metrics) feeds the Design phase. The customer experience described in the PR/FAQ is delivered by an **API** — every customer-facing capability becomes an API at the design stage, and every client (UI, CLI, SDK, MCP, AI agent, partner) consumes that API. See `.kiro/skills/amazon/working-backwards/SKILL.md` Tenet #6 and `.kiro/skills/amazon/using-amazon-skills/SKILL.md` Operating Behavior #9 (API First).

## Operating Contract

Read `.kiro/steering/amazon-engineering.md` for the full agent operating contract: approval gates, surface assumptions, push back, verify don't assume.

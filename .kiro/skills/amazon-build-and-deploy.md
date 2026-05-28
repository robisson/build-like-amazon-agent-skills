# Amazon Build and Deploy

## Description
Router skill for Build, Review, and Deploy phases. Routes to the canonical skill files under `.kiro/skills/amazon/`.

## When to Use
- Implementing features after design phase is complete
- Reviewing pull requests
- Planning deployment for new services
- Preparing for operational readiness reviews

## Source of Truth

This skill is a thin router. Read these directly for the actual guidance:

| Phase | Skill | Path |
|-------|-------|------|
| Onboarding | Brownfield Discovery (3 paths: anchor only / validate-the-why / forward WB + gap) | `.kiro/skills/amazon/brownfield-discovery/SKILL.md` |
| Build | Spec-Driven Implementation | `.kiro/skills/amazon/spec-driven-implementation/SKILL.md` |
| Build | Incremental Implementation (incl. Code Quality Bar) | `.kiro/skills/amazon/incremental-implementation/SKILL.md` |
| Build | Test-Driven Development | `.kiro/skills/amazon/test-driven-development/SKILL.md` |
| Build | Operational Code | `.kiro/skills/amazon/operational-code/SKILL.md` |
| Build internal mechanism | Implementation Memory | `.kiro/skills/amazon/implementation-memory/SKILL.md` |
| Build | Infrastructure as Code | `.kiro/skills/amazon/infrastructure-as-code/SKILL.md` |
| Review | Code Review Bar Raising | `.kiro/skills/amazon/code-review-bar-raising/SKILL.md` |
| Review | Operational Readiness Review | `.kiro/skills/amazon/operational-readiness-review/SKILL.md` |
| Deploy | Progressive Deployment | `.kiro/skills/amazon/progressive-deployment/SKILL.md` |
| Deploy | Pipeline Safety | `.kiro/skills/amazon/pipeline-safety/SKILL.md` |
| Deploy | Feature Flag Lifecycle | `.kiro/skills/amazon/feature-flag-lifecycle/SKILL.md` |

## Workflow

When the user asks to build, review, or deploy:

0. **First, classify the change** using the proportionality ladder in `.kiro/skills/amazon/using-amazon-skills/SKILL.md` → "Match the Ceremony to the Change". Trivial → direct to code; Small → direct or lightweight spec; Medium → `/spec` + `/build`; Large → full `/design` + `/spec` + `/build`. For brownfield projects without BLA artifacts, propose `/onboard` first for medium/large changes.
1. For implementation: Read `.kiro/skills/amazon/spec-driven-implementation/SKILL.md` first, then `.kiro/skills/amazon/incremental-implementation/SKILL.md`. During `/build`, automatically read `.kiro/skills/amazon/implementation-memory/SKILL.md` after the current spec/tasks are known. Select active rules using multi-signal matching (Tags, File patterns, `Applies when`). Semi-automatic trigger: after PASSED WITH FIXES NEEDED and fixes done, generate self-reflection, extract candidates, present to user for Accept/Reject/Edit. Manual trigger: after PASSED, prompt user to test/debug, update only after Quality Memory Review request. Nudge if ≥3 builds without update. Also capture from `/review` (recurring findings) and `/learn` (COE actions). This is an internal build mechanism, not a user-facing command.
2. For code review: Read `.kiro/skills/amazon/code-review-bar-raising/SKILL.md`
3. For deployment: Read `.kiro/skills/amazon/progressive-deployment/SKILL.md`
4. For brownfield onboarding (existing project, no BLA artifacts): Read `.kiro/skills/amazon/brownfield-discovery/SKILL.md`

## Bar Raiser Personas

When a skill specifies bar raiser review, the persona guidance is embedded in the skill files and in the steering file (`.kiro/steering/amazon-engineering.md`).

## Non-Negotiable Behaviors

These are the rules the canonical skills enforce — listed here as a quick reference, not as duplicated content:

1. **Match the ceremony to the change.** Trivial → direct to code; Small → direct or lightweight spec; Medium → `/spec` + `/build`; Large → full flow. The agent picks. For brownfield, propose `/onboard` first on medium/large changes. See `.kiro/skills/amazon/using-amazon-skills/SKILL.md` → "Match the Ceremony to the Change".
2. **API First** — API specs precede client specs. See `.kiro/skills/amazon/using-amazon-skills/SKILL.md`.
3. **Track tasks during build** — Orchestrator owns `tasks.md`. `[ ] → [-] → [x]` or `[!]`.
4. **`/build` is autonomous to feature completion.** No gates between specs/waves/PASSED reviews. Stops only for hard blockers, FAILED review, or explicit user pause request.
5. **Implementation memory** — Internally use `.kiro/skills/amazon/implementation-memory/SKILL.md` and `docs/implementation-memory.md` during build. Multi-signal matching (Tags, File patterns, `Applies when`). Semi-auto trigger on PASSED WITH FIXES NEEDED (self-reflection → candidates → Accept/Reject/Edit). Nudge after 3 builds without update. Multi-source capture from `/review` and `/learn`. Staleness: flag rules unused >90 days. Do not expose as a user command.
6. **Code Quality Bar** — Paradigm by context, SOLID where it pays, clean naming, no dead code, no premature abstraction. See `.kiro/skills/amazon/incremental-implementation/SKILL.md`.
7. **Tests first; observable by default; ship small.** See the build skills above.
8. **Progressive rollout; rollback in <5 minutes; alarms before customers.** See the deploy skills above.

## Operating Contract

Read `.kiro/steering/amazon-engineering.md` for the full agent operating contract: approval gates, surface assumptions, push back, verify don't assume.

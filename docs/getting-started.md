# Getting Started

Build Like Amazon turns your AI coding agent into one that thinks like an Amazon engineer — starts from the customer, designs before coding, ships in slices, learns from incidents.

This page is **how to start using it in 10 minutes**, with concrete examples for the situations you actually run into.

---

## 1. Install (pick your agent)

The fastest path is **Claude Code**, which has first-class support for slash commands. The other integrations work; their setup snippets are in [the README](../README.md#quick-start).

```bash
# Clone next to your project
git clone https://github.com/robisson/build-like-amazon.git

# Drop the contract and slash commands into your project
cp build-like-amazon/CLAUDE.md your-project/CLAUDE.md
cp -r build-like-amazon/.claude/commands/ your-project/.claude/commands/

# Optional: keep skills/, agents/, patterns/ next to your project
# so commands can reference them. Either symlink or copy:
ln -s "$(pwd)/build-like-amazon/skills" your-project/skills
ln -s "$(pwd)/build-like-amazon/agents" your-project/agents
ln -s "$(pwd)/build-like-amazon/patterns" your-project/patterns
```

That's it. Open your project, start Claude Code, and use the slash commands directly.

---

## 2. The 60-second mental model

There are five phases. The agent picks the right one based on what you ask:

```
Working Backwards → Design → Build → Deploy → Operate → Learn ↺
```

**You don't need to know all of them.** Most of the time you'll just say what you want, and the agent will pick the right ceremony level. The user-facing surface is mostly **slash commands**:

| If you want to... | Use |
|---|---|
| Start a new product or feature from scratch | `/wb` |
| Adopt this on an existing project (no design docs yet) | `/onboard` |
| Design a non-trivial change | `/design` |
| Add one more feature when design already exists | `/spec` |
| Implement specs that are ready | `/build` |
| Get a code review | `/review` |
| Deploy safely | `/deploy` |
| Set up runbooks and alarms before launch | `/operate` |
| Run a blameless post-incident analysis | `/learn` |

**Key principle:** the agent matches the ceremony to the size of the change. Trivial fixes don't need a Design Doc; new products don't skip `/wb`. You don't have to think about it — the agent decides and only asks when there's genuine ambiguity.

---

## 3. Try it now — 4 scenarios

Pick the one that matches what you're doing right now:

- [Scenario A — Brand new product or service](#scenario-a--im-starting-a-brand-new-productservice)
- [Scenario B — Existing project, first-time adoption](#scenario-b--i-have-an-existing-project-and-want-help-maintaining-it)
- [Scenario C — Small change in an existing project](#scenario-c--i-want-to-make-a-small-change-in-an-existing-project)
- [Scenario D — Production incident](#scenario-d--something-broke-in-production)

### Scenario A — "I'm starting a brand new product/service"

This is the canonical Amazon flow. Use `/wb` first, the agent will guide the rest.

```
/wb I want to build a service that lets product managers query customer feedback
   across Slack, Zendesk, and email using natural language
```

What happens:
- The agent walks you through 5 stages: Listen → Define → Invent → Refine → Test
- Each stage **stops for your approval** — you review the output before moving on
- Output: an approved PR/FAQ + success metrics in `docs/working-backwards/`

After approval, you say `/design`. The agent reads your PR/FAQ and produces:
- Design Doc (with patterns considered, dependency behavior, operational concerns)
- API Contract (OpenAPI / GraphQL / `.proto` / AsyncAPI / etc. — agent picks the right standard for your protocol)
- Threat Model
- Specs ready for `/build`

Then `/build` runs everything to completion autonomously.

### Scenario B — "I have an existing project and want help maintaining it"

Run **`/onboard`**. The agent asks you which of the 3 paths you want:

```
/onboard
```

The agent will ask:

```
Detected: existing project, no BLA artifacts. How would you like to use /onboard?

[A] Anchor only (Recommended)
    Design Doc + API contracts + Threat Model from existing code.
    "Give the agent context so future /spec and /build are precise."
    ~15–30min.

[B] Validate the *why*
    Everything in [A] + inferred PR/FAQ + hard questions from
    the doc-bar-raiser where the code can't tell us why.
    "I built fast and want to check I'm solving the right problem."
    ~30–45min.

[C] Forward WB + Gap Analysis
    Full /wb from scratch (5 stages, approval gates), then compare
    "what I'd build today" vs "what actually exists."
    "I'm pivoting or want to revalidate from scratch."
    ~1–2h.
```

You pick a letter. Most people start with **[A]** — fast, pragmatic, anchors everything. Use **[B]** when you suspect you built without clarity on the "why". Use **[C]** for strategic re-evaluation.

Output: `docs/design/<service>/` with a `REVERSE-ENGINEERED` banner. Path B also produces `docs/working-backwards/<service>/` with an inferred PR/FAQ + questions. Path C produces canonical WB artifacts (approved through the real process with you) + a gap analysis.

### Scenario C — "I want to make a small change in an existing project"

Just ask for what you want. The agent classifies the size and picks the right path.

```
/build add a red 'Cancel order' button on the checkout screen
```

If your project has no specs and no Design Doc, the agent will ask **outcome-framed options** (not process names):

```
Detected: small UI change, no specs in this project.

[A] Direct implementation — TDD + Code Quality Bar. ~30min. (Recommended.)
[B] Lightweight spec — single spec for traceability. ~1h.
[C] Run /onboard first — anchor the project, then create the spec.
    ~30min onboarding + ~1h spec.
```

You pick a letter. No need to know what "Tier 1" or "spec-driven-implementation" means.

### Scenario D — "Something broke in production"

```
/learn We had an incident: payments service returned 5xx for 12 minutes
   after the v2.4 deploy. Traffic was at peak, ~8% of orders failed.
```

What happens:
- Agent walks you through a **blameless** Correction of Errors (COE)
- Timeline reconstruction, Five Whys, root cause, contributing factors
- Action items as **mechanisms** (automated safeguards), not "be more careful"
- Output: a COE document ready for review

If the COE points at a recurring issue, the agent will suggest `/operate` to upgrade runbooks, alarms, or dashboards.

---

## 4. Common situations and which command to use

| Situation | Command | Notes |
|---|---|---|
| New product / new service | `/wb` → `/design` → `/build` | Don't skip `/wb`; the customer is the foundation |
| Existing project, first-time BLA adoption | `/onboard` once, then normal flow | Run before any medium/large change |
| New feature in existing product | `/design` → `/spec` → `/build` | If `/onboard` was done, this is fast |
| Adding one more endpoint, design already done | `/spec` → `/build` | No need to re-design |
| Trivial fix (typo, dep bump, comment) | Just say it directly | The agent applies Code Quality Bar without spec |
| Code review on a PR | `/review` | Pulls in code review bar raiser persona |
| Production deploy | `/deploy` | Progressive rollout with auto-rollback |
| Pre-launch readiness | `/operate` | Alarms, dashboards, runbooks |
| Post-incident | `/learn` | Blameless COE + mechanisms |

---

## 5. Override the defaults when you need to

By default `/build` runs **all specs end-to-end without pausing**. If you want it to pause between specs (for review, for sanity check, for any reason), say so in the prompt:

```
/build run the auth specs, but pause between specs and ask me before each one
```

The agent will switch to step-by-step mode for that invocation. Default returns next time.

Same idea for any other override — the agent listens to natural language, you don't need a flag system.

---

## 6. What makes this different from a generic AI coder

Five things compound:

- **Approval gates** during `/wb`, `/design`, `/spec` — the agent stops and shows you the work, you approve, it continues. Quality compounds at each gate.
- **Bar raiser personas** in `agents/` — review code, designs, threat models, COEs through specific lenses. Ten of them, each with hard questions ready.
- **Architectural patterns** in `patterns/` — when relevant, the agent pulls cell-based, shuffle-sharding, etc. into your design as real alternatives, not as forgotten options.
- **Autonomous `/build`** — once specs are approved, the agent ships everything to completion. No "should I continue?" between specs.
- **Mechanisms over good intentions** — every COE produces an automated safeguard. "We'll be careful" is a red flag.

---

## 7. FAQ

**Do I have to start from `/wb` every time?**
No. `/wb` is for new products. For existing projects, `/onboard` once, then use `/design`, `/spec`, or just describe a change directly.

**What if my change is trivial?**
Just describe it. The agent will skip the heavy ceremony and apply the Code Quality Bar directly. No spec, no Design Doc.

**What if I'm not sure which command to use?**
Just describe what you want in plain text. The meta-skill (`skills/using-amazon-skills/SKILL.md`) routes ambiguous requests to the right command.

**Will this slow me down?**
For trivial work, no — the agent skips ceremony. For real features, yes initially, no longer-term: teams that design before coding ship more reliably and recover from incidents faster.

**Does it work with non-Claude agents?**
Yes. Cursor, Gemini CLI, Kiro, GitHub Copilot, OpenAI Codex, OpenCode, Aider — all supported with their own setup snippets in the [README](../README.md#quick-start).

**Where do my project files live?**
- `docs/working-backwards/` — PR/FAQ, success metrics
- `docs/design/<feature>/` — Design Doc, API contracts, Threat Model
- `specs/<slice>/` — requirements + design + tasks for each implementation slice
- `docs/coe/` — incident analyses

**My team has its own way of doing things. Can I adapt?**
Adjust the ceremony, terminology, thresholds. But don't remove the hard parts (gates, bar raisers, mechanisms) — they exist because real incidents demanded them.

---

## 8. Where to go next

- **Philosophy** — read [`docs/philosophy.md`](philosophy.md) for *why* the practices exist
- **Skill anatomy** — read [`docs/skill-anatomy.md`](skill-anatomy.md) if you want to write your own skill
- **All skills** — full catalog in the [README](../README.md#all-27-skills)
- **Bar raiser personas** — [`agents/`](../agents/) directory
- **Architectural patterns** — [`patterns/`](../patterns/) directory
- **Operating contract for agents** — [`AGENTS.md`](../AGENTS.md) (read this if you're a contributor or building a new integration)

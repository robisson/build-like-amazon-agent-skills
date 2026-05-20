# Onboard — Reverse-Engineer an Existing Project

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

`/onboard` activates the **brownfield-discovery** skill. It runs once per project (or when the project drifts significantly) and produces anchoring artifacts derived from the real code, IaC, and observability.

`/onboard` has **three paths**, picked by the user at the start. The agent classifies and asks; the user picks an outcome, not a process step.

| Path | Outcome | Time |
|---|---|---|
| **A — Anchor only** *(default, recommended)* | Design Doc + API contracts + Threat Model from existing code. No customer/PR/FAQ. | ~15–30min |
| **B — Validate the *why*** | Path A + reverse-engineered PR/FAQ + hard questions from `doc-bar-raiser` where the code can't tell us why | ~30–45min |
| **C — Forward WB + Gap Analysis** | Full canonical `/wb` from scratch (5 stages with gates, agent reading existing code) + Path A + `gap-analysis.md` | ~1–2h |

The output anchors all subsequent `/spec` and `/build` invocations — instead of re-discovering the project on every change, the agent reads the persisted artifacts.

## When to Use

- The project already has significant code, IaC, CI, and possibly observability — but no Build Like Amazon artifacts (`docs/design/`, `docs/working-backwards/`)
- A medium or large change is coming, and anchoring the agent on the real state of the project will pay back many times
- The user explicitly invokes `/onboard`
- The project has drifted significantly from the prior reverse-engineered baseline (architecture change, major refactor, new pattern adopted)
- The user wants to validate that what's been built actually serves a real customer problem (Path B)
- The project is pivoting / re-strategizing and the user wants to re-derive the WB from scratch and see the gap (Path C)

## When NOT to Use

- Greenfield project — use `/wb` → `/design` instead
- Project already has canonical Design Doc — that is the anchor; don't overwrite it
- Trivial or small changes — the proportionality ladder in `skills/using-amazon-skills/SKILL.md` handles those without onboarding
- "Just to have docs" — onboarding exists to anchor change, not to produce documentation for documentation's sake

## Prerequisites

- Read access to the full project (code, IaC, CI configs, dashboards if available)
- The project must have been authored to some degree — onboarding an empty repo produces nothing

## Step 0: Confirm Onboarding Is the Right Path

Before running discovery, confirm with `AskUserQuestion`:

1. Detect whether `docs/design/` already contains a Design Doc (canonical or reverse-engineered).
   - If it exists with the **REVERSE-ENGINEERED** banner: ask whether the user wants to refresh it. If no significant drift, recommend skipping.
   - If it exists as canonical (no banner): warn that onboarding would overwrite. Recommend cancellation unless explicitly desired.
2. Detect project size / complexity. If the project is trivially small (a single file, a script), recommend skipping onboarding and going directly via `/build` or `/spec`.

If onboarding is the right path, proceed to Step 1.

## Step 1: Pick the Path (A / B / C)

Use `AskUserQuestion` to surface the three paths to the user, framed by **outcome**, not by process. Names like "Path A", "brownfield-discovery", "Reverse Working Backwards" do **not** appear in the question — the user picks based on what they want to get out of `/onboard`.

Recommended question text:

> Detected: existing project, no BLA artifacts. How would you like to use `/onboard`?
>
> **[A] Anchor only** *(Recommended)*
> Produce a Design Doc, API contracts, and a Threat Model from the existing code. Future `/spec` and `/build` use these as anchor. Does *not* try to recover the customer story or PR/FAQ.
> Use when: "I'll keep building here, give the agent the context it needs." ~15–30min.
>
> **[B] Validate the *why***
> Everything in [A], plus an inferred PR/FAQ reconstructed from the code, README, and docs. The doc-bar-raiser surfaces hard questions where the code can't tell us why.
> Use when: "I built fast and want to check whether I'm solving the right problem." ~30–45min.
>
> **[C] Forward WB + Gap Analysis**
> Run a full `/wb` from scratch (5 stages with approval gates) as if greenfield, with the agent reading the existing code during the conversation. At the end, produce a `gap-analysis.md` comparing "what we'd build today" vs "what exists."
> Use when: "I'm pivoting / re-strategizing / want to revalidate from scratch." ~1–2h.

If the user does not pick or asks the agent to pick, default to **A**.

## Step 2: Run the Chosen Path

Read skill at `skills/brownfield-discovery/SKILL.md` and follow the Process section for the chosen path:

- **Path A** — Steps 1–6 of the skill, then Path A's closing gate.
- **Path B** — Steps 1–6 + 7 (reverse-engineer WB) + 8 (Doc Bar Raiser pass) + 9 (Path B closing gate).
- **Path C** — Steps 1–6 + 7' (full canonical `/wb` flow with all 5 approval gates) + 8' (Gap Analysis) + 9' (Path C closing gate).

## Output

### Path A
```
docs/design/<service-name>/
├── design-doc.md           (REVERSE-ENGINEERED banner, per-section confidence)
├── api-contracts.md        (pointers to canonical contracts when they exist)
├── openapi.yaml            (or .proto, .graphql, asyncapi.yaml, etc., per protocol)
├── threat-model.md         (baseline only)
└── patterns-observed.md    (pattern catalog cross-reference)
```

### Path B (Path A + WB inferred)
```
docs/design/<service-name>/        (same as Path A)
docs/working-backwards/<service-name>/
├── customer-profile.md           (REVERSE-ENGINEERED, INFERRED — needs validation)
├── problem-statement.md          (REVERSE-ENGINEERED, INFERRED)
├── solution-sketch.md            (REVERSE-ENGINEERED — higher confidence, derived from API/UI)
├── prfaq.md                      (DRAFT — INFERRED, with FAQ marked TO BE FILLED where evidence is missing)
└── bar-raiser-questions.md       (structured hard questions for the user to answer with real customer evidence)
```

### Path C (Path A + canonical WB + gap analysis)
```
docs/design/<service-name>/        (same as Path A)
docs/working-backwards/<service-name>/
├── customer-profile.md           (canonical — produced through full WB flow with user)
├── problem-statement.md          (canonical)
├── solution-sketch.md            (canonical)
├── prfaq.md                      (canonical — approved through PR/FAQ review)
└── success-metrics.md            (canonical)
docs/design/<service-name>/gap-analysis.md   (extend / sunset / re-justify / align)
```

## Boundaries

- `/onboard` does **NOT** make architecture changes. It only documents existing state (Path A and B) or proposes alignment (Path C gap analysis as recommendations).
- `/onboard` does **NOT** retroactively approve decisions. The REVERSE-ENGINEERED banner is mandatory on inferred design artifacts.
- `/onboard` does **NOT** replace `/wb` or `/design` for new features. It anchors the project so subsequent `/design` calls have proper context.
- `/onboard` does **NOT** fabricate customer stories. In Path B, the agent surfaces the questions the user must answer with real customer evidence; it does not invent the answers.
- `/onboard` is **idempotent in spirit** for Path A — running it on an unchanged project twice produces the same artifacts. Path C is *not* idempotent — it produces a new WB based on what the user thinks today.
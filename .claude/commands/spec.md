# Spec — Create a New Implementation Spec

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

This command creates a **single new spec** (vertical slice of value) when the design phase is already complete. Use it to incrementally add features, endpoints, or capabilities without re-running the full `/design` flow.

## Step 0: State Detection + Proportionality Check

Before creating a spec, detect the project state and classify the requested change. The user should not have to think about which path is right — the agent decides, and asks only when there is genuine ambiguity.

1. **Read repo state**:
   - Does `docs/design/<feature-or-service>/design-doc.md` exist (greenfield with full flow)?
   - Does `docs/design/` contain a reverse-engineered Design Doc (banner says "REVERSE-ENGINEERED" — produced by `/onboard`)?
   - Does the project have significant code, IaC, CI but no BLA artifacts (brownfield, no onboarding done)?
   - Are there existing specs in `specs/` that already cover this slice?

2. **Classify the requested change** using the ladder in `skills/using-amazon-skills/SKILL.md`: Trivial / Small / Medium / Large.

3. **Decide the path**:

   | State | Change size | Path |
   |---|---|---|
   | Design Doc exists (canonical or reverse-engineered) | Medium / Large | Proceed with full spec creation below. |
   | Design Doc exists | Trivial / Small | The spec is overkill for this size. Recommend going direct via `/build` instead. Use `AskUserQuestion` to confirm before creating a heavy spec. |
   | No Design Doc, brownfield project | Medium / Large | Use `AskUserQuestion` to offer: [A] Run `/onboard` first to reverse-engineer the project (recommended for medium+), then create the spec; [B] Create a lightweight spec anchored on the existing code without a Design Doc; [C] Run full `/design` from scratch. Pick one before proceeding. |
   | No Design Doc, brownfield project | Trivial / Small | Recommend skipping spec creation; go direct via `/build`. Confirm with the user. |
   | No Design Doc, greenfield project | any | Recommend `/design` first. Spec creation needs an anchor. |

4. **Asking the user — outcome-framed options only**. When ambiguity requires a choice, the question must offer concrete outcomes (time, scope, traceability), not process names.

5. **After the user picks (or no question was needed)**: proceed with the chosen path. Spec creation continues with the steps below; alternative paths divert to other commands.

⛔ **PREREQUISITE for full spec creation**: A System Design Document MUST exist (canonical or reverse-engineered). If none exists and the user did not pick a lightweight alternative in Step 0, STOP.

## When to Use

- You already have an approved Design Document
- You want to add one more feature/endpoint/capability to an existing system
- You're extending something that was previously built (e.g., "add another API endpoint")
- You don't need to revisit the macro architecture — just plan and implement one slice

## What to Do

1. **Read the existing context:**
   - Load the System Design Document (identify its location)
   - Load any existing specs (to understand what's already built)
   - Identify any dependency-management decisions already captured in the Design Document
   - Identify any feature-flag lifecycle decisions already captured in the Design Document
   - Identify any operational-excellence decisions already captured in the Design Document
   - Read `skills/spec-driven-implementation/SKILL.md` for the full process
   - Read the templates in `skills/spec-driven-implementation/templates/`

2. **Create the spec following the templates EXACTLY:**

   ### Step 1: requirements.md
   - Use the template from `skills/spec-driven-implementation/templates/requirements-template.md` VERBATIM
   - Extract requirements for THIS slice only (not the whole system)
   - Use EARS notation: "THE [Subject] SHALL [behavior]", "WHEN [condition] THE [Subject] SHALL [action]"
   - Reference the Design Document sections that cover this slice
   - 🚦 **GATE**: Present requirements.md to the user. Ask: "Do these requirements capture what you want? Anything missing or wrong?"
   - ⛔ DO NOT proceed until the user approves.

   ### Step 2: design.md
   - Use the template from `skills/spec-driven-implementation/templates/design-template.md` VERBATIM
   - Detail ONLY this slice's design (not a repeat of the macro design)
   - Include Mermaid diagrams, interfaces, error handling, dependency behavior inherited from the Design Document, operational behavior inherited from the Design Document, and PBT properties
   - Reference requirements by number for traceability
   - Do not rediscover or redesign dependency-management behavior; preserve the approved design decisions.
   - Do not invent feature-flag, rollout, kill switch, or cleanup behavior; preserve the approved design decisions.
   - Do not invent dashboards, alarms, runbooks, operational metrics, severity expectations, or operational burden; preserve the approved design decisions.
   - 🚦 **GATE**: Present design.md to the user. Ask: "Does this design look right? Any trade-offs to discuss?"
   - ⛔ DO NOT proceed until the user approves.

   ### Step 3: tasks.md
   - Use the template from `skills/spec-driven-implementation/templates/tasks-template.md` VERBATIM
   - Decompose into phased tasks with dependency graph
   - Include green-build gates, wave assignments, size estimates
   - Add Dependency Graph JSON at the bottom with waves
   - Use status markers: `- [ ]` pending, `- [-]` in progress, `- [x]` done, `- [!]` blocked
   - 🚦 **GATE**: Present tasks.md to the user. Ask: "Task plan looks good? Dependencies correct?"
   - ⛔ DO NOT proceed until the user approves.

3. **Run Spec Coherence Review:**
   - Validate this spec against the existing Design Document
   - Check for contradictions, scope creep, architectural misalignment, dependency-management drift, feature-flag lifecycle drift, and operational-excellence drift
   - Produce `coherence-review.md` with Action Items for Build Agent
   - 🚦 **GATE**: If NEEDS REVISION, go back and fix. If APPROVED, spec is ready for `/build`.

## Output

A complete spec directory:
```
specs/<slice-name>/
├── requirements.md      (EARS notation, approved)
├── design.md            (Mermaid, interfaces, PBT props, approved)
├── tasks.md             (waves, dependency graph, approved)
└── coherence-review.md  (validation against Design Doc)
```

Ready for execution with `/build`.

## Template Enforcement

⛔ If your output doesn't match the templates, STOP and redo:
- requirements.md MUST have EARS notation (SHALL/WHEN/IF)
- design.md MUST have Mermaid diagrams and requirement traceability
- tasks.md MUST have dependency graph JSON with waves at the bottom
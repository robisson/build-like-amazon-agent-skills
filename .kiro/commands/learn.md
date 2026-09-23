<!-- MIRROR: This file mirrors .claude/commands/learn.md. Do not edit directly — sync from the Claude version. -->

# Learn — Correction of Errors and Mechanisms

You are activating the **learn** skill chain: `correction-of-errors` → `mechanism-creation`.

## What to do

1. Read skills at `skills/correction-of-errors/` and `skills/mechanism-creation/`.
2. Help the user learn from failures and build systems that prevent recurrence.

### Step 1: Correction of Errors (COE)
Guide the user through writing a COE:
- **Incident summary**: What happened, when, impact (duration, customers affected).
- **Timeline**: Minute-by-minute from detection to resolution.
- **Root cause analysis**: Use 5 Whys — dig past symptoms to systemic causes.
- **Contributing factors**: What conditions allowed this to happen?
- **What went well**: Acknowledge what worked (detection, response, tooling).
- **Action items**: Each with owner, due date, and completion criteria.
  - Categorize: immediate fix, short-term mitigation, long-term prevention.

Key COE principles:
- Blameless — focus on systems, not individuals.
- Be brutally honest — the goal is learning, not looking good.
- Action items must be mechanisms, not heroics.

Once the COE is drafted, load `agents/coe-reviewer.md` and review it through the COE reviewer lens.

### Step 2: Mechanism Creation
Convert learnings into durable mechanisms:
- **Automation**: Replace manual steps with automated checks.
- **Guardrails**: Pipeline gates, config validation, pre-deploy checks.
- **Process changes**: Updated runbooks, new review steps, training.
- **Architectural improvements**: Eliminate the class of failure entirely.
- **Metrics and alarms**: Detect the preconditions before they become incidents.

A mechanism is complete when:
- It works without human willpower or memory.
- It prevents the entire CLASS of problem, not just this instance.
- It's verified through testing or simulation.

## Implementation Memory Capture

After corrective actions are defined, check whether any action item is an **implementation-level** corrective action (i.e., something that should change how code is written in future builds — not an org/process/people action). If so:

1. Read `skills/implementation-memory/SKILL.md`.
2. Generate a self-reflection: "What implementation practice would have prevented or mitigated this incident? What general rule should apply to future builds?"
3. Extract up to 2 candidate learnings from implementation-level action items.
4. Present candidates to the user for Accept / Reject / Edit (same format as `/build` semi-automatic trigger).
5. Apply admission checks and rejection rules before writing to `docs/implementation-memory.md`.

If no implementation-level action item exists (all actions are org/process/infra), skip this step silently.

## Output

Save to `docs/coe/<incident-name>/`:
- `coe-report.md`
- `action-items.md`
- `mechanisms.md`

**Flow metrics.** `/learn` owns two of the six events for the `learn` phase — `phase_started` and
`phase_completed` — and appends each as one JSON line to `docs/bla-metrics.jsonl`: `phase_started` once the
change is classified as Medium or above, `phase_completed` once the artifacts above are saved. The COE
review of Step 1 is a review, not a gate over a BLA artefact, and `/learn` persists no BLOCKING findings,
so `gate_approved`, `gate_rework` and `review_blocking_finding` are not its to emit — no command emits an
event another one owns (owner table in `docs/flow-metrics.md`). A COE about a flow-metric series is still
bound by rule 2 of `docs/flow-metrics.md`: reconstruct a timeline in the COE, never in the series. **Emit
only at Medium and above**; at Trivial and Small emit nothing. If the line cannot be written — no writable
tree, no `docs/` directory, the adopter declined — state in one line that the flow measurement for this
phase was not recorded, and **continue**: measurement never blocks a COE or a mechanism.

# Learn — Correction of Errors and Mechanisms

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

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
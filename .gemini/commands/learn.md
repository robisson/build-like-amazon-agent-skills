<!-- MIRROR: This file mirrors .claude/commands/learn.md. Do not edit directly — sync from the Claude version. -->

# Learn — Correction of Errors and Mechanisms

Activate the **learn** skill chain: `skills/correction-of-errors/` → `skills/mechanism-creation/`.

## Instructions

Help the user learn from failures and build systems that prevent recurrence.

### Step 1: Correction of Errors (COE)
Guide the COE writing:
- **Incident summary**: What happened, when, impact (duration, customers).
- **Timeline**: Minute-by-minute from detection to resolution.
- **Root cause**: 5 Whys — dig past symptoms to systemic causes.
- **Contributing factors**: What conditions allowed this?
- **What went well**: Detection, response, tooling that worked.
- **Action items**: Owner, due date, completion criteria each.
  - Immediate fix, short-term mitigation, long-term prevention.

COE principles:
- Blameless — focus on systems, not individuals.
- Brutally honest — the goal is learning.
- Action items must be mechanisms, not heroics.

### Step 2: Mechanism Creation
Convert learnings into durable mechanisms:
- **Automation**: Replace manual steps with automated checks.
- **Guardrails**: Pipeline gates, config validation, pre-deploy checks.
- **Process**: Updated runbooks, new review steps, training.
- **Architecture**: Eliminate the class of failure entirely.
- **Observability**: Detect preconditions before they become incidents.

A mechanism is complete when:
- It works without human willpower or memory.
- It prevents the CLASS of problem, not just this instance.
- It's verified through testing or simulation.

## Output

Save to `docs/coe/<incident-name>/`:
- `coe-report.md`
- `action-items.md`
- `mechanisms.md`

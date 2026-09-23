# Deploy — Progressive Deployment

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

You are activating the **deploy** skill chain: `feature-flag-lifecycle` → `progressive-deployment` → `pipeline-safety`.

## What to do

1. Read skills at `skills/feature-flag-lifecycle/`, `skills/progressive-deployment/`, and `skills/pipeline-safety/`.
2. Help the user plan and execute a safe deployment strategy.

### Step 1: Feature Flag Lifecycle
If the approved design/spec uses feature flags, define the release lifecycle:
- Flag starts with safe default OFF.
- OFF behavior preserves existing behavior or graceful fallback.
- Kill switch behavior is documented and works without deployment.
- Rollout stages, success metrics, guardrail metrics, and stop conditions are defined.
- Cleanup task exists for after 100% rollout and stabilization.

If no feature flag is used, state why progressive deployment alone is sufficient.

### Step 2: Progressive Deployment
Define the rollout plan:
- **Stage 1 — One-box**: Deploy to a single host. Bake for 30+ minutes. Watch error rates.
- **Stage 2 — Regional canary**: 5-10% of traffic in one region. Monitor key metrics.
- **Stage 3 — Regional full**: Full traffic in one region. Compare against control region.
- **Stage 4 — Global rollout**: Expand region by region with bake time between each.

For each stage define:
- Duration (minimum bake time)
- Success criteria (metrics that must stay green)
- Rollback trigger (automatic and manual conditions, including feature flag OFF when applicable)
- Approval gates (who approves promotion to next stage)

### Step 3: Pipeline Safety
Load `agents/ops-bar-raiser.md` and review the deployment plan through the operations bar raiser lens.

Ensure the deployment pipeline enforces:
- **Automated testing gate**: Unit, integration, and contract tests pass.
- **Static analysis gate**: No new critical/high findings.
- **Deployment hygiene**: Infrastructure-as-code, no manual changes.
- **Rollback capability**: One-click rollback to previous known-good version.
- **Alarm integration**: Pipeline halts if production alarms fire during bake.
- **Change management**: Deployment windows, freeze periods, emergency procedures.

## Key Principles

- Every deployment is a controlled experiment.
- Prefer boring deployments — surprise is the enemy.
- If you can't roll back in <5 minutes, you're not ready to deploy.
- Blast radius awareness: limit what breaks if something goes wrong.

## Output

Save to `docs/deployment/<feature-name>/`:
- `rollout-plan.md`
- `pipeline-config.md`

**Flow metrics.** `/deploy` owns two of the six events for the `deploy` phase — `phase_started` and
`phase_completed` — and appends each as one JSON line to `docs/bla-metrics.jsonl`: `phase_started` once the
change is classified as Medium or above, `phase_completed` once the artifacts above are saved. It owns no
gate event: the promotion approvals of Step 2 are the deployment's own gates, not gates over a BLA
artefact, and `/deploy` persists no review report, so `gate_approved`, `gate_rework` and
`review_blocking_finding` are not its to emit — no command emits an event another one owns (owner table in
`docs/flow-metrics.md`). **Emit only at Medium and above**; at Trivial and Small emit nothing. If the line
cannot be written — no writable tree, no `docs/` directory, the adopter declined — state in one line that
the flow measurement for this phase was not recorded, and **continue**: measurement never blocks a rollout
stage or a rollback.
<!-- MIRROR: This file mirrors .claude/commands/deploy.md. Do not edit directly — sync from the Claude version. -->

# Deploy — Progressive Deployment

Activate the **deploy** skill chain: `skills/feature-flag-lifecycle/` → `skills/progressive-deployment/` → `skills/pipeline-safety/`.

## Instructions

Help the user plan and execute a safe deployment strategy.

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
- **One-box**: Single host, bake 30+ min, watch error rates.
- **Regional canary**: 5-10% traffic in one region, monitor metrics.
- **Regional full**: 100% in one region, compare against control.
- **Global rollout**: Region by region with bake time between each.

For each stage define:
- Duration (minimum bake time)
- Success criteria (metrics that must stay green)
- Rollback trigger (automatic and manual, including feature flag OFF when applicable)
- Approval gates (who promotes to next stage)

### Step 3: Pipeline Safety
Load `agents/ops-bar-raiser.md` and review the deployment plan through the operations bar raiser lens.

Ensure the pipeline enforces:
- **Test gate**: Unit, integration, contract tests pass.
- **Static analysis**: No new critical/high findings.
- **IaC only**: No manual infrastructure changes.
- **Rollback**: One-click to previous known-good version.
- **Alarm integration**: Pipeline halts on production alarms during bake.
- **Change management**: Deployment windows, freezes, emergency procedures.

## Principles

- Every deployment is a controlled experiment.
- Prefer boring deployments — surprise is the enemy.
- If rollback takes >5 minutes, you're not ready to deploy.
- Blast radius awareness: limit damage from failures.

## Output

Save to `docs/deployment/<feature-name>/`:
- `rollout-plan.md`
- `pipeline-config.md`

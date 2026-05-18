# Deploy — Progressive Deployment

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

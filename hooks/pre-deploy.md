# Pre-Deploy Hook

## Purpose

Final safety checks before code reaches production. These gates run in the deployment pipeline after build and test succeed but before any production instance receives the new code. They verify the operational environment is ready to receive a deployment safely.

---

## Checks (in order)

### 1. Active Alarm Check

**What**: Query the alarm system for any active alarms on the target service.

**Behavior**:
- P1 (Critical) or P2 (High) active → **BLOCK deployment** (hard stop, no override without senior leadership approval)
- P3 (Medium) active → **WARN** (deployment allowed but requires deployer acknowledgment)
- P4 (Low) active → **INFO** (noted in deployment log, no action required)

**Why**: Deploying while alarms are active makes diagnosis harder. Is the problem from the existing alarm or the new deployment? You can't tell. Fix the alarm first, then deploy.

**Override**: P1/P2 override requires senior engineer approval + documented justification + mandatory post-deploy review.

---

### 2. Active Incident Check

**What**: Query incident management system for ongoing incidents involving this service or its critical dependencies.

**Behavior**:
- Active incident on this service → **BLOCK deployment**
- Active incident on critical dependency → **WARN** (deployer must confirm dependency is not related)

**Why**: Deploying during an incident adds variables. If the deployment makes things worse, it's harder to isolate. If the deployment is unrelated, it can wait until the incident is resolved.

---

### 3. Deployment Window Check

**What**: Verify current time is within the team's configured deployment window.

**Default windows**:
- Allowed: Monday-Thursday, 09:00-16:00 local time
- Warning: Friday 09:00-14:00 (allowed with acknowledgment)
- Blocked: Friday after 14:00, weekends, holidays, blackout periods

**Why**: Deployments outside business hours have longer detection times (no one watching) and slower response times (on-call is sleeping). Blackout periods protect during peak traffic events.

**Override**: Senior engineer approval + extended bake times (2x normal).

---

### 4. Rollback Target Verification

**What**: Confirm that a rollback target exists and is valid.

**Checks**:
- Previous known-good artifact exists in artifact store
- Previous artifact's health was verified (it was the active production artifact)
- Rollback mechanism is configured and functional
- Estimated rollback time calculated and acceptable (<5 minutes)

**Why**: If you can't rollback, you can't safely deploy. The ability to undo is what makes progressive deployment safe. Without a verified rollback target, you're making an irreversible change.

**Action on failure**: BLOCK. Fix rollback capability before deploying.

---

### 5. Capacity Check

**What**: Verify the fleet has sufficient capacity to perform a rolling deployment without dropping below minimum healthy instances.

**Checks**:
- Current fleet size - deployment batch size ≥ minimum healthy instances
- Current CPU/memory utilization allows for reduced fleet during rolling deploy
- Auto-scaling is configured and responsive (can scale up if needed)
- No other deployments to this fleet are in progress

**Why**: Rolling deployments temporarily reduce capacity. If you're already at 90% utilization with minimum fleet, taking instances out for deployment causes overload on remaining instances.

**Action on failure**: BLOCK. Scale up first, then deploy. Or reduce deployment batch size.

---

### 6. Dependency Health Check

**What**: Verify critical downstream dependencies are healthy before deploying.

**Checks**:
- Each critical dependency's health endpoint returns healthy
- Dependency latency is within normal range
- No active alarms on critical dependencies

**Why**: If a dependency is already degraded, your deployment may push it over the edge (increased traffic during deployment) or mask the dependency issue with your own changes.

**Behavior**:
- Critical dependency unhealthy → **WARN** (proceed with caution, explicit acknowledgment)
- Multiple dependencies unhealthy → **BLOCK**

---

### 7. Configuration Validation

**What**: Validate that all configuration for the target environment is present and syntactically correct.

**Checks**:
- All required environment variables defined
- Configuration files parse without errors
- Feature flag states are intentional (no accidentally-enabled flags)
- Database connection strings point to correct environment (not cross-env)
- Secret references resolve (secrets exist in secrets manager)

**Why**: Configuration errors are the #1 cause of deployment failures. Catching them before deployment prevents the deploy-fail-rollback-fix-redeploy cycle.

**Action on failure**: BLOCK with specific configuration error.

---

### 8. Database Migration Compatibility

**What**: If the deployment includes database schema changes, verify they are backward-compatible.

**Checks**:
- Migration can be applied without downtime
- Current running code works with new schema (forward compatibility)
- New code works with current schema (backward compatibility for rollback)
- Migration has been tested in staging/pre-prod
- Migration is reversible (or documented as irreversible with explicit approval)

**Why**: Database migrations are the riskiest part of many deployments. An incompatible migration that requires coordinated code+schema change creates a point where rollback is impossible.

**Action on failure**: BLOCK. Redesign migration for backward compatibility.

---

### 9. Change Size Assessment

**What**: Assess the size and risk of the change being deployed.

**Checks**:
- Number of files changed
- Lines of code added/modified
- Number of services/endpoints affected
- Whether the change touches critical paths (authentication, payment, data)

**Behavior**:
- Small change (≤100 lines, non-critical path) → Standard bake times
- Medium change (101-500 lines, or touches critical path) → Extended bake times (1.5x)
- Large change (>500 lines, or multiple critical paths) → Maximum bake times (2x) + active monitoring requirement

**Why**: Larger changes have higher probability of containing issues. Bake time should be proportional to risk.

---

### 10. Synthetic Canary Baseline

**What**: Verify that synthetic canary tests are passing BEFORE deployment, establishing a known-good baseline.

**Checks**:
- Synthetic canary suite has passed for the last 30 minutes
- Canary covers critical customer journeys
- Canary will continue running during and after deployment

**Why**: If canary is already failing before deployment, you can't use it to validate the deployment. You need a green baseline to detect deployment-caused degradation.

**Action on failure**: BLOCK. Fix canary or fix the issue canary is detecting.

---

## Gate Resolution

All BLOCK checks must pass before deployment proceeds. The pipeline visualizes each check's status:

```
✅ Alarm Check — No active alarms
✅ Incident Check — No active incidents
✅ Deployment Window — Within allowed window
✅ Rollback Target — Previous artifact verified
✅ Capacity Check — Fleet at 60% utilization, sufficient headroom
⚠️ Dependency Health — Service B p99 elevated (acknowledged by deployer)
✅ Configuration — All configs valid
✅ Database Migration — No migrations in this deploy
✅ Change Size — Small change, standard bake times
✅ Synthetic Canary — Green for 45 minutes

→ DEPLOYMENT APPROVED — Proceeding to One-Box stage
```

---

## Override Policy

- WARN checks: Deployer acknowledges and documents reason. No approval needed.
- BLOCK checks: Requires senior engineer approval + written justification.
- All overrides: Logged permanently. Reviewed in the recurring metrics review cadence. Pattern of overrides triggers pipeline improvement.
- Multiple BLOCK overrides in one deployment: Requires VP-level approval (this should almost never happen).

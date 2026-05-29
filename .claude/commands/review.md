# Review — Code Review Bar Raising

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

You are activating the **review** skill chain: `code-review-bar-raising` → `operational-readiness-review`.

## What to do

1. Read skills at `skills/code-review-bar-raising/` and `skills/operational-readiness-review/`.
2. Perform a comprehensive review of the code or system under examination.

### Step 1: Code Review (Bar Raising)
Review code against these dimensions:
- **Correctness**: Does it do what it claims? Edge cases handled?
- **Simplicity**: Is there a simpler way? Remove unnecessary abstractions.
- **Naming**: Are names precise and self-documenting?
- **Testing**: Are tests sufficient, meaningful, and maintainable?
- **Security**: Input validation, authz checks, secret handling?
- **Performance**: Obvious inefficiencies? Unbounded operations?
- **Operational readiness**: Logging, metrics, error handling, retries?
- **Documentation**: Would a new team member understand this in 6 months?

Provide feedback as:
- 🚫 **Must fix** — blocks merge (correctness, security, data loss risks)
- ⚠️ **Should fix** — strongly recommended (clarity, maintainability)
- 💡 **Consider** — optional improvements (style, alternative approaches)

### Step 2: Operational Readiness Review
Before production deployment, verify:
- Runbook exists for common failure scenarios
- Alarms fire before customers notice
- Rollback plan is documented and tested
- Load testing validates capacity assumptions
- Dependencies are understood and failure modes documented
- On-call team knows about the change

## Implementation Memory Capture

After the review is complete and findings are resolved, check whether any findings represent a **recurring pattern** (same finding across 2+ PRs, or the reviewer explicitly flags "this keeps happening"). If so:

1. Read `skills/implementation-memory/SKILL.md`.
2. Generate a self-reflection: "What recurring implementation mistake does this finding reveal? What rule would prevent it in future builds?"
3. Extract up to 2 candidate learnings.
4. Present candidates to the user for Accept / Reject / Edit (same format as `/build` semi-automatic trigger).
5. Apply admission checks and rejection rules before writing to `docs/implementation-memory.md`.

If no recurring pattern is identified, skip this step silently.

## Output

Save review findings to `docs/reviews/<feature-name>/`:
- `code-review.md` (findings and recommendations)
- `orr-checklist.md` (operational readiness status)
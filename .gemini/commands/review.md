<!-- MIRROR: This file mirrors .claude/commands/review.md. Do not edit directly — sync from the Claude version. -->

# Review — Code Review Bar Raising

Activate the **review** skill chain: `skills/code-review-bar-raising/` → `skills/operational-readiness-review/`.

## Instructions

Perform a comprehensive review of code and operational readiness.

### Step 1: Code Review (Bar Raising)
Review against these dimensions:
- **Correctness**: Does it do what it claims? Edge cases?
- **Simplicity**: Is there a simpler way?
- **Naming**: Precise and self-documenting?
- **Testing**: Sufficient, meaningful, maintainable?
- **Security**: Input validation, authz, secrets?
- **Performance**: Inefficiencies? Unbounded operations?
- **Observability**: Logging, metrics, error handling?
- **Documentation**: Understandable in 6 months?

Categorize feedback:
- 🚫 **Must fix** — blocks merge (correctness, security, data loss)
- ⚠️ **Should fix** — strongly recommended (clarity, maintainability)
- 💡 **Consider** — optional (style, alternatives)

### Step 2: Operational Readiness Review
Before production, verify:
- Runbook for common failure scenarios
- Alarms fire before customers notice
- Rollback plan documented and tested
- Load testing validates capacity
- Dependency failure modes documented
- On-call team briefed on the change

## Principles

- Review code like you'll be paged for it at 3 AM.
- Be kind, be specific, be constructive.
- The bar raiser's job: would I hire this code?

## Implementation Memory Capture

After findings are resolved, check for **recurring patterns** (same finding across 2+ reviews, or explicitly flagged as "this keeps happening"). If found:

1. Read `skills/implementation-memory/SKILL.md`.
2. Self-reflect: "What recurring mistake does this reveal? What rule prevents it?"
3. Extract up to 2 candidates. Present for Accept / Reject / Edit.
4. Apply admission checks before writing to `docs/implementation-memory.md`.

If no recurring pattern, skip silently.

## Output

Save to `docs/reviews/<feature-name>/`:
- `code-review.md`
- `orr-checklist.md`

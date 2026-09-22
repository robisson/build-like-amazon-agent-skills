# Review — Code Review Bar Raising

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

You are activating the **review** skill chain: `code-review-bar-raising` → `operational-readiness-review`.

## What to do

1. Read skills at `skills/code-review-bar-raising/` and `skills/operational-readiness-review/`.
2. Perform a comprehensive review of the code or system under examination.

Both steps below are gates, not commentary. A finding at canonical severity BLOCKING that is still open removes the option to approve and advance: the only remaining options are fix it, accept it with the risk recorded in the accepted-risk table, or pause. A review report without a parseable verdict block counts as BLOCKING. 🚫 **Must fix** is this command's spelling of BLOCKING — the mapping is in `AGENTS.md` → *One Severity Scale and One Verdict Scale*.

### Step 1: Code Review (Bar Raising)
Load `agents/code-review-bar-raiser.md` and review the code through the code review bar raiser lens.

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
Load `agents/ops-bar-raiser.md` and review the change through the operations bar raiser lens.

Before production deployment, verify:
- Runbook exists for common failure scenarios
- Alarms fire before customers notice
- Rollback plan is documented and tested
- Load testing validates capacity assumptions
- Dependencies are understood and failure modes documented
- On-call team knows about the change

## Finding format

Every finding in a persisted report is written in this one shape:

`[SEVERITY] file:line — <concrete condition> → <observable wrong result> → <required fix>`

- The admission rule is **no anchor, no entry**: a finding with no `file:line` anchor — `file:section` for a document — does not enter the report. If you cannot point at the line, you have a suspicion to go investigate, not a finding to report.
- **ID** — `F-01`, `F-02`, … assigned in the order found and stable for the life of the report. A re-review reuses the ID and never renumbers, because the ID is how the fix, the re-review and any accepted-risk row all refer to the same thing.
- **Impact** — what breaks in production, in one line. This is the golden rule's answer, written down.
- **Confidence** — `high`, `medium` or `low`: how sure you are that the condition actually holds.
- **Minimal fix** — the smallest change that removes the condition, not the redesign you would prefer.
- **Status** — one of `OPEN`, `FIXED`, `ACCEPTED-WITH-RISK`, `NOT-REPRODUCIBLE`, `SUPERSEDED`, defined in `skills/code-review-bar-raising/SKILL.md` → *Finding lifecycle in a persisted report*.

`[SEVERITY]` is a slot, not a literal: write the label this surface already uses and let the canonical level appear in the report's `Findings:` counts line (`AGENTS.md` → *One Severity Scale and One Verdict Scale*).

Order the findings by impact. The rule is literal: **priority is impact, never confidence.** A `low`-confidence finding about silent data loss outranks a `high`-confidence finding about a name. Confidence tells the author how hard to look before acting; it never demotes a finding and is never a reason to leave one out.

**IDs and the lifecycle apply only to a report persisted to disk** — the Medium and Large ceremony levels, where a file exists for a later review to update. An inline review of a Trivial change carries no IDs and no lifecycle: there is no file, so there is nothing to renumber and nothing to supersede. The anchor rule and the golden rule still apply; they cost nothing.

🚫 **Must fix**, ⚠️ **Should fix** and 💡 **Consider** go in the `[SEVERITY]` slot. Both outputs of this command — `docs/reviews/<feature-name>/code-review.md` and `orr-checklist.md` — are persisted reports, so both carry IDs and the lifecycle, and a second review of the same feature updates them instead of overwriting them.

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
---
name: Implementation Memory
description: Internal /build flow mechanism that maintains fixed-size procedural memory of durable implementation-quality lessons.
leadership_principles:
  - Insist on the Highest Standards
  - Learn and Be Curious
  - Ownership
---

# Implementation Memory

## Overview

Implementation memory is a compact, fixed-size set of rules that improves future `/build` executions. It captures durable lessons from completed builds, code review feedback, test failures, and user feedback, then applies only the relevant lessons to later implementation work.

This is procedural memory, not history. It stores rules for how to implement better next time. It does not store product context, design history, changelog entries, ADRs, raw retrospectives, PR transcripts, or conversation logs.

This mechanism is harness-agnostic by design. It uses a plain markdown file in the repo (`docs/implementation-memory.md`) intentionally. It is not tied to any agent's native memory system. Any AI agent that can read markdown and follow instructions can consume and update it.

This is an internal flow mechanism. Users do not invoke it as a slash command or choose it as a standalone workflow. Existing build commands and build-oriented assistant rules call it automatically at the defined points in the `/build` flow.

## Capture Points

Implementation memory can be fed from multiple workflow stages — not only `/build`:

| Source | When | What to extract |
|--------|------|-----------------|
| `/build` (post-implementation review) | After PASSED WITH FIXES NEEDED or user validation | Procedural lessons from fix tasks, debug cycles, review findings |
| `/review` (code review) | After review feedback is resolved | Recurring review findings that apply beyond one PR |
| `/learn` (COE) | After corrective actions are defined | Operational lessons that should influence future implementation |

All sources use the same Quality Memory Review process, admission checks, and rejection rules.

## Internal Flow Hooks

Use this mechanism in these places:

1. **Before `/build` task execution**: read the current spec/tasks first, then select only active memory rules whose `Applies when` field AND `Tags`/`File patterns` match the current work.
2. **After implementation review (semi-automatic trigger)**: when the verdict is PASSED WITH FIXES NEEDED, the agent MUST automatically extract up to 2 candidate learnings from the fix findings and present them to the user for Accept / Reject / Edit. This is the primary memory population path. When the verdict is PASSED, prompt the user to test the delivered behavior and bring back failures or feedback.
3. **After user validation or explicit request**: run a Quality Memory Review using implementation results, implementation review, test/debug feedback, and user feedback to decide whether memory should be updated.
4. **After `/review` findings are resolved**: if the review surfaced recurring patterns (same finding across 2+ PRs or explicitly flagged as "this keeps happening"), extract candidates and present for Accept / Reject / Edit.
5. **After `/learn` corrective actions**: if a COE produces an implementation-level corrective action (not an org/process action), extract a candidate and present for Accept / Reject / Edit.
6. **Periodic nudge**: after 3 builds without a memory update (tracked via `Last build without update` counter at the bottom of the memory file), include in the end-of-build summary: "You have had N builds without memory update. Would you like a quick Quality Memory Review?"

Do not use this skill to replace requirements, design documents, ADRs, release notes, PR/FAQ, postmortems, or review artifacts.

## Canonical Artifact

The project-level memory artifact is:

```text
docs/implementation-memory.md
```

If the file does not exist before a build, continue without memory guardrails. After the build, create it only when at least one candidate learning passes the admission bar. A repository may also keep an empty canonical file with the required structure so future builds have a stable location.

## Memory Limits

The memory is intentionally small:

- Maximum 12 active rules.
- Maximum 120 words per active rule.
- Maximum 2 candidate learnings extracted per Quality Memory Review.
- Rewrite the whole file when updating; never append a chronological build log.
- Prefer rules that prevent bugs, review rework, security issues, rollout failures, weak tests, or operational gaps.

## Active Rule Format

Every active rule must use this shape:

```markdown
### IM-XXX: [Short rule name]
Tags: [api, error-handling, testing, infra, ui, data-pipeline, security, observability, workflow, ...]
File patterns: [optional glob patterns, e.g. src/api/**, tests/integration/**]
Applies when: [Spec/component/risk conditions where this rule is relevant.]
Rule: [Actionable implementation behavior.]
Avoid: [Specific behavior to avoid.]
Evidence: [Review feedback | user feedback | test failure | build defect | repeated pattern.]
Impact: [Critical | High | Medium]
Confidence: [Proven (prevented issues) | Established (applied successfully) | New (just added)]
Hit count: [N — number of builds where this rule was selected and applied]
Prevented: [N — number of times this rule demonstrably prevented an issue]
Created: [YYYY-MM-DD]
Last used: [YYYY-MM-DD]
Builds on: [[IM-YYY]] (optional — reference to a related/prerequisite rule)
```

Use stable IDs. When removing a rule, do not renumber unrelated rules unless the file is being deliberately compacted for readability.

## Pre-Build Selection

Before implementation starts:

1. Read the current `specs/<slice-name>/requirements.md`, `design.md`, `tasks.md`, and `coherence-review.md` if present.
2. Read `docs/implementation-memory.md` if it exists.
3. Select active rules using this multi-signal matching (a rule is selected if ANY signal matches):
   - **Tags match**: rule tags overlap with the current spec's domain/technology areas.
   - **File patterns match**: the spec's tasks touch files matching the rule's glob patterns.
   - **Applies when matches**: the LLM judges the prose description to be relevant to the current spec, task, component, dependency, or risk profile.
4. Convert selected rules into implementation guardrails, test checks, or review checks.
5. Ignore unmatched rules. They are not requirements for the current build.
6. Increment `Hit count` for each selected rule.

Memory rules never override approved requirements, design, tasks, or coherence-review action items.

## Semi-Automatic Trigger (Primary Population Path)

When the implementation review verdict is **PASSED WITH FIXES NEEDED**, the agent does not wait for the user to request memory update. Instead:

1. Generate a structured self-reflection (2-3 sentences): "What went wrong? Why? What would have prevented it?"
2. Use the self-reflection (not the raw findings) to extract up to 2 candidate learnings.
3. Present candidates to the user in this format:

```text
Memory candidates extracted from this build:

[1] IM-00X: [Short rule name]
    Tags: [...]
    Applies when: [...]
    Rule: [...]
    Avoid: [...]

[2] IM-00Y: [Short rule name]
    Tags: [...]
    Applies when: [...]
    Rule: [...]
    Avoid: [...]

Actions: [Accept all] [Accept 1 only] [Accept 2 only] [Edit before saving] [Reject all]
```

4. Apply the user's decision. If accepted, run admission checks and write.
5. If rejected, do not ask again for this build.

This ensures memory is populated even when users forget to ask for Quality Memory Review.

## Post-Review User Validation Handoff

After implementation review is written (for PASSED verdicts without fix tasks), do not treat the model review as the final validation of product behavior. The final build response must explicitly hand the implementation to the user for real testing and invite a debug loop.

Use this shape:

```text
Implementation is complete and implementation review has run. Please test the delivered behavior in the product. If anything is wrong, bring me the failure, error, or feedback and we will debug it together until it is OK. After you consider the implementation validated, ask me to run Quality Memory Review and I will capture only durable learnings worth keeping.
```

If no user validation/debug feedback is available yet, skip memory update and report: `Implementation memory skipped: waiting for user validation/debug feedback and an explicit Quality Memory Review request.`

## Quality Memory Review

Run this after the user asks for it, confirms the implementation is validated, or when the semi-automatic trigger fires. Use implementation verification, implementation-review findings, user test results, debug fixes, and final user feedback as evidence:

1. **Self-reflection first** — Before extracting candidates, generate a 2-3 sentence structured reflection: "What went wrong or almost went wrong? Why did it happen? What general rule would have prevented it?" This reflection is the input for extraction, not the raw findings.
2. Extract at most 2 candidate learnings from the reflection.
3. Reject any candidate that fails the rejection rules.
4. Add or merge only candidates that pass at least 2 admission checks.
5. Merge duplicates into existing active rules instead of adding near-copies.
6. If the memory would exceed 12 active rules, prune weaker rules before writing.
7. Rewrite the whole memory file if an update is warranted.
8. Leave memory unchanged when no candidate meets the bar.
9. Reset the `Builds without update` counter to 0 when memory is updated.

The Quality Memory Review response must state whether implementation memory was updated, unchanged, or skipped. When it changes:
- Summarize the rule IDs added, merged, or removed.
- Show the diff (what was added/changed/removed) directly in the response so the user sees changes without opening the file.

When it is skipped, state why.

## Admission Checks

A candidate learning must pass at least 2 of these checks:

- Avoids a likely future bug.
- Avoids repeated review rework.
- Improves tests, security, operations, or rollout safety.
- Applies beyond one feature.
- Corrects a recurring agent tendency.

## Rejection Rules

Reject candidates that are:

- Product requirements.
- Feature-specific facts.
- Architecture decisions or ADR content.
- Release notes or changelog entries.
- Raw retrospectives, raw review transcripts, or raw user quotes.
- Secrets, credentials, customer data, private incident details, or proprietary feedback.
- Environment-specific operational facts that will become stale.
- Stylistic preferences without quality impact.

## Staleness and Decay

Rules decay over time. The following thresholds guide pruning:

- **Stale threshold**: a rule not selected (Last used not updated) for >90 days is a candidate for pruning.
- **Inactive threshold**: a rule not selected in 5 consecutive Quality Memory Reviews is a candidate for pruning.
- **Low-confidence, low-hit**: a rule with Confidence: New and Hit count: 0 after 3 builds is a candidate for pruning.

Staleness alone does not trigger automatic removal. The agent flags stale rules during Quality Memory Review and asks the user: "Rule IM-XXX has not been used in N days. Keep or remove?"

## Merge, Conflict, and Pruning Rules

When a candidate overlaps an existing rule, merge it into the existing rule and update `Evidence`, `Impact`, `Confidence`, `Hit count`, or `Last used` if warranted.

When rules conflict, keep the more specific and higher-impact rule. If the conflict is ambiguous, leave memory unchanged and report the conflict in the final response.

When pruning is required, remove in this order:

1. Rules that exceed the stale threshold (>90 days unused).
2. Rules that are too specific to one feature.
3. Rules duplicated by requirements, design, ADRs, or repository docs.
4. Rules with Confidence: New and Hit count: 0.
5. Low-impact or mostly stylistic rules.
6. Rules superseded by a stronger rule.

## Rule Composition

Rules may reference other rules using the `Builds on: [[IM-YYY]]` field. This indicates:

- The referenced rule should also be selected when the referencing rule is selected.
- Together they form a composite pattern that captures a more complex lesson without exceeding the 120-word limit per rule.
- When pruning, if a rule that others build on is removed, check whether dependent rules still make sense alone.

## Domain-Scoped Memory (for large projects)

For projects with distinct domains (e.g., monorepos), the memory may be split:

```text
docs/implementation-memory.md              # global (max 12 rules)
docs/implementation-memory-<domain>.md     # domain-scoped (max 6 rules each)
```

Pre-build selection loads the global file plus the domain file matching the current spec's primary domain. Domain files follow the same format and rules but with a reduced cap of 6 rules.

When to split: only when the global memory is consistently full (12 rules) AND rules from different domains are competing for slots. Do not split preemptively.

## Manual Scenarios

| Scenario | Expected behavior |
|---|---|
| No memory file exists | Build proceeds; Quality Memory Review may create memory if strong candidates exist. |
| Memory has 12 rules and 2 strong candidates | Merge or remove weaker rules; final memory still has at most 12 rules. |
| Candidate is a product requirement | Reject candidate. |
| Candidate duplicates an existing rule | Merge/refine existing rule instead of duplicating. |
| Current spec matches no active rules | Select no memory guardrails. |
| Review/user feedback is unavailable (PASSED verdict) | Skip memory update and ask the user to test/debug before requesting Quality Memory Review. |
| PASSED WITH FIXES NEEDED verdict | Semi-automatic trigger fires: extract candidates, present to user for Accept/Reject/Edit. |
| User validates after debug and asks for Quality Memory Review | Extract up to 2 durable learnings from the full implementation/review/test/debug cycle. |
| 3 builds without memory update | Nudge in end-of-build summary. |
| Rule IM-003 not used in 90+ days | Flag during next Quality Memory Review; ask user to keep or remove. |
| `/review` finds recurring pattern | Extract candidate and present for Accept/Reject/Edit. |
| `/learn` COE has implementation-level action | Extract candidate and present for Accept/Reject/Edit. |

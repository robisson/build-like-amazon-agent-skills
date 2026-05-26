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

This is an internal flow mechanism. Users do not invoke it as a slash command or choose it as a standalone workflow. Existing build commands and build-oriented assistant rules call it automatically at the defined points in the `/build` flow.

## Internal Flow Hooks

Use this mechanism in three places only:

1. **Before `/build` task execution**: read the current spec/tasks first, then select only active memory rules whose `Applies when` field matches the current work.
2. **After implementation review**: prompt the user to test the implemented behavior, bring back failures or feedback, and continue debugging with the agent until the implementation is accepted.
3. **After user validation or explicit request**: run a Quality Memory Review using implementation results, implementation review, test/debug feedback, and user feedback to decide whether memory should be updated.

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
Applies when: [Spec/component/risk conditions where this rule is relevant.]
Rule: [Actionable implementation behavior.]
Avoid: [Specific behavior to avoid.]
Evidence: [Review feedback | user feedback | test failure | build defect | repeated pattern.]
Impact: [Critical | High | Medium]
Last used: [YYYY-MM-DD]
```

Use stable IDs. When removing a rule, do not renumber unrelated rules unless the file is being deliberately compacted for readability.

## Pre-Build Selection

Before implementation starts:

1. Read the current `specs/<slice-name>/requirements.md`, `design.md`, `tasks.md`, and `coherence-review.md` if present.
2. Read `docs/implementation-memory.md` if it exists.
3. Select only active rules whose `Applies when` field matches the current spec, task, component, dependency, or risk profile.
4. Convert selected rules into implementation guardrails, test checks, or review checks.
5. Ignore unmatched rules. They are not requirements for the current build.

Memory rules never override approved requirements, design, tasks, or coherence-review action items.

## Post-Review User Validation Handoff

After implementation review is written, do not treat the model review as the final validation of product behavior. The final build response must explicitly hand the implementation to the user for real testing and invite a debug loop.

Use this shape:

```text
Implementation is complete and implementation review has run. Please test the delivered behavior in the product. If anything is wrong, bring me the failure, error, or feedback and we will debug it together until it is OK. After you consider the implementation validated, ask me to run Quality Memory Review and I will capture only durable learnings worth keeping.
```

If no user validation/debug feedback is available yet, skip memory update and report: `Implementation memory skipped: waiting for user validation/debug feedback and an explicit Quality Memory Review request.`

## Quality Memory Review

Run this only after the user asks for it or confirms the implementation is validated. Use implementation verification, implementation-review findings, user test results, debug fixes, and final user feedback as evidence:

1. Extract at most 2 candidate learnings.
2. Reject any candidate that fails the rejection rules.
3. Add or merge only candidates that pass at least 2 admission checks.
4. Merge duplicates into existing active rules instead of adding near-copies.
5. If the memory would exceed 12 active rules, prune weaker rules before writing.
6. Rewrite the whole memory file if an update is warranted.
7. Leave memory unchanged when no candidate meets the bar.

The Quality Memory Review response must state whether implementation memory was updated, unchanged, or skipped. When it changes, summarize the rule IDs added, merged, or removed. When it is skipped, state why.

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

## Merge, Conflict, and Pruning Rules

When a candidate overlaps an existing rule, merge it into the existing rule and update `Evidence`, `Impact`, or `Last used` if warranted.

When rules conflict, keep the more specific and higher-impact rule. If the conflict is ambiguous, leave memory unchanged and report the conflict in the final response.

When pruning is required, remove in this order:

1. Rules that are too specific to one feature.
2. Rules duplicated by requirements, design, ADRs, or repository docs.
3. Stale rules that have not affected recent builds.
4. Low-impact or mostly stylistic rules.
5. Rules superseded by a stronger rule.

## Manual Scenarios

| Scenario | Expected behavior |
|---|---|
| No memory file exists | Build proceeds; Quality Memory Review may create memory if strong candidates exist. |
| Memory has 12 rules and 2 strong candidates | Merge or remove weaker rules; final memory still has at most 12 rules. |
| Candidate is a product requirement | Reject candidate. |
| Candidate duplicates an existing rule | Merge/refine existing rule instead of duplicating. |
| Current spec matches no active rules | Select no memory guardrails. |
| Review/user feedback is unavailable | Skip memory update and ask the user to test/debug before requesting Quality Memory Review. |
| User validates after debug and asks for Quality Memory Review | Extract up to 2 durable learnings from the full implementation/review/test/debug cycle. |

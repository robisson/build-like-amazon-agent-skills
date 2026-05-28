# Implementation Quality Memory

Purpose: Fixed-size procedural memory for implementation quality. This is not product context, design history, changelog, ADR, or raw retrospective storage. This mechanism is harness-agnostic — any AI agent that can read markdown can consume and update it.

Limits:
- Max 12 active rules.
- Max 120 words per rule.
- Rewrite whole file after each build update.
- Prefer rules that prevent bugs, review rework, security issues, rollout failures, weak tests, or operational gaps.

Update policy:
- Add or merge at most 2 candidate learnings per Quality Memory Review.
- Semi-automatic trigger: after PASSED WITH FIXES NEEDED, extract candidates and present to user for Accept/Reject/Edit.
- Manual trigger: run Quality Memory Review after user validation/debug feedback or an explicit user request.
- Nudge: after 3 builds without update, remind user in end-of-build summary.
- Add or merge a candidate only when it passes at least 2 admission checks from `skills/implementation-memory/SKILL.md`.
- Reject product requirements, feature facts, architecture decisions, changelog entries, raw feedback, secrets, customer data, and one-off details.
- If adding a rule would exceed 12 active rules, merge or remove weaker rules before writing.
- Stale threshold: rules unused for >90 days are candidates for pruning during Quality Memory Review.

Capture sources: `/build` (post-implementation review), `/review` (recurring findings), `/learn` (COE implementation-level actions).

## Active Rules

### IM-001: Produce Required Workflow Artifacts
Tags: [workflow, artifact-generation, build-output]
File patterns: specs/**/implementation-review.md, specs/**/coherence-review.md
Applies when: Executing repository workflows that define review, coherence, implementation-review, or other persisted artifacts.
Rule: Generate the required artifact file in the expected path before treating the workflow step as complete.
Avoid: Replacing an artifact-producing workflow step with a chat-only summary.
Evidence: User feedback.
Impact: High
Confidence: Established
Hit count: 2
Prevented: 1
Created: 2026-05-26
Last used: 2026-05-26

### IM-002: Keep Workflow Mechanisms Native And Internal
Tags: [workflow, skill-design, internal-mechanism]
File patterns: skills/**/*.md, .claude/commands/*.md
Applies when: Implementing a skill, command, Markdown workflow, or internal quality mechanism.
Rule: Describe documentation-only contracts as workflow behavior, tables, templates, and verification checks; integrate internal mechanisms at the existing workflow step where they belong.
Avoid: Inventing runtime code interfaces or exposing internal mechanisms as new user-facing slash commands unless explicitly requested.
Evidence: User feedback.
Impact: High
Confidence: Established
Hit count: 2
Prevented: 1
Created: 2026-05-26
Last used: 2026-05-26

## Rule Shape

Use this shape when adding an active rule:

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

## Metadata

Builds without update: 0
Last Quality Memory Review: 2026-05-26

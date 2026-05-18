# Contributing to Amazon Agent Skills

Thank you for your interest in contributing! This project thrives on community contributions — whether it's a new skill, an improvement to an existing one, or a bug fix in the documentation.

## Table of Contents

- [Getting Started](#getting-started)
- [Skill Anatomy](#skill-anatomy)
- [Writing a New Skill](#writing-a-new-skill)
- [Rationalizations Table](#rationalizations-table)
- [Verification Checkpoints](#verification-checkpoints)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
- [Code of Conduct](#code-of-conduct)

## Getting Started

1. **Fork** this repository
2. **Clone** your fork locally
3. **Create a branch** for your contribution: `git checkout -b skill/my-new-skill`
4. **Write** your skill following the anatomy below
5. **Test** your skill with at least one AI agent (Claude, Cursor, Gemini, etc.)
6. **Submit** a pull request

## Skill Anatomy

Every skill follows a consistent structure that AI agents can parse reliably:

```markdown
---
name: skill-name
command: /command
phase: working-backwards | design | build | deploy | operate | learn | meta
description: One-line description of what this skill does
bar-raisers:
  - persona-name
triggers:
  - natural language trigger
  - another trigger phrase
---

# Skill Title

## Purpose

Why this skill exists and what outcome it produces.

## Context Assessment

How to determine if this skill applies to the current situation.
Include decision criteria for two-way vs one-way doors.

## Process

### Step 1: [Step Name]

Detailed instructions for this step.

**Inputs:**
- What information is needed

**Outputs:**
- What this step produces

**Decision Point:**
- Criteria for proceeding vs. iterating

### Step 2: [Step Name]

...continue for all steps...

## Verification Checkpoints

| Checkpoint | Criteria | Blocker? |
|-----------|----------|----------|
| ... | ... | Yes/No |

## Rationalizations

| Step | Rationale | What Happens If Skipped |
|------|-----------|------------------------|
| ... | ... | ... |

## Examples

### Good Example
...

### Anti-pattern
...

## Bar Raiser Questions

Questions the designated bar raiser will ask at review:
- ...
```

## Writing a New Skill

### 1. Identify the Workflow

A good skill encodes a **specific, repeatable engineering workflow** — not general advice. Ask yourself:

- Can I describe this as a series of concrete steps?
- Does skipping a step lead to measurable negative outcomes?
- Would two senior engineers following this produce similar results?
- Is this workflow used repeatedly across different projects?

### 2. Choose the Phase

Map your skill to the lifecycle phase where it primarily operates:

| Phase | Focus | Examples |
|-------|-------|---------|
| Working Backwards | Customer problem → Solution definition | PR/FAQ, customer interview, idea validation |
| Design | Architecture and system design | Design review, API design, data modeling |
| Build | Implementation and code quality | Coding standards, testing, code review |
| Deploy | Getting code to production safely | Progressive deployment, feature flags |
| Operate | Running production systems | Runbooks, on-call, capacity planning |
| Learn | Learning from production | COE, metrics review, retrospectives |
| Meta | Skills about skills | Skill authoring, skill composition |

### 3. Write the Process

Each step should be:

- **Concrete**: An agent can execute it without interpretation
- **Verifiable**: There's a clear way to check if it was done correctly
- **Rationalized**: The "why" is documented alongside the "what"
- **Bounded**: Has explicit inputs, outputs, and decision criteria

### 4. Add Decision Frameworks

For any point where judgment is required, provide explicit criteria:

```markdown
**Decision: Full design review vs. lightweight review**

Use full design review when:
- Change affects more than 2 services
- Change introduces a new data store
- Change modifies a public API contract
- Change affects authentication/authorization flow

Use lightweight review when:
- Change is contained within a single service
- Change doesn't modify external contracts
- Change is easily reversible (two-way door)
```

### 5. Include Anti-patterns

Show what the skill prevents, not just what it produces. This helps agents recognize when they're drifting off course.

## Rationalizations Table

Every major step MUST include a rationalization entry. This is critical because:

1. **Agents optimize** — without rationale, they'll skip steps that seem redundant
2. **Context matters** — explaining "why" helps agents apply judgment appropriately
3. **Trust building** — engineers following the skill need to understand the reasoning

Format:

| Step | Rationale | What Happens If Skipped |
|------|-----------|------------------------|
| Write press release before solution | Forces clarity on customer value before falling in love with a technical approach | Teams build solutions looking for problems; scope creep; unclear success criteria |
| Security bar raiser review | Catches threat model gaps before implementation where fixes are 10-100x more expensive | Vulnerabilities ship to production; retrofit security is architecturally painful |
| Progressive deployment with canary | Limits blast radius of defects to a small percentage of traffic | Full fleet deployments turn bugs into outages; rollback doesn't help if 100% of customers were impacted |

## Verification Checkpoints

Checkpoints define what "done" means for each phase. They can be:

- **Blocking** (Yes): Must pass before proceeding. Used for one-way doors and safety-critical steps.
- **Non-blocking** (No): Should be checked but won't halt progress. Used for best practices that can be addressed later.

```markdown
## Verification Checkpoints

| Checkpoint | Criteria | Blocker? |
|-----------|----------|----------|
| Customer problem validated | At least 3 data points confirming the problem exists | Yes |
| Press release reviewed | At least one stakeholder has read and provided feedback | Yes |
| Solution is reversible | Deployment can be rolled back within 5 minutes | Yes |
| Documentation updated | README and runbooks reflect the change | No |
| Metrics dashboard created | Key metrics are visible and alarmed | No |
```

## Pull Request Process

1. **Title**: `[phase] Add skill-name skill` (e.g., `[build] Add dependency-audit skill`)
2. **Description**: Include:
   - What workflow this skill encodes
   - Why it belongs in this project (ties to Amazon methodology)
   - How you tested it (which agent, what scenario)
3. **Checklist**:
   - [ ] Skill follows the anatomy structure
   - [ ] All steps have rationalizations
   - [ ] Verification checkpoints are defined
   - [ ] At least one example and one anti-pattern included
   - [ ] Bar raiser questions are specified
   - [ ] Tested with at least one AI agent
4. **Review**: A maintainer will review for:
   - Consistency with existing skills
   - Clarity and executability of instructions
   - Appropriate scope (not too broad, not too narrow)
   - Correct phase classification

## Style Guide

### Language

- Write in **imperative mood** for instructions ("Write the press release", not "You should write the press release")
- Use **second person** sparingly — prefer direct instructions
- Be **precise** — "Review the API contract" not "Think about the API"
- Avoid **hedging** — "Do X" not "Consider doing X" (unless it's genuinely optional)

### Formatting

- Use ATX-style headers (`#`, `##`, `###`)
- Use tables for structured data (checkpoints, rationalizations)
- Use code blocks for examples and templates
- Use bold for key terms on first introduction
- Use bullet lists for criteria and checklists
- Keep lines under 120 characters where possible

### Naming

- Skill files: `phase-name.md` (e.g., `build-review.md`, `deploy-progressive.md`)
- Commands: Short, memorable, verb-based (e.g., `/deploy`, `/review`, `/learn`)
- Personas: `[Adjective] Bar Raiser` (e.g., "Security Bar Raiser")

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to uphold a welcoming, inclusive, and respectful environment.

### Our Standards

- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy toward other community members

### Enforcement

Instances of unacceptable behavior may be reported to the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

---

Thank you for helping make AI agents better engineers. Every skill you contribute helps thousands of developers ship better software, faster and safer.

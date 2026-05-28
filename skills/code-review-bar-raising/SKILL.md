---
name: Raising the Bar in Code Review
description: Applying Amazon's raise-the-bar principle to every code review. What reviewers look for — clarity, correctness, design, reuse, operational readiness. "Ship It" means the change raises or maintains the quality bar.
leadership_principles:
  - Insist on the Highest Standards
  - Earn Trust
  - Learn and Be Curious
---

## Overview

Raising the Bar in Code Review applies Amazon's raise-the-bar principle to software changes. This is not a special role or a designated reviewer. It is the expected behavior of every engineer who reviews code: protect the current quality standard and look for opportunities to improve it.

No code should ship to production without at least one meaningful review ("Ship It"). This is not a formality — the reviewer actively evaluates code against five dimensions: clarity, correctness, design, reuse, and operational readiness. A reviewer who rubber-stamps code is lowering the bar.

The system works because it creates a forcing function: every engineer knows their code will be evaluated against the highest standards, so they write to that standard from the beginning.

## When to Use

- Every code change before it merges to the main branch
- Design decisions that manifest in code structure
- Infrastructure changes (Terraform, CDK, CloudFormation)
- Configuration changes that affect production behavior
- Database migrations and schema changes
- Test additions or modifications

## Agent Persona

Load `agents/code-review-bar-raiser.md` for code review. Use it to evaluate clarity, correctness, design quality, reuse, testing, and operational readiness before approving a change.

## Amazon Context

Amazon's raise-the-bar principle is simple: important decisions should improve the standard over time, not merely avoid obvious failure. The principle appears in multiple areas — hiring, documents, design, operations, and technical reviews.

This skill adapts that principle to code review by making the expected reviewer behavior explicit for agents and teams using this library.

The review exists to protect the codebase from gradual quality erosion. Delivery pressure must never become the measure of review quality. An approval that lowers the bar is a failure of the process.

## The Process

### 1. Author Responsibilities (Before Requesting Review)

Before marking a PR for review, the author must:

- [ ] Self-review the diff (read your own code as if seeing it for the first time)
- [ ] Verify all tests pass and coverage hasn't decreased
- [ ] Write a clear PR description explaining:
  - **What** changed and **why**
  - **How** to test it (manually, if applicable)
  - **Risk** level and rollback plan
  - **Dependencies** or ordering constraints
- [ ] Keep the PR focused (one logical change, < 400 lines preferred)
- [ ] Respond to pre-existing lint/style issues in the changed files
- [ ] Link to the relevant design document or ticket

### 2. The Five Dimensions of Review

Reviewers evaluate every PR against these dimensions:

#### Clarity
> "Can a new team member understand this code without additional context?"

- [ ] Names are descriptive and consistent (variables, functions, classes)
- [ ] Complex logic has explanatory comments (why, not what)
- [ ] Abstractions have clear responsibilities
- [ ] No clever tricks that sacrifice readability for brevity
- [ ] Function length is reasonable (< 30 lines for most functions)
- [ ] Code reads top-to-bottom without jumping around

#### Correctness
> "Does this code do what it claims to do, in all cases?"

- [ ] Happy path works correctly
- [ ] Edge cases handled (null, empty, max values, concurrent access)
- [ ] Error conditions produce appropriate responses
- [ ] Thread safety considered (if applicable)
- [ ] No off-by-one errors in loops or boundaries
- [ ] Tests actually verify the claimed behavior (not just exercising code)
- [ ] No silent data loss or truncation

#### Design
> "Is the architecture appropriate for the problem and the system?"

- [ ] Follows established patterns in the codebase
- [ ] Appropriate level of abstraction (not over- or under-engineered)
- [ ] Dependencies flow in the right direction
- [ ] New interfaces are minimal and extensible
- [ ] Changes are backward-compatible unless explicitly versioned
- [ ] Separation of concerns is maintained
- [ ] SOLID principles applied where relevant

#### Reuse
> "Does this leverage existing code and create reusable components?"

- [ ] No reinventing existing utilities (checked internal libraries)
- [ ] Shared logic extracted to appropriate level (util, library, service)
- [ ] New utilities are generic enough for reuse
- [ ] DRY principle applied in production code (not tests)
- [ ] Common patterns use established team conventions

#### Operational Readiness
> "Can we operate this code in production at 3 AM?"

- [ ] Metrics emitted for new code paths (latency, errors)
- [ ] Structured logging with appropriate detail
- [ ] Feature flags for behavioral changes
- [ ] Graceful degradation for new dependencies
- [ ] Timeout and retry configuration present
- [ ] Alarms defined for new failure modes
- [ ] Rollback strategy is clear and tested
- [ ] No hardcoded values that should be configuration

### 3. Review Workflow

```
Author submits PR
       │
       ▼
Reviewer evaluates the change as a quality gate
       │
       ▼
First pass: Architecture and design concerns
       │
       ├── Major concerns? → Block with explanation, schedule discussion
       │
       └── No major concerns → Detailed review of all 5 dimensions
                │
                ▼
       Comments posted (categorized by severity)
                │
                ▼
       Author addresses feedback
                │
                ▼
       Reviewer re-reviews changes
                │
                ├── Still has issues → Another round (max 2-3 rounds)
                │
                └── Satisfied → "Ship It" ✅
```

### 4. Comment Severity Levels

Reviewers categorize their feedback:

| Prefix | Meaning | Author Action |
|--------|---------|---------------|
| `[BLOCKING]` | Must fix before merge. Correctness or operational issue. | Fix required. |
| `[IMPORTANT]` | Should fix. Design or clarity issue. | Fix or explain why not. |
| `[NIT]` | Minor style or preference. Nice to have. | Fix if easy, skip if not. |
| `[QUESTION]` | Clarification needed. Might reveal an issue. | Answer in comment or code. |
| `[PRAISE]` | Particularly good code. Worth calling out. | Enjoy. Keep doing this. |

### 5. When to Escalate or Discuss

- Fundamental design disagreement → Schedule a focused discussion
- PR too large to review effectively → Ask author to split
- Cross-team impact → Pull in a reviewer from the affected team
- Performance-critical path → Request benchmark data
- Security-sensitive change → Include security review

### 6. Review Decision Framework

```
┌─────────────────────────────────────────────────────────┐
│ "Ship It" means:                                         │
│                                                          │
│  ✅ I would be comfortable being paged at 3 AM           │
│     for an issue in this code                            │
│  ✅ I can explain what this code does to someone who     │
│     hasn't seen it                                       │
│  ✅ The tests give me confidence the code is correct     │
│  ✅ The operational instrumentation will detect problems │
│  ✅ This code raises (or at minimum maintains) our bar   │
│                                                          │
│ "Ship It" does NOT mean:                                 │
│                                                          │
│  ❌ This code is perfect                                 │
│  ❌ I would have written it exactly this way             │
│  ❌ There are zero possible improvements                 │
│  ❌ I understand every line in detail                    │
└─────────────────────────────────────────────────────────┘
```

## Mechanisms Over Good Intentions

| Mechanism | What It Enforces | How |
|-----------|-----------------|-----|
| Branch protection rules | No merge without meaningful review | GitHub/GitLab configured to require review approval |
| Reviewer calibration | Reviewers apply a consistent standard | Review past reviews, compare decisions, and align expectations |
| Review comment templates | Structured feedback | IDE/tool integration prompts for severity and category |
| Quarterly review calibration | Consistent standards across reviewers | Reviewers assess the same PR independently, then compare notes |

## Common Rationalizations

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|----------------|-------------------|
| "It's a small change, it doesn't need a real review" | Small changes break production all the time. A one-line config change caused one of Amazon's largest outages. | Every change gets the same process. Small changes still deserve proper review. No shortcuts. |
| "I trust the author, just Ship It" | Trust is earned through evidence, not assumed. Even expert engineers make mistakes. The review protects them too. | Read the code. Check the tests. Verify the operational readiness. Trust and verify. |
| "We need to ship, let's merge and fix later" | "Fix later" means "never fix" in 80% of cases. The tech debt accumulates. The bar lowers for the next PR. | Split the PR if it's too large. Schedule a discussion if there's disagreement. Don't compromise the bar. |
| "The reviewer is being too picky, this is just style" | What looks like style is often clarity. Code is read 10x more than it's written. Readability is not a preference—it's an operational requirement. | If you disagree with a NIT, say so. But if the feedback is [IMPORTANT] or [BLOCKING], the reviewer has seen something you haven't. Listen. |
| "Only senior engineers can do this kind of review" | Treating quality as a specialist role creates bottlenecks and weakens ownership. Every reviewer is responsible for the bar. | Teach the review standard explicitly. Pair newer reviewers with experienced engineers. Calibrate on real PRs. |

## Red Flags

- PRs approved without comments (rubber-stamping)
- Same quality issues appearing repeatedly in reviews (not learning)
- Reviewers only checking style, ignoring operational readiness
- Authors pushing back on all feedback without engagement
- Only one or two people are treated as capable of meaningful review
- "Ship It" given with "I'll look more closely later" caveat
- Large PRs (500+ lines) approved without splitting request
- No [BLOCKING] comments ever used (standards too low)
- Review comments are only about formatting and naming

## Verification

After establishing the review process, verify:

- [ ] Every merged PR has at least one meaningful "Ship It" based on the five review dimensions
- [ ] Reviewers are evaluating all five dimensions (not just style)
- [ ] Review comments are categorized by severity
- [ ] Quarterly calibration sessions are happening
- [ ] Review capability is being developed across the team
- [ ] Authors report learning from reviews (feedback is educational)
- [ ] Production incidents traceable to reviewed code are rare
- [ ] Team coding standards are documented and referenced in reviews
- [ ] Review coverage exists for all technology stacks the team uses without relying on a single person

## Implementation Memory Capture

After review findings are resolved, check whether any finding represents a **recurring pattern** (same finding appears across 2+ reviews, or the reviewer explicitly flags "this keeps happening"). If a recurring pattern is identified:

1. Read `skills/implementation-memory/SKILL.md`.
2. Generate a self-reflection: "What recurring implementation mistake does this review finding reveal? What rule would prevent it in future builds?"
3. Extract up to 2 candidate learnings.
4. Present candidates to the user for Accept / Reject / Edit.
5. Apply admission checks and rejection rules before writing to `docs/implementation-memory.md`.

If no recurring pattern is identified, skip this step silently. This keeps the memory focused on durable, cross-cutting lessons rather than one-off feedback.

## Tenets

1. **"Ship It" is a commitment.** When you approve code, you're saying "I stand behind this code in production." Your name is on it. Review accordingly.
2. **The bar is the commitment.** Delivery pressure never justifies approving code that fails correctness, clarity, design, reuse, or operational readiness.
3. **Feedback is a gift.** Every review comment is an opportunity for the author to learn, the team to align, and the codebase to improve. Give generously. Receive graciously.
4. **The bar only goes up.** Each review should leave the codebase better than before. "Good enough" is not the standard. "Better than yesterday" is.
5. **Clarity over cleverness.** If the reviewer can't understand the code, the on-call engineer at 3 AM won't either. Readability is the highest standard.
6. **Operational readiness is non-negotiable.** A correct, clear, well-designed change without metrics and logs is not ready to ship. All five dimensions must pass.
7. **Teach, don't gatekeep.** Review exists to raise the team's bar, not to demonstrate superiority. Every blocking comment should explain why and suggest how.

<!-- MIRROR: This file mirrors .claude/commands/build.md. Do not edit directly — sync from the Claude version. -->

# Build — Execute Specs

## ⛔ Default Execution Mode: Fully Autonomous Until the Feature Is Done

**Unlike `/design` and `/wb`, `/build` runs without human gates by default. The approval gates happened *before* `/build` (during spec creation in `/design`). Once specs exist and are approved, `/build` executes everything end-to-end.**

When the user invokes `/build` (with no other instruction), the agent MUST:

1. Read **all** specs in `specs/` and identify the execution order (hardest-first, established during `/design`).
2. Execute **every spec in order**, end-to-end, without pausing between specs and without asking permission to continue.
3. Within each spec, execute all waves wave-by-wave per the dependency graph, without pausing between waves.
4. Within each wave, dispatch all tasks in parallel as sub-agents, without pausing between tasks.
5. After each spec, run the Post-Implementation Review automatically (see end of this file). If verdict is **PASSED** or **PASSED WITH FIXES NEEDED**, proceed to the next spec without asking. Only **FAILED** stops execution to surface to the user.
6. Stop only when **all specs in `specs/` are in a terminal state** (every task `[x]` or `[!]`). At that point, present a single end-of-build summary.

### When to stop and ask the user (the only valid reasons)

The agent MAY only stop autonomous execution when one of these is true:

- **Hard blocker**: a sub-agent reports `[!]` blocked and the blocker requires human input (missing credential, missing upstream service, ambiguous design that needs clarification, etc.). Mark the task `[!]` with reason and present.
- **Failed Post-Implementation Review**: verdict is `FAILED` (fundamentally wrong implementation, requirement entirely unimplemented, architectural gap). Present `implementation-review.md` and wait for guidance.
- **Green-build gate fails and cannot self-recover**: tests broken in a way that cannot be fixed with a follow-up task within scope.
- **The user explicitly asked to pause/checkpoint** (see override below).

> ⛔ **Anti-pattern**: stopping at the end of a spec and asking "should I proceed to the next spec?" when nothing is blocking. The default is to proceed.
>
> ⛔ **Anti-pattern**: presenting a status summary mid-feature with the implication "let me know if you want me to continue." The agent continues unless one of the four reasons above applies.
>
> ⛔ **Anti-pattern**: declaring "I've completed the work!" while `tasks.md` still has `[ ]` or `[-]` entries, or while there are subsequent specs in `specs/` not yet executed. That is not "done"; that is stopping early.

### Override: when the user wants step-by-step

The default is fully autonomous. The user can explicitly opt into a paused mode by including instructions like:

- *"build spec by spec, ask me before each one"*
- *"pause after each wave"*
- *"checkpoint between Spec 1 and Spec 2"*
- *"step-by-step build"*

When such an instruction is present in the user's message, switch to a paused mode for **that** invocation: complete the indicated unit (a wave, a spec, etc.), present a brief status, and wait for explicit "continue" before proceeding. Without such instruction, run autonomous to feature completion.

You are activating the **build** skill chain: `incremental-implementation` → `test-driven-development` → `operational-code`.

## Step 0: State Detection + Proportionality Check

Before executing anything, classify the invocation against the repo state and the change requested. The user should never have to think about which ceremony level applies — the agent decides, and only asks when there is genuine ambiguity.

1. **Read repo state**:
   - Does `specs/` exist with `requirements.md` + `design.md` + `tasks.md` for at least one slice?
   - Does `docs/design/<feature-or-service>/` exist with a `design-doc.md`?
   - Does `docs/working-backwards/` exist?
   - Is the project structurally a brownfield (significant code, IaC, CI present) or greenfield (mostly empty)?

2. **Read the user's request and classify the change** using the ladder in `skills/using-amazon-skills/SKILL.md` → "Match the Ceremony to the Change":
   - Trivial / Small / Medium / Large / New product

3. **Decide the path**:

   | State | Change size | Path |
   |---|---|---|
   | `specs/` exists, ≥1 spec ready | any | Execute the existing specs autonomously per "Default Execution Mode" below. |
   | No `specs/`, change is **Trivial** or **Small** | small | Switch to direct implementation: apply Code Quality Bar from `incremental-implementation`, write tests, modify code, single PR. Skip spec creation. Tell the user briefly what you're doing and why. |
   | No `specs/`, change is **Medium** or **Large**, project is **brownfield** without BLA artifacts | medium / large | Use `AskUserQuestion` to offer 2-3 outcome-framed options (see "Asking the user" below). Do not proceed without picking one. |
   | No `specs/`, change is **Medium** or **Large**, greenfield context | medium / large | Tell the user `/build` cannot create specs and recommend `/design` first. |

4. **Asking the user — outcome-framed options only**. When ambiguity requires a choice, the question must offer concrete outcomes (time, scope, traceability), not process names. Example for *"add a red button on screen X"* in a brownfield without BLA artifacts:

   > Detected: small UI change, no specs in this project.
   >
   > [A] Direct implementation — implement now with TDD + Code Quality Bar. ~30min. *Recommended.*
   > [B] Lightweight spec — produce a single spec (requirements + tasks, no design doc) for traceability. ~1h.
   > [C] Reverse-engineer the project first — run `/onboard` to produce a Design Doc and contracts from existing code, then create the spec on top. ~30min onboarding + ~1h spec.

   Names like "Tier 1", "spec-driven-implementation", "PR/FAQ" do not appear in the question.

5. **After the user picks (or if no question was needed)**: proceed to the chosen path. If the path is "execute existing specs", continue with the Default Execution Mode below. If the path is "direct implementation", apply Code Quality Bar and ship; do not invent intermediate artifacts.

## What /build Does

/build reads existing specs and executes their tasks. It does NOT create specs, write requirements, or produce design documents. All of that is the responsibility of `/design`.

## What to do

1. Read skills at `skills/incremental-implementation/`, `skills/test-driven-development/`, and `skills/operational-code/`.
2. Read ALL specs in `specs/` directory. Identify the execution order (specs are ordered by dependency — hardest-first).
3. For the current spec, read `tasks.md` and execute tasks following the dependency graph.

### Execution Flow

1. **Read existing specs** — Load `specs/<slice-name>/tasks.md` for the current slice. Do NOT create new specs.
2. **Pick up `tasks.md`** — Parse the phases, waves, and dependency graph from the current spec.
2b. **Check for coherence review** — If `specs/<slice-name>/coherence-review.md` exists, read the "Action Items for Build Agent" section. These action items are binding constraints that override or clarify tasks.md. Keep them visible throughout execution.
2c. **Apply implementation memory** — After the current spec/tasks and coherence-review action items are known, read `skills/implementation-memory/SKILL.md`. If `docs/implementation-memory.md` exists, read it and select active rules using multi-signal matching: Tags overlap with the spec's domain, File patterns match files the tasks will touch, OR `Applies when` prose is judged relevant. Convert selected rules into implementation guardrails, test checks, or review checks for this build. Increment `Hit count` for each selected rule. Unmatched rules are ignored and MUST NOT become requirements.
3. **Execute tasks wave-by-wave:**
   - **ALWAYS execute all tasks in Wave 1 IN PARALLEL** (these have no dependencies — parallelization is mandatory, not optional).
   - After Wave 1 completes, verify green-build gate passes (all tests green, no regressions).
   - **Execute all Wave 2 tasks IN PARALLEL** (they depend on Wave 1 outputs but NOT on each other).
   - Continue until all waves in the current phase are complete.
   - Verify the phase-level green-build gate before advancing to the next phase.
4. **Track task status in `tasks.md` — the orchestrator owns this file, not sub-agents.**

   Status markers:
   - `- [ ]` not yet started
   - `- [-]` in progress
   - `- [x]` done and verified
   - `- [!]` blocked (include reason inline, e.g. `- [!] Task 2.3: blocked — upstream API not deployed`)

   **State transition protocol — non-negotiable:**

   The orchestrator (the agent running `/build`) is the *only* writer of `tasks.md`. Sub-agents never edit `tasks.md` directly — they receive task context, do the work, and report status back to the orchestrator. This avoids concurrent-write conflicts and keeps the file's history coherent.

   For each wave, the orchestrator follows this sequence:

   1. **Before dispatching the wave**: edit `tasks.md` and flip every task in the wave from `- [ ]` to `- [-]`. Save the file. *Then* dispatch sub-agents. This ordering is critical: if the session is interrupted between the edit and the dispatch, a resume can scan `[-]` markers and pick up cleanly.
   2. **While sub-agents work**: do not touch `tasks.md`.
   3. **As each sub-agent reports back**: if it succeeded, edit `tasks.md` and flip its task from `- [-]` to `- [x]`. If it reports a blocker, flip to `- [!]` with the reason inline.
   4. **Before declaring the wave complete**: re-read `tasks.md` and verify that *every* task in the wave is `[x]` or `[!]`. If any task is still `[ ]` or `[-]`, you have a bug — either a sub-agent finished without reporting, or you skipped a transition. Stop and reconcile.
   5. **Only then** advance to the next wave.

   **Resuming after interruption**: when resuming a `/build` session, scan `tasks.md` first.
   - `[-]` = work in flight when interrupted; verify what was actually completed (look at the codebase) and reconcile to `[x]` or `[ ]`.
   - `[!]` = blocked; check whether the blocker is resolved.
   - `[x]` and `[ ]` = trustworthy as-is.
   - Continue from the first `[ ]` task whose dependencies are all `[x]`.

   ⛔ **Anti-pattern**: dispatching a sub-agent for Task 2.3 while `tasks.md` still shows `- [ ]` for Task 2.3. The file no longer reflects reality, and any interruption corrupts the resume path.

   ⛔ **Anti-pattern**: completing all the technical work for a wave (code, tests, green-build) but never updating `tasks.md`. The work is invisible to the next reader, future sessions cannot resume correctly, and the `/build` review checkpoint cannot run.

   ⛔ **Anti-pattern**: a sub-agent editing `tasks.md` itself. Two sub-agents writing in parallel will clobber each other's edits. Sub-agents report status; the orchestrator writes.

5. **Respect green-build gates between phases** — All tests must pass. No regressions allowed. If a gate fails, fix before proceeding.
6. **Parallelization is MANDATORY within waves** — Tasks in the same wave have no intra-wave dependencies by construction. You MUST dispatch sub-agents for all independent tasks within a wave simultaneously. Do NOT execute them sequentially.

   **How to parallelize:**
   - Read the dependency graph from tasks.md (JSON at the bottom)
   - Identify which tasks are in the same wave
   - Start ALL tasks in that wave at the same time (one sub-agent per task)
   - Wait for all sub-agents in the wave to complete
   - Only then advance to the next wave

   **Context each sub-agent MUST receive:**
   Sub-agents start from zero — they have no memory of the project. When dispatching a sub-agent for a task, you MUST provide it with:
   - The specific task description and acceptance criteria from tasks.md
   - The relevant requirement(s) from requirements.md (only the ones this task implements)
   - The relevant design section(s) from design.md (only §N.N referenced by _Design:_ annotation)
   - Action items from coherence-review.md that apply to this task (if any)
   - File paths and interfaces it will need to touch (from design.md components section)
   - Any constraints from previous waves (e.g., "Task 1.2 created the schema at src/models/user.ts — use that interface")
   - An explicit instruction: **"Do not edit `tasks.md`. Report your status back when done; the orchestrator updates the file."**

   **What the sub-agent reports back:**
   At completion, the sub-agent must return one of:
   - **Success** — task implemented, tests written and passing, with a summary of files changed.
   - **Blocked** — describe the blocker concretely (e.g., "Task 2.3 cannot proceed because the upstream contract from Task 1.4 is missing field X").
   - **Failed** — implementation attempted but tests fail or acceptance criteria are not met; include what was tried.

   The orchestrator then translates that report into the correct marker in `tasks.md` (`[x]`, `[!]`, or revert to `[ ]` for retry).

   ⛔ **Anti-pattern**: Dispatching a sub-agent with only "implement Task 2.3" and no context. The sub-agent will guess, hallucinate interfaces, or duplicate work.

   ⛔ **Anti-pattern**: Executing Wave 1 tasks one-by-one sequentially when they have no dependencies between them. This wastes time and defeats the purpose of wave-based planning.

7. **After all tasks in a spec are done, run the Post-Implementation Review and immediately move to the next spec** — Do NOT pause to ask the user. Follow the spec ordering established during `/design`. The agent stops only when *all* specs in `specs/` are in a terminal state, or when one of the four valid stop reasons (top of this file) applies.

### For Each Task

Apply these practices from the skill chain:

#### Incremental Implementation
- Each task produces a small, shippable increment (max 1-2 day chunk).
- Each increment must be independently deployable and rollback-safe.
- Every PR should be reviewable in <30 minutes.
- Use feature flags to hide incomplete work from customers.

#### Test-Driven Development
- Write the test FIRST — define the expected behavior before coding it.
- Unit tests for logic, integration tests for boundaries, contract tests for APIs.
- Tests must be deterministic, fast, and independent.
- Every bug fix starts with a failing test that reproduces the bug.

#### Operational Code
- Code must be observable: structured logging, metrics emission, trace propagation.
- Handle failures gracefully: retries with backoff, circuit breakers, timeouts.
- Configuration externalized — no hardcoded values for anything environment-specific.
- Alarms and dashboards defined alongside the code, not as an afterthought.

## Key Principles

- /build EXECUTES specs. /design CREATES specs. Never cross the boundary.
- Ship small, ship often, learn fast.
- If it's not tested, it's not done. If it's not monitored, it's not shipped.
- Code is written once but read 100 times — optimize for readability.
- Green-build gates are non-negotiable. Never skip them.
- Parallelism is earned through the dependency graph, not assumed.

## Output

For each completed spec:
- Implementation code (all tasks marked `[x]` in tasks.md)
- Tests (unit + integration, matching acceptance criteria from requirements.md)
- Observability instrumentation (logs, metrics, alarms)
- `tasks.md` is in a terminal state: every task is `[x]` (done) or `[!]` (blocked, with reason). No `[ ]` or `[-]` may remain when the spec is declared complete. If any do, the spec is not done — reconcile before moving on.

---

## Post-Implementation Review

After ALL tasks in a spec's `tasks.md` are marked `[x]` (or `[!]` with a documented blocker) and BEFORE declaring the spec "done" or moving to the next spec / `/deploy`:

**Verify the marker invariant first.** Re-read `tasks.md` and confirm no task is left in `[ ]` or `[-]`. If any are, the previous wave was not properly closed — go back, finish the missing tasks, and only then proceed to review.

**Then run an implementation review.** This is NOT optional — it is a quality gate equivalent to green-build gates.

### What to Check

1. Does the implementation match what the spec defined? (requirement by requirement)
2. Are all acceptance criteria from requirements.md satisfied?
3. Were any tasks skipped or partially implemented?
4. Do PBT properties pass (if defined in design.md)?
5. Is there code that wasn't specified in any requirement? (scope creep)
6. Does the implementation introduce operational concerns not addressed in design.md?

### Review Output Format

Produce the following structured review and save it to `specs/<slice-name>/implementation-review.md`:

```markdown
## Implementation Review — [Spec Name]

### Verdict: PASSED | PASSED WITH FIXES NEEDED | FAILED

### Requirement Coverage
| Requirement | Acceptance Criteria | Implementation | Status |
|---|---|---|---|
| Req 1.1 | "THE system SHALL return 200 on success" | `handler.ts:45` | ✅ Met |
| Req 1.2 | "WHEN input is invalid THE system SHALL return 400" | Not found | ❌ Missing |
| Req 2.1 | "THE system SHALL log all requests" | `middleware.ts:12` | ⚠️ Partial (missing error path) |

### Findings
- [FIX REQUIRED] Req 1.2 — No validation handler found. Add input validation returning 400.
- [FIX REQUIRED] Req 2.1 — Logging exists for success path but not error path. Add error logging in catch block.
- [MINOR] Task 3.2 — Test covers happy path but not edge case from AC 3.2.c.
- [OK] All PBT properties from design.md §6 pass.
- [OK] No unspecified code found — implementation is within scope.

### Fix Tasks (append to tasks.md as "Phase N+1: Review Fixes")
- [ ] Fix: Add input validation handler for Req 1.2 (Size: S, Design: §3.3, Requirements: 1.2)
- [ ] Fix: Add error-path logging for Req 2.1 (Size: S, Design: §3.5, Requirements: 2.1)
- [ ] Fix: Add edge case test for AC 3.2.c (Size: S, Requirements: 3.2)
```

### Verdicts and Actions

| Verdict | Action |
|---------|--------|
| **PASSED** | Proceed to next spec or `/deploy` **without asking the user**. No fixes needed. The review is informational, not a gate. |
| **PASSED WITH FIXES NEEDED** | Append "Fix Tasks" to `tasks.md` as a new `## Phase N+1: Review Fixes`. Execute these fix tasks IMMEDIATELY — **no human gate needed** (these are minor, within-scope fixes). After fixes are done, re-verify only the fixed items, then proceed to the next spec. |
| **FAILED** | STOP. Present the review to the user for a decision. Do NOT auto-fix — the scope of failure requires human judgment (possible design gap, missing requirement, or fundamental misunderstanding). This is one of the four valid stop reasons. |

### Execution Rules

1. **Generate the review** by comparing every requirement + acceptance criterion in `requirements.md` against the actual implementation.
2. **Check PBT properties** from `design.md` — run them if a test runner is available, otherwise manually verify the implementation satisfies them.
3. **Check for scope creep** — scan implementation for functionality not traced to any requirement. Flag it.
4. **Write the structured output** to `specs/<slice-name>/implementation-review.md`.
5. **Implementation memory — verdict-dependent behavior**:
   - **If PASSED WITH FIXES NEEDED** (semi-automatic trigger): After fix tasks are done, generate a self-reflection ("What went wrong? Why? What would have prevented it?"), extract up to 2 candidate learnings from the reflection, and present them to the user for Accept / Reject / Edit. Do not wait for the user to ask. This is the primary memory population path.
   - **If PASSED** (manual trigger): Ask the user to test the delivered behavior, bring back failures or feedback, and debug with the agent until accepted. Report `Implementation memory: waiting for user validation and Quality Memory Review request.` When the user later asks for Quality Memory Review, generate self-reflection, extract candidates, apply admission/rejection checks, and update memory only if warranted.
   - **Periodic nudge**: Read the `Builds without update` counter from `docs/implementation-memory.md`. If ≥3, include in end-of-build summary: "You have had N builds without memory update. Would you like a quick Quality Memory Review?"
   - **Show diff on update**: When memory is updated, show the rule IDs added/merged/removed directly in the response.
6. **If PASSED WITH FIXES NEEDED**:
   - Append the "Fix Tasks" section to `tasks.md` under a new phase header: `## Phase N+1: Review Fixes`
   - Add a green-build gate: `✅ **Green-build gate**: All prior phases pass. Review fixes are isolated corrections.`
   - Execute the fix tasks following normal task execution rules (TDD, operational code, incremental implementation).
   - After all fix tasks are `[x]`, re-run verification ONLY on the items that were flagged — not a full re-review.
   - Then trigger the semi-automatic memory extraction (step 5 above).
7. **If PASSED**: Mark spec as DONE. Update `tasks.md` status. **Proceed to the next spec immediately — do NOT ask the user for permission.** Only stop if this is the last spec in `specs/`.
8. **If FAILED**: Present `implementation-review.md` to the user with a clear explanation of what failed and why auto-fix is insufficient.

### What "FAILED" Means (vs. "PASSED WITH FIXES NEEDED")

| PASSED WITH FIXES NEEDED | FAILED |
|--------------------------|--------|
| Implementation exists but is incomplete or has minor gaps | Implementation is fundamentally wrong or missing |
| Fixes are additive (add a handler, add a test, add logging) | Fixes require rethinking the approach or design |
| Each fix is Size S or M | Fixes would be Size L or XL |
| No requirement is completely unaddressed | One or more requirements are entirely unimplemented |
| Within the architecture described in design.md | Requires architectural changes not in design.md |

---

## End of Build — when to actually stop

`/build` is **complete** only when every spec in `specs/` is in a terminal state:

- Every task in every `tasks.md` is `[x]` (done) or `[!]` (blocked, with documented reason).
- Every spec has a `specs/<slice-name>/implementation-review.md` with verdict PASSED or PASSED WITH FIXES NEEDED.
- No spec is left unstarted.

Only at that point do you produce the **end-of-build summary** to the user:

```
✅ /build complete

Specs executed: <N>
- <spec-1>: PASSED (X tasks done)
- <spec-2>: PASSED WITH FIXES NEEDED (Y tasks done, Z fix-tasks applied, memory candidates presented)
- <spec-N>: PASSED (W tasks done)

Total tasks done: <total>
Blocked tasks: <count> (see below)
Tests: green-build gate passed at every phase boundary
Implementation memory: <status — one of:>
  - "updated: added IM-00X, merged IM-00Y" (if semi-auto trigger fired and user accepted)
  - "candidates presented, awaiting user decision" (if semi-auto fired, user hasn't responded)
  - "waiting for user validation and Quality Memory Review request" (if all PASSED)
  - "nudge: N builds without update — consider running Quality Memory Review" (if counter ≥3)

Next steps:
- Test the implemented behavior in the product
- Bring back any failure, error, or feedback and debug with the agent until it is OK
- Ask for Quality Memory Review after validation to capture durable implementation learnings
- /review (code review bar raising)
- /deploy (progressive rollout)

Blocked items needing your attention:
- spec-3 / Task 4.2: <reason — what's needed from user>
```

If at any point during execution one of the four valid stop reasons fires, present **that** information instead and wait. Otherwise, do not stop.

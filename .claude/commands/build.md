# Build — Execute Specs

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

## ⛔ Default Execution Mode: Fully Autonomous Until the Feature Is Done

**Unlike `/design` and `/wb`, `/build` runs without human gates by default. The approval gates happened *before* `/build` (during spec creation in `/design`). Once specs exist and are approved, `/build` executes everything end-to-end.**

When the user invokes `/build` (with no other instruction), the agent MUST:

1. Read **all** specs in `specs/` and identify the execution order (hardest-first, established during `/design`).
2. Execute **every spec in order**, end-to-end, without pausing between specs and without asking permission to continue.
3. Within each spec, execute all waves wave-by-wave per the dependency graph, without pausing between waves.
4. Within each wave, dispatch all tasks in parallel as sub-agents, without pausing between tasks.
5. After each spec, run the Post-Implementation Review automatically (see end of this file). If verdict is **PASSED** or **PASSED WITH FIXES NEEDED**, proceed to the next spec without asking. Only **FAILED** stops execution to surface to the user.
6. Stop only when **all specs in `specs/` are in a terminal state** (every task `[x]` or `[!]`). At that point, present a single end-of-build summary.

> **Execution closure is not delivery.** "Every task `[x]` or `[!]`" is the *execution closure* condition — it says the orchestrator has nothing left to dispatch. It does not say the spec was delivered. A spec with at least one `[!]` corresponding to an unimplemented acceptance criterion **cannot** receive verdict `PASSED` in `implementation-review.md`: the best available verdict is `PASSED WITH FIXES NEEDED`, or `FAILED` if an entire requirement is unimplemented. Closure ends execution; the verdict reports delivery.

### When to stop and ask the user (the only valid reasons)

The agent MAY only stop autonomous execution when one of these is true:

- **Hard blocker**: a sub-agent reports `[!]` blocked and the blocker requires human input (missing credential, missing upstream service, ambiguous design that needs clarification, etc.). Mark the task `[!]` with reason and present.

  Not every `[!]` is a hard blocker, and the difference decides whether execution stops. If the blocker **requires human input** to resolve, stop and present. If the blocker is **workaroundable or merely local** — one task cannot proceed but the rest of the wave can — mark that task `[!]` with its reason, leave its dependents `[ ]`, and let the wave finish. Both outcomes use the same four markers; no new state is introduced.
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
2c. **Apply implementation memory** — After the current spec/tasks and coherence-review action items are known, read `skills/implementation-memory/SKILL.md`. If `docs/implementation-memory.md` exists, read it and select active rules using multi-signal matching: Tags overlap with the spec's domain, File patterns match files the tasks will touch, OR `Applies when` prose is judged relevant. A rule is selected only when its `Phase` matches the current phase — `build` here — and any one of those signals matches; a `Phase: design` or `Phase: operate` rule is never selected during `/build`. Convert selected rules into implementation guardrails, test checks, or review checks for this build. Increment `Hit count` for each selected rule. Unmatched rules are ignored and MUST NOT become requirements.
3. **Execute tasks wave-by-wave:**
   - **ALWAYS execute all tasks in Wave 1 IN PARALLEL** (these have no dependencies — parallelization is mandatory, not optional).
   - After Wave 1 completes, verify green-build gate passes (all tests green, no regressions).
   - **Execute all Wave 2 tasks IN PARALLEL** (they depend on Wave 1 outputs but NOT on each other).
   - **Dispatch only tasks whose dependencies are all `[x]`.** A task marked `[!]` never satisfies another task's dependency — a blocked task produced no output for a dependent to build on. So when a task ends `[!]`, every task that depends on it (directly or transitively) is **not dispatched**, stays `[ ]`, and is reported as not dispatched with the blocking task named. The rest of the wave proceeds normally.
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
   4. **Before declaring the wave complete**: re-read `tasks.md` and verify that *every* task in the wave is `[x]` or `[!]`. If any task is still `[ ]` or `[-]`, you have a bug — either a sub-agent finished without reporting, or you skipped a transition. Stop and reconcile. The single exception: a task left `[ ]` because it was **not dispatched** (a dependency ended `[!]`) is not a bug, but it must be named explicitly in the wave report alongside the blocking task. Where a Python 3 runtime is available, `python3 tools/bla-check tasks specs/<slice-name>` performs this same marker check mechanically over the whole spec; what to do when it is unavailable is defined once, at the Post-Implementation Review's marker check.

      Then reconcile the claim against reality. Record the git ref before dispatching the wave, and at the close run `git diff --name-only <wave-start-ref>` to list every path the wave actually changed. Each of those paths must appear in the `writes` set of some task **in this wave** — a path claimed only by a task in an earlier wave is unclaimed here, because the claim has to live where the change happened. **Unclaimed changed paths block stage completion**: the task that produced the path goes to `[!]` with the path named in the reason, not to `[x]`, and the wave does not close until either `tasks.md` claims the path or the change is reverted. This catches the case the declared sets cannot: two tasks that did not collide on paper and did collide on disk. Outside a git working tree the comparison is unavailable — say so in one line and continue, for the same reason the marker check degrades rather than blocking.
   5. **Only then** advance to the next wave.

   **Closing the spec.** Undispatched tasks may sit at `[ ]` while waves run, but they may not survive into closure. Before declaring the spec closed, flip every task still `[ ]` whose dependency chain ends in a `[!]` to `[!]` itself, with the reason inline (e.g. `- [!] Task 3.1: not dispatched — depends on Task 2.3, which is [!]`). Execution closure then still means what it says: every task `[x]` or `[!]`, no new state introduced.

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
   - Skip any task whose `depends_on` includes a task that is not `[x]` — a task marked `[!]` never satisfies another task's dependency, so its dependents are left `[ ]` and reported as not dispatched rather than dispatched with missing inputs
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
- `tasks.md` is in a terminal state: every task is `[x]` (done) or `[!]` (blocked, with reason). No `[ ]` or `[-]` may remain when the spec is declared complete. If any do, the spec is not done — reconcile before moving on. This is *execution closure*, not delivery: it means nothing is left to dispatch, not that everything was delivered. What was delivered is stated by the verdict in `implementation-review.md`.

---

## Post-Implementation Review

After ALL tasks in a spec's `tasks.md` are marked `[x]` (or `[!]` with a documented blocker) and BEFORE declaring the spec "done" or moving to the next spec / `/deploy`:

**Verify the marker invariant first.** Re-read `tasks.md` and confirm no task is left in `[ ]` or `[-]`. If any are, the previous wave was not properly closed — go back, finish the missing tasks, and only then proceed to review. When `tools/bla-check` and a Python 3 runtime are both present, run `python3 tools/bla-check tasks specs/<slice-name>` and treat any `FALHA` line as this check failing: the tool re-reads the same markers you just read, and unlike you it cannot skim. When there is no Python runtime, or the tool is not present in this project, state in one line that the marker guarantee for this spec has **dropped to LLM verification** — and **continue**. Never block on a missing runtime: `skills/implementation-memory/SKILL.md` promises the mechanism is harness-agnostic by design, and a hard runtime dependency would break that promise for every adopter.

**Then run an implementation review.** This is NOT optional — it is a quality gate equivalent to green-build gates. Load `agents/implementation-verifier.md` and verify the implementation through the implementation verifier lens.

**Dispatch it with author-isolated context for Medium and Large.** At those ceremony levels (`AGENTS.md` → *Match the Ceremony to the Change*) the implementation review is dispatched as a sub-agent, using the same sub-agent protocol as any task wave — and for the same reason it works there: a dispatched reviewer must start from zero and has no memory of the project, which is precisely the property a review of your own output needs. Give the reviewer sub-agent exactly this and nothing more:

- the spec artifacts — `requirements.md`, `design.md` (§6 Properties table included) and `tasks.md` with its final markers;
- the frozen API contract the implementation was built against;
- the diff under review, and the scope it was allowed to touch;
- the action items from `coherence-review.md` that bound this spec.

Do **not** pass your justifications for any of it: no "we did X because Y", no walkthrough of your reasoning, no defence of a shortcut. A reviewer handed the author's reasoning reviews the reasoning and approves it, which is how a self-check disguises itself as a review.

For **Trivial** and **Small** changes, continue with persona activation in this context — the ladder scopes the cost, and there is no diff big enough to justify a dispatch. Either way this is the **same review mechanism** with the same verdicts, the same finding format and the same single report at `specs/<slice-name>/implementation-review.md`; the only variable is whether the reviewer is isolated from the author. There is no second review and no second report.

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
- **F-01** [FIX REQUIRED] `handler.ts:45` — Req 1.2 has no validation branch on the request body → an invalid body is accepted and answered `200` instead of `400` → add the input validation handler. Impact: invalid records reach the store. Confidence: high. Minimal fix: validate at the handler boundary. Status: OPEN
- **F-02** [FIX REQUIRED] `middleware.ts:12` — Req 2.1 logging covers the success path only → a failed request leaves no trace for the on-call → add error logging in the catch block. Impact: failures are unsupportable at 3 AM. Confidence: high. Minimal fix: one log line in the existing catch. Status: OPEN
- **F-03** [MINOR] `handler.test.ts:88` — Task 3.2 covers the happy path but not AC 3.2.c → the edge case can regress unnoticed → add the edge-case test. Impact: none today. Confidence: high. Minimal fix: one test case. Status: OPEN
- [OK] All PBT properties from design.md §6 pass.
- [OK] No unspecified code found — implementation is within scope.

### Fix Tasks (append to tasks.md as "Phase N+1: Review Fixes")
- [ ] Fix: Add input validation handler for Req 1.2 (Size: S, Design: §3.3, Requirements: 1.2)
- [ ] Fix: Add error-path logging for Req 2.1 (Size: S, Design: §3.5, Requirements: 2.1)
- [ ] Fix: Add edge case test for AC 3.2.c (Size: S, Requirements: 3.2)
```

### Finding format

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

`[FIX REQUIRED]` and `[MINOR]` go in the `[SEVERITY]` slot. `[OK]` lines are not findings: they carry no ID, no status, and no place in any count. `implementation-review.md` is a persisted report, so the re-verification after the fix tasks updates it — moving each finding to `FIXED` — instead of writing a fresh report over it.

### Verdicts and Actions

**Precondition on `PASSED`.** Execution closure is not delivery. A spec whose `tasks.md` contains at least one `[!]` corresponding to an unimplemented acceptance criterion **cannot** be given verdict `PASSED`, however clean the rest of the run was — the lowest admissible verdict is `PASSED WITH FIXES NEEDED`, and `FAILED` when an entire requirement is unimplemented. `PASSED` asserts that every acceptance criterion in `requirements.md` is met; a blocked task that owns one of them contradicts that assertion.

**This review is a gate.** A finding at canonical severity BLOCKING that is still open removes the option to approve and advance: the only remaining options are fix it, accept it with the risk recorded in the accepted-risk table, or pause. A review report without a parseable verdict block counts as BLOCKING. In this command the BLOCKING level is spelled `[FIX REQUIRED]` (see `AGENTS.md` → *One Severity Scale and One Verdict Scale*), so an open `[FIX REQUIRED]` finding blocks moving to the next spec or to `/deploy`. Executing the fix tasks immediately, as the table below requires, *is* the fix option — what is not available is advancing while one is still open.

**Who produces what.** Three roles, and none of them is the same agent wearing a different hat. The **review is produced by the dispatched `agents/implementation-verifier.md`**, never by the orchestrator that wrote the code: the producer of an artifact cannot be the reviewer of it, and a self-check that finds nothing is indistinguishable from a review that was never run. The **fix tasks are executed by the orchestrator** (or by the sub-agents it dispatches for them), because the verifier must not touch the implementation it verified. The **re-verification after the fixes is a fresh dispatch** of the verifier — a new reviewer instance reading the code as it now stands, with the previous `implementation-review.md` as input so the findings keep their IDs — and never a self-check by whoever applied the fix. None of this adds a human gate: `/build` stays autonomous end to end. What changes is only who produces the report and who revalidates it.

| Verdict | Action |
|---------|--------|
| **PASSED** | Proceed to next spec or `/deploy` **without asking the user**. No fixes needed. This verdict is only available when no BLOCKING finding is open: it is the gate opening, not a note. |
| **PASSED WITH FIXES NEEDED** | Append "Fix Tasks" to `tasks.md` as a new `## Phase N+1: Review Fixes`. Execute these fix tasks IMMEDIATELY — **no human gate needed** (these are minor, within-scope fixes), because executing them is how the open findings get closed. Do not proceed while one is still open. After fixes are done, re-verify only the fixed items — by a fresh dispatch of the verifier, not by the agent that applied the fix — then proceed to the next spec. |
| **FAILED** | STOP. Present the review to the user for a decision. Do NOT auto-fix — the scope of failure requires human judgment (possible design gap, missing requirement, or fundamental misunderstanding). This is one of the four valid stop reasons. |

### Execution Rules

1. **Generate the review** by dispatching `agents/implementation-verifier.md`, which compares every requirement + acceptance criterion in `requirements.md` against the actual implementation. The orchestrator does not write this report about its own output.
2. **Check PBT properties** from `design.md` — run them if a test runner is available, otherwise manually verify the implementation satisfies them. **Record which route you took for each property**: a property checked by reading the code is reported as `NOT EXECUTED` or `VERIFIED BY INSPECTION`, never as a pass. A report verified by reading must not be indistinguishable from one backed by 1,000 green cases, and the count of properties not executed belongs in the review.
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
   - Execute the fix tasks following normal task execution rules (TDD, operational code, incremental implementation). The orchestrator owns these; the verifier that reported them does not touch the code.
   - After all fix tasks are `[x]`, re-run verification ONLY on the items that were flagged — not a full re-review — as a **fresh dispatch** of `agents/implementation-verifier.md`, given the previous `implementation-review.md` so each finding keeps its ID and moves to `FIXED`. The agent that applied a fix never certifies its own fix.
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

Only at that point do you produce the **end-of-build summary** to the user. **The header is conditional on the blocked-task count** — do not print a green checkmark over a run that left work blocked:

- `Blocked tasks == 0` → `✅ /build complete`
- `Blocked tasks > 0` → `⚠️ /build ended with <N> blocked task(s)`, with N the actual count

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

When the blocked count is greater than zero, the same body is used with the warning header instead, and the blocked items are the first thing the user reads:

```
⚠️ /build ended with 2 blocked task(s)

Specs executed: 3
- spec-1: PASSED (8 tasks done)
- spec-2: PASSED WITH FIXES NEEDED (11 tasks done, 2 fix-tasks applied)
- spec-3: PASSED WITH FIXES NEEDED (6 tasks done, 2 blocked)

Blocked items needing your attention:
- spec-3 / Task 4.2: blocked — upstream payments API not deployed to staging
- spec-3 / Task 4.5: not dispatched — depends on Task 4.2

Total tasks done: 25
Blocked tasks: 2
...
```

If at any point during execution one of the four valid stop reasons fires, present **that** information instead and wait. Otherwise, do not stop.

---
name: Incremental Implementation
description: Implementing features in thin vertical slices that each deliver value independently. Feature flags, safe defaults, rollback-friendly changes. Never a big-bang deployment.
leadership_principles:
  - Bias for Action
  - Deliver Results
  - Insist on the Highest Standards
---

## Overview

Incremental implementation means decomposing any feature into the thinnest possible vertical slices—each of which is independently deployable, testable, and rollback-safe. Every slice passes through the full stack (API → logic → storage → observability) rather than building horizontal layers that only work when all layers are combined.

At Amazon, this is not optional. A team that attempts a big-bang release—weeks of uncommitted code merged at once—will face pipeline rejection, delayed launches, and operational incidents. The one-slice-at-a-time principle ensures that at any point in time, `main` is deployable and the system is in a known-good state.

## When to Use

- Starting implementation of any feature approved through design review
- Breaking down a design document into implementation tasks
- Planning sprint work or developer assignments
- Any time a change would touch more than ~200 lines of production code
- When you notice a PR has grown beyond a single logical change

## Amazon Context

Amazon deploys million times per year across its services. This velocity is only possible because each deployment is small, reversible, and independent. The culture of "one commit per slice" emerged from painful lessons: large merges cause cascading failures, extended debugging sessions, and blocked pipelines.

Amazon's deployment system enforces bake times between stages. If your deployment contains 15 unrelated changes and one fails, all 15 roll back. This economic reality makes small, focused deployments the only rational strategy.

Feature flags let teams deploy code to production without exposing it to customers. This decouples deployment from release, allowing code to bake safely while business stakeholders decide when to activate.

## The Process

### 1. Slice Identification

Given a design document, decompose the feature into slices using these criteria:

| Criteria | Good Slice | Bad Slice |
|----------|-----------|-----------|
| Vertical completeness | Touches API → logic → storage → test | Only adds a database table |
| Independent value | Works even if later slices are never built | Requires slice 3 and 5 to function |
| Size | 50-200 lines of production code | 1000+ lines |
| Reviewability | One reviewer can understand in 30 min | Requires 2-hour review meeting |
| Rollback safety | Can be reverted without data migration | Creates irreversible schema changes |

### 2. Ordering Slices

1. **Infrastructure slice** — Create the feature flag, add the config entry, wire the empty handler. Deploy. Verify no regression.
2. **Data slice** — Add storage (table, column, index) behind the flag. Deploy with writes disabled. Verify schema migration.
3. **Core logic slice** — Implement the minimal happy path. Deploy behind flag. Verify with integration test.
4. **Edge case slices** — One per error condition or alternative path. Each independently deployed.
5. **Observability slice** — Metrics, alarms, dashboard for the new feature. Deploy. Verify emissions.
6. **Activation slice** — Enable the feature flag for canary traffic. Monitor. Gradually increase.

### 3. Commit Discipline

Each slice gets exactly one commit (or one squash-merged PR):

```
feat(orders): add feature flag for async-order-processing
feat(orders): add OrderEvent DynamoDB table with TTL
feat(orders): implement order placement behind flag
feat(orders): handle duplicate order submissions
feat(orders): add latency and error metrics for order flow
feat(orders): enable async-order-processing for 1% canary
```

### 4. Feature Flag Integration

Every behavioral change ships behind a flag:

```python
# Safe default: feature OFF
if feature_flags.is_enabled("async-order-processing", default=False):
    return await process_order_async(order)
else:
    return process_order_sync(order)  # existing path unchanged
```

Rules:
- Default is always the **existing behavior** (safe default)
- Flag evaluation is always at the **entry point**, not buried in logic
- Both paths have tests
- Flag cleanup is scheduled (ticket created at flag introduction)

### 5. Rollback-Friendly Changes

Every slice must answer: "How do I undo this in under 5 minutes?"

| Change Type | Rollback Strategy |
|-------------|-------------------|
| New code behind flag | Turn off flag (seconds) |
| Database additive (new table/column) | Leave in place, stop writing |
| Database destructive (drop/rename) | NEVER in same slice as logic change |
| Config change | Revert config (deploy not needed) |
| API contract change | Version the API, keep old version alive |

### 6. Verification at Each Slice

Before merging each slice:
- [ ] All existing tests pass (zero regression)
- [ ] New tests cover the slice's behavior
- [ ] Feature flag default is safe (off = old behavior)
- [ ] Slice is independently deployable
- [ ] Rollback plan documented in PR description
- [ ] Metrics/logs added to verify the slice works in production
- [ ] Code Quality Bar (next section) is met

## Code Quality Bar

Incremental delivery is necessary but not sufficient. The code inside each slice must be readable, testable, and maintainable by an engineer who is not the author. Quality is not the polish phase — it is how the code is written from the first line.

This section is the bar the agent applies while writing code. The Code Review Bar Raiser will hold the same bar after the fact; meeting it during writing avoids the rework loop.

### Pick the paradigm by context

Paradigm choice is a tool, not an identity. Match it to the shape of the problem:

- **Functional / data-oriented** — when the work is *transformation*: parsing, validating, mapping, aggregating, formatting, rendering. Prefer pure functions, immutable data, composition. The same input always produces the same output, side effects are explicit and pushed to the edges. Most pipelines, request/response handlers without I/O, and pure business logic fit here.
- **Object-oriented with SOLID** — when the domain has *entities with identity and lifecycle*: a `Reservation` that moves through states, an `Order` that owns invariants, a `Connection` that holds resources. Prefer encapsulation, polymorphism for variant behavior, and dependency inversion at boundaries.
- **Procedural** — for short, linear scripts and operational glue. Don't over-architect a 30-line task runner.

The same codebase routinely mixes paradigms. A handler at the edge does I/O (procedural shell), calls pure functions for transformation (functional core), and persists to a domain entity (OO at the storage boundary). This is the **functional core, imperative shell** pattern, and it is the default when no other shape is forced by the problem.

Don't argue paradigms. Pick the one that makes *this* code clearer to read and easier to test, and move on.

### SOLID, applied where it pays

SOLID is for the OO parts of the codebase. Apply each principle when it solves a real problem; don't apply them ceremonially.

- **Single Responsibility** — a class or module changes for one reason. If you can describe what it does only with "and", split it.
- **Open / Closed** — the code is open for extension, closed for modification. Reach for this when you have a *real* axis of variation (multiple payment providers, multiple auth methods), not when you imagine one might appear.
- **Liskov Substitution** — subclasses honor the contract of their parent. If a subclass throws on a method the parent guarantees, the hierarchy is wrong.
- **Interface Segregation** — clients depend only on the methods they use. Big "do-everything" interfaces couple unrelated callers.
- **Dependency Inversion** — depend on abstractions at *system boundaries* (storage, network, time, randomness). Do not invert dependencies inside your own pure logic where the indirection adds noise without value.

The trap with SOLID is over-application. Three classes is not a hierarchy. One implementation behind an interface is premature abstraction. Add the interface when the second concrete implementation is real, not hypothetical.

### Clean code basics that make the difference

These are not stylistic preferences — they are how the next engineer (or your future self at 3 AM) reads the code.

- **Naming carries the design.** A function named `process` tells you nothing; `chargeCustomerWithRetry` tells you what, who, and how. Variables named `data`, `info`, `temp`, `result` are red flags — they mean the author hadn't decided what the thing was.
- **Functions do one thing at one level of abstraction.** If a function mixes business logic with I/O parsing and string formatting, it is three functions glued together. Split until each function reads like a single sentence.
- **Keep functions small and shallow.** If you need to scroll, it's too big. If you need to track three nested conditionals, it's too deep. Extract early-return guards, extract intermediate variables with meaningful names, and the depth disappears.
- **Cyclomatic complexity is a smell, not a metric.** If a function has many branches, it is doing many things. The fix is rarely "tolerate the complexity" — it is decomposition (extract method, replace conditional with polymorphism, table-driven dispatch).
- **No comments that describe *what*; only *why*.** If the code needs a comment to explain what it does, rename the function or extract a variable until it doesn't. Reserve comments for non-obvious *why* — a workaround for a specific bug, a deliberate trade-off, a hidden invariant.
- **Dead code is debt.** Unused parameters, commented-out blocks, branches that can never run — delete them. Git remembers; the file should not.
- **Errors are values at boundaries, exceptions inside.** Translate provider exceptions to domain types at the seam. Don't let `requests.HTTPError` leak into your business logic.

### Avoid the cheap shortcuts

These are common shortcuts that look pragmatic in the moment and become someone else's incident later:

- **`any` / `unknown` / dynamic typing as escape hatches.** They hide problems instead of solving them. Type the boundary.
- **God objects, god functions, god modules.** When everything depends on one place, every change is risky. Decompose.
- **Mutable globals.** State that anyone can change is state that someone *will* change at the worst time. Pass dependencies explicitly.
- **Premature DRY in production code.** Three lines that look similar but evolve independently are not duplication — they are independent decisions. DRY is for repeated *concepts*, not repeated *characters*.
- **Over-mocking in tests.** If your test mocks five collaborators to test one function, the function's design is the problem, not the test. (See `test-driven-development`.)
- **Configurable behavior with no caller.** Don't add a parameter "in case someone needs it later". You'll add it when the real caller arrives.

### What "good enough" looks like, slice by slice

Each slice's code, before merge, should pass this read-aloud test:

> *"A teammate who didn't write this code can read the diff in 10 minutes, explain in their own words what changed, why it changed, and how to undo it — without asking the author."*

If the answer is no, the code is not done. Rename until functions describe themselves. Extract until each piece does one thing. Delete the dead branch. Reduce the nesting. Then merge.

## Mechanisms Over Good Intentions

| Mechanism | What It Enforces | How |
|-----------|-----------------|-----|
| PR size limits | Max 400 lines per PR | CI check rejects oversized PRs |
| Feature flag registry | All new features gated | Deployment pipeline checks flag existence |
| Pipeline bake times | Each deployment observed before proceeding | Deploy canary stages |
| Commit message linting | One logical change per commit | Conventional commits enforced in CI |
| Deployment frequency dashboard | Teams track deployment cadence | Weekly metrics review surfaces stalled code |

## Common Rationalizations

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|----------------|-------------------|
| "It's all one feature, it has to go together" | Features are always decomposable. If you can't find slices, you don't understand the feature yet. | Spend 30 more minutes on decomposition. Draw a dependency graph. The slices will appear. |
| "It's faster to build it all and test once" | It feels faster but isn't. Integration bugs compound. A 2-week big-bang becomes a 4-week debug session. | Track actual cycle time. Small slices shipped daily outperform weekly big merges every time. |
| "The feature flag adds complexity" | Flags add trivial complexity. Debugging a 2000-line merge at 2 AM adds real complexity. | The flag cost is 3 lines of code. The debugging cost is 3 hours of incident response. Choose. |
| "I need the database change and the logic together to test" | You can test writes to a new table without activating the feature. Separate deploy from release. | Deploy the table. Write integration tests that directly exercise it. Then deploy the logic that calls it. |
| "We'll just be careful with the big merge" | Hope is not a strategy. Every big-bang incident report starts with this sentence. | Mechanisms over good intentions. If the process allows big merges, someone will ship a broken one. |

## Red Flags

- A PR has been open for more than 3 days without merging
- A branch has diverged from `main` by more than 500 lines
- A developer says "I'll merge it all once it's done"
- No feature flags exist for a multi-week implementation
- The sprint plan has a single task called "Implement feature X"
- Deployment frequency drops below once per developer per day
- PR descriptions say "Part 1 of 5" but Part 1 doesn't work alone
- Schema migrations are bundled with logic changes in one deployment
- A function in the diff is so deeply nested or branchy that the author themselves struggles to explain it line by line
- Functions named `process`, `handle`, `do`, or variables named `data`, `info`, `temp` survive into the merged code
- A class accumulated responsibilities described with "and" — "manages connections **and** parses messages **and** retries failures"
- An abstraction exists with exactly one implementation and no concrete second one in sight
- A comment is needed to explain *what* the next line of code does
- A test mocks the world to verify a single function — the function's design is the real problem
- Provider-specific exception types (`requests.HTTPError`, `psycopg2.OperationalError`) leak into business logic

## Verification

After implementing a feature incrementally, verify:

- [ ] Every slice was deployed independently to production
- [ ] No slice caused a rollback or alarm in production
- [ ] Feature flags were used for all behavioral changes
- [ ] Each PR was reviewed and merged within 1 business day
- [ ] The feature can be disabled instantly via flag (test this)
- [ ] Total implementation time was shorter than estimated big-bang time
- [ ] New developers can understand individual commits in isolation
- [ ] No "fix" commits were needed after merge (each slice was complete)

## Tenets

1. **Every commit deploys.** If merging your commit would break `main`, it's not ready. No exceptions.
2. **Thin beats complete.** A working slice that handles 1 case is better than a comprehensive slice that handles 10 cases but isn't finished.
3. **Flags are free, incidents are expensive.** The cost of a feature flag is negligible. The cost of rolling back an unflagged change at 3 AM is enormous.
4. **Safe defaults always.** A flag's default value must produce the pre-existing behavior. New features are off until explicitly activated.
5. **Rollback in minutes, not hours.** If you can't explain how to undo your change in one sentence, the change is too big.
6. **Deploy daily or explain why not.** Deployment frequency is a health metric. If you're not deploying, something is blocked—find it and fix it.
7. **The PR is the unit of work.** Not the feature, not the sprint, not the ticket. One PR = one slice = one deploy = one logical change.
8. **Quality is written, not added later.** Naming, decomposition, paradigm choice, error boundaries, simplicity — these are decisions made while writing the slice, not in a "cleanup pass" that never happens. The first draft is the design document for the next reader.
9. **Pick the paradigm by the problem, not by allegiance.** Functional core, imperative shell. SOLID where entities have lifecycle. Procedural for short scripts. Mix freely; defend each choice with the reading experience of the next engineer.
10. **A teammate must read the diff in ten minutes and explain it back.** That is the definition of done for code quality, more reliable than any metric. Rename, extract, delete until they can.

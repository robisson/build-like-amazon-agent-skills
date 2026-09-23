# Tasks: [Slice Name]

> **Spec for**: [Parent Design Document title and link]
> **Slice**: [N of M] — [One-line description]
> **Author**: [Name]
> **Status**: Draft | In Review | Approved | In Progress | Done
> **Last Updated**: [Date]
> **Requirements**: [Link to requirements.md]
> **Design**: [Link to design.md]
> **Critical Path Estimate**: [Total days for longest dependency chain]
> **Total Effort Estimate**: [Sum of all task sizes]

---

## Task Status Markers

```
- [ ] Pending     — Not started
- [-] In Progress — Currently being worked on (agent can resume here if interrupted)
- [x] Done        — Completed and verified
- [!] Blocked     — Cannot proceed (add reason after marker)
```

The resume rule is **not** defined here. See `.claude/commands/build.md` → "Resuming after interruption" for the single definition of how an interrupted build picks work back up; this template only defines the markers it reads. The legend above is canonical vocabulary — do not restate the resume procedure alongside it.

## Legend

### Task Type Icons
- 🏗️ Infrastructure / Setup — Environment, configuration, scaffolding
- 🔧 Implementation — Production code that delivers behavior
- 🧪 Testing — Test code, test infrastructure, verification
- 📖 Documentation — API docs, runbooks, ADRs
- 🚀 Deployment — Pipeline changes, feature flags, rollout config
- 🔍 Spike / Investigation — Time-boxed research for unknowns

### Decision Type Icons
- 🔒 **One-way door** — Irreversible decision (schema migration, public API, data deletion). Needs explicit approval before execution.
- 🔓 **Two-way door** — Reversible decision (internal implementation, feature flag, configuration). Bias for action.

### Size Estimates
- **S** (Small): < 2 hours. Mechanical, low risk.
- **M** (Medium): 2-4 hours. Some complexity, well-understood domain.
- **L** (Large): 4-8 hours. Significant complexity or unknown territory.
- **XL** (Extra Large): 1-2 days. High complexity, consider splitting further.

### Traceability Annotations
- `Requirements: X.Y.Z` — Links to requirement section in requirements.md
- `Design: §N.N` — Links to design section in design.md
- `Depends on: Task X.Y` — Explicit dependency (must complete before this task starts)
- `Blocks: Task X.Y` — This task blocks another (forward reference)
- `Wave: N` — Parallel execution group (all tasks in same wave can run concurrently)
- `Writes: path, path` — The files this task writes. Two tasks may share a wave only when their `Writes` sets do **not** intersect; a path ending in `/` is a directory and collides with everything beneath it. A task that changes no file in the repository carries no `Writes` annotation — there is then nothing for the wave check to compare on its behalf.

---

## Phase 1: Foundation

> **Goal**: Establish infrastructure, scaffolding, and interfaces. After this phase, the skeleton compiles and all existing tests still pass.

✅ **Green-build gate**: All existing tests pass. CI pipeline green. No regressions introduced. New interfaces compile (implementations may be stubs).

---

### Task 1.1: [Scaffold project structure] 🏗️ 🔓

_Size: S | Requirements: N/A (infrastructure) | Design: §2.1_
_Depends on: None_
_Wave: 1_
_Blocks: Task 1.2, Task 1.3_
_Writes: tsconfig.json, jest.config.js, src/domain/types.ts, src/api/generated/_

- [ ] Create directory structure per design architecture
- [ ] Add configuration files (tsconfig, eslint, jest config)
- [ ] Create placeholder modules with exported interfaces
- [ ] Verify project compiles with `npm run build`

**Done when**: `npm run build` succeeds, `npm test` passes (0 tests is acceptable at this stage).

---

### Task 1.2: [Create database schema migration] 🏗️ 🔒

_Size: M | Requirements: 3.1.1 | Design: §4.2_
_Depends on: Task 1.1_
_Wave: 2_
_Blocks: Task 2.1, Task 2.2_
_Writes: migrations/0001_create_resource.sql, migrations/0001_create_resource.rollback.sql, src/db/schema.ts_

⚠️ **One-way door**: Schema migration is irreversible in production. Requires review before execution.

- [ ] Write migration script (CREATE TABLE with constraints)
- [ ] Write rollback script (DROP TABLE — only usable before data exists)
- [ ] Add indexes per design §4.2
- [ ] Run migration against local database
- [ ] Verify migration is idempotent (running twice doesn't error)

**Done when**: Migration runs successfully. Schema matches design §4.2 exactly. Rollback script verified.

---

### Task 1.3: [Set up feature flag] 🏗️ 🔓

_Size: S | Requirements: N/A (infrastructure) | Design: §2.1_
_Depends on: Task 1.1_
_Wave: 2_
_Writes: config/feature-flags.json, src/api/flag-gate.ts, test/flag-gate.test.ts_

- [ ] Register feature flag `[flag-name]` in configuration system
- [ ] Set default to OFF (disabled)
- [ ] Add flag check to entry point (returns 404 or fallback when off)
- [ ] Write test verifying behavior-when-off matches current behavior

**Done when**: Feature flag exists. When OFF, system behavior is unchanged. Test proves it.

---

## Phase 2: Core Implementation

> **Goal**: Implement the primary happy path. After this phase, the core feature works end-to-end behind the feature flag.

✅ **Green-build gate**: Phase 1 gate still passes. New unit tests pass. Integration test for happy path passes. Feature flag OFF = no behavioral change.

---

### Task 2.1: [Implement repository layer] 🔧 🔓

_Size: M | Requirements: 3.1.1, 3.1.2 | Design: §3.3, §4_
_Depends on: Task 1.2_
_Wave: 3_
_Blocks: Task 2.3_
_Writes: src/db/resource-repository.ts, test/resource-repository.test.ts, test/integration/resource-repository.it.ts_

- [ ] Implement `save()` method with conflict detection
- [ ] Implement `findById()` method with null handling
- [ ] Implement `findByFilter()` with pagination
- [ ] Write unit tests for each method (mock database)
- [ ] Write integration test with real database (Testcontainers)

**Done when**: All repository methods work against real database. Test coverage > 90% for this module.

---

### Task 2.2: [Implement domain validators] 🔧 🔓

_Size: S | Requirements: 3.1.1 AC-1, 3.3.1 | Design: §3.1_
_Depends on: Task 1.1_
_Wave: 2_
_Writes: src/domain/validators.ts, test/validators.pbt.ts_

- [ ] Implement input validation (name length, metadata constraints)
- [ ] Implement business rule validation
- [ ] Write property-based tests for validators (Design §6, Property 2)
- [ ] Verify all invalid inputs produce clear error messages

**Done when**: Validators catch all invalid inputs from requirements. PBT passes with 1000+ generated cases.

---

### Task 2.3: [Implement service layer — happy path] 🔧 🔓

_Size: L | Requirements: 3.1.1, 3.1.2 | Design: §3.2_
_Depends on: Task 2.1, Task 2.2_
_Wave: 4_
_Blocks: Task 3.1_
_Writes: src/service/resource-service.ts, test/resource-service.test.ts, test/integration/create-get-roundtrip.it.ts_

- [ ] Implement `createResource()` with idempotency check
- [ ] Implement `getResource()` with not-found handling
- [ ] Wire validator → service → repository
- [ ] Write unit tests with mocked repository
- [ ] Write integration test for full create→get roundtrip
- [ ] Verify idempotency property (Design §6, Property 1)

**Done when**: Create and Get work end-to-end. Idempotency PBT passes. All Phase 2 tests green.

---

## Phase 3: Error Handling & Edge Cases

> **Goal**: Handle all failure modes identified in the design. After this phase, the system is production-ready (behind flag).

✅ **Green-build gate**: Phases 1-2 gates pass. Error handling tests pass. Chaos tests pass. No regressions.

---

### Task 3.1: [Implement retry and circuit breaker] 🔧 🔓

_Size: M | Requirements: 3.3.1 | Design: §5.2, §5.3_
_Depends on: Task 2.3_
_Wave: 5_
_Writes: src/resilience/retry.ts, src/resilience/circuit-breaker.ts, test/resilience.test.ts_

- [ ] Implement exponential backoff with jitter (per design §5.2)
- [ ] Implement circuit breaker with configured thresholds (per design §5.3)
- [ ] Write tests simulating transient failures (verify retry behavior)
- [ ] Write tests simulating sustained failures (verify circuit opens)
- [ ] Write test verifying non-retryable errors fail immediately

**Done when**: Retry policy matches design §5.2 exactly. Circuit breaker thresholds match §5.3. Fault injection tests pass.

---

### Task 3.2: [Implement error response mapping] 🔧 🔓

_Size: S | Requirements: 3.3.1 | Design: §3.1 Error Contract_
_Depends on: Task 2.3_
_Wave: 5_
_Writes: src/api/error-mapper.ts, test/error-mapper.test.ts_

- [ ] Map each domain error to HTTP status code per design §3.1
- [ ] Include structured error body with `code`, `message`, context fields
- [ ] Write tests for each error mapping
- [ ] Verify error responses match API contract (schema validation)

**Done when**: Every domain error produces the correct HTTP response per design. No information leakage in error bodies.

---

### Task 3.3: [Implement concurrency handling] 🔧 🔓

_Size: M | Requirements: 3.2.1 | Design: §4.1_
_Depends on: Task 2.1_
_Wave: 4_
_Writes: src/db/optimistic-lock.ts, test/concurrency.test.ts_

- [ ] Implement optimistic concurrency control (version field)
- [ ] Handle version conflict with appropriate error
- [ ] Write test for concurrent updates (parallel writes to same resource)
- [ ] Verify soft-delete invariant property (Design §6, Property 5)

**Done when**: Concurrent updates don't silently overwrite. Version conflicts produce clear errors. PBT passes.

---

## Phase 4: Observability & Documentation

> **Goal**: Add metrics, logging, alarms, and documentation. After this phase, the feature is operable in production.

✅ **Green-build gate**: All previous gates pass. Metrics emit correctly. Logs contain required fields. Documentation is complete.

---

### Task 4.1: [Add metrics and structured logging] 🔧 🔓

_Size: M | Requirements: 4.3 | Design: §2.1_
_Depends on: Task 2.3_
_Wave: 5_
_Writes: src/observability/metrics.ts, src/observability/logger.ts, test/metrics.test.ts_

- [ ] Emit latency metric for each operation (p50, p95, p99)
- [ ] Emit error count metric by error category
- [ ] Emit throughput metric (requests/second)
- [ ] Add structured logging with correlation ID, operation, duration
- [ ] Write test verifying metrics are emitted on each code path

**Done when**: All operations emit metrics. Logs are structured and searchable. Dashboard can be built from emitted metrics.

---

### Task 4.2: [Create alarms and dashboard] 🏗️ 🔓

_Size: S | Requirements: 4.3 | Design: §5.1_
_Depends on: Task 4.1_
_Wave: 6_
_Writes: infra/alarms.ts, infra/dashboard.ts_

- [ ] Create alarm for error rate > [threshold]
- [ ] Create alarm for latency p99 > [threshold]
- [ ] Create dashboard with key metrics
- [ ] Verify alarms trigger correctly (test with synthetic errors)

**Done when**: Alarms fire when thresholds are breached. Dashboard shows all key metrics.

---

### Task 4.3: [Write API documentation and runbook] 📖 🔓

_Size: S | Requirements: N/A | Design: §3.1_
_Depends on: Task 3.2_
_Wave: 6_
_Writes: openapi.yaml, .bla/operations/runbook.md_

- [ ] Write API reference documentation (OpenAPI spec)
- [ ] Write operational runbook for common failure scenarios
- [ ] Document rollback procedure
- [ ] Review documentation with a peer (can they operate this at 3 AM?)

**Done when**: New engineer can understand, deploy, and troubleshoot this feature using only the documentation.

---

## Phase 5: Deployment & Activation

> **Goal**: Deploy behind feature flag, validate in production, gradually activate.

✅ **Green-build gate**: All previous gates pass. Feature works end-to-end in staging. Rollback procedure verified.

---

### Task 5.1: [Deploy to production (flag OFF)] 🚀 🔓

_Size: S | Requirements: N/A | Design: N/A_
_Depends on: All Phase 4 tasks_
_Wave: 7_

This task changes no file in the repository — it deploys code that is already committed — so it declares no `Writes` annotation. Wave 7 holds it alone, so there is no intersection to compute either.

- [ ] Deploy all code to production with feature flag OFF
- [ ] Verify no regression in existing behavior
- [ ] Verify metrics are emitting (even with flag off, infrastructure metrics should appear)
- [ ] Monitor error rates for 1 hour post-deployment

**Done when**: Code is in production. Flag is OFF. No regressions. Metrics flowing.

---

### Task 5.2: [Activate for canary traffic] 🚀 🔓

_Size: S | Requirements: N/A | Design: N/A_
_Depends on: Task 5.1_
_Wave: 8_

No `Writes` annotation either: the flag value lives in the configuration system at runtime, not in the tree.

- [ ] Enable feature flag for 1% of traffic (or internal users only)
- [ ] Monitor latency, error rate, and throughput for 24 hours
- [ ] Verify acceptance criteria pass with real traffic
- [ ] Compare metrics against baseline (no degradation)

**Done when**: Canary traffic validates the feature works in production. Metrics within acceptable bounds.

---

### Task 5.3: [Gradual rollout] 🚀 🔓

_Size: S | Requirements: N/A | Design: N/A_
_Depends on: Task 5.2_
_Wave: 9_
_Writes: config/feature-flags.json, src/api/flag-gate.ts_

- [ ] Increase to 10% → monitor 4 hours
- [ ] Increase to 50% → monitor 4 hours
- [ ] Increase to 100%
- [ ] Remove feature flag code (cleanup PR)

**Done when**: Feature is at 100%. Feature flag removed. All acceptance criteria verified at scale.

---

## Dependency Graph

```json
{
  "metadata": {
    "slice": "[Slice Name]",
    "total_tasks": 15,
    "total_phases": 5,
    "critical_path_tasks": ["1.1", "1.2", "2.1", "2.3", "4.1", "4.2", "5.1", "5.2", "5.3"],
    "critical_path_estimate_days": "[N]",
    "parallelism_factor": 1.67
  },
  "tasks": {
    "1.1": { "depends_on": [], "wave": 1, "size": "S", "type": "infrastructure", "door": "two-way", "writes": ["tsconfig.json", "jest.config.js", "src/domain/types.ts", "src/api/generated/"] },
    "1.2": { "depends_on": ["1.1"], "wave": 2, "size": "M", "type": "infrastructure", "door": "one-way", "writes": ["migrations/0001_create_resource.sql", "migrations/0001_create_resource.rollback.sql", "src/db/schema.ts"] },
    "1.3": { "depends_on": ["1.1"], "wave": 2, "size": "S", "type": "infrastructure", "door": "two-way", "writes": ["config/feature-flags.json", "src/api/flag-gate.ts", "test/flag-gate.test.ts"] },
    "2.1": { "depends_on": ["1.2"], "wave": 3, "size": "M", "type": "implementation", "door": "two-way", "writes": ["src/db/resource-repository.ts", "test/resource-repository.test.ts", "test/integration/resource-repository.it.ts"] },
    "2.2": { "depends_on": ["1.1"], "wave": 2, "size": "S", "type": "implementation", "door": "two-way", "writes": ["src/domain/validators.ts", "test/validators.pbt.ts"] },
    "2.3": { "depends_on": ["2.1", "2.2"], "wave": 4, "size": "L", "type": "implementation", "door": "two-way", "writes": ["src/service/resource-service.ts", "test/resource-service.test.ts", "test/integration/create-get-roundtrip.it.ts"] },
    "3.1": { "depends_on": ["2.3"], "wave": 5, "size": "M", "type": "implementation", "door": "two-way", "writes": ["src/resilience/retry.ts", "src/resilience/circuit-breaker.ts", "test/resilience.test.ts"] },
    "3.2": { "depends_on": ["2.3"], "wave": 5, "size": "S", "type": "implementation", "door": "two-way", "writes": ["src/api/error-mapper.ts", "test/error-mapper.test.ts"] },
    "3.3": { "depends_on": ["2.1"], "wave": 4, "size": "M", "type": "implementation", "door": "two-way", "writes": ["src/db/optimistic-lock.ts", "test/concurrency.test.ts"] },
    "4.1": { "depends_on": ["2.3"], "wave": 5, "size": "M", "type": "implementation", "door": "two-way", "writes": ["src/observability/metrics.ts", "src/observability/logger.ts", "test/metrics.test.ts"] },
    "4.2": { "depends_on": ["4.1"], "wave": 6, "size": "S", "type": "infrastructure", "door": "two-way", "writes": ["infra/alarms.ts", "infra/dashboard.ts"] },
    "4.3": { "depends_on": ["3.2"], "wave": 6, "size": "S", "type": "documentation", "door": "two-way", "writes": ["openapi.yaml", ".bla/operations/runbook.md"] },
    "5.1": { "depends_on": ["4.1", "4.2", "4.3", "3.1", "3.2", "3.3"], "wave": 7, "size": "S", "type": "deployment", "door": "two-way" },
    "5.2": { "depends_on": ["5.1"], "wave": 8, "size": "S", "type": "deployment", "door": "two-way" },
    "5.3": { "depends_on": ["5.2"], "wave": 9, "size": "S", "type": "deployment", "door": "two-way", "writes": ["config/feature-flags.json", "src/api/flag-gate.ts"] }
  },
  "waves": {
    "1": ["1.1"],
    "2": ["1.2", "1.3", "2.2"],
    "3": ["2.1"],
    "4": ["2.3", "3.3"],
    "5": ["3.1", "3.2", "4.1"],
    "6": ["4.2", "4.3"],
    "7": ["5.1"],
    "8": ["5.2"],
    "9": ["5.3"]
  },
  "critical_path": ["1.1", "1.2", "2.1", "2.3", "4.1", "4.2", "5.1", "5.2", "5.3"],
  "one_way_doors": ["1.2"]
}
```

---

## Completion Checklist

- [ ] All tasks marked done
- [ ] All green-build gates pass
- [ ] All PBT properties verified by `implementation-verifier`
- [ ] All acceptance criteria from requirements.md verified
- [ ] Code review completed (`code-review-bar-raising`)
- [ ] Documentation complete and peer-reviewed
- [ ] Feature deployed and validated in production
- [ ] Feature flag removed (cleanup PR merged)

# Tasks: Done On Top Of Blocked Fixture

`Task 3.1` is `[x]` while the task it depends on is `[!]`: a blocked task produced
no output for a dependent to build on. Expect `FALHA [task-dep-blocked]` and exit 1.

## Phase 2: Core Implementation

### Task 2.3: Implement the service layer

_Size: L | Wave: 1_
_Depends on: None_

- [!] Task 2.3: blocked — the upstream payments API is not deployed to staging

## Phase 3: Error Handling

### Task 3.1: Implement retry and circuit breaker

_Size: M | Wave: 2_
_Depends on: Task 2.3_

- [x] Task 3.1: retry policy and circuit breaker wired

## Dependency Graph

```json
{
  "metadata": { "slice": "dep-blocked-fixture", "total_tasks": 2 },
  "tasks": {
    "2.3": { "depends_on": [], "wave": 1, "size": "L" },
    "3.1": { "depends_on": ["2.3"], "wave": 2, "size": "M" }
  }
}
```

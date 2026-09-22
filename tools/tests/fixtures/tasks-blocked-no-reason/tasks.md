# Tasks: Blocked Without a Reason Fixture

A `[!]` marker with nothing a reader can act on. Expect
`FALHA [task-blocked-no-reason]` and exit 1.

## Phase 1: Foundation

### Task 1.1: Scaffold project structure

_Size: S | Wave: 1_
_Depends on: None_

- [x] Create the directory structure
- [x] Add the configuration files

## Phase 2: Core Implementation

### Task 2.3: Implement the service layer

_Size: L | Wave: 2_
_Depends on: Task 1.1_

- [!] Task 2.3

## Dependency Graph

```json
{
  "metadata": { "slice": "blocked-no-reason-fixture", "total_tasks": 2 },
  "tasks": {
    "1.1": { "depends_on": [], "wave": 1, "size": "S" },
    "2.3": { "depends_on": ["1.1"], "wave": 2, "size": "L" }
  }
}
```

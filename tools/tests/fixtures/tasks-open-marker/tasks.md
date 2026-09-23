# Tasks: Open Marker Fixture

Identical to `tasks-clean` except that one checkbox was never closed. Expect
`FALHA [task-marker-open]` and exit 1.

## Phase 1: Foundation

### Task 1.1: Scaffold project structure

_Size: S | Wave: 1_
_Depends on: None_

- [x] Create the directory structure
- [ ] Add the configuration files

### Task 1.2: Create the schema migration

_Size: S | Wave: 2_
_Depends on: Task 1.1_

- [x] Write the migration script
- [x] Run the migration locally

## Dependency Graph

```json
{
  "metadata": { "slice": "open-marker-fixture", "total_tasks": 2 },
  "tasks": {
    "1.1": { "depends_on": [], "wave": 1, "size": "S" },
    "1.2": { "depends_on": ["1.1"], "wave": 2, "size": "S" }
  }
}
```

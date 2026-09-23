# Tasks: Intra-Wave Dependency Fixture

Task 1.2 depends on task 1.1 and the graph puts both in wave 1. Nothing collides on
disk, so the write intersection is empty and that check says nothing — yet `/build`
dispatches only tasks whose dependencies are all `[x]`, so 1.2 is never dispatched in
wave 1. Expect `FALHA [wave-dep-intra]` and exit 1.

## Phase 1: Foundation

### Task 1.1: Scaffold project structure

_Size: S | Wave: 1_

- [x] Create the directory structure

### Task 1.2: Create the schema migration

_Size: S | Wave: 1_
_Depends on: Task 1.1_

- [x] Write the migration script

## Dependency Graph

```json
{
  "metadata": { "slice": "intra-wave-fixture", "total_tasks": 2 },
  "tasks": {
    "1.1": { "depends_on": [], "wave": 1, "size": "S", "writes": ["src/index.ts"] },
    "1.2": { "depends_on": ["1.1"], "wave": 1, "size": "S", "writes": ["src/db/schema.ts"] }
  }
}
```

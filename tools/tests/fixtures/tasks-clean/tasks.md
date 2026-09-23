# Tasks: Clean Fixture

A spec in execution closure: every task is `[x]` or `[!]`, the blocked one carries
its reason inline, and the dependency graph matches the document exactly. It also
opted in to per-task completion evidence: `.reports/` exists and carries one file per
done task, each opening with its `**Agent:** <task-id>` marker line. The blocked task
needs none — it was never done.

## Phase 1: Foundation

### Task 1.1: Scaffold project structure

_Size: S | Wave: 1_
_Depends on: None_

- [x] Create the directory structure
- [x] Add the configuration files

### Task 1.2: Create the schema migration

_Size: S | Wave: 2_
_Depends on: Task 1.1_

- [x] Write the migration script
- [x] Run the migration locally

## Phase 2: Core Implementation

### Task 2.1: Implement the service layer

_Size: M | Wave: 3_
_Depends on: Task 1.2_

- [!] Task 2.1: blocked — the upstream contract is missing field `tenantId`

## Dependency Graph

```json
{
  "metadata": { "slice": "clean-fixture", "total_tasks": 3 },
  "tasks": {
    "1.1": { "depends_on": [], "wave": 1, "size": "S" },
    "1.2": { "depends_on": ["1.1"], "wave": 2, "size": "S" },
    "2.1": { "depends_on": ["1.2"], "wave": 3, "size": "M" }
  }
}
```

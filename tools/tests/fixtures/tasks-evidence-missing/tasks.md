# Tasks: Evidence Missing Fixture

This spec opted in to per-task completion evidence — `.reports/` exists — and then
did not keep the promise for two of its three done tasks.

Expect two `FALHA [task-evidence-missing]` lines and exit 1: task 1.2 has no
`.reports/1.2.md` at all, and task 1.3 has the file but its first line is a title
instead of the `**Agent:** 1.3` marker, so nothing can attribute it. Task 1.1 is the
passing shape. Markers are all `[x]`, and no task declares `writes`, so no other rule
has anything to say here.

## Phase 1: Foundation

### Task 1.1: Scaffold project structure

_Size: S | Wave: 1_
_Depends on: None_

- [x] Create the directory structure

### Task 1.2: Create the schema migration

_Size: S | Wave: 2_
_Depends on: None_

- [x] Write the migration script

### Task 1.3: Register the feature flag

_Size: S | Wave: 3_
_Depends on: None_

- [x] Register the flag and default it to OFF

## Dependency Graph

```json
{
  "metadata": { "slice": "evidence-missing-fixture", "total_tasks": 3 },
  "tasks": {
    "1.1": { "depends_on": [], "wave": 1, "size": "S" },
    "1.2": { "depends_on": [], "wave": 2, "size": "S" },
    "1.3": { "depends_on": [], "wave": 3, "size": "S" }
  }
}
```

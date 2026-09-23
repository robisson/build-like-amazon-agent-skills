# Tasks: Partial Graph Fixture

A spec whose graph is present but incomplete in the two ways that weaken a verdict
without invalidating it. Task 1.3 has a section and a graph entry but no marker
anywhere, so its state is not derivable. Task 1.2 declares no `writes` while its
wave-1 neighbours do, so the intersection check for that wave is only partial.

Both are `AVISO`: the run reports them and still exits 0, because a warning never
changes the exit code.

## Phase 1: Foundation

### Task 1.1: Scaffold project structure

_Size: S | Wave: 1_

- [x] Create the directory structure

### Task 1.2: Create the schema migration

_Size: S | Wave: 1_

- [x] Write the migration script

### Task 1.3: Set up the feature flag

_Size: S | Wave: 1_

This task carries prose and no checkbox, which is exactly the shape that makes its
state undecidable.

## Dependency Graph

```json
{
  "metadata": { "slice": "partial-graph-fixture", "total_tasks": 3 },
  "tasks": {
    "1.1": { "depends_on": [], "wave": 1, "size": "S", "writes": ["src/index.ts"] },
    "1.2": { "depends_on": [], "wave": 1, "size": "S" },
    "1.3": { "depends_on": [], "wave": 1, "size": "S", "writes": ["config/flags.json"] }
  }
}
```

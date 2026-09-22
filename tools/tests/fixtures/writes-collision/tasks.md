# Tasks: Writes Collision Fixture

Two tasks share wave 1 with no dependency between them, yet both declare that they
write `src/api/handler.ts`. Dispatched in parallel they would clobber each other.

Expect `FALHA [wave-writes-intersection]` and exit 1: the pairwise intersection of the
`writes` sets inside a wave must be empty, and here it is not. Task 1.1 also declares the
directory form `src/api/generated/` with a trailing slash — that entry collides with
anything beneath it, and with nothing that merely sits next to it.

## Phase 1: Foundation

### Task 1.1: Generate the API handlers

_Size: S | Wave: 1_
_Depends on: None_

- [x] Generate the handler from the contract
- [x] Commit the generated output

### Task 1.2: Add request validation

_Size: S | Wave: 1_
_Depends on: None_

- [x] Validate the request body at the handler boundary
- [x] Write the unit tests

## Dependency Graph

```json
{
  "metadata": { "slice": "writes-collision-fixture", "total_tasks": 2 },
  "tasks": {
    "1.1": {
      "depends_on": [], "wave": 1, "size": "S",
      "writes": ["src/api/handler.ts", "src/api/generated/"]
    },
    "1.2": {
      "depends_on": [], "wave": 1, "size": "S",
      "writes": ["src/api/handler.ts"]
    }
  }
}
```

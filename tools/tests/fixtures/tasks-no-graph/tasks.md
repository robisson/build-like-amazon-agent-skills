# Tasks: No Graph Fixture

A spec that carries no dependency graph. Every marker is closed, so no `FALHA` is
possible; the graph rules cannot run at all. The checker must say so with
`AVISO [task-graph-absent]` and still exit 0 — that is the half of the output
contract no other fixture exercises.

## Phase 1: Foundation

### Task 1.1: Scaffold project structure

_Size: S_

- [x] Create the directory structure
- [x] Add the configuration files

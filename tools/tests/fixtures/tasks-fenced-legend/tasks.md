# Tasks: Fenced Legend Fixture

The fence regression. Every open marker in this file lives inside a fenced block —
the status legend, a nested example, and the dependency graph — so the checker must
see none of them. Expect exit 0.

## Task Status Markers

```
- [ ] Pending     — Not started
- [-] In Progress — Currently being worked on
- [x] Done        — Completed and verified
- [!] Blocked     — Cannot proceed (add reason after marker)
```

An example of how the legend is quoted inside documentation, opened with four
backticks so the inner three-backtick fences do not close it:

````
```
- [ ] this open marker is two fences deep
```
````

The same legend with a tilde fence, which a backtick fence must not close:

~~~
- [-] in progress, inside a tilde fence
~~~

## Phase 1: Foundation

### Task 1.1: Scaffold project structure

_Size: S | Wave: 1_
_Depends on: None_

- [x] Create the directory structure
- [x] Add the configuration files

### Task 1.2: Wire the entry point

_Size: S | Wave: 2_
_Depends on: Task 1.1_

- [x] Register the feature flag
- [x] Verify behaviour when the flag is off

## Dependency Graph

```json
{
  "metadata": { "slice": "fenced-legend-fixture", "total_tasks": 2 },
  "tasks": {
    "1.1": { "depends_on": [], "wave": 1, "size": "S" },
    "1.2": { "depends_on": ["1.1"], "wave": 2, "size": "S" }
  }
}
```

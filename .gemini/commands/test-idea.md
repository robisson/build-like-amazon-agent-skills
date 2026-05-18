<!-- MIRROR: This file mirrors .claude/commands/test-idea.md. Do not edit directly — sync from the Claude version. -->

# Test Idea — How Will We Measure Success?

Activate the **wb-test-and-iterate** skill from `skills/wb-test-and-iterate/`. Phase 5 of Working Backwards.

## Instructions

Define how to validate the idea and measure its impact.

1. Review the PR/FAQ and solution sketch.
2. Help the user build a validation plan:
   - What key assumptions must be true for success?
   - How can we test each assumption cheaply and quickly?
   - What does the MVP look like? (minimum to learn, not minimum to ship)
   - What metrics prove we solved the problem?
3. Write a **Success Metrics** document:
   - Input metrics (what we control: adoption, usage, features shipped)
   - Output metrics (what we move: satisfaction, time saved, errors reduced)
   - Guardrail metrics (what must NOT get worse)
   - Target values and measurement timeline
   - Kill criteria (when do we stop if it's not working?)

## Principles

- Measure outcomes, not outputs — "customer success" not "features shipped."
- Every metric needs baseline, target, and deadline.
- Prefer leading indicators over lagging ones.
- Design experiments that can fail — unfalsifiable tests teach nothing.

## Output

Save to `docs/working-backwards/<feature-name>/success-metrics.md`.
Suggest next step: "Working Backwards complete. Run /design to start technical design."

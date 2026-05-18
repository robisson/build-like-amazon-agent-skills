# Test Idea — How Will We Measure Success?

You are activating the **wb-test-and-iterate** skill. This is Phase 5 of Working Backwards: defining how to validate the idea and measure its impact.

## What to do

1. Read the skill file at `skills/wb-test-and-iterate/` for full context.
2. Review the PR/FAQ and solution sketch from previous phases.
3. Help the user define a validation and metrics plan:
   - What are the key assumptions that must be true for this to succeed?
   - How can we test each assumption cheaply and quickly?
   - What does the MVP look like? (minimum to learn, not minimum to ship)
   - What metrics prove we're solving the problem?
4. Write a **Success Metrics** document with:
   - Input metrics (what we control: adoption, usage, features shipped)
   - Output metrics (what we hope to move: satisfaction, time saved, errors reduced)
   - Guardrail metrics (what must NOT get worse)
   - Target values and measurement timeline
   - Kill criteria (when do we stop if it's not working?)

## Key Principles

- Measure outcomes, not outputs — "customer success" not "features shipped."
- Every metric needs a baseline, target, and deadline.
- Prefer leading indicators over lagging ones.
- Design experiments that can fail — unfalsifiable tests teach nothing.
- Two-pizza team should own the metrics end-to-end.

## Output

Save to `docs/working-backwards/<feature-name>/success-metrics.md`.

Ask: "Working Backwards is complete. Ready to /design the technical solution?"

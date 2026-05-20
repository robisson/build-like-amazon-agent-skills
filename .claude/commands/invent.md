# Invent — What Is the Solution?

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

You are activating the **wb-invent** skill. This is Phase 3 of Working Backwards: inventing the simplest solution that solves the customer's problem.

## What to do

1. Read the skill file at `skills/wb-invent/` for full context.
2. Review the customer profile and problem statement from previous phases.
3. Guide the user through solution ideation:
   - What is the ideal customer experience? (describe the end state)
   - What are 3 possible approaches? (brainstorm before converging)
   - Which approach is simplest while fully solving the problem?
   - What would the customer's new workflow look like step-by-step?
4. Write a **Solution Sketch** with:
   - Elevator pitch (2-3 sentences max)
   - Customer experience walkthrough (narrative form)
   - Key capabilities required
   - What we're explicitly NOT building (anti-scope)
   - Open questions and risks

## Key Principles

- Start with the customer experience, not the architecture.
- Simplify ruthlessly — if a feature doesn't serve the core problem, cut it.
- "What would have to be true?" — identify assumptions to validate.
- Prefer reversible decisions; avoid one-way doors when possible.
- Think big, start small, launch fast.

## Output

Save to `docs/working-backwards/<feature-name>/solution-sketch.md`.

Ask: "Would you like to proceed to /refine (PR/FAQ writing)?"
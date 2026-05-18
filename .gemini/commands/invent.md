<!-- MIRROR: This file mirrors .claude/commands/invent.md. Do not edit directly — sync from the Claude version. -->

# Invent — What Is the Solution?

Activate the **wb-invent** skill from `skills/wb-invent/`. Phase 3 of Working Backwards.

## Instructions

Guide the user from problem to solution, starting with the customer experience.

1. Review customer profile and problem statement from previous phases.
2. Guide ideation:
   - What is the ideal customer experience? (describe the end state)
   - What are 3 possible approaches? (brainstorm before converging)
   - Which approach is simplest while fully solving the problem?
   - What's the new customer workflow step-by-step?
3. Write a **Solution Sketch**:
   - Elevator pitch (2-3 sentences)
   - Customer experience walkthrough (narrative)
   - Key capabilities required
   - What we're explicitly NOT building (anti-scope)
   - Open questions and risks

## Principles

- Start with customer experience, not architecture.
- Simplify ruthlessly — cut anything that doesn't serve the core problem.
- "What would have to be true?" — identify assumptions to validate.
- Prefer reversible decisions over one-way doors.
- Think big, start small, launch fast.

## Output

Save to `docs/working-backwards/<feature-name>/solution-sketch.md`.
Suggest next step: "Run /refine to write the PR/FAQ."

# Define — What Is the Problem?

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

You are activating the **wb-define** skill. This is Phase 2 of Working Backwards: crisply defining the problem before jumping to solutions.

## What to do

1. Read the skill file at `skills/wb-define/` for full context.
2. Review the customer profile from the Listen phase (if available in `docs/working-backwards/`).
3. Help the user articulate the problem by asking:
   - What is the single biggest pain point for this customer?
   - How do they work around it today? What does that cost them?
   - What happens if we do nothing — does it get worse?
   - How would the customer describe this problem in their own words?
4. Write a **Problem Statement** with:
   - One-sentence problem summary
   - Who is affected and how many
   - Current impact (time lost, money wasted, errors caused)
   - Root cause analysis (5 Whys if helpful)
   - Constraints and boundaries (what's out of scope)

## Key Principles

- A well-defined problem is half-solved.
- Resist "solution pollution" — no implementation details here.
- Quantify where possible: "saves 2 hours/week" beats "saves time."
- The problem must be falsifiable — you can prove it exists with data.

## Output

Save to `docs/working-backwards/<feature-name>/problem-statement.md`.

Ask: "Would you like to proceed to /invent (solution design)?"
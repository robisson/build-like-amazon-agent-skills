<!-- MIRROR: This file mirrors .claude/commands/define.md. Do not edit directly — sync from the Claude version. -->

# Define — What Is the Problem?

Activate the **wb-define** skill from `skills/wb-define/`. Phase 2 of Working Backwards.

## Instructions

Help the user articulate the problem crisply, without jumping to solutions.

1. Review the customer profile from `docs/working-backwards/` if available.
2. Ask:
   - What is the single biggest pain point for this customer?
   - How do they work around it today? What does that cost?
   - What happens if we do nothing?
   - How would the customer describe this problem in their words?
3. Write a **Problem Statement**:
   - One-sentence summary
   - Who is affected and how many
   - Current impact (quantified: time, money, errors)
   - Root cause analysis (5 Whys)
   - Constraints and boundaries (what's out of scope)

## Principles

- A well-defined problem is half-solved.
- No "solution pollution" — zero implementation details here.
- Quantify: "saves 2 hours/week" beats "saves time."
- Must be falsifiable — you can prove it exists with data.

## Output

Save to `docs/working-backwards/<feature-name>/problem-statement.md`.
Suggest next step: "Run /invent to design the solution."

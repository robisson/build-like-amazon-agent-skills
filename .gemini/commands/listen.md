<!-- MIRROR: This file mirrors .claude/commands/listen.md. Do not edit directly — sync from the Claude version. -->

# Listen — Who Is the Customer?

Activate the **wb-listen** skill from `skills/wb-listen/`. Phase 1 of Working Backwards.

## Instructions

Help the user deeply understand their customer before proposing any solution.

1. Ask the user to describe their customer. Probe with:
   - Who specifically are they? (role, context, environment)
   - What are they trying to accomplish today?
   - What tools/processes do they currently use?
   - What frustrates them most?
2. Synthesize a **Customer Profile**:
   - Customer archetype (1-2 sentence persona)
   - Current workflow (step-by-step)
   - Pain points (ranked by severity and frequency)
   - Unmet needs (what they wish existed)
   - Representative quotes or anecdotes

## Principles

- Listen before solutioning — do NOT propose fixes yet.
- Be specific: "backend engineers deploying 3x/day" not "developers."
- Distinguish what customers SAY vs what they DO.
- One customer segment at a time.

## Output

Save to `docs/working-backwards/<feature-name>/customer-profile.md`.
Suggest next step: "Run /listen to continue to problem definition."

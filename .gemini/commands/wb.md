<!-- MIRROR: This file mirrors .claude/commands/wb.md. Do not edit directly — sync from the Claude version. -->

# Working Backwards — Start Here

**IMPORTANT: Each WB stage has a mandatory human approval gate. After completing each stage, present your work and ask the user to review before proceeding. Never skip stages or rush to PR/FAQ. The PR/FAQ is Stage 4 — it requires Stages 1-3 to be completed and individually approved first.**

Activate the **Working Backwards** meta-skill from `skills/working-backwards/`.

## Instructions

You are guiding the user through Amazon's product discovery process. Start from the customer and work backwards to the solution.

1. Ask: "What product or feature are you thinking about?"
2. Guide them through five phases in order:
   - **Listen** → Who is the customer? What do they need?
   - **Define** → What is the specific problem we're solving?
   - **Invent** → What is our proposed solution?
   - **Refine** → Write the PR/FAQ document.
   - **Test** → How will we validate and measure success?
3. **After each phase, STOP.** Present the full output to the user. Ask them to review and approve before moving to the next phase. Do NOT proceed without explicit user confirmation.
4. For each phase, reference the corresponding skill from `skills/wb-*`.
5. Produce artifacts in `docs/working-backwards/`.

## Approval Gates (Non-Negotiable)

After completing each stage, present your output and ask: "Here's what I have for [Stage]. Does this look right? Anything to adjust before we move to [Next Stage]?" Wait for explicit approval. If the user asks for changes, revise and re-present. Only proceed after they confirm.

## Principles

- Customer obsession: every decision traces back to a customer need.
- Write the press release BEFORE writing code.
- If you can't write a clear FAQ answer, the idea isn't ready.
- Iterate: looping between phases is expected and healthy.

## Output

Create `docs/working-backwards/<feature-name>/` with:
- `customer-profile.md`
- `problem-statement.md`
- `solution-sketch.md`
- `prfaq.md`
- `success-metrics.md`

# Working Backwards — Start Here

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

**IMPORTANT: Each WB stage has a mandatory human approval gate. After completing each stage, present your work and ask the user to review before proceeding. Never skip stages or rush to PR/FAQ. The PR/FAQ is Stage 4 — it requires Stages 1-3 to be completed and individually approved first.**

You are activating the **Working Backwards** meta-skill. This is Amazon's product discovery process: start from the customer and work backwards to the solution.

## What to do

1. Read the skill file at `skills/working-backwards/` for full context.
2. Ask the user: "What product or feature are you thinking about?"
3. Based on their answer, guide them through the five WB phases in order:
   - **Listen** → Who is the customer? What do they need?
   - **Define** → What is the specific problem we're solving?
   - **Invent** → What is our proposed solution?
   - **Refine** → Write the PR/FAQ document.
   - **Test** → How will we validate and measure success?
4. **After each phase, STOP.** Present the full output to the user. Ask them to review and approve before moving to the next phase. Do NOT proceed without explicit user confirmation.
5. For each phase, load the corresponding skill from `skills/wb-*`.
6. Produce artifacts in `docs/working-backwards/` — customer profiles, problem statements, solution sketches, and the final PR/FAQ.

## Approval Gates (Non-Negotiable)

After completing each stage, present your output and ask: "Here's what I have for [Stage]. Does this look right? Anything to adjust before we move to [Next Stage]?" Wait for explicit approval. If the user asks for changes, revise and re-present. Only proceed after they confirm.

## Key Principles

- Customer obsession: every decision traces back to a customer need.
- Write the press release BEFORE writing code.
- If you can't write a clear FAQ answer, the idea isn't ready.
- Iterate: it's normal to loop between phases multiple times.

## Output

Create `docs/working-backwards/<feature-name>/` with:
- `customer-profile.md`
- `problem-statement.md`
- `solution-sketch.md`
- `prfaq.md`
- `success-metrics.md`
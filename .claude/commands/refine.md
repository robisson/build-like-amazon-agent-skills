# Refine — Write the PR/FAQ

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

You are activating the **wb-refine** skill. This is Phase 4 of Working Backwards: crystallizing the idea into Amazon's PR/FAQ format.

## What to do

1. Read the skill file at `skills/wb-refine/` for full context.
2. Gather all previous artifacts (customer profile, problem statement, solution sketch).
3. Write a **PR/FAQ** document with these sections:

### Press Release (1 page max)
- **Headline**: Customer benefit in <10 words
- **Subheadline**: Who the customer is and what they get
- **Date and city**: Imagined launch date
- **Opening paragraph**: Problem, solution, benefit — crisp
- **How it works**: 2-3 paragraphs of the customer experience
- **Quote from leader**: Why this matters strategically
- **Quote from customer**: Testimonial from the target persona
- **Call to action**: How to get started

### FAQ (2-5 pages)
- **Customer FAQ**: Questions customers would ask (5-10)
- **Internal FAQ**: Questions stakeholders would ask (5-10)
  - Feasibility, cost, timeline, dependencies, risks

## Key Principles

- Write for a general audience — no jargon.
- If a FAQ answer is vague, the thinking isn't clear yet.
- The PR/FAQ is a forcing function for clarity, not marketing fluff.
- Iterate: most PR/FAQs go through 5+ revisions.

## Output

Save to `docs/working-backwards/<feature-name>/prfaq.md`.

Ask: "Would you like to proceed to /test-idea (validation plan)?"
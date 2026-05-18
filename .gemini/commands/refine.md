<!-- MIRROR: This file mirrors .claude/commands/refine.md. Do not edit directly — sync from the Claude version. -->

# Refine — Write the PR/FAQ

Activate the **wb-refine** skill from `skills/wb-refine/`. Phase 4 of Working Backwards.

## Instructions

Crystallize the idea into Amazon's PR/FAQ format using all previous artifacts.

1. Gather customer profile, problem statement, and solution sketch.
2. Write a **PR/FAQ** document:

### Press Release (1 page max)
- **Headline**: Customer benefit in <10 words
- **Subheadline**: Who the customer is and what they get
- **Date/city**: Imagined launch date
- **Opening paragraph**: Problem → solution → benefit
- **How it works**: 2-3 paragraphs of customer experience
- **Leader quote**: Why this matters strategically
- **Customer quote**: Testimonial from target persona
- **Call to action**: How to get started

### FAQ (2-5 pages)
- **Customer FAQ** (5-10 questions customers would ask)
- **Internal FAQ** (5-10 questions on feasibility, cost, timeline, risks)

## Principles

- Write for a general audience — no jargon.
- Vague FAQ answers mean unclear thinking — iterate.
- This is a forcing function for clarity, not marketing fluff.
- Most PR/FAQs need 5+ revisions. That's normal.

## Output

Save to `docs/working-backwards/<feature-name>/prfaq.md`.
Suggest next step: "Run /test-idea to define success metrics."

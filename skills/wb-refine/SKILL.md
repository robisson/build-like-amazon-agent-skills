---
name: wb-refine
description: "Stage 4 of Working Backwards: Write the PR/FAQ — a press release announcing the product as if it already exists, plus a comprehensive FAQ addressing hard questions. This is the core Amazon mechanism that forces clarity, customer-centric thinking, and rigorous pre-mortems before any code is written."
leadership_principles:
  - Customer Obsession
  - Insist on the Highest Standards
  - Have Backbone; Disagree and Commit
  - Think Big
  - Earn Trust
---

# WB-Refine: The PR/FAQ

## Overview

The PR/FAQ is Amazon's most iconic product development mechanism. It is a document (typically 6-12 pages) consisting of a Press Release (1-1.5 pages) and a Frequently Asked Questions section (4-10 pages). The press release is written as if the product already exists and is being announced to customers. The FAQ section answers the hardest questions — both from customers (external FAQ) and from leadership/stakeholders (internal FAQ).

The PR/FAQ is NOT a marketing document. It is a **thinking tool**. Writing forces precision. The press release format forces customer-centricity. The FAQ format forces you to confront uncomfortable questions before you've invested months of engineering effort.

A PR/FAQ typically goes through 10-20 revisions before approval. This is intentional. Each revision sharpens the thinking, closes logical gaps, and strengthens the argument. A first draft is never good enough — if it is, the author isn't being honest about the hard questions.

## When to Use

- After completing Stage 3 (Invent) with a recommended solution
- As the primary decision artifact for any significant product investment
- When seeking leadership approval for resource allocation
- To align cross-functional teams (engineering, design, marketing, operations) on a shared vision
- When an existing initiative has lost clarity and needs to be re-grounded in customer value

## Agent Persona

Load `agents/doc-bar-raiser.md` when reviewing the PR/FAQ. Use it to evaluate narrative clarity, customer specificity, FAQ rigor, and whether the document is strong enough to proceed to design.

## Amazon Context

At Amazon, the PR/FAQ is read silently at the beginning of meetings. There are no presentations, no slides, no verbal pitches before reading. Everyone reads the document simultaneously (typically 20-30 minutes), then the discussion begins. This is deliberate:

- **Silent reading equalizes information.** Everyone has the same context, regardless of whether they got a "pre-read" or verbal briefing.
- **Full sentences force complete thoughts.** You can't hide behind bullet points in a narrative document.
- **The author does the hard thinking, not the reader.** In slide culture, the audience fills in the gaps. In document culture, the author must be explicit.

The document goes through a **Doc Bar Raiser** review — a senior person trained in evaluating PR/FAQs who provides structured feedback on:
- Clarity of customer definition
- Strength of the problem statement
- Compelling nature of the solution
- Rigor of the FAQ answers
- Quality of the writing itself

Common Doc Bar Raiser feedback:
- "Who specifically is this for? 'Developers' is not specific enough."
- "This FAQ answer doesn't actually answer the question."
- "Your press release headline wouldn't make a customer stop scrolling."
- "I count 3 solutions in here. Pick one."
- "What data supports this claim?"

## PR/FAQ Format Rules

These rules are NON-NEGOTIABLE. A PR/FAQ that violates these is structurally invalid and must be rewritten.

### Press Release Structure

1. **NO headers inside the Press Release.** The PR is a continuous narrative. No `##`, no `###`, no `**Section Name**` used as headers. It reads like a newspaper article.
2. **NO bullet lists in the Press Release.** Every point is expressed as narrative prose in paragraph form. Feature lists are forbidden.
3. **Narrative paragraphs only.** Each paragraph flows into the next. The PR tells a STORY, not a list.
4. **TWO quotes mandatory.** One spokesperson quote (VP/Director explaining WHY we built this). One customer quote (user describing their EXPERIENCE with the product). Both are required. No exceptions.
5. **Present tense.** Written as if the product launched TODAY. "Enables", "reduces", "is" — never "will enable", "is going to reduce".
6. **Benefits, not features.** Describe what CHANGES for the customer, not what technology you built. "Reduces diagnosis time from 4 hours to 5 minutes" not "Uses distributed tracing with Kafka event streams".
7. **One page maximum.** If the PR exceeds one page, cut. Conciseness is non-negotiable.
8. **10th-grade reading level.** No jargon. No undefined acronyms. A customer with no technical background must understand the PR.

### FAQ Structure

1. **Split into TWO distinct sections:** External FAQ (customer questions) and Internal FAQ (business/viability questions). Never combine them.
2. **External FAQ (5-8 questions):** What a CUSTOMER would ask. Pricing, migration, limitations, comparison to alternatives, data security, getting started.
3. **Internal FAQ (5-8 questions):** What LEADERSHIP/FINANCE would ask. Cost to build, timeline, team size, success metrics, risks, opportunity cost, dependencies.
4. **Honest answers.** At least 2 questions in each section must expose genuine limitations or uncomfortable truths.

### Visuals

1. **At least one visual is mandatory.** Architecture diagram, customer journey mockup, wireframe, or before/after comparison.
2. **Visuals support the narrative** — they help the reader SEE the customer experience.

## The Process (Detailed)

### Step 1: Write the Press Release

The press release follows a strict structure (see templates/prfaq-template.md):

1. **Headline:** The customer benefit in one sentence (what, for whom)
2. **Subheadline:** One sentence expanding on who benefits and how
3. **Opening paragraph:** City, date, announcement. What is it and why it matters
4. **Problem paragraph:** What's wrong today (from Stage 2 Define)
5. **Solution paragraph:** What the product does and how it works (from Stage 3 Invent)
6. **Quote from company leader:** Why we built this, connecting to mission
7. **Customer experience paragraph:** Walk through the experience step by step
8. **Quote from beta customer:** Validation in the customer's voice
9. **Getting started / availability:** How to start using it
10. **Call to action:** Next step for the reader

**Writing rules:**
- Write at a 10th-grade reading level (no jargon, no acronyms)
- Every sentence must be understandable by someone who has never heard of your company
- Lead with WHAT and WHY, not HOW (technology)
- The headline must make a customer stop and pay attention
- Use specific numbers where possible ("reduces X by 70%", "in under 5 minutes")
- One page maximum. If you need more, you haven't been concise enough

### Step 2: Write the External FAQ (Customer Questions)

5-10 questions that real customers would ask. Be honest — include the questions you HOPE they don't ask.

**Must-include questions:**
1. What is it? (Crisp 2-sentence answer)
2. Who is it for? (Specific segment)
3. How does it work? (User experience walkthrough)
4. How much does it cost? (Or pricing model)
5. How is this different from [obvious competitor/alternative]?
6. What are the limitations? (Be honest — trust is earned through transparency)
7. Is my data secure? (If applicable)
8. How do I get started?

**Honesty test:** If every FAQ answer makes the product look perfect, you're lying to yourself. Include at least 2 questions that expose genuine limitations or tradeoffs.

### Step 3: Write the Internal FAQ (Stakeholder Questions)

5-10 questions from leadership, partner teams, finance, legal, and skeptics:

**Must-include questions:**
1. How big is the opportunity? (TAM/SAM/SOM with assumptions)
2. Why will we win? (Competitive advantage, not just features)
3. What's the investment required? (People, time, infrastructure)
4. What are we NOT doing to do this? (Opportunity cost)
5. What's the biggest risk? (And mitigation plan)
6. How will we measure success? (Leading indicators in first 90 days)
7. What if we're wrong? (Reversibility, exit strategy)
8. Why now? (Why this half, this year, this team)
9. What dependencies do we have? (Other teams, third parties)
10. What will V2 look like? (Shows you've thought beyond launch)

**Rigor test:** For each answer, ask "would a skeptical VP accept this?" If not, strengthen the evidence or acknowledge the uncertainty.

### Step 4: Create Supporting Visuals

Depending on the product:
- **Customer journey mockup:** Screens, workflows, or interactions (even hand-drawn)
- **Architecture overview:** High-level system diagram (for technical products)
- **Business model canvas:** Revenue model, cost structure, key partnerships
- **Timeline / roadmap:** Phases from now to GA

Visuals are appendices. They support the narrative — they don't replace it.

### Step 5: Iterate (Minimum 3 Revisions)

**Revision 1: Self-review (Day 2)**
- Read the document fresh after sleeping on it
- Mark every sentence where you think "I'm not sure this is true"
- Tighten language (cut word count by 20%)
- Ensure press release tells a complete story WITHOUT the FAQ

**Revision 2: Peer review (Day 3-5)**
- Share with 2-3 colleagues who were NOT involved in writing
- Ask them: "After reading, what problem are we solving and for whom?"
- If their answer doesn't match your intent, rewrite — don't explain verbally
- Incorporate feedback that strengthens clarity; push back on feedback that adds complexity

**Revision 3: Bar raiser / senior review (Day 6-10)**
- Share with a Doc Bar Raiser or senior leader
- Expect hard questions and non-obvious objections
- Revise based on feedback, then re-submit
- Repeat until approved (some documents take 10+ revisions)

### Step 6: Submit for Decision

The PR/FAQ is presented in a review meeting:
1. Document distributed (or read silently in the room)
2. 20-30 minutes of silent reading
3. Discussion starts with the most senior person asking the first question
4. Author responds to questions, takes notes on feedback
5. Meeting ends with: Approved / Approved with changes / Not approved (revise and return)

### Final Step: Present and Wait for Approval

Present your complete PR/FAQ document to the user. Ask:
- "Here's the PR/FAQ I've drafted for the Refine stage. Please review it carefully."
- "What needs changing? Any sections that don't land, questions missing from the FAQ, or framing issues?"

Wait for the user to respond with explicit approval or requested changes.

- If they request changes → revise the PR/FAQ → re-present → ask again.
- If they approve → proceed to Stage 5 (Test & Iterate).

⛔ DO NOT proceed to the Test & Iterate stage until the user explicitly approves or says to continue.

## Alternative Document Formats

Not every initiative needs a full PR/FAQ. Amazon uses these lighter formats:

| Format | Length | When to Use |
|--------|--------|-------------|
| **5 Customer Questions** | 1 page | Initial screening, brainstorming |
| **Dear Customer Letter** | 2-3 pages | Incremental features, existing products |
| **PR/FAQ** | 6-12 pages | New products, significant investments |
| **PRFAQ + Appendix** | 12-20+ pages | Major strategic initiatives, new businesses |

See templates/ folder for all formats.

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "We'll write it up clearly" | Specific template structure enforced. Doc Bar Raiser reviews for compliance |
| "We'll get feedback" | Minimum 3 revision cycles with documented feedback. First drafts never approved |
| "We'll address hard questions" | FAQ section must include uncomfortable questions. Reviewer specifically checks for "softball" FAQs |
| "We'll be customer-focused" | Press release must be readable by a customer with no inside knowledge. Jargon = rejection |
| "Leadership will support this" | Document is the decision mechanism. No verbal approval. No slide deck. The document must stand alone |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "PR/FAQs are just bureaucracy" | The PR/FAQ IS the thinking. Without it, you're making investment decisions based on vibes and verbal pitches | Embrace the process. Teams that write rigorous PR/FAQs ship better products faster because they solve the right problem the first time |
| "Our first draft is good enough" | First drafts are never good enough. They contain ambiguity, optimistic assumptions, and unanswered questions that only surface through review | Plan for 3+ revisions. Calendar time for peer review and Bar Raiser feedback. Budget 2-3 weeks total |
| "The FAQ is just for formality" | The FAQ is where the real thinking happens. The press release is the vision; the FAQ is the stress test. Weak FAQs = unstressed plans | Include questions you're afraid of. "What if adoption is 50% of our projection?" "What if the key technical bet fails?" Answer honestly |
| "We need to start building while we write" | Building before the PR/FAQ is approved means you might build the wrong thing. The PR/FAQ prevents waste, not speed | Writing a good PR/FAQ takes 2-3 weeks. Building the wrong thing takes 6-12 months. The math is obvious |
| "This is a technical initiative, customers won't see it" | Every technical initiative exists to serve a customer outcome. If you can't articulate the customer benefit, you can't prioritize against alternatives | Find the customer. "Reduced deploy time for engineers" IS a customer benefit. "Refactored the caching layer" is not. Connect to outcomes |

## Red Flags

- Press release headline describes technology, not customer benefit
- No specific customer quote (even hypothetical) in the press release
- FAQ section has only easy questions with obvious answers
- Internal FAQ doesn't address competitive risk or failure scenarios
- Document was written by one person without peer review
- First draft submitted for leadership review (no iterations)
- The "customer" in the press release is actually the team building the product
- No numbers anywhere in the document (no sizing, no timeline, no metrics)
- Document reads as an internal proposal, not a customer announcement
- The problem paragraph doesn't make the reader feel urgency
- Multiple solutions described (pick one)
- FAQ answers are longer than the press release (proportion suggests unfocused thinking)
- **⛔ STRUCTURAL:** Bullet lists or numbered lists appear inside the Press Release section (PR must be pure narrative paragraphs)
- **⛔ STRUCTURAL:** Section headers (##, ###) appear inside the Press Release (PR has no internal headers — it reads like a news article)
- **⛔ STRUCTURAL:** Feature dumps instead of customer benefits ("supports gRPC, Kafka, and Redis" instead of "reduces response time by 80%")
- **⛔ STRUCTURAL:** Missing spokesperson quote OR missing customer quote (both are mandatory)
- **⛔ STRUCTURAL:** FAQ not split into External and Internal sections (they serve different audiences and must be separate)
- **⛔ STRUCTURAL:** No visuals section (at least one diagram, mockup, or wireframe is required)
- **⛔ STRUCTURAL:** Written in future tense ("will enable", "is going to") instead of present tense ("enables", "is")

## Verification

Before submitting for leadership decision:

- [ ] Press release is ≤1.5 pages and tells a complete story standalone
- [ ] Headline communicates customer benefit (not technology or company achievement)
- [ ] Problem paragraph uses customer language and cites data
- [ ] Solution paragraph describes the experience, not the architecture
- [ ] At least one customer quote (real or realistic) validates the value proposition
- [ ] External FAQ includes ≥2 genuinely hard questions with honest answers
- [ ] Internal FAQ addresses: sizing, competition, risk, investment, and timing
- [ ] Document has been through ≥3 revision cycles with substantive feedback
- [ ] A Doc Bar Raiser (or equivalent) has reviewed and approved the document quality
- [ ] Any reader can explain what we're building, for whom, and why after reading only the PR
- [ ] Supporting visuals are included as appendices (not inline clutter)
- [ ] Writing is at 10th-grade reading level (no unexplained jargon or acronyms)

## Tenets

1. **The document is the decision.** Not a slide deck, not a verbal pitch, not a whiteboard drawing. If it's not in the document, it doesn't exist. If it's unclear in the document, it's unclear in the thinking.
2. **Write for the customer, not for yourself.** Every sentence in the press release must be meaningful to someone who has never heard of your company or technology. If an outsider can't understand it, simplify.
3. **Hard questions are a gift.** FAQ questions that make you uncomfortable are the most valuable. They reveal assumptions you haven't stress-tested. Seek them out. Answer them honestly.
4. **Iterate until it's clear, not until you're tired.** If the document isn't clear after 3 revisions, the thinking isn't clear. The fix is more thinking, not more polish.
5. **Disagree during review, commit after approval.** The PR/FAQ review process is where intellectual debate happens. Once approved, the team executes with full commitment. Relitigating during execution is destructive.

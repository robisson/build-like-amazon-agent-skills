# Anatomy of a SKILL.md

## Overview

Every skill in this repository follows a consistent format. This document explains each section, its purpose, and the rules for writing new skills.

---

## File Structure

Skills live in `skills/<skill-name>/SKILL.md`. Some skills have additional files:
- `skills/<skill-name>/templates/` — Templates related to the skill
- `skills/<skill-name>/examples/` — Real-world examples
- `skills/<skill-name>/checklists/` — Standalone checklists

---

## Format Specification

### Frontmatter (Required)

```yaml
---
name: Human-Readable Skill Name
description: One-sentence description of what this skill covers and why it matters.
leadership_principles:
  - Customer Obsession
  - Ownership
  - (2-4 most relevant principles)
---
```

**Rules**:
- `name`: Title case, 2-5 words
- `description`: Single sentence, <150 characters, states what and why
- `leadership_principles`: List 2-4 most relevant Amazon Leadership Principles. These are not decoration—they ground the skill in the cultural framework

---

### Overview (Required)

A 3-5 sentence paragraph that explains:
1. What this skill/practice is
2. Why it exists (what problem it prevents)
3. What the outcome looks like when done well

**Rules**:
- No bullet points — flowing prose
- Written for someone who has never heard of this practice
- Must answer: "Why should I care?"
- No jargon without explanation

---

### When to Use (Required)

Bullet list of specific situations where this skill applies.

**Rules**:
- 5-8 concrete scenarios
- Each starts with a gerund (-ing) or "When" or "After"
- Specific enough that a reader can recognize their situation
- Include both obvious cases and non-obvious ones

---

### Amazon Context (Required)

2-3 paragraphs explaining why Amazon does this, what problems it solved, and what happens when teams don't follow it.

**Rules**:
- Connect to real consequences (incidents, customer impact, team dysfunction)
- Explain the scale factor: "This matters more at scale because..."
- Don't be hagiographic — explain the reasoning, not just the authority
- Include the failure mode: what happens when this ISN'T followed

---

### The Process (Required)

The detailed step-by-step process for executing this skill.

**Rules**:
- Numbered steps within each phase
- Specific actions, not vague directions
- Include timing, thresholds, and acceptance criteria where applicable
- Distinguish between required steps and recommended steps
- Use sub-headings for distinct phases

---

### Mechanisms Over Good Intentions (Required)

A table showing how good intentions are insufficient without automated mechanisms.

**Format**:
```markdown
| Intention | Mechanism |
|-----------|-----------|
| "I'll remember to..." | Automated system that enforces... |
```

**Rules**:
- 4-6 rows
- Left column: What a well-intentioned person SAYS they'll do
- Right column: The automated mechanism that GUARANTEES it happens
- Mechanisms must be specific and implementable

---

### Common Rationalizations (Required)

A 3-column table showing excuses, why they're wrong, and what to do instead.

**Format**:
```markdown
| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
```

**Rules**:
- 4-6 rows
- Left column: Direct quotes you'll hear from teams resisting the practice
- Middle column: Specific explanation of why the rationalization fails
- Right column: Concrete alternative action

---

### Red Flags (Required)

Bullet list of warning signs that this skill is not being followed correctly.

**Rules**:
- 8-12 items
- Observable behaviors (things you can see or measure)
- Written as statements, not questions
- Include both "not doing it at all" and "doing it poorly" signals

---

### Verification (Required)

Checklist of items to verify the skill is being applied correctly.

**Format**:
```markdown
- [ ] Specific verifiable condition
```

**Rules**:
- 8-12 items
- Each item is independently verifiable (yes/no)
- Cover the most important aspects of the skill
- Ordered from most critical to least critical
- A team should be able to self-assess against this checklist

---

### Tenets (Required)

5 principles that capture the essence of this skill.

**Rules**:
- Exactly 5 tenets
- Each is one sentence (bold), followed by one sentence explanation
- Written as beliefs/principles, not rules
- Should be memorable and quotable
- Ordered from most fundamental to most nuanced

---

## Writing Guidelines

### Voice and Tone

- **Direct**: State things plainly. "Do X" not "It might be beneficial to consider X"
- **Specific**: Numbers, thresholds, timeframes. Not "quickly" but "within 5 minutes"
- **Opinionated**: Take a clear stance. These are best practices, not suggestions
- **Practical**: Every sentence should lead to action or understanding
- **Honest**: Acknowledge trade-offs. Don't pretend practices are free

### What to Avoid

- **Hedging language**: "might", "could", "consider", "it depends" (unless you explain what it depends ON)
- **Abstract benefits**: "improves quality" (how? by what measure?)
- **Placeholder content**: Nothing marked TODO, TBD, or "to be determined"
- **Implementation details**: Skills describe WHAT and WHY, not specific tool configurations
- **Length for length's sake**: If a section can be shorter, make it shorter

### Quality Checklist for Skill Authors

Before submitting a new skill:

- [ ] Frontmatter is complete and accurate
- [ ] Overview answers "why should I care?" in <5 sentences
- [ ] When to Use lists 5+ specific scenarios
- [ ] Amazon Context explains consequences of not following the skill
- [ ] The Process has numbered, actionable steps with specific criteria
- [ ] Mechanisms table has 4+ rows with implementable mechanisms
- [ ] Rationalizations table addresses real objections you've heard
- [ ] Red Flags are observable (not just "not doing it well")
- [ ] Verification checklist items are independently verifiable
- [ ] Tenets are memorable and capture the essence
- [ ] No placeholder content (TODO, TBD)
- [ ] Someone unfamiliar with the topic can follow it

# Philosophy: Amazon's Engineering Culture Encoded as Skills

## Why Encode Engineering Culture?

Amazon's engineering culture is built on **mechanisms** — repeatable processes that produce consistent outcomes regardless of who executes them. This makes it uniquely well-suited for AI agent skills: every step is specific, verifiable, and enforceable.

The principles below explain why this skill set works the way it does.

---

## 1. Mechanisms Over Good Intentions

> "Good intentions don't work. Mechanisms do." — Jeff Bezos

A mechanism is a complete process that makes the right thing happen automatically. It has four parts:

1. **The tool** — what you use (template, checklist, automation)
2. **The adoption** — how people start using it (training, defaults)
3. **The inspection** — how you verify it's being followed (metrics, audits)
4. **The correction** — what happens when it fails (escalation, improvement)

Every skill in this repository is a mechanism. It doesn't rely on engineers "remembering to do the right thing" — it encodes the right thing as a workflow with verification steps.

**Example**: The `progressive-deployment` skill doesn't say "deploy carefully." It specifies: one-box for 1 hour → one-AZ for 4 hours → regional for 24 hours, with automated rollback if alarms fire. That's a mechanism.

---

## 2. Bar Raisers at Every Stage

Quality doesn't come from a final review at the end — it comes from **raising the bar continuously**. In Amazon's culture, specialized reviewers exist at every stage:

| Stage | Bar Raiser | What They Enforce |
|-------|-----------|-------------------|
| Working Backwards | Doc Bar Raiser | Clarity, customer obsession, data |
| Design | Design Bar Raiser + PE | Trade-offs, scalability, simplicity |
| Code | Code Review Bar Raiser | Quality, testability, operational readiness |
| Security | Security Guardian | Threat model, IAM, data handling |
| Operations | Ops Bar Raiser | Alarms, runbooks, "can you operate at 3AM?" |
| Post-incident | COE Reviewer | Real root cause, mechanisms > blame |

In this skill set, each bar raiser is an **agent persona** that can review artifacts at its stage. The agent asks hard questions, flags issues, and can recommend blocking progression until concerns are addressed.

---

## 3. Ownership End-to-End

> "You build it, you run it."

The team that writes the code is the team that operates it in production. This principle means:

- Skills don't separate "dev skills" from "ops skills" — they form a **continuous lifecycle**
- The `operational-code` skill ensures observability is built in from day one, not bolted on later
- The `operational-readiness-review` skill ensures you can operate before you launch
- The operational skills assume the builder is accountable for production outcomes

---

## 4. Working Backwards From the Customer

Everything starts with the customer. Not with the technology, not with the architecture, not with what's easy to build. The Working Backwards process (5 stages) exists to prevent the most common failure: building something nobody needs.

The skills encode this as:
- You cannot start building without a PR/FAQ or 5CQ
- The PR/FAQ is written in customer language, not technical language
- Metrics of success are defined before implementation begins
- The lifecycle is **circular** — lessons from production feed back into Working Backwards

---

## 5. Two-Way Doors vs. One-Way Doors

Not every decision deserves the same rigor. Amazon classifies decisions:

- **One-way doors** (irreversible, high-consequence): Full process, multiple bar raisers, explicit sign-off. Examples: API contracts, data model schemas, public interfaces.
- **Two-way doors** (reversible, low-consequence): Lighter process, bias for action, iterate quickly. Examples: feature flag experiments, internal tool choices, algorithm tweaks.

Skills explicitly mark decision points with 🔒 (one-way) or 🚪 (two-way) to calibrate the appropriate level of rigor.

---

## 6. Circular Lifecycle

The most important arrow in the system is the one from **Learn → Working Backwards**. Every COE, every metrics review, every operational lesson feeds directly into the next iteration.

```
WB → Design → Spec → Build → Deploy → Operate → Learn
 ↑                                                  │
 └──────────────── (feedback loop) ─────────────────┘
```

This compounding quality loop is what separates good teams from great ones. A team that writes 10 COEs and creates 10 mechanisms is exponentially more reliable than one that writes 10 COEs and hopes people remember the lessons.

---

## 7. Write It Down

Amazon is a writing culture. Narratives force clarity of thought in ways that slides and verbal discussions cannot:

- PR/FAQs force you to articulate customer value before building
- Design Documents force you to consider alternatives and trade-offs
- COEs force you to find root causes and create mechanisms
- Spec requirements (EARS notation) force you to be unambiguous and testable

Every skill produces **written artifacts** — not because documentation is the goal, but because the act of writing forces rigorous thinking.

---

## 8. Simplicity as a Feature

> "The best systems are simple systems. Complexity is not a sign of thoroughness — it's a sign of unresolved trade-offs."

Skills actively fight complexity:
- `incremental-implementation` enforces thin vertical slices over big-bang rewrites
- `design-document` requires listing alternatives and justifying why simpler options were rejected
- `mechanism-creation` asks "what's the simplest automation that prevents recurrence?"
- Every `Common Rationalizations` table includes entries about unnecessary complexity

---

## Summary

| Principle | How It's Encoded |
|-----------|-----------------|
| Mechanisms over intentions | Every skill is a complete mechanism with verification |
| Bar raisers everywhere | 10 agent personas covering every stage |
| End-to-end ownership | Lifecycle skills from WB through Operate |
| Customer backwards | WB skills gate progression until customer value is clear |
| Decision classification | 🔒/🚪 markers on decision points |
| Circular lifecycle | Learn feeds WB; COEs create mechanisms |
| Write it down | Every skill produces written artifacts |
| Simplicity | Anti-rationalization tables fight complexity |

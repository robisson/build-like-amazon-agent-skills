# 5 Customer Questions (5CQ) Template

## Instructions

The 5 Customer Questions are a lightweight tool for quickly evaluating whether an idea has substance before committing to a full PR/FAQ process. Answer each question in 1-3 sentences. The entire document should take 30-60 minutes to write.

**When to use 5CQ:**
- Brainstorming sessions to screen multiple ideas quickly
- Hack-a-thons and innovation sprints
- Initial validation before investing in full Working Backwards
- Feature proposals that may not warrant a full PR/FAQ
- Responding to leadership when they ask "what are you thinking about?"

**The bar for 5CQ:** If you can't answer all 5 questions clearly, the idea isn't ready for any investment — not even further research. If you CAN answer all 5, you've earned the right to decide whether a full WB process (PR/FAQ) is warranted.

---

## 5CQ DOCUMENT

**Initiative Name:** [Short, memorable name]

**Author:** [Name]

**Date:** [Date]

**Status:** Draft / Under Review / Approved for PR/FAQ / Parked

---

### 1. Who is the customer?

[Name a specific, observable customer segment. Not "everyone." Not "developers." Include role, context, and an observable characteristic that makes them findable.]

*Good example: "Senior data engineers at enterprise companies (1000+ employees) who manage more than 50 data pipelines and currently use Apache Airflow."*

*Bad example: "Data professionals who want better tools."*

**Segment size estimate:** [How many of these customers exist? Source?]

---

### 2. What is the customer's problem or opportunity?

[State the problem in the customer's words — the language they would use at their desk, not your technical framing. Include when this problem occurs and what it costs them.]

*Good example: "When a data pipeline fails at 3 AM, these engineers are paged and spend 45-90 minutes identifying which of their 50+ pipelines failed, why, and which downstream consumers are affected — before they can even start fixing it."*

*Bad example: "They need better observability for their data infrastructure."*

**Evidence:** [What data supports this? Interviews, tickets, analytics, market research?]

---

### 3. What is the most important customer benefit?

[Single benefit. Clear enough to be a press release headline. Stated as an outcome for the customer, not a feature of the product.]

*Good example: "Identify the root cause of any data pipeline failure in under 5 minutes, without needing to check multiple tools or dashboards."*

*Bad example: "Unified observability platform with AI-powered root cause analysis."*

**Measurable improvement:** [How much better is this than today? X% faster? Y hours saved?]

---

### 4. How do you know what the customer needs?

[Cite specific evidence. Not "we believe" or "it's obvious." What conversations, data, research, or observations support your understanding?]

*Good example: "12 customer interviews (March 2026), 340 support tickets about pipeline debugging in Q1, and internal telemetry showing 73% of pipeline failures take >2 hours to diagnose."*

*Bad example: "We've seen competitors launch similar products, so there must be demand."*

**Confidence level:** [High (direct customer data) / Medium (proxy data) / Low (hypothesis only)]

---

### 5. What does the customer experience look like?

[Describe the end-to-end experience in 3-5 concrete steps. What does the customer DO? What do they SEE? Write it like a user story walkthrough.]

*Good example:*
1. *Pipeline fails at 3:07 AM. Engineer receives a single alert (not 15 cascading alerts).*
2. *Alert includes: which pipeline, probable root cause (ranked), and list of affected downstream consumers.*
3. *Engineer opens the investigation view, sees a correlated timeline of events leading to failure.*
4. *One-click remediation for common failure types (retry, skip bad record, scale resources).*
5. *Downstream consumers are automatically notified with ETA for data availability.*

*Bad example: "The product gives them a dashboard with all their pipeline information."*

---

## DECISION GATE

After completing the 5CQ, answer:

| Question | Answer |
|----------|--------|
| Can you name 3 specific people who have this problem? | Yes / No |
| Is the customer segment large enough to matter? (>$XM opportunity) | Yes / No |
| Do you have evidence beyond intuition? | Yes / No |
| Is the benefit compelling enough for a press release headline? | Yes / No |
| Can you describe the experience without referencing technology? | Yes / No |

**If all Yes:** Proceed to full Working Backwards (PR/FAQ)
**If 3-4 Yes:** Spend 1-2 weeks on targeted research to fill gaps, then re-evaluate
**If ≤2 Yes:** Park the idea. Return when you have more evidence or a sharper framing

---

## NEXT STEPS

- [ ] 5CQ reviewed by at least one peer
- [ ] Decision: Proceed to full WB / Research needed / Park
- [ ] If proceeding: Assign owner for PR/FAQ, set target completion date
- [ ] If research needed: Define specific questions to answer and timeline

---

## COMPARISON: Multiple Ideas

*When evaluating multiple ideas in a brainstorming session, use this summary table:*

| Criterion | Idea A | Idea B | Idea C |
|-----------|--------|--------|--------|
| Customer specificity | [1-5] | [1-5] | [1-5] |
| Problem clarity | [1-5] | [1-5] | [1-5] |
| Benefit compellingness | [1-5] | [1-5] | [1-5] |
| Evidence strength | [1-5] | [1-5] | [1-5] |
| Experience clarity | [1-5] | [1-5] | [1-5] |
| **TOTAL** | | | |

*Advance the top 1-2 scoring ideas to full Working Backwards. Park the rest — don't abandon them permanently, but don't split focus.*

---
name: Correction of Errors
description: Blameless post-incident analysis focused on timeline, 5 Whys, mechanisms over people, and concrete action items with owners.
leadership_principles:
  - Ownership
  - Earn Trust
  - Dive Deep
  - Insist on the Highest Standards
  - Learn and Be Curious
---

# Correction of Errors (COE)

## Overview

A [Correction of Errors (COE)](https://www.youtube.com/watch?v=Prd2VvSo_p8) is a blameless post-incident document that analyzes what happened, why it happened, and what mechanisms will prevent recurrence. The goal is not to assign blame—it is to improve the system so the same class of failure cannot happen again. COEs produce mechanisms (automated safeguards), not promises ("we'll be more careful"). Every COE must result in concrete action items with owners and due dates that make the system more resilient.

## When to Use

- After any incident that reveals a systemic gap (even if low severity)
- After near-misses that could have been highly severy with slightly different conditions
- When the same type of failure recurs (even at low severity)
- When requested by leadership for learning purposes

## Agent Persona

Load `agents/coe-reviewer.md` when reviewing a COE. Use it to enforce blameless analysis, timeline accuracy, root-cause depth, mechanism quality, and concrete action items with owners and dates.

## Amazon Context

Amazon's COE process is one of its most powerful learning mechanisms. The document is written by the team that experienced the incident, reviewed by senior leadership, and shared broadly for organizational learning. The key insight: people don't cause failures—systems allow failures. If a single person's mistake can cause a customer-impacting incident, the system lacks sufficient safeguards. COEs that conclude "the engineer should have been more careful" are rejected. COEs that conclude "we will add an automated check that prevents this class of error" are accepted.

## The Process

### Timeline (Within 24 hours of incident)

1. Incident Commander or on-call engineer drafts initial timeline
2. All participants review and add their perspective
3. Timeline must include:
   - Exact times (timezone-explicit) for each event
   - What was observed at each point
   - What actions were taken and by whom
   - What information was available (and what wasn't)
   - When customer impact started and ended

### 5 Whys Analysis

Start with the customer impact and ask "why" until you reach systemic root causes:

1. **Why** were customers affected? → Service returned 500 errors for 23 minutes
2. **Why** did the service return 500s? → Database connections were exhausted
3. **Why** were connections exhausted? → A code change introduced a connection leak
4. **Why** wasn't the leak caught? → Integration tests don't measure connection pool behavior
5. **Why** wasn't it detected earlier? → No alarm on connection pool utilization

Root causes from this example:
- Missing test coverage for resource management
- Missing operational alarm for connection pool health
- Code review didn't catch the missing connection close

### Writing the COE

**Section 1: Summary**
- One paragraph: What happened, when, customer impact, duration
- Severity level and scope (customers affected, regions, revenue impact)

**Section 2: Customer Impact**
- What did customers experience?
- How many customers were affected?
- What was the duration of impact?
- Were there any data loss or consistency issues?

**Section 3: Timeline**
- Minute-by-minute account of the incident
- Include detection time, mitigation actions, resolution time

**Section 4: Root Cause Analysis (5 Whys)**
- The complete 5 Whys chain(s)
- Identify contributing factors vs. root causes
- Multiple root cause chains are common and expected

**Section 5: Action Items**
- Each action item has: description, owner (individual), due date, status
- Categories: Immediate (7 days), Short-term (30 days), Long-term (90 days)
- Must include at least one mechanism (automated safeguard)
- "Be more careful" is never an acceptable action item

**Section 6: Lessons Learned**
- What went well during the incident response?
- What could have been done better?
- Are there broader organizational lessons?

### COE Review

1. Team reviews internally first (ensures accuracy)
2. Manager reviews for completeness and mechanism quality
3. Senior leadership reviews for organizational learning opportunities
4. Shared with broader organization (relevant teams, COE digest)

### Action Item Tracking

- All action items entered in tracking system with due dates
- Reviewed in the recurring Metrics Review cadence
- Overdue items escalated to manager, then skip-level
- COE not "closed" until all action items are completed
- Quarterly review of action item completion rates

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "We'll be more careful during code review" | Automated static analysis that detects the specific pattern that caused the incident |
| "We'll remember to check that next time" | Automated pre-deploy check that verifies the condition |
| "The on-call will know to look for this" | Alarm that automatically detects this condition and pages |
| "We'll test this scenario" | Integration test added to the pipeline that fails if this scenario recurs |
| "We'll document this for future reference" | Runbook entry with specific steps, linked to the relevant alarm |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "It was a human error" | Humans always make errors. The question is: why did the system allow it to cause customer impact? | Identify the missing safeguard. Add automation that catches this error before it reaches production |
| "It was an edge case we couldn't predict" | If it happened, it can happen again. Every edge case needs a mechanism once discovered | Add the test case, add the alarm, add the guard. "Unpredictable" means "we hadn't thought about it yet" |
| "We were unlucky" | Luck is not an operational strategy. If a system can fail given bad luck, it will | Design for resilience. Assume failure will happen and build safeguards |
| "We need to train people better" | Training fades. People rotate. Knowledge is lost | Build the knowledge into the system: automated checks, guardrails, circuit breakers |

## Red Flags

- COE that blames an individual ("John deployed without checking")
- Action items that are all "be more careful" or "remember to check"
- No mechanism-based action items
- COE written 2+ weeks after the incident (memory fades)
- Action items with no owner or no due date
- Same root cause appearing in multiple COEs (action items not effective)
- COE never shared beyond the immediate team
- Action items never completed (marked "will not fix")
- Timeline missing key decision points
- No mention of what went well (discourages future good behavior)

## Verification

- [ ] Timeline is complete with exact timestamps
- [ ] 5 Whys reaches systemic root causes (not human error)
- [ ] At least one action item creates an automated mechanism
- [ ] Every action item has an owner and due date
- [ ] COE reviewed by manager and senior leadership
- [ ] COE shared with relevant broader teams
- [ ] Action items tracked in operational review
- [ ] No blame language in the document
- [ ] Similar incident from the past? Check if previous COE actions were completed

## Tenets

1. **Blameless means systemic.** If your conclusion requires a person to have done something differently, dig deeper into why the system allowed it.
2. **Mechanisms over promises.** "We will" is not a solution. "The system will automatically" is a solution.
3. **Every incident is a gift.** It revealed a weakness you didn't know about. Fix it before it happens again at larger scale.
4. **Share broadly.** The same failure patterns exist across teams. One team's COE prevents another team's severity.
5. **Action items are commitments.** They are not suggestions. They have owners, dates, and tracking. Incomplete action items mean the COE failed.

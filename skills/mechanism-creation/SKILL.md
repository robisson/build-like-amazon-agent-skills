---
name: Mechanism Creation
description: Turning lessons learned into automated mechanisms that prevent recurrence of problems.
leadership_principles:
  - Invent and Simplify
  - Insist on the Highest Standards
  - Ownership
  - Think Big
---

# Mechanism Creation

## Overview

A mechanism is an automated system, process, or tool that prevents a known class of failure without requiring human vigilance. Mechanisms replace good intentions with guaranteed outcomes. When you discover a problem—through COEs, operational reviews, or metrics analysis—the highest-quality response is not "we'll be more careful" but "we'll build a mechanism that makes this class of error impossible." Mechanisms are Amazon's primary tool for converting incidents into permanent improvements.

## When to Use

- After any COE identifies a systemic gap
- When the same type of issue recurs despite awareness
- When a manual process is the only thing preventing failure
- When a checklist item is routinely missed
- When "human error" is cited as a root cause (this means a mechanism is missing)
- When scaling a process beyond what human attention can reliably cover

## Amazon Context

Jeff Bezos famously said: "Good intentions don't work. Mechanisms do." This captures a core Amazon principle: you cannot rely on people to consistently do the right thing under pressure, fatigue, or time constraints. Instead, you build systems that make the right thing automatic and the wrong thing difficult or impossible. Every recurring problem at Amazon is eventually addressed by a mechanism. Teams that rely on training, documentation, or vigilance instead of mechanisms eventually have the same incident again.

## The Process

### Identifying Mechanism Opportunities

Look for these signals that a mechanism is needed:

1. **Recurring incidents**: Same root cause appears in 2+ COEs
2. **Human-dependent safeguards**: "The engineer checks X before Y" — what happens when they forget?
3. **Manual checklists**: Steps that must be performed in order — what happens when step 3 is skipped?
4. **Training-dependent processes**: "New hires are trained on this" — what happens before training?
5. **"We'll be more careful" action items**: If the solution requires sustained human attention, it will fail
6. **Scaling breakdowns**: Process that worked with 3 people but fails with 30

### Mechanism Design Principles

**Principle 1: Prevent, don't detect**
- Best: Make the error impossible (e.g., type system prevents invalid states)
- Good: Block the error before it reaches production (e.g., automated gate)
- Acceptable: Detect and auto-remediate quickly (e.g., alarm + automatic rollback)
- Worst: Detect and alert a human (e.g., alarm + manual intervention)

**Principle 2: Fail closed, not open**
- If the mechanism itself fails, the default should be safe (block, not allow)
- Example: If the deployment alarm check can't reach the alarm system, block the deploy (don't proceed assuming everything is fine)

**Principle 3: Zero human action required in the happy path**
- The mechanism should work without anyone knowing it exists
- Humans should only be involved when the mechanism catches something

**Principle 4: Provide clear feedback when triggered**
- When the mechanism blocks or catches something, explain why
- Include: what was caught, why it's dangerous, what to do instead
- Poor feedback leads to people working around the mechanism

**Principle 5: Make it easy to do the right thing**
- Don't just block the wrong path—illuminate the right path
- Example: Don't just reject a deployment; show the developer what alarm is firing and link to the runbook

### Mechanism Categories

**Pipeline Mechanisms** (prevent bad code from reaching production)
- Static analysis rules for known-bad patterns
- Automated test coverage requirements
- Security scanning gates
- Deployment blocker on active alarms
- Mandatory bake time enforcement

**Runtime Mechanisms** (prevent bad behavior in production)
- Circuit breakers for dependency failures
- Rate limiters for traffic spikes
- Automatic scaling for capacity
- Timeout enforcement on all network calls
- Retry with exponential backoff and jitter

**Operational Mechanisms** (prevent operational mistakes)
- Automated alarm on metric degradation
- Automatic rollback on deployment failure
- Stale ticket escalation
- On-call fatigue alerts
- Feature flag expiration enforcement

**Process Mechanisms** (prevent process gaps)
- PR/FAQ required before design (template enforcement)
- Design review required before implementation (pipeline gate)
- Operational readiness review required before launch
- COE required after P1/P2 incidents (automatic ticket creation)
- Recurring metrics review report generation

### Building the Mechanism

1. **Define the failure mode**: What specific thing goes wrong?
2. **Define the trigger condition**: What signals that this failure is about to happen or has happened?
3. **Define the automated response**: What should happen without human intervention?
4. **Define the escape valve**: How does a human override if the mechanism is wrong?
5. **Define success metrics**: How do you know the mechanism is working?
6. **Test the mechanism**: Verify it triggers correctly (and doesn't false-positive excessively)
7. **Monitor the mechanism**: Track trigger rate, false positives, and overrides

### Mechanism Evaluation

After deploying a mechanism, evaluate:
- **Trigger rate**: How often does it fire? (Too often = too sensitive or systemic issue)
- **False positive rate**: How often does it fire incorrectly? (Target: <5%)
- **Override rate**: How often is it overridden? (High override = wrong threshold or bad design)
- **Prevention effectiveness**: Did the target class of failure stop recurring?
- **Developer experience**: Do engineers understand why it triggered and what to do?

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "Developers will write tests" | Coverage gate blocks merge below threshold |
| "We'll deploy carefully" | Pipeline enforces progressive deployment with automatic rollback |
| "We'll monitor after launch" | Launch blocked without operational readiness review completion |
| "We'll update documentation" | Stale doc detection alerts owners when docs haven't been updated in 90 days |
| "We'll clean up tech debt" | Tech debt tickets auto-escalate to manager at 30 days age |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "We just need better training" | Training fades. People leave. New hires join. The gap returns | Build the knowledge into an automated check that enforces the standard |
| "A mechanism is overkill for this" | If the problem has occurred more than once, it's not overkill | The cost of building a mechanism is almost always less than the cost of the next incident |
| "We'll add the mechanism later, first let's ship" | "Later" never comes. Ship with the mechanism or accept the risk explicitly | If you know the failure mode, prevent it now. Don't create known risk |
| "People will work around it" | If people work around your mechanism, either the mechanism is wrong or you need enforcement | Investigate WHY they work around it. Fix the mechanism or the incentive |

## Red Flags

- COE action items that don't include at least one mechanism
- Same incident type occurring 3+ times without a mechanism
- Mechanisms that are always overridden (wrong threshold or bad design)
- Mechanisms with no monitoring (you don't know if they're working)
- Mechanisms without escape valves (they'll be bypassed entirely when they block incorrectly)
- "Be more careful" as a solution to a systemic problem
- Manual processes that are critical to service safety
- Mechanisms that block without explaining why or what to do instead
- No tracking of mechanism effectiveness after deployment

## Verification

- [ ] Every COE produces at least one mechanism-based action item
- [ ] Mechanisms are automated (no human action required in happy path)
- [ ] Mechanisms fail closed (safe default when mechanism itself fails)
- [ ] Mechanisms provide clear feedback when triggered
- [ ] Mechanisms have escape valves for legitimate overrides
- [ ] Override usage is tracked and reviewed (high override = problem)
- [ ] Mechanism effectiveness is measured (did target failures decrease?)
- [ ] False positive rate is tracked (target: <5%)
- [ ] Mechanisms are tested (confirmed they trigger correctly)
- [ ] Team can list their top 5 mechanisms and what each prevents

## Tenets

1. **Good intentions don't work. Mechanisms do.** If it requires sustained human vigilance, it will eventually fail.
2. **Prevent rather than detect.** The best mechanism makes the failure impossible, not just visible.
3. **Every mechanism earns its keep.** Track effectiveness. Remove or fix mechanisms that don't prevent real problems.
4. **Make the right thing easy and the wrong thing hard.** Don't just block—guide toward the correct path.
5. **Mechanisms compound.** Each mechanism makes the system more resilient. Over time, well-mechanized teams spend less time on incidents and more time on innovation.

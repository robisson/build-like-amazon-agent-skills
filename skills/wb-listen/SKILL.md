---
name: wb-listen
description: "Stage 1 of Working Backwards: Identify who the customer is and gather deep insights about their current experience, pain points, and unmet needs through systematic observation and data collection."
leadership_principles:
  - Customer Obsession
  - Dive Deep
  - Learn and Be Curious
  - Earn Trust
---

# WB-Listen: Who Is the Customer and What Insights Do We Have?

## Overview

Listen is the foundation of Working Backwards. Before you can solve a problem, you must deeply understand who experiences it and how it affects them. This stage produces a Customer Insight Summary that documents: who the customer is (specific segment), what their current experience looks like, what data supports your understanding, and what gaps remain in your knowledge.

The output of this stage is not a persona document or a market analysis slide. It is a written narrative (1-2 pages) that makes any reader feel the customer's pain or see their opportunity. If the reader doesn't feel a sense of urgency after reading it, you haven't listened deeply enough.

## When to Use

- Starting any new product, feature, or initiative
- When the team disagrees on who the target customer is
- When assumptions about customer needs haven't been validated with data
- When entering a new market or customer segment
- After a product launch that underperformed expectations (re-listen)
- Annually, to refresh understanding of how customer needs have evolved

## Amazon Context

Amazon's Leadership Principle #1 is Customer Obsession: "Leaders start with the customer and work backwards." This is not aspirational — it is operational. Teams are expected to cite specific customer data (support contacts, usage patterns, interview quotes, behavioral analytics) in their PR/FAQ documents. "We believe customers want X" is not acceptable without evidence.

At Amazon, customer listening takes many forms:
- **CSAT/NPS surveys** with verbatim analysis
- **Contact driver analysis** from customer support tickets
- **Voice of the Customer (VOC) meetings** where leaders listen to actual customer calls
- **Customer Advisory Boards** for enterprise products
- **Usability studies** observing customers attempting tasks
- **Behavioral data** from instrumented products
- **Social media and review mining** for unsolicited feedback

The discipline is: never assume you know what the customer wants. Always verify with data. The most dangerous product decisions come from teams that are "too close" to their product and project their own preferences onto customers.

## The Process

### Step 1: Define the Customer Segment

Identify your target customer with enough specificity that you could find them and talk to them.

**Bad segments:**
- "Developers" (too broad — which developers? building what? at what company size?)
- "Everyone who uses our product" (not a segment)
- "Small businesses" (which vertical? which stage? which geography?)

**Good segments:**
- "Backend engineers at companies with 50-500 employees who deploy to AWS and currently spend >2 hours/week on deployment pipeline maintenance"
- "First-time homebuyers in metropolitan areas who have been pre-approved but haven't found a property within 60 days"
- "Data analysts at Fortune 500 companies who create >10 reports per month and rely on 3+ data sources"

Template: `[Role/Title] at [Organization Type] who [Observable Behavior] and [Measurable Characteristic]`

### Step 2: Gather Quantitative Data

Collect data that characterizes the segment's size, behavior, and trends:

1. **Segment size:** How many of these customers exist? What's the growth rate?
2. **Current behavior:** What do they do today? How often? How long does it take?
3. **Pain signals:** Support tickets, churn rate, feature request frequency, workaround adoption
4. **Spending signals:** What are they paying for adjacent solutions? What's the willingness-to-pay indicator?
5. **Trend data:** Is this problem getting better or worse over time?

Sources to mine:
- Product analytics (usage funnels, drop-off points, feature adoption)
- Support ticket categorization and frequency
- Sales call recordings and lost-deal analysis
- Market research reports and analyst briefings
- Competitor reviews and comparison shopping behavior
- Public forums, Stack Overflow, Reddit, community channels

### Step 3: Gather Qualitative Data

Numbers tell you what; conversations tell you why.

**Customer Interviews (minimum 5, ideally 10-15):**
1. Recruit participants from your defined segment
2. Use open-ended questions — never lead with your solution
3. Ask about their current process, not hypothetical futures
4. Listen for emotional language (frustrated, annoyed, worried, confused)
5. Ask "why?" at least 3 times to get past surface answers
6. Record (with permission) and transcribe for team review

**Key Interview Questions:**
- "Walk me through the last time you [task related to your area]. What happened?"
- "What's the hardest part of [activity]? Why?"
- "When you get stuck, what do you do? Who do you ask?"
- "If you could wave a magic wand and fix one thing about [process], what would it be?"
- "What have you tried? What worked? What didn't?"

**Observation:**
- Watch customers attempt tasks (usability testing)
- Shadow them during their actual workflow (contextual inquiry)
- Review screen recordings of product usage
- Attend their team meetings to understand context

### Step 4: Synthesize Into Insight Themes

Group findings into 3-5 themes that represent patterns across multiple data points:

1. **Theme name:** A short, memorable label
2. **Evidence:** 3+ data points supporting this theme (mix of quant and qual)
3. **Customer quote:** A verbatim quote that captures the emotional truth
4. **Magnitude:** How many customers? How frequently? What's the cost?
5. **Trend:** Getting better, worse, or staying the same?

### Step 5: Write the Customer Insight Summary

Produce a 1-2 page narrative document:

```
CUSTOMER INSIGHT SUMMARY
========================

Customer Segment: [Specific definition from Step 1]
Segment Size: [Number of customers, with growth rate]
Date of Research: [When data was collected]
Data Sources: [List sources: N interviews, M support tickets, analytics from X tool]

CURRENT EXPERIENCE
[Narrative description of what the customer's life looks like today.
Written in present tense. Concrete, specific, vivid.]

KEY INSIGHTS
1. [Theme 1]: [2-3 sentence description with data point]
   Customer quote: "[Verbatim]"
   
2. [Theme 2]: [2-3 sentence description with data point]
   Customer quote: "[Verbatim]"

3. [Theme 3]: [2-3 sentence description with data point]
   Customer quote: "[Verbatim]"

WHAT WE DON'T YET KNOW
[List of open questions that require further investigation]

IMPLICATIONS
[What this means for the opportunity. What should we explore solving?]
```

### Final Step: Present and Wait for Approval

Present your complete Customer Insight Summary to the user. Ask:
- "Here's what I have for the Listen stage. Does this customer profile look right?"
- "Anything you'd like to adjust before we move to Define (problem statement)?"

Wait for the user to respond with explicit approval or requested changes.

- If they request changes → revise the Customer Insight Summary → re-present → ask again.
- If they approve → proceed to Stage 2 (Define).

⛔ DO NOT proceed to the Define stage until the user explicitly approves or says to continue.

## Example Output

```
CUSTOMER INSIGHT SUMMARY
========================

Customer Segment: Platform engineers at mid-size SaaS companies (100-1000
employees) responsible for maintaining internal developer platforms that serve
20-100 development teams.

Segment Size: ~45,000 professionals in the US (growing 28% YoY per 
LinkedIn data + Gartner 2025 Platform Engineering report)

Date of Research: March 2026
Data Sources: 12 customer interviews, 847 support tickets (Q1 2026),
product analytics (Jan-Mar 2026), 3 community forum analyses

CURRENT EXPERIENCE
Platform engineers at mid-size companies spend 60-70% of their time on
maintenance tasks: updating dependencies, rotating credentials, responding
to pager alerts for infrastructure issues, and debugging deployment
failures that block development teams. They are hired to build golden paths
that accelerate developers, but they spend most of their time firefighting.

Their internal customers (developers) are frustrated by slow response times
and inconsistent tooling. Platform engineers are frustrated because they
can see what "good" looks like but can't get there because of interrupt-driven
workloads.

KEY INSIGHTS
1. Maintenance Tax: Platform engineers spend 12-15 hours/week on unplanned
   maintenance (credential rotation, dependency updates, incident response).
   This leaves <30% of their time for platform improvements.
   Customer quote: "I'm a glorified janitor. I was hired to build a platform
   and I spend all day cleaning up messes."

2. Tribal Knowledge Bottleneck: When one platform engineer leaves, 2-3
   months of context are lost. Runbooks are outdated within weeks of writing.
   8 of 12 interviewees cited "lack of documentation" as their top pain point.
   Customer quote: "When Sarah left, half our deployment pipeline became a
   black box. We're still reverse-engineering her decisions six months later."

3. Developer Satisfaction Drives Priority: Platform teams are measured by
   developer satisfaction surveys, but they lack the tools to connect their
   work to developer outcomes. They operate on gut feel about what matters most.
   Customer quote: "I know developers are unhappy with deploy times but I
   don't know if fixing the CI bottleneck or the staging environment would
   move the needle more."

WHAT WE DON'T YET KNOW
- Exact budget authority (who approves tooling purchases?)
- How they evaluate build-vs-buy for platform components
- Whether they would trust automated maintenance over manual control

IMPLICATIONS
There is an opportunity to reduce the maintenance tax dramatically, freeing
platform engineers to do the work they were hired to do. The solution must
build trust gradually (they won't hand over full control on day one) and
show clear connection between platform work and developer outcomes.
```

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "We'll talk to customers soon" | Stage gate: no advancement to Define without a completed Customer Insight Summary |
| "We already know our customers" | Required: minimum 5 new data points (interviews, recent tickets, fresh analytics) collected within 60 days |
| "One customer told us this" | Minimum 3 corroborating data points for each insight theme (no single-source insights) |
| "The data speaks for itself" | Every quantitative finding must be paired with qualitative context explaining WHY |
| "We'll validate later" | Customer Insight Summary is reviewed by a peer outside the team before advancing |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "We don't have time for customer research" | Building without research is the most expensive form of waste — you'll build the wrong thing and rebuild later | Time-box to 2 weeks. 5 interviews + analytics review. Imperfect data > no data |
| "Our PM already knows the customer" | Individual knowledge is not team knowledge. Undocumented insights die when people move | Write it down. If the PM knows it, it should take 2 hours to document, not 2 weeks |
| "Customers don't know what they want" | Customers can't design solutions, but they are experts on their own problems and behaviors | Ask about problems and current behavior, never about hypothetical solutions |
| "We have telemetry data, that's enough" | Telemetry shows WHAT happens but never WHY. You need both behavioral data and motivational context | Combine quant (what) with qual (why). Neither alone is sufficient |
| "Our competitor already validated this market" | Competitor's customers ≠ your customers. Their problem framing ≠ your customers' problem framing | Do your own research. Competitor validation reduces market risk but doesn't eliminate customer risk |

## Red Flags

- Customer segment defined as "everyone" or using only demographic labels
- Insights based entirely on one data source (e.g., only surveys, only one interview)
- No direct customer quotes anywhere in the document
- Research is >6 months old and not refreshed
- Team can't name 3 specific customers who represent the segment
- All insights confirm the team's pre-existing hypothesis (confirmation bias)
- No "What We Don't Yet Know" section (suggests insufficient intellectual honesty)
- Customer segment was chosen because it's convenient, not because it's the largest or most impactful opportunity

## Verification

Before advancing to Stage 2 (Define):

- [ ] Customer segment is defined with specificity (role + org type + behavior + characteristic)
- [ ] Segment size is quantified with a credible source
- [ ] Minimum 5 customer interviews or equivalent qualitative sources completed
- [ ] Quantitative data from at least 2 independent sources
- [ ] 3-5 insight themes identified, each with 3+ supporting data points
- [ ] Customer quotes included (verbatim, not paraphrased)
- [ ] "What We Don't Yet Know" section is honest and actionable
- [ ] Document reviewed by at least one person outside the immediate team
- [ ] Research is less than 90 days old (or refreshed with recent data)
- [ ] Team can explain why THIS segment over other possible segments

## Tenets

1. **Observation over assumption.** Never substitute what you think customers want for what they actually say and do. Your intuition is a hypothesis, not a fact.
2. **Breadth before depth.** Talk to many customers before going deep with a few. Premature depth leads to over-fitting to one customer's unique situation.
3. **Quantitative and qualitative together.** Numbers without stories are context-free. Stories without numbers are anecdotes. You need both.
4. **Intellectual honesty about gaps.** Admitting what you don't know is a sign of rigor, not weakness. Document gaps explicitly so they can be addressed.
5. **Fresh data, always.** Customer needs evolve. Research from last year may be dangerously outdated. Re-validate before major investment decisions.

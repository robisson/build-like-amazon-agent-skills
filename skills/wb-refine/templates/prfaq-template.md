# PR/FAQ Template — STRICT FORMAT

---

## ⛔ FORMAT RULES — READ BEFORE WRITING

### MANDATORY STRUCTURE

The PR/FAQ has exactly THREE sections:
1. **PRESS RELEASE** — Pure narrative paragraphs. NO headers. NO bullet lists. Reads like a newspaper article.
2. **FAQ** — Split into External (customer questions) and Internal (business/viability questions).
3. **VISUALS** — At least one visual (architecture diagram, mockup, flow, wireframe).

### WHAT YOU MUST DO

- Write the Press Release as continuous narrative paragraphs (like a news article)
- Write in present tense as if the product already launched TODAY
- Include exactly TWO quotes: one spokesperson, one customer
- Keep the entire Press Release to ONE PAGE maximum
- Split FAQ into External (5-8 questions) and Internal (5-8 questions)
- Use specific numbers, data, and metrics throughout
- Write at 10th-grade reading level (no jargon, no undefined acronyms)
- Include at least one visual in the Visuals section

### WHAT YOU MUST NOT DO

- ❌ DO NOT use section headers inside the Press Release (no "## The Problem", no "## Solution", no "### Key Capabilities")
- ❌ DO NOT use bullet lists anywhere in the Press Release (narratives only!)
- ❌ DO NOT list features — describe BENEFITS to the customer
- ❌ DO NOT use numbered lists in the Press Release (except the FAQ section)
- ❌ DO NOT write more than 1 page for the Press Release
- ❌ DO NOT skip either quote (spokesperson AND customer are mandatory)
- ❌ DO NOT combine External and Internal FAQ into one mixed section
- ❌ DO NOT omit the Visuals section
- ❌ DO NOT write in future tense ("will be", "is going to") — present tense only ("is", "enables", "reduces")
- ❌ DO NOT use marketing superlatives ("revolutionary", "best-in-class", "world-class")

### ANTI-PATTERNS (If your output looks like this, you did it WRONG)

**BAD — Headers inside PR:**
```
## The Problem
Customers struggle with...

## Our Solution
We built...

## Key Capabilities
- Feature 1
- Feature 2
```

**BAD — Bullet lists in PR:**
```
The product offers:
- Automated deployment
- Real-time monitoring
- One-click rollback
```

**BAD — Feature dump instead of benefits:**
```
Product X includes: Kubernetes orchestration, gRPC APIs, 
distributed tracing, and a React dashboard.
```

**BAD — Missing quotes or single combined FAQ:**
```
## FAQ
Q1: What is it?
Q2: How much does it cost us to build?
(mixing customer and internal questions)
```

---

## PRESS RELEASE

> ⛔ **SELF-CHECK BEFORE OUTPUT**: After writing, verify: (1) NO headers inside this section, (2) NO bullet/numbered lists, (3) NO "Key capabilities:" or "How it works:" labels, (4) TWO quotes present, (5) present tense throughout, (6) ≤ 1 page, (7) benefits not features. If ANY fails, rewrite before presenting.

[Product Name]

[One sentence following this formula: "For [target customer] who [need/pain], [Product Name] is [category] that [primary benefit]."]

[City name][Date] - [Company Name] announces [Product Name], [one sentence: what it is and what it does for customers]. [One sentence: why this matters now]. [One sentence: the single most important outcome for the customer].

[Target customers] today spend [quantified time/money/effort] on [painful current process]. When [triggering situation occurs], they are forced to [specific painful workaround], resulting in [quantified negative impact — hours lost, dollars wasted, errors introduced, customers affected]. [Data point from research/industry source] confirms this is not an edge case — [scope of the problem across the market].

[Product Name] eliminates this burden by [primary mechanism described as customer benefit, not technical feature]. [What changes in the customer's daily experience — be specific and concrete]. Customers [specific action they can now take] in [new timeframe] instead of [old timeframe], [additional benefit that matters to them].

"[Statement connecting this product to the company's mission and customer obsession]," says [Full Name], [Title — VP or Director level], [Company Name]. "[Explanation of WHY we invested here — what customer truth drove this decision]. [Forward-looking commitment to this problem space]."

[Product Name] works by [brief, accessible explanation of how the customer uses it — NO deep technical jargon]. [Walk through the experience in 2-3 sentences: what they do, what they see, what outcome they get]. [One sentence on integration or setup simplicity if relevant].

"[Specific statement about the customer's experience USING the product — emotional, concrete, with a measurable result]," says [Full Name], [Title], [Company/Organization — represents target customer]. "[How this changed their daily work or team's effectiveness]. [Specific metric or time improvement they experienced]."

To get started with [Product Name], [specific single action: visit URL, sign up, install, contact — one clear next step].

---

## FREQUENTLY ASKED QUESTIONS

### External FAQ (Customer Questions)

**Q1: What is [Product Name] and who is it for?**

A: [2-3 sentences. What it is, who specifically benefits, what outcome they get.]

**Q2: How does [Product Name] work?**

A: [4-6 sentences walking through the customer experience. What they do step by step. What they see. What outcome they receive. No internal implementation details.]

**Q3: How much does [Product Name] cost?**

A: [Specific pricing model with numbers or ranges. Include an example: "A typical team of X people doing Y would pay approximately $Z/month." Mention free tier if applicable.]

**Q4: How do I migrate from my current solution / get started?**

A: [3-5 sentences on the onboarding path. Prerequisites, time estimate, what support is available. Address the switching cost concern directly.]

**Q5: What about my existing [relevant infrastructure/workflow/data]?**

A: [How the product integrates with or replaces what they already have. Be specific about compatibility.]

**Q6: What are the limitations? What does it NOT do?**

A: [Honest answer listing 2-3 genuine limitations. This builds trust. Example: "Currently supports X and Y but not Z. Z support is planned for [timeframe]."]

**Q7: How is this different from [obvious competitor or alternative]?**

A: [Honest comparison. Acknowledge competitor strengths. Explain why your approach serves THIS customer segment better. Specifics, not adjectives.]

**Q8: What happens if [failure scenario relevant to this product]?**

A: [How the product handles failures, data loss scenarios, outages. What guarantees exist. What the customer's recourse is.]

### Internal FAQ (Business & Viability Questions)

**Q1: How much does it cost us to build this?**

A: [Team size, timeline, infrastructure costs broken into phases. Example: "Phase 1 (MVP, 12 weeks): 4 engineers + 1 PM = $X loaded. Phase 2 (GA, 12 more weeks): add 2 engineers + marketing $Y. Total year-1 investment: $Z."]

**Q2: How long until we launch? What's the timeline?**

A: [Specific milestones with dates. MVP, beta, GA. What's the critical path. What could delay it.]

**Q3: What team do we need? Do we have them?**

A: [Roles needed, current availability, hiring plan if gaps exist. Be explicit about what's missing today.]

**Q4: How do we measure success? What are the metrics?**

A: [Leading indicators for first 90 days — not vanity metrics. Specific targets: "Success = X active users doing Y at least Z times per week by day 90."]

**Q5: What's the biggest risk and how do we mitigate it?**

A: [Name the #1 risk honestly. Specific mitigation plan. What happens if mitigation fails. When do we pull the plug.]

**Q6: What are we NOT doing in order to do this?**

A: [Explicit opportunity cost. Which initiatives are delayed or cancelled. Which team is redirected. Be honest about tradeoffs.]

**Q7: What dependencies do we have on other teams?**

A: [Every cross-team dependency listed. What you need, when, what happens if they can't deliver, whether you've secured commitment.]

**Q8: Why now? Why not six months from now?**

A: [Compelling timing argument. Market shift, competitive window, technology enabler, customer demand inflection. "Later" must have a clear cost.]

---

## VISUALS

[Include at least ONE of the following — more is better:]

- **Customer Experience Mockup**: Wireframe or screenshot showing what the customer sees/does
- **Architecture Overview**: High-level boxes-and-arrows diagram (not detailed design)
- **Customer Journey Flow**: Step-by-step flow from problem to resolution using the product
- **Before/After Comparison**: Visual showing the customer's world before vs. after

[Place diagrams, mockups, or wireframes here. Even hand-drawn sketches are acceptable. The goal is to help the reader SEE the customer experience.]

---

## GOOD vs BAD EXAMPLE

### ✅ GOOD (Correct format — narrative paragraphs, no headers, no bullets):

```
DataSync Pro

For platform engineering teams who lose hours diagnosing deployment failures, DataSync Pro is a deployment observability tool that reduces root-cause identification from 4 hours to under 5 minutes.

Amazon today announces DataSync Pro, a deployment observability tool that automatically correlates deployment events with infrastructure changes. Platform engineering teams at mid-size companies can now identify the root cause of deployment failures in under 5 minutes, eliminating the manual log-diving that consumes an average of 4.2 hours per incident.

Platform engineering teams today spend an average of 4.2 hours per deployment failure chasing root causes across disconnected monitoring tools. When a deployment triggers an alert at 2 AM, the on-call engineer must manually correlate CloudWatch metrics, deployment logs, configuration changes, and infrastructure events across 6-8 different dashboards. According to the 2024 DORA report, 78% of engineering teams cite deployment failure diagnosis as their top operational pain point, costing mid-size companies an average of $23,000 per incident in engineer time and customer impact.

DataSync Pro eliminates this burden by automatically building a causal timeline of every change that occurred within the blast radius of a deployment. Engineers open a single view that shows exactly which configuration change, code commit, or infrastructure drift caused the failure. Teams identify root causes in under 5 minutes instead of 4+ hours, and junior engineers resolve incidents that previously required senior escalation.

"We built DataSync Pro because we watched platform teams waste their best engineers on toil that machines should handle," says Maria Chen, VP of Developer Tools, Amazon. "Every hour an engineer spends chasing logs is an hour they're not building for customers. DataSync Pro gives that time back."

DataSync Pro works by instrumenting the deployment pipeline and correlating events across infrastructure, application, and configuration layers in real time. When a failure occurs, the engineer clicks "Diagnose" and sees a ranked list of probable causes with confidence scores and evidence links. The entire experience takes less than 60 seconds from alert to actionable insight.

"Last Tuesday we had a P1 at 3 AM and our most junior engineer resolved it in 4 minutes using DataSync Pro — that same class of incident used to take our seniors 3+ hours," says James Park, Staff Platform Engineer, Acme Corp. "We've cut our mean-time-to-resolution by 87% since adopting it. My team actually sleeps through the night now."

To get started with DataSync Pro, visit datasyncpro.example.com and connect your first deployment pipeline in under 10 minutes.
```

### ❌ BAD (Wrong format — has headers, bullet lists, feature dumps):

```
## DataSync Pro

## Problem
Platform engineers waste time diagnosing failures.

## Solution
DataSync Pro provides:
- Automatic event correlation
- Real-time causal analysis
- Multi-source log aggregation
- AI-powered root cause detection
- Customizable dashboards

## Key Features
1. Kubernetes-native deployment tracking
2. gRPC-based event streaming
3. Distributed tracing integration
4. React-based dashboard UI

## How it works
The system uses a Kafka event bus to...
```

The BAD example fails because: it uses headers inside the PR, uses bullet/numbered lists, dumps features instead of benefits, uses technical jargon (Kafka, gRPC, Kubernetes), and reads like a product spec instead of a newspaper announcement.

---

## REVISION HISTORY

| Version | Date | Reviewer | Key Changes |
|---------|------|----------|-------------|
| 0.1 | [Date] | Self-review | Initial draft |
| 0.2 | [Date] | [Peer name] | [Summary of changes] |
| 0.3 | [Date] | [Bar Raiser name] | [Summary of changes] |
| 1.0 | [Date] | [Approver name] | Approved for execution |

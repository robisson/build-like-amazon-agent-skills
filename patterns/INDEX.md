# Patterns Index

Lightweight catalog for agent pattern selection. The agent reads ONLY this file during `/design` and `/spec` to decide which patterns are relevant. Only load the full `PATTERN.md` when `applies_when` criteria match the workload.

---

## cell-based-architecture

**Category**: blast-radius-reduction

**Description**: Replicates the full workload into multiple isolated instances (cells), each handling a subset of customers/traffic behind a thin router. A failure in one cell does not cascade to others.

**Applies when**:
- Workload requires extreme resilience (RPO < 5s, RTO < 30s)
- Downtime carries reputational or financial damage at scale
- Ultra-scale system: too big or too critical to fail
- Multi-tenant SaaS with tenants that may need fully dedicated tenancy
- Poison-pill requests must be contained to a subset of customers

**Does NOT apply when**:
- Single-tenant or low-tenant-count workload
- Acceptable blast radius is the whole region
- Engineering org cannot sustain operating tens-to-hundreds of replicas

**Full pattern**: [`cell-based-architecture/PATTERN.md`](cell-based-architecture/PATTERN.md)

---

## saas-architecture

**Category**: multi-tenancy

**Description**: Architectural pattern for delivering software as a service to multiple tenants through a unified control plane (onboarding, identity, billing, metrics) with silo/pool deployment models in the application plane.

**Applies when**:
- Building a software product delivered as a service (not installed software)
- Multiple customers (tenants) share the same operational environment
- Business requires frictionless onboarding and rapid time-to-value
- Operational efficiency matters more than per-customer customization
- Growth strategy depends on adding tenants without proportional ops cost
- You need unified deployment, billing, metrics, and identity across all tenants

**Does NOT apply when**:
- Product is a one-off system for a single organization
- Regulatory requirements mandate completely separate customer-controlled environments
- Customer count will remain permanently small (< 5) with deep customization each
- Building infrastructure, not application software

**Full pattern**: [`saas-architecture/PATTERN.md`](saas-architecture/PATTERN.md)

---

## agentic-ai

**Category**: ai-systems

**Description**: Foundational blueprints for designing goal-oriented AI agents that perceive, reason, act, and learn. Covers agent patterns (reasoning, RAG, tool-based, orchestration, multi-agent, memory-augmented), LLM workflow patterns (chaining, routing, parallelization, orchestration, evaluator loops), and cloud-native agentic architectures.

**Applies when**:
- Building AI-powered applications that go beyond static or deterministic automation
- System requires autonomous goal-directed behavior (not just Q&A)
- Tasks require dynamic tool selection, multi-step reasoning, or coordination across agents
- Workload benefits from LLM-driven decision making embedded in structured workflows
- You need agents that perceive, reason, act, and learn — not just generate text

**Does NOT apply when**:
- Deterministic logic suffices (simple rules, CRUD, if/else)
- Latency requirements are sub-100ms
- Task is well-defined, single-step, doesn't benefit from reasoning
- Cost constraints prevent LLM invocations at required scale
- Full explainability requires 100% deterministic audit trail with no probabilistic components

**Full pattern**: [`agentic-ai/PATTERN.md`](agentic-ai/PATTERN.md)

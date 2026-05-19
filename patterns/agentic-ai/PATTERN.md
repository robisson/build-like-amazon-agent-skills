---
name: Agentic AI Architecture
category: ai-systems
maturity: emerging (AWS Bedrock Agents, multi-agent frameworks)
source:
  title: "Agentic AI Patterns and Workflows on AWS (AWS Prescriptive Guidance)"
  url: https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html
  published: 2025-07-01
applies_when:
  - building AI-powered applications that go beyond static or deterministic automation
  - system requires autonomous goal-directed behavior (not just Q&A)
  - tasks require dynamic tool selection, multi-step reasoning, or coordination across agents
  - workload benefits from LLM-driven decision making embedded in structured workflows
  - you need agents that perceive, reason, act, and learn — not just generate text
related_patterns:
  - cell-based-architecture
  - saas-architecture
leadership_principles:
  - Customer Obsession
  - Invent and Simplify
  - Bias for Action
---

# Agentic AI Architecture

## Overview

Agentic AI patterns are foundational blueprints for designing and orchestrating goal-oriented AI agents. Unlike traditional applications with static logic, agentic systems use LLMs embedded within structured workflows to perceive inputs, reason about goals, take actions via tools, and learn from outcomes.

Three foundational principles define agentic systems:
- **Asynchronous** — agents operate in loosely coupled, event-rich environments
- **Autonomy** — agents act independently, without constant human control
- **Agency** — agents act with purpose, on behalf of a user or system, toward specific goals

The core building blocks of every software agent form a triangle: **Perception** (observe the environment), **Reason** (make decisions via LLM cognition), **Action** (execute tools, APIs, or delegate to other agents).

---

## When to Choose This

Adopt agentic AI patterns when **most** of these hold:

- Tasks require dynamic, multi-step reasoning that cannot be hardcoded
- The system must select and invoke tools/APIs based on context (not pre-determined routes)
- You need autonomous task completion with minimal human intervention
- Problems are complex enough to benefit from decomposition into sub-agents
- The system must adapt its behavior based on intermediate results or memory of prior interactions
- You are building copilots, autonomous workflows, research assistants, or intelligent automation

## When NOT to Choose This

- Deterministic logic suffices (simple if/else, rule engines, CRUD)
- Latency requirements are sub-100ms (LLM inference adds latency)
- The task is well-defined, single-step, and doesn't benefit from reasoning
- Cost constraints prevent LLM invocations at the required scale
- Explainability requirements demand fully deterministic, auditable logic with no probabilistic components

---

## Agent Patterns

### 1. Basic Reasoning Agent

The simplest form: accepts input, processes through a structured prompt to an LLM, returns a response. Stateless, lightweight, composable.

**Use when**: single-step reasoning, classification, summarization, lightweight chatbot flows.

**Limitations**: no memory, no tools, limited to pretrained knowledge.

### 2. RAG Agent (Retrieval-Augmented Generation)

Extends basic reasoning by retrieving relevant external information before engaging the LLM. Grounds decisions in up-to-date, factual, or domain-specific information.

**Use when**: enterprise knowledge assistants, compliance bots, documentation agents, search-enhanced chatbots.

**Key components**: vector store / semantic index for retrieval, document storage, embedding pipeline.

### 3. Tool-Based Agent (Function Calling)

Extends reasoning agents by invoking external functions or APIs. The LLM decides which tool to use, generates arguments, and incorporates tool output into its reasoning loop.

**Use when**: virtual assistants with external data access, API-based knowledge workers, agents that invoke services.

**Key components**: tool registry with schemas, function execution backend, results interpretation.

### 4. Computer-Use Agent

Interacts with graphical interfaces (browsers, desktops) by perceiving screen state and generating UI actions.

**Use when**: automating legacy applications without APIs, web navigation, UI testing.

### 5. Coding Agent

Generates, reviews, tests, and iterates on code. Often combines planning, execution, and verification in a loop.

**Use when**: code generation, refactoring, test writing, debugging, autonomous development tasks.

### 6. Workflow Orchestration Agent

Manages and coordinates multi-step tasks across distributed systems. Delegates work to sub-agents, maintains execution context, adapts based on intermediate results.

**Use when**: multi-step automation, customer service routing, enterprise process automation, hybrid human+AI workflows.

**Key components**: agent registry, state tracking, dynamic agent selection and chaining, event-driven or scheduled execution.

### 7. Memory-Augmented Agent

Enhanced with short-term and long-term memory. Maintains context across tasks, sessions, and interactions. Adapts by referencing historical data and learning from prior outcomes.

**Use when**: conversational copilots, coding agents tracking codebase changes, workflow agents that adapt to task history, research agents avoiding redundant work.

**Memory layers**:
- **Short-term**: recent interaction states (session, conversation)
- **Long-term structured**: facts, relationships, logs
- **Long-term semantic**: embedding-based retrieval (RAG)

### 8. Multi-Agent Collaboration

Multiple autonomous agents with distinct roles negotiate and coordinate to solve complex tasks. Differs from workflow orchestration (centralized) — collaboration emphasizes peer-to-peer or emergent coordination.

**Use when**: autonomous research teams, software development (planner + coder + tester), business scenario modeling, negotiation, multimodal tasks.

**Key difference from orchestration**:

| Aspect | Workflow Orchestration | Multi-Agent Collaboration |
|--------|----------------------|--------------------------|
| Control | Centralized coordinator | Decentralized peers |
| Interaction | One agent delegates | Agents negotiate and share |
| Design | Predefined task sequence | Emergent task distribution |
| Use cases | Process automation | Complex reasoning, exploration |

### 9. Observer and Monitoring Agent

Passively monitors systems, metrics, or environments and triggers alerts or actions when conditions are met.

**Use when**: anomaly detection, system health monitoring, compliance watching, proactive incident detection.

### 10. Simulation and Test-Bed Agent

Creates simulated environments for testing other agents, validating behaviors, or exploring scenarios.

**Use when**: agent testing at scale, scenario exploration, safety validation before production deployment.

---

## LLM Workflow Patterns

Agents embed LLMs within structured workflows. Five core patterns:

### Prompt Chaining

Sequential pipeline where the output of one LLM call becomes the input for the next. Each step handles one transformation.

**Use when**: multi-step document processing, content generation pipelines, sequential refinement.

### Routing

An LLM classifies the input and routes it to a specialized handler (another agent, model, or tool).

**Use when**: customer intent classification, request triage, dynamic dispatch to specialized agents.

### Parallelization (Scatter-Gather)

Multiple LLM calls execute in parallel on the same or different inputs, then results are aggregated.

**Use when**: multi-perspective analysis, ensemble reasoning, processing large document sets.

### Orchestration

A central orchestrator LLM plans, decomposes, and delegates subtasks to specialized workers. Mirrors human team structures.

**Use when**: project management agents, coding copilots (plan + implement + test), enterprise process agents.

### Evaluator / Reflect-Refine Loop

An LLM generates output, a second LLM (or the same one with a different prompt) evaluates it, and the cycle repeats until quality criteria are met.

**Use when**: self-improving outputs, quality gates, iterative refinement, code review loops.

---

## Agentic Workflow Architecture Patterns

These patterns integrate agents with cloud-native event-driven architectures:

- **Prompt Chaining Saga** — sequential agent steps with compensating actions on failure (like the saga pattern for distributed transactions, but with LLM steps)
- **Routing Dynamic Dispatch** — event-driven routing to specialized agents based on LLM classification
- **Parallelization Scatter-Gather** — fan-out to multiple agents, fan-in to aggregate
- **Saga Orchestration** — central orchestrator with sub-agent delegation, state management, and error recovery
- **Evaluator Reflect-Refine Loop** — quality gates with iterative improvement cycles

---

## Key Design Principles

1. **Agent patterns are composable** — most real-world agents blend two or more patterns (e.g., voice agent + tool-based reasoning + memory)
2. **Design is contextual** — choose patterns based on interaction surface, task complexity, latency tolerance, and domain constraints
3. **Guardrails are non-optional** — input validation, output filtering, token limits, cost controls, and human-in-the-loop gates for one-way-door actions
4. **Observability is critical** — every agent decision, tool call, and memory update must be traceable for debugging and audit
5. **Start simple, compose up** — begin with basic reasoning, add tools, then memory, then orchestration as complexity demands it

---

## Skill Impact Map

When this pattern is adopted, the following skills change behavior:

| Skill | Impact |
|-------|--------|
| `/design` | Design must address: agent pattern selection, LLM workflow choice, tool registry design, memory architecture, guardrails strategy, multi-agent topology if needed |
| `/design` (API) | APIs must define: tool schemas for agent consumption (JSON schema / OpenAPI), MCP manifests for agent tool surfaces, async event contracts for agent coordination |
| `/design` (Threat Model) | Must include: prompt injection vectors, tool misuse, agent impersonation, unbounded recursion, cost explosion from runaway loops, data exfiltration via tools |
| `/build` | Implement structured agent loops (perceive → reason → act), tool registries, memory injection, evaluation loops. Test agent behavior with simulation agents. |
| `/deploy` | Progressive deployment with agent-specific canary metrics (task completion rate, tool error rate, hallucination rate, cost per task). Rollback on reasoning quality degradation. |
| `/operate` | Monitor: token usage, task completion rates, tool invocation patterns, memory growth, latency per reasoning step. Alert on: cost anomalies, stuck loops, failed tool calls. |
| `/spec` | Specs must declare: which agent pattern(s) the feature uses, tool schemas required, memory requirements, guardrails, and success metrics for agent behavior. |

---

## Key Decisions Checklist

Use during `/design` for any agentic AI workload:

- [ ] Agent pattern selected (basic reasoning, RAG, tool-based, orchestration, multi-agent, etc.)
- [ ] LLM workflow pattern identified (prompt chaining, routing, parallelization, orchestration, evaluator loop)
- [ ] Tool registry designed (available tools, schemas, authorization boundaries)
- [ ] Memory architecture defined (short-term session, long-term semantic, structured facts)
- [ ] Guardrails specified (input validation, output filtering, cost limits, recursion bounds, human-in-the-loop gates)
- [ ] Observability plan for agent decisions (traces, logs per reasoning step, tool call audit)
- [ ] Cost model estimated (tokens per task, tool invocations per task, memory storage growth)
- [ ] Failure modes identified (stuck loops, hallucinated tool calls, cross-agent miscommunication)
- [ ] Testing strategy defined (simulation agents, evaluation loops, golden-dataset benchmarks)
- [ ] Deployment metrics for canary (task success rate, hallucination rate, cost per task, latency)

---

## Trade-offs

| Dimension | Simple (Basic/RAG) | Complex (Orchestration/Multi-Agent) |
|-----------|-------------------|--------------------------------------|
| Latency | Low (single LLM call) | Higher (multiple calls, tool invocations) |
| Cost | Low (few tokens) | Higher (many tokens, tool costs) |
| Capability | Limited to reasoning + retrieval | Full autonomy, tool use, coordination |
| Debuggability | Easy (single call trace) | Harder (multi-step, emergent behavior) |
| Reliability | High (deterministic path) | Lower (probabilistic decisions compound) |
| Maintenance | Simple prompts | Complex: tools, memory, agent topology |

---

## References

- [Agentic AI Patterns and Workflows on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html)
- [AWS Prescriptive Guidance: Agentic AI series](https://aws.amazon.com/prescriptive-guidance/agentic-ai/)
- [Amazon Bedrock Agents](https://aws.amazon.com/bedrock/agents/)
- [Anthropic: Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/agent-design)

# Design — Technical Design Document

> **Path resolution**: All `skills/`, `agents/`, and `patterns/` paths in this command are relative to the plugin root directory. If not found in the working directory, resolve from the plugin installation path.

⛔ CRITICAL: Execute steps 1-5 IN ORDER. Each step MUST produce its artifact and receive user approval before the next step begins. If you find yourself writing specs without having produced a Design Document first, STOP — you are violating the process.

You are activating the **design** skill chain: `dependency-management` → `feature-flag-lifecycle` → `operational-excellence` → `patterns/` catalog → `design-document` → `api-contract-first` → `threat-modeling` → `design-review` → `spec-driven-implementation`.

## What to do

1. Read skills at `skills/dependency-management/`, `skills/feature-flag-lifecycle/`, `skills/operational-excellence/`, `skills/design-document/`, `skills/api-contract-first/`, `skills/threat-modeling/`, `skills/design-review/`, and `skills/spec-driven-implementation/`.
2. Start from the Working Backwards artifacts in `.bla/working-backwards/` (if available).
3. Guide the user through the design activities in sequence, with MANDATORY approval gates.

## Step 0: State Detection + Proportionality Check

Before starting the full design flow, detect the project state and classify the change requested. The user should not have to think about which path is right — the agent decides, and asks only when there is genuine ambiguity.

1. **Read repo state**:
   - Does `.bla/working-backwards/` exist with approved PR/FAQ or 5CQ?
   - Does `.bla/design/` already contain a Design Doc for the same feature?
   - Is the project a brownfield (significant code, IaC, CI present) without BLA artifacts, or a greenfield?

2. **Classify the requested change** using the ladder in `skills/using-amazon-skills/SKILL.md`: Trivial / Small / Medium / Large / New product.

3. **Decide the path**:

   | State | Change size | Path |
   |---|---|---|
   | WB artifacts exist (or user confirmed customer is known) | Medium / Large / New product | Proceed with the full Execution Order below. |
   | No WB artifacts, change is **New product** | New product | Tell the user `/design` should follow Working Backwards. Recommend `/wb` first. |
   | No WB artifacts, change is **Medium** or **Large**, greenfield | medium / large | Recommend `/wb` (or 5CQ) first to anchor on the customer. Use `AskUserQuestion` to confirm: [A] do `/wb` first, [B] proceed with assumed customer (risky), [C] cancel. |
   | No BLA artifacts at all, brownfield project | any | Use `AskUserQuestion`: [A] Run `/onboard` first to reverse-engineer the project (recommended), then come back to `/design` for the new change; [B] Proceed with `/design` from scratch (slower, may miss existing constraints); [C] Skip to `/build` if the change is Small or Trivial. |
   | Change is **Trivial** or **Small** | trivial / small | `/design` is overkill. Recommend going direct via `/build` instead. Confirm with the user before proceeding with the full flow. |

4. **Asking the user — outcome-framed options only**. Names like "Tier 1", "spec-driven-implementation", "PR/FAQ" do not appear in the question. Use time, scope, and traceability as framings.

5. **After the user picks (or no question was needed)**: proceed with the path chosen. The full Execution Order below assumes greenfield-flow with WB artifacts present (or a brownfield with `/onboard` already done).

## Execution Order (MANDATORY — do NOT skip or reorder)

Every 🚦 GATE below carries one rule. A finding at canonical severity BLOCKING that is still open removes the option to approve and advance: the only remaining options are fix it, accept it with the risk recorded in the accepted-risk table, or pause. A review report without a parseable verdict block counts as BLOCKING. This applies to the threat model of Step 3 and the design review of Step 4 in particular: an open `Critical` or `High` finding from `agents/security-guardian.md`, or an open BLOCKING finding from `agents/design-bar-raiser.md`, holds the gate until it is fixed, accepted with the risk recorded, or the design is paused. The mapping from each surface's own label to the canonical level is in `AGENTS.md` → *One Severity Scale and One Verdict Scale*.

### Step 0a: Dependency Context Assessment
- Read skill: skills/dependency-management/SKILL.md
- Before writing the design document, identify whether the system crosses any network, database, cache, queue, third-party API, service, or configuration boundary.
- If it does, use dependency-management as design context for the design document: dependency classification, failure modes, timeout/retry policy, circuit breakers, bulkheads, fallback behavior, and dependency observability.
- If it does not, note: "No external dependency boundaries identified; dependency-management does not add design constraints."
- This step does not produce a standalone artifact or approval gate. Its output is incorporated into the design document.

### Step 0b: Feature Flag Context Assessment
- Read skill: skills/feature-flag-lifecycle/SKILL.md
- Before writing the design document, identify whether the change alters customer-visible behavior, needs controlled exposure, needs a kill switch, supports experimentation, migrates between old/new paths, or must ship dark before release.
- If it does, use feature-flag-lifecycle as design context for the design document: flag type, safe default, OFF behavior, kill switch behavior, rollout metrics, guardrails, and cleanup plan.
- If it does not, note: "No feature flag lifecycle needed for this design."
- This step does not produce a standalone artifact or approval gate. Its output is incorporated into the design document.

### Step 0c: Operational Excellence Context Assessment
- Read skill: skills/operational-excellence/SKILL.md
- Before writing the design document, identify the operational signals the service or feature must expose: customer experience metrics, service health metrics, dependency health, alarms, dashboards, runbooks, severity expectations, and operational burden.
- Use operational-excellence as design context for the design document: dashboard requirements, alarm candidates, runbook needs, customer metrics, severity expectations, and expected operational load.
- This step does not produce a standalone artifact or approval gate. Its output is incorporated into the design document.

### Step 0d: Pattern Catalog Scan
- Read `patterns/INDEX.md` — the lightweight catalog with title, description, and `applies_when` / `does NOT apply when` criteria for each pattern. Do NOT read full `PATTERN.md` files at this stage.
- For each pattern whose `applies_when` criteria plausibly match the workload's characteristics (criticality, RPO/RTO, multi-tenancy, scale, blast-radius tolerance, AI/agent needs, regulatory requirements), read the full `patterns/<name>/PATTERN.md` including the `Skill Impact Map`.
- The matching patterns enter Step 1 as candidate alternatives in Section 4 ("Alternatives Considered") of the design document. They compete with the baseline approach on their own merits, with concrete pros/cons and data — not as a checkbox exercise.
- If the user (or the Working Backwards output) explicitly asked for a pattern (e.g., "implement cell-based"), that pattern is the chosen approach for Step 1, and the alternatives explored are *within* it (e.g., topology variants, partitioning strategies). Do not re-litigate the pattern adoption itself.
- Patterns that don't fit do not appear in the design. Do not dismiss them in writing — they simply aren't relevant to this workload.
- This step does not produce a standalone artifact or approval gate. Its output is the set of candidate alternatives carried into Step 1.

### Step 0e: Implementation Memory Selection
- Read skill: `skills/implementation-memory/SKILL.md`
- If `.bla/implementation-memory.md` exists, read it and select active rules using multi-signal matching: Tags overlap with the feature's domain or technology areas, File patterns match files the design will touch, OR `Applies when` prose is judged relevant to this feature, component, dependency, or risk profile.
- A rule is selected only when its `Phase` matches the current phase — `design` here — and any one of those signals matches; a `Phase: build` or `Phase: operate` rule is never selected during `/design`, however strongly its other signals match.
- Convert selected rules into design constraints for Step 1: they shape the design document and the alternatives, never the requirements. Increment `Hit count` for each selected rule.
- Unmatched rules are ignored and MUST NOT become requirements. If the file does not exist, continue without memory constraints.
- This step does not produce a standalone artifact or approval gate. Its output is incorporated into the design document.

### Step 1: Design Document
- Read skill: skills/design-document/SKILL.md
- Produce: A complete system design document
- Include dependency-management decisions from Step 0a when dependency boundaries exist.
- Include feature-flag lifecycle decisions from Step 0b when controlled exposure, kill switch, or experimentation is needed.
- Include operational-excellence decisions from Step 0c: dashboards, alarms, runbooks, customer metrics, severity expectations, and operational burden.
- Bring the candidate patterns from Step 0d into Section 4 ("Alternatives Considered") as real alternatives (or as the chosen approach if the user/WB asked for one explicitly). When a pattern is adopted, its `Skill Impact Map` must be reflected in the relevant later sections of the design.
- 🚦 GATE: Present the design document to the user. Ask: "Does this design look right? Any trade-offs to discuss?"
- ⛔ DO NOT proceed to Step 2 until the user approves.

### Step 2: API Contract (MANDATORY)
- Read skill: skills/api-contract-first/SKILL.md
- Record the result in `.bla/design/<feature-name>/api-contracts.md`, following `skills/api-contract-first/templates/api-contracts-template.md` — it is the shape of `api-contracts.md`, the contract index and decision record that sits beside the artefacts: one row per surface with protocol, standard, artefact path and reason, plus the clients, the versioning stance and what is frozen since when. It does not replace any artefact below.
- Every design has an API. If you cannot identify the API, the design is not finished — go back to Step 1. The API is the only customer-facing contract; everything else (UI, CLI, SDK, MCP, AI agent, partner integration, batch job) is a **client** of the API.
- Identify the protocol(s) and pick the **native contract standard for each protocol** — OpenAPI is not the universal answer. Use the table in `skills/api-contract-first/SKILL.md` ("Pick the right contract standard for the protocol") to choose. Quick reference:
  - **REST / HTTP** → OpenAPI 3.x (or Smithy if AWS-style with SDK gen)
  - **GraphQL** → GraphQL SDL (`.graphql` schema)
  - **gRPC** → Protocol Buffers (`.proto`, proto3)
  - **Async / events** (SQS, Kinesis, MSK / Kafka, EventBridge, SNS) → AsyncAPI 3.x + payload schema (JSON Schema / Avro / Protobuf depending on serializer)
  - **Data contracts** (warehouse, lakehouse, topics) → Open Data Contract Standard (ODCS) when adoptable; else the store's native schema language (dbt contracts, Iceberg/Delta schema, Avro, etc.)
  - **MCP tools** → MCP server manifest (`mcp-tools.json`) with JSON Schema for args
  - **AI agent tools** → provider-native tool spec (Anthropic / OpenAI / Bedrock) with JSON Schema for input
  - **Webhooks** → AsyncAPI (or OpenAPI for receiver-side) + JSON Schema payload
- For multi-protocol surfaces, produce **one artifact per protocol** (e.g., `openapi.yaml` + `asyncapi.yaml` if the service exposes both REST and events). Do not try to merge them into a single document.
- Produce: the appropriate contract artifact(s). Save with the canonical filename for each standard (`openapi.yaml`, `schema.graphql`, `service.proto`, `asyncapi.yaml`, `data-contract.yaml`, `mcp-tools.json`, etc.).
- 🚦 GATE: Present the API contract(s). Ask: "Does this API contract look right? Is the right standard chosen for each protocol? Is the contract stable enough that all clients (UI/CLI/SDK/MCP/agent/partner) can be built against it?"
- ⛔ DO NOT proceed to Step 3 until the user approves.

### Step 3: Threat Modeling (if security-sensitive)
- Read skill: skills/threat-modeling/SKILL.md
- Follow `skills/threat-modeling/templates/threat-model-template.md` — it is the shape of `threat-model.md`, including the terminal verdict block `agents/security-guardian.md` ends the file with.
- Load `agents/security-guardian.md` and review the design through the security guardian lens.
- Produce: Threat model with mitigations
- 🚦 GATE: Present the threat model. Ask: "Any security concerns I missed?"
- ⛔ DO NOT proceed to Step 4 until the user approves.
- If not security-sensitive, skip with note: "Low security impact, skipping formal threat model."

### Step 4: Design Review Checklist
- Read skill: skills/design-review/SKILL.md
- Load `agents/design-bar-raiser.md` and review the design through the design bar raiser lens. **Self-assessment is not a design review.** For a **Medium** or **Large** design, dispatch it as a sub-agent with author-isolated context: it receives the design artifacts, the API contract(s) and `requirements.md`, and **not** your rationale for any of them — a reviewer handed the author's reasoning reviews the reasoning instead of the design. For **Trivial** and **Small**, activate the persona in this context; the ceremony ladder scopes it (`AGENTS.md` → *Match the Ceremony to the Change*). It is the same review either way, with the reviewer isolated from the author where that pays for itself.
- Run the design review checklist as the dispatched reviewer, against the artifacts rather than against the intent behind them
- Present the reviewer's findings and checklist result, attributed to the reviewer — not a self-assessment of your own design
- If the review is contested — two defensible options and no agreement — load `agents/principal-engineer.md` and break the tie through the principal engineer lens.
- 🚦 GATE: Ask: "Ready to proceed to implementation planning?"
- ⛔ DO NOT proceed to Step 5 until the user approves.

### Step 5: Spec-Driven Implementation (Create N specs)
- Read skill: skills/spec-driven-implementation/SKILL.md
- ONLY NOW create specs (requirements → design → tasks)
- Preserve dependency-management decisions from the approved design document in each relevant spec. Do not rediscover or redesign dependency behavior during `/build`.
- Preserve feature-flag lifecycle decisions from the approved design document in each relevant spec. Do not invent rollout, kill switch, or cleanup behavior during `/build`.
- Preserve operational-excellence decisions from the approved design document in each relevant spec. Do not invent dashboards, alarms, runbooks, metrics, severity expectations, or operational burden during `/build`.
- Each spec follows the templates EXACTLY (see Template Enforcement below)
- 🚦 GATE: Between EACH artifact (requirements → user approves → design → user approves → tasks → user approves)

### Step 5b: Spec Coherence Review (automatic gate)
- After all 3 spec artifacts (requirements.md, design.md, tasks.md) are approved for a slice, a **Spec Coherence Review** runs automatically before the spec is released to `/build`.
- This review checks for drift between the spec and the approved Design Document (contradictions, missing traceability, scope creep, dependency feasibility, operational-excellence consistency, one-way door consistency).
- Output is saved to `.bla/specs/<slice-name>/coherence-review.md` with a structured "Action Items for Build Agent" section that the build agent treats as binding constraints.
- If the review verdict is **NEEDS REVISION**, go back and fix the spec artifacts before releasing to `/build`.
- See `skills/spec-driven-implementation/SKILL.md` → Step 7 for full details and output format.

## Finding format

Every finding in a persisted report is written in this one shape:

`[SEVERITY] file:line — <concrete condition> → <observable wrong result> → <required fix>`

- The admission rule is **no anchor, no entry**: a finding with no `file:line` anchor — `file:section` for a document — does not enter the report. If you cannot point at the line, you have a suspicion to go investigate, not a finding to report.
- **ID** — `F-01`, `F-02`, … assigned in the order found and stable for the life of the report. A re-review reuses the ID and never renumbers, because the ID is how the fix, the re-review and any accepted-risk row all refer to the same thing.
- **Impact** — what breaks in production, in one line. This is the golden rule's answer, written down.
- **Confidence** — `high`, `medium` or `low`: how sure you are that the condition actually holds.
- **Minimal fix** — the smallest change that removes the condition, not the redesign you would prefer.
- **Status** — one of `OPEN`, `FIXED`, `ACCEPTED-WITH-RISK`, `NOT-REPRODUCIBLE`, `SUPERSEDED`, defined in `skills/code-review-bar-raising/SKILL.md` → *Finding lifecycle in a persisted report*.

`[SEVERITY]` is a slot, not a literal: write the label this surface already uses and let the canonical level appear in the report's `Findings:` counts line (`AGENTS.md` → *One Severity Scale and One Verdict Scale*).

Order the findings by impact. The rule is literal: **priority is impact, never confidence.** A `low`-confidence finding about silent data loss outranks a `high`-confidence finding about a name. Confidence tells the author how hard to look before acting; it never demotes a finding and is never a reason to leave one out.

**IDs and the lifecycle apply only to a report persisted to disk** — the Medium and Large ceremony levels, where a file exists for a later review to update. An inline review of a Trivial change carries no IDs and no lifecycle: there is no file, so there is nothing to renumber and nothing to supersede. The anchor rule and the golden rule still apply; they cost nothing.

The threat model of Step 3 and the review checklist of Step 4 are persisted reports, so both carry IDs and the lifecycle. For a design finding the anchor is the design document's section (`design-doc.md §4`) or the contract artifact and the path inside it (`openapi.yaml` → `/orders` `post`) — that is this surface's `file:line`.

## Important: Boundary with /build

The `/design` command is responsible for creating ALL specs. The `/build` command does NOT create specs — it reads existing specs and executes their tasks. If `/build` is invoked and no specs exist, it must stop and tell the user to run `/design` first.

## Output

Save to `.bla/design/<feature-name>/`:
- `design-doc.md`
- `api-contracts.md`
- API contract artifact(s) — **one per protocol**, using the canonical standard:
  - REST → `openapi.yaml`
  - GraphQL → `schema.graphql`
  - gRPC → `service.proto`
  - Async / events → `asyncapi.yaml` + `schemas/<event-name>.{json,avsc,proto}`
  - Data contract → `data-contract.yaml` (ODCS) or store-native (`model.yml` for dbt, etc.)
  - MCP → `mcp-tools.json`
  - AI agent tools → `tools.json`
- `threat-model.md`
- `review-checklist.md`

Save specs to `.bla/specs/<slice-name>/`:
- `requirements.md`
- `design.md`
- `tasks.md`

**Flow metrics.** `/design` owns five of the six events for the `design` phase — `phase_started`,
`phase_completed`, `gate_approved`, `gate_rework` and `review_blocking_finding` — and appends each as one
JSON line to `.bla/metrics.jsonl`: `phase_started` at the end of Step 0, once the proportionality
check returns Medium or above; `phase_completed` once the artifacts above are saved; `gate_approved` or
`gate_rework` at the Step 4 and Step 5b gates, according to the verdict; and one `review_blocking_finding`
per finding admitted at canonical severity BLOCKING in the threat model or the review checklist, carrying
its `F-NN` ID. It never emits `spec_completed`, which `/build` owns — no command emits an event another one
owns (owner table in `docs/flow-metrics.md`). **Emit only at Medium and above**; at Trivial and Small emit
nothing. If the line cannot be written — no writable tree, no `docs/` directory, the adopter declined —
state in one line that the flow measurement for this phase was not recorded, and **continue**: measurement
never blocks a gate.
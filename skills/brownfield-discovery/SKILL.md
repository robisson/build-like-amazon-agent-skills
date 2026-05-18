---
name: Brownfield Discovery
description: Reverse-engineer an existing project to produce a Design Doc, API contracts, and a Threat Model anchored in the real code, IaC, and observability. Run once per project. Output anchors all subsequent /spec and /build invocations.
leadership_principles:
  - Dive Deep
  - Are Right, A Lot
  - Insist on the Highest Standards
  - Bias for Action
---

# Brownfield Discovery

## Overview

Build Like Amazon's canonical flow assumes a greenfield path: `/wb` → `/design` → `/spec` → `/build`. Most real adoption happens on **existing projects** with code, IaC, CI/CD, observability, and on-call already running — but no BLA artifacts.

This skill closes that gap. It does an **engineering reverse pass** on the project: reads the code, IaC, CI, dashboards, and external dependency calls, then produces a Design Document, API contracts, and a Threat Model anchored in the **real state** of the system. Subsequent `/spec` and `/build` invocations use these reverse-engineered artifacts as their anchor — exactly as they would use canonical artifacts in greenfield.

This is not retroactive approval. The output carries a banner saying "REVERSE-ENGINEERED — not approved by any bar raiser, used as context, not as historical decision record." It exists so the agent stops re-discovering the project on every invocation and so future bar raisers have something to compare against.

## When to Use

- The project already exists (significant code, IaC, CI present) and there are no BLA artifacts (`docs/design/`, `docs/working-backwards/`)
- The user asks for a **medium or large** change in such a project (small / trivial changes don't need this — they go through the proportionality ladder directly)
- The user explicitly invokes `/onboard`
- Periodically, when the project drifts significantly from the prior reverse-engineered baseline (architecture change, major refactor)

**Do NOT use for:**
- Greenfield projects (use `/wb` → `/design` instead)
- Projects that already have a canonical Design Doc (use that as the anchor)
- Trivial or small changes (the ladder in `using-amazon-skills/SKILL.md` handles those without needing discovery)
- "Just to have docs" — discovery is a means to anchor future changes, not documentation for documentation's sake

## Amazon Context

Inside Amazon, services accumulate years of decisions that live only in the heads of long-tenured engineers and in the code. New owners onboarding a service do **System Onboarding** — a structured pass where they read the code, the runbooks, the COE history, and produce a written summary of the system as it is. This skill is the same pattern: a one-time, structured pass that produces written artifacts so the next reader (human or agent) is not starting from scratch.

The artifacts produced are deliberately marked as reverse-engineered. Pretending a reverse-engineered Design Doc is the same as one approved by a Design Bar Raiser would corrupt the process — bar raisers exist precisely because retroactive justification is not the same as upfront design.

## The Process

`brownfield-discovery` runs in **one of three paths**, picked by the user via `AskUserQuestion` at the start. The differences:

| Path | Purpose | Output | Time |
|---|---|---|---|
| **A — Anchor** (default, recommended) | Anchor the agent on the real state of the project so future `/spec` and `/build` are precise. Does **not** touch customer / problem / PR/FAQ. | Design Doc + API contracts + Threat Model + patterns-observed | ~15–30min |
| **B — Reverse Working Backwards** | Validate that the project is solving the right customer problem, **as-built**. Inferred PR/FAQ with hard questions for the user where the code cannot answer. | Path A's output + reverse-engineered customer-profile / problem-statement / solution-sketch / PR/FAQ (DRAFT, INFERRED) + bar-raiser questions | ~30–45min |
| **C — Forward WB + Gap Analysis** | Run a fresh Working Backwards as if greenfield (with full approval gates), then compare it to the existing project. Surfaces strategic gaps. | Path A's output + full WB artifacts + `gap-analysis.md` | ~1–2h, with gates |

The agent presents these three as **outcome-framed options** (not process names) and runs the chosen path. The shared engine (Steps 1–6 below) is the same; Path B and C **extend** Path A with additional steps.

---

### Step 0: Pick the path

Use `AskUserQuestion` to surface the three options to the user, framed by outcome:

> Detected: existing project, no BLA artifacts. How would you like to use `/onboard`?
>
> [A] **Anchor only** — produce a Design Doc, API contracts, and a Threat Model from the existing code. Future `/spec` and `/build` use these as anchor. *Does not* try to recover the customer story or PR/FAQ. Recommended for "I'll keep building here, give me the agent the context it needs." ~15–30min.
>
> [B] **Validate the *why*** — everything in [A], plus an inferred PR/FAQ reconstructed from the code, README, and docs. The doc-bar-raiser persona surfaces hard questions where the code can't tell us why. Recommended for "I built fast and want to check whether I'm solving the right problem." ~30–45min.
>
> [C] **Forward WB + Gap Analysis** — full `/wb` from scratch (5 stages with approval gates) as if this were greenfield, with the agent reading the existing code during the conversation. At the end, produces a `gap-analysis.md` comparing "what we'd build today" vs "what exists." Recommended for "I'm pivoting / re-strategizing / want to revalidate from scratch." ~1–2h.

If the user does not answer or asks the agent to pick, default to **A**.

---

### Steps 1–6 — Shared engine (run in all 3 paths)

These steps form Path A in full. Path B and Path C extend them with additional steps below.

#### 1. Inventory pass (read-only, ~5–10min)

Read the project in breadth, not depth. Goal: a bird's-eye view.

- **Languages, frameworks, runtime versions** — `package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, `Cargo.toml`, etc.
- **Entrypoints** — handlers, `main`, Lambda function entries, controllers, queue consumers, scheduled jobs
- **IaC** — CloudFormation templates, CDK code, Terraform, Pulumi, Kubernetes manifests
- **CI/CD** — `.github/workflows`, `.gitlab-ci.yml`, `buildspec.yml`, `Jenkinsfile`, pipeline configs
- **Observability** — structured logging libraries, metrics emission, alarms / dashboards declared in IaC, OpenTelemetry instrumentation
- **External dependencies** — HTTP clients, SDK clients (DynamoDB, S3, etc.), queue producers/consumers, database connections
- **Tests** — unit / integration / e2e coverage; testing frameworks
- **Config** — environment variables, parameter store, config files; what's externalized vs hardcoded
- **Auth / security boundaries** — middleware, IAM roles, API keys, JWT verification, encryption usage
- **Data stores** — schemas, migrations, ownership

Produce a brief inventory list. Don't write prose yet.

#### 2. Architecture inference (~5–10min)

From the inventory, infer:

- **High-level architecture** — components, data flows (read path / write path), sync vs async boundaries. Express as a Mermaid diagram.
- **Existing API surface(s)** — what does this service expose? REST endpoints (route table → OpenAPI), gRPC services (`.proto` files or inferred from code), event topics/queues (publishers, subscribers, payload shapes), CLI commands, MCP tools, etc.
- **Patterns present (or absent)** — single-instance? Multi-AZ? Multi-region? Cell-based? Bulkhead isolation? Control-plane / data-plane split? Static stability? Event-driven with outbox? Saga? Cross-reference `patterns/*/PATTERN.md` and assess whether each is **present**, **partial**, or **absent**.
- **Trust boundaries** — where untrusted input enters; how it's validated; what crosses an authentication/authorization boundary.

For each inference, note your **confidence level** (high / medium / low) and the **evidence** that supports it (file paths, line ranges, IaC resources). Inferences with low confidence are flagged for the user.

#### 3. Reverse-engineer the Design Document

Produce `docs/design/<service-name>/design-doc.md` using the canonical template (`skills/design-document/templates/design-doc-template.md`), with these adjustments:

- **Banner at top** — must say:
  > ⚠️ **REVERSE-ENGINEERED** — produced by `brownfield-discovery` from the existing codebase on `<date>`. Not approved by any bar raiser. Use as context for future changes, not as a historical record of decisions made. Sections marked LOW CONFIDENCE were inferred without strong evidence and should be reviewed.

- **Per-section confidence**: each section ends with a confidence line: `[Confidence: HIGH / MEDIUM / LOW]` and one sentence on what supports the rating.

- **Section 1 (Problem Statement)** — likely **LOW** in Path A: the customer problem rarely lives in the code. Pull what you can from the README, docstrings, marketing pages if present; otherwise mark explicitly as "TO BE FILLED — customer context not inferable from code." (In Path B and C, this section is filled more completely — see Steps 7+ below.)

- **Section 2 (Requirements)** — **MEDIUM to HIGH** for non-functional requirements that show up in code (latency targets in alarms, throughput in autoscaling configs, error budgets in dashboards). Functional requirements: **MEDIUM** at best — list the observable behaviors the API exposes.

- **Section 3 (Proposed Architecture)** — **HIGH** confidence: this is the strongest part of reverse-engineering. Diagrams, components, data flows, storage choices.

- **Section 4 (Alternatives Considered)** — **NOT INFERABLE**. Mark as: "Not reverse-engineered — alternatives considered at original design time are not recoverable from code. Future changes should re-evaluate alternatives in context."

- **Section 5 (Trade-offs)** — **MEDIUM**: infer from architecture choices made (e.g., "this service uses DynamoDB; the implied trade-off is key-value over ad-hoc query, accepting that analytical queries require a separate path"). Flag inferred trade-offs explicitly.

- **Section 6 (Cost Estimation)** — **MEDIUM** if billing data accessible; otherwise estimate from infrastructure footprint (instance counts, storage GB, request volume from metrics). Mark assumptions.

- **Section 7 (Operational Concerns)** — **HIGH**: existing alarms, dashboards, runbooks (if present) are observable directly. List them as-is. Gaps (no alarm for X) are findings, not failures.

- **Section 8 (Testing Strategy)** — **HIGH**: what tests exist; what's missing.

The Design Doc is **not pristine** — it carries the project's existing debt visibly. Don't paper over gaps; surface them.

#### 4. Reverse-engineer the API Contracts

For each API surface identified in step 2, produce the canonical contract artifact (per `skills/api-contract-first/SKILL.md` mapping):

- **REST**: if `openapi.yaml` exists, link it; if not, generate one from route definitions in code (Express/Fastify routes, FastAPI decorators, Spring `@RequestMapping`, etc.). Save to `docs/design/<service>/openapi.yaml`.
- **gRPC**: link existing `.proto` files; if missing (rare), reconstruct from generated stubs.
- **GraphQL**: link existing schema; if absent (rare), inspect resolvers.
- **Events / async**: produce an `asyncapi.yaml` describing channels (queues / topics) and operations (publish / subscribe), plus payload schemas (JSON Schema / Avro / Protobuf) inferred from event producers' code.
- **MCP tools**: read tool definitions if exposed.
- **CLI / SDK**: list commands, flags, exit codes; output schemas.

Each artifact carries a header comment: `# REVERSE-ENGINEERED from <source files>. Confidence: HIGH/MEDIUM/LOW. Review before relying on this for client integration.`

#### 5. Reverse-engineer the Threat Model

Produce `docs/design/<service>/threat-model.md`:

- **Trust boundaries observed** — where untrusted input enters; auth/authz checkpoints; encryption boundaries.
- **Existing controls** — auth middleware, input validation, encryption at rest / in transit, secrets management (where), audit logging.
- **Obvious gaps** — missing input validation on a public endpoint, secrets in environment variables without rotation, logs that may contain PII, unauthenticated internal endpoints.
- **STRIDE quick pass** — for each major component, list which STRIDE categories have observable mitigations and which don't.

This is **not a complete threat model** — it's a starting baseline. Mark as such.

#### 6. Pattern catalog cross-reference

For each pattern in `patterns/*/PATTERN.md`, note: **present**, **partial**, or **absent** in the current architecture. This goes into a section of the Design Doc and into a separate `patterns-observed.md`, becoming input for future `/design` invocations that scan the pattern catalog.

Don't recommend pattern changes here — that's a future `/design` decision. Only document what's there.

---

### Path A only — close out

After steps 1–6, present the closing summary via `AskUserQuestion`:

> Path A complete. Produced in `docs/design/<service>/`:
> - `design-doc.md` — confidence: HIGH on architecture/operations, LOW on customer problem and alternatives
> - API contracts — confidence HIGH (one artifact per protocol used)
> - `threat-model.md` — baseline only
> - `patterns-observed.md`
>
> [A] Accept as starting context (recommended)
> [B] Review LOW-confidence sections together
> [C] Discard

If [A]: save artifacts; brief end-of-onboarding summary; done.
If [B]: walk through LOW-confidence sections; prompt for input; update.
If [C]: delete or move to `docs/design/_discarded/`.

**Skip Steps 7+ if Path A was chosen.**

---

### Path B — Reverse Working Backwards (extends 1–6)

#### 7. Reverse-engineer the WB artifacts (~10–20min)

Produce inferred WB artifacts in `docs/working-backwards/<service-name>/`. Each artifact carries the same banner as the Design Doc — **REVERSE-ENGINEERED, INFERRED**, with per-section confidence.

Sources for inference:
- README, top-level project docs, comments
- API endpoint names and shapes (suggests intended capabilities)
- UI labels, error messages, copy that's visible to end users (suggests audience)
- Documentation in `docs/`, especially anything that looks like requirements or design discussion
- Test names (often describe customer-visible behaviors)
- Issue tracker / commit messages (when present)

Produce these files (DRAFT, INFERRED):

- **`customer-profile.md`** — who appears to be the customer based on the artifacts. Confidence will usually be **LOW**: inferring "who" from code is unreliable.
- **`problem-statement.md`** — what problem the project appears to solve. Pull from README + docs; do not fabricate.
- **`solution-sketch.md`** — the existing system, described in the language of "what this lets the customer do." Higher confidence — derived from API + UI surface.
- **`prfaq.md`** — DRAFT press release + FAQ, with each FAQ answer either filled (from inferable content) or marked `TO BE FILLED — needs customer evidence`.

**Mark every section that depends on customer evidence as `INFERRED — needs validation`.** Never fabricate. The customer story is the part that the code cannot answer.

#### 8. Doc Bar Raiser pass (mandatory in Path B)

Activate the `doc-bar-raiser` persona (`agents/doc-bar-raiser.md`) in **"Inferred PR/FAQ review" mode**. The persona's job here is *not* to bless the PR/FAQ — it's to surface **the questions the user has to answer themselves** by talking to real customers / sponsors / stakeholders.

Produce `docs/working-backwards/<service-name>/bar-raiser-questions.md` with the structured questions, grouped by section (customer, problem, solution, business case, metrics).

#### 9. Path B closing gate

Present via `AskUserQuestion`:

> Path B complete. Produced everything from Path A, plus inferred WB artifacts in `docs/working-backwards/<service>/`.
>
> Notably: the doc-bar-raiser surfaced N questions where the code cannot tell us *why*. Strongly recommend you answer them before continuing.
>
> [A] Accept as starting context. I'll keep the bar-raiser questions visible for future invocations.
> [B] Walk through the bar-raiser questions with me now.
> [C] Discard the WB artifacts (keep Path A's design artifacts).

---

### Path C — Forward WB + Gap Analysis (full /wb run, then compare)

Path C is the heaviest path. It is intended for **strategic re-evaluation** — pivots, major refactors, "we lost our way" moments. It runs the canonical Working Backwards flow with full approval gates, **knowing** the existing project, and produces a gap analysis at the end.

#### 7'. Run Working Backwards from scratch (full /wb flow)

Hand off to the canonical `working-backwards` skill (`skills/working-backwards/SKILL.md`). Run all 5 stages with their mandatory approval gates:

- Listen → Define → Invent → Refine → Test

**Critical**: during this WB run, the agent has read access to the existing project. Use it to:
- Acknowledge what already exists when the user proposes a solution ("you already have X — does the customer profile we just defined still match?")
- Push back when the WB the user is constructing diverges from what's been built ("you said the customer is A, but the existing system mostly serves B — which is right?")

**Equally critical**: do *not* let the existing project bias the WB. The whole point of Path C is to re-derive from the customer outwards. If the WB says "build Y" and Y already exists, that's a useful confirmation. If WB says "build Z" and the system actually does W, that's a strategic gap — record it.

The WB artifacts go to `docs/working-backwards/<service>/` as canonical (no INFERRED banner — they were produced through the real WB process with the user).

#### 8'. Gap Analysis (~10–20min)

After WB approval, produce `docs/design/<service>/gap-analysis.md`:

- **Capabilities in the new WB** — what the PR/FAQ says the product enables for the customer
- **Capabilities in the existing system** — derived from the Design Doc produced in Steps 1–6
- **Gaps**:
  - **In WB but not built** — capabilities the customer should have per the new WB but the project does not deliver
  - **Built but not in WB** — capabilities that exist but don't map to anything in the new WB (candidates for sunset / refactor / re-justification)
  - **Built but materially different** — capabilities present in both, but with implementation that diverges from what the new WB envisions
- **Recommendations**: for each gap, classify as `extend` (add to project) / `sunset` (remove from project) / `re-justify` (keep but document why) / `align` (refactor toward the WB target).

The recommendations are *suggestions for future `/design` invocations* — Path C does not implement them.

#### 9'. Path C closing gate

Present via `AskUserQuestion`:

> Path C complete. Produced:
> - Full canonical WB artifacts in `docs/working-backwards/<service>/`
> - Reverse-engineered design artifacts in `docs/design/<service>/` (from steps 1–6)
> - `gap-analysis.md` cross-referencing them
>
> [A] Accept all. Future `/spec` and `/build` use the design artifacts as anchor; the gap-analysis informs the next `/design`.
> [B] Walk through the gap-analysis with me to prioritize next moves.
> [C] Discard all and go back to default.

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|---|---|
| "I'll remember the project's architecture" | Persisted in `docs/design/<service>/design-doc.md` so the next agent invocation reads it instead of re-inferring |
| "I'll be careful not to break things" | Threat model + existing alarms documented; patterns catalog cross-referenced so future changes know what's load-bearing |
| "We'll add docs later" | Discovery is a one-time investment that pays back on every subsequent `/spec` and `/build` |
| "Reverse-engineered docs are as good as designed ones" | Banner + per-section confidence + non-inferable sections marked explicitly |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---|---|---|
| "We don't have time to onboard the agent on this project" | Without onboarding, the agent re-discovers the project on every invocation, hallucinating interfaces and missing existing constraints. The cost compounds. | Spend the 15-30min once; save it on every subsequent change. |
| "The reverse-engineered Design Doc is good enough as a permanent record" | It's a starting point, not the source of truth. Bar raiser approval is what makes a Design Doc canonical. | Use it as anchor; promote sections to canonical only after a real `/design` review when scope warrants. |
| "We should reverse-engineer everything before any change" | Diminishing returns. Trivial and small changes don't need the discovery. | Run `/onboard` only when the next change is medium or larger (per the proportionality ladder). |
| "The agent should figure it out from code each time" | LLMs hallucinate when reading code without anchors. Persisted artifacts are the anchors. | Onboard once; persist; reuse. |

## Red Flags

- 🚩 Reverse-engineered Design Doc has no confidence ratings — the agent hid its uncertainty.
- 🚩 "Customer Problem" section is filled in with confidence HIGH — the agent inferred a customer story from code, which is rarely possible.
- 🚩 "Alternatives Considered" is filled in — alternatives at original design time are not recoverable from code; the agent fabricated them.
- 🚩 Threat Model is presented as complete — it's a baseline, not a full threat model.
- 🚩 Discovery was run on a trivial project where no future medium/large change is planned — wasted effort.
- 🚩 The user accepted the discovery output without reviewing low-confidence sections, then later relied on those sections as if they were canonical.

## Verification

### Path A (always)
- [ ] User explicitly chose a path (A / B / C) via Step 0 — choice is logged in the output summary
- [ ] Inventory pass produced a concrete list of languages, IaC, CI, observability, deps, data stores, auth boundaries
- [ ] Architecture inference produced a Mermaid diagram with confidence ratings on each component
- [ ] `docs/design/<service>/design-doc.md` exists with the REVERSE-ENGINEERED banner and per-section confidence
- [ ] At least one API contract artifact exists per identified API surface, with the standard appropriate to the protocol (OpenAPI / `.proto` / AsyncAPI / etc.)
- [ ] Threat model baseline exists with trust boundaries, existing controls, obvious gaps
- [ ] Pattern catalog cross-reference exists in the Design Doc and as a separate `patterns-observed.md`
- [ ] Subsequent `/spec` and `/design` invocations are aware of these artifacts (they appear in repo state detection)

### Path B (in addition to A)
- [ ] WB artifacts exist in `docs/working-backwards/<service>/` with **REVERSE-ENGINEERED, INFERRED** banner and per-section confidence
- [ ] No customer story / problem / metric was fabricated — sections that depend on customer evidence are marked `INFERRED — needs validation`
- [ ] `bar-raiser-questions.md` exists with structured hard questions from the doc-bar-raiser

### Path C (in addition to A)
- [ ] Full canonical WB artifacts produced through the canonical `working-backwards` skill, with all 5 approval gates honored — these do **not** carry the INFERRED banner because they came from the user, not from inference
- [ ] `gap-analysis.md` exists with capabilities-in-WB / capabilities-built / gaps grouped as `extend / sunset / re-justify / align`

## Tenets

1. **Discovery is investment, not documentation.** It exists to anchor future changes, not to look professional.
2. **Confidence ratings are non-negotiable.** Never claim certainty about what was inferred without strong evidence.
3. **The customer story rarely lives in code.** Don't fabricate it. In Path B, surface the questions; do not invent the answers.
4. **Reverse-engineered ≠ approved.** The banner is mandatory on inferred artifacts. Bar raisers exist precisely because retroactive justification is not the same as upfront design. Path C produces canonical WB artifacts because they go through the canonical WB process *with the user* — those don't carry the INFERRED banner.
5. **Run once, reuse always.** If the project drifts significantly later, re-run discovery — but in steady state, the artifacts persist and serve every subsequent `/spec` and `/build`.
6. **Surface debt; don't paper over it.** Gaps in observability, missing tests, missing controls — list them as findings. Reverse-engineering is also auditing.
7. **The user picks the path; the agent does not assume.** A new project may need only Path A. A pivot needs Path C. The choice belongs to the user, with outcome-framed options.

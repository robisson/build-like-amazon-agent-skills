# API Contracts: [System or Feature Name]

## Instructions

This file is an **index and a decision record**. It is never the contract. The contract is the
protocol-native artefact — `openapi.yaml`, `schema.graphql`, `service.proto`, `asyncapi.yaml`,
`data-contract.yaml`, `mcp-tools.json`, `tools.json` — and this file says which ones exist, where they
are, which standard each one uses and why. A markdown file cannot be code-generated from, mocked
against, or diffed for breaking changes; those artefacts can.

**Start by enumerating the surfaces, then pick a standard per surface.** Do not start from REST.
**OpenAPI is not the universal answer** — it is the answer for one protocol out of the ten in the table
*Pick the right contract standard for the protocol* in `skills/api-contract-first/SKILL.md`, which is the
authority for the choice. And **one protocol, one canonical artefact — do not merge them**: a service
exposing REST and events produces both an `openapi.yaml` and an `asyncapi.yaml`, never one hybrid file.

**The bar:** every surface a client can reach appears in section 1 with a real artefact path. A surface
with an empty `Artefact path` cell is an undocumented contract, which Hyrum's Law makes a promise anyway.
A surface described only in prose here is not specified — go write its artefact.

Used by `/design` Step 2 and by `/onboard` Path A, where the cells carry the confidence of what was read
off existing code rather than what was designed.

---

## 1. Surface Index

| Surface | Protocol | Standard chosen | Artefact path | Why this standard |
|---|---|---|---|---|
| [Public order API] | REST / HTTP | OpenAPI 3.x | `openapi.yaml` | [clients already generate SDKs from it] |
| [Internal query API] | GraphQL | GraphQL SDL | `schema.graphql` | [the schema *is* the contract] |
| [Service-to-service] | gRPC | Protocol Buffers, proto3 | `service.proto` | [code-gen for both ends] |
| [Order events] | Async — SQS / Kafka / EventBridge | AsyncAPI 3.x + payload schema | `asyncapi.yaml`, `schemas/order-placed.avsc` | [channel level plus the serializer's own schema] |
| [Warehouse table] | Data contract | ODCS, or the store's native schema | `data-contract.yaml` | [producer and consumer can both adopt it] |
| [Agent tool server] | MCP | MCP server manifest | `mcp-tools.json` | [the tool list a client discovers] |
| [Model tool calls] | AI agent tools | Provider-native tool spec | `tools.json` | [provider requires its own shape] |
| [Subscriber callbacks] | Webhooks | AsyncAPI, or OpenAPI receiver-side | `webhooks.asyncapi.yaml` | [publisher-to-subscriber is first class] |
| [`mytool` CLI] | CLI | Documented explicitly — commands, flags, exit codes, JSON output schemas | `cli-contract.md`, `output-schemas/` | [no industry standard exists] |
| [Java client] | SDK | Language-native interfaces, generated upstream | [generated from `openapi.yaml`] | [never hand-written] |

Delete the rows that do not exist. Do not delete a row because its artefact has not been written yet —
that is the finding this table is for.

*Good: `POST /v1/payments` and the `payment.settled` event are two surfaces, two rows, two artefacts: `openapi.yaml` and `asyncapi.yaml` plus `schemas/payment-settled.avsc`.*

*Bad: one row, "REST API — `openapi.yaml`", with the events described in a paragraph underneath it.*

## 2. Clients

Every consumer of every surface above, with the artefact it builds against. **All clients are equivalent
from the contract's point of view** (`AGENTS.md` → *API First (the 2002 API Mandate, applied)*): a web UI,
a mobile app, a CLI, an SDK, an MCP server, an AI agent, another internal service, a partner integration,
a batch ETL job. There is no privileged client and no "frontend" exception.

| Client | Type | Surfaces it consumes | Owner | Breaking-change contact |
|---|---|---|---|---|
| [checkout-web] | web UI | [Public order API] | [team] | [alias] |
| [partner-x] | partner integration | [Order events] | [external] | [alias] |

If a client needs behavior a surface does not expose, **evolve the surface**. Logic added to the client to
work around a missing API capability is the defect this section exists to make visible.

## 3. Compatibility and Versioning Stance

One row per surface. The rules for what is and is not breaking, and the three versioning strategies, are
in `skills/api-contract-first/SKILL.md` → *Backward Compatibility Rules* and *Versioning Strategy*. Do not
restate them here; state the **choice** and the **commitment**.

| Surface | Versioning strategy | Current version | Oldest supported | Sunset commitment | Compatibility test |
|---|---|---|---|---|---|
| [Public order API] | [additive, date-based] | [2026-03-01] | [2025-01-15] | [12 months after successor GA] | [contract test in CI, name it] |

*Good: additive date-based; new clients get the latest, existing clients stay frozen at their declared version; breaking-change detection runs in CI as `contract-diff` against the published baseline.*

*Bad: we will version when we need to.*

## 4. Frozen State

This is what `/build` and `agents/implementation-verifier.md` compare the implementation against. A
surface with no freeze date is not frozen, and an implementation cannot be verified against it.

| Surface | Artefact path | Frozen at (commit or tag) | Frozen since | Approved by | Changes since freeze |
|---|---|---|---|---|---|
| [Public order API] | `openapi.yaml` | [`a1b2c3d`] | [date] | [reviewer] | [none, or the PR that unfroze it] |

An unfrozen surface may still be implemented against — say so explicitly in the last cell, because a
reviewer cannot otherwise tell a deliberate draft from an accidental one.

## Verification

- [ ] Every surface a client can reach has a row in section 1, including events, data and tool surfaces
- [ ] The standard in each row is the protocol's native one, not the one already familiar to the team
- [ ] No row merges two protocols into one artefact
- [ ] Every artefact path either exists on disk or is named as a gap with an owner
- [ ] Every client in section 2 names the surfaces it consumes and who to contact before a breaking change
- [ ] Every surface has a versioning strategy and a sunset commitment, not "to be decided"
- [ ] A contract test that fails the build on a breaking change is named per surface, or its absence is a finding
- [ ] Every frozen surface carries a commit or tag and a date

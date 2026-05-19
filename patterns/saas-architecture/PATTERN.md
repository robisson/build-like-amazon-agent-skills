---
name: SaaS Architecture
category: multi-tenancy
maturity: proven (AWS SaaS Factory, hundreds of ISV implementations)
source:
  title: "SaaS Architecture Fundamentals (AWS Whitepaper)"
  url: https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/saas-architecture-fundamentals.html
  published: 2022-08-03
applies_when:
  - building a software product delivered as a service (not installed software)
  - multiple customers (tenants) share the same operational environment
  - business requires frictionless onboarding and rapid time-to-value
  - operational efficiency matters more than per-customer customization
  - growth strategy depends on adding tenants without proportional ops cost
  - you need unified deployment, billing, metrics, and identity across all tenants
related_patterns:
  - cell-based-architecture
  - control-plane-data-plane-split
  - strangler-fig
  - feature-flag-lifecycle
leadership_principles:
  - Customer Obsession
  - Frugality
  - Bias for Action
  - Ownership
---

# SaaS Architecture

## Overview

SaaS (Software as a Service) is first and foremost a **business model**, not an architecture pattern. The architecture you build exists to serve business objectives: agility, operational efficiency, frictionless onboarding, innovation velocity, market responsiveness, and growth.

The core insight: instead of each customer running their own environment (installed software model), all tenants are managed, onboarded, billed, and operated through a **single, unified experience**. Tenants consume the same version of the software, deployed through the same pipeline, monitored through the same operational pane.

This does not mean all resources must be shared. Resources can be **siloed** (dedicated to a tenant) or **pooled** (shared across tenants) at any layer — compute, storage, queues, caches. The unifying principle is that all tenants are managed collectively through shared control plane services, regardless of how the underlying application plane is deployed.

---

## When to Choose This

Adopt SaaS architecture when **most** of these hold:

- You are building a product that multiple customers will consume as a service
- Growth matters: adding 100 or 1,000 customers should not proportionally increase operational cost
- Customers expect frictionless onboarding (self-service sign-up, immediate time-to-value)
- You want to release features to all customers simultaneously through a single deployment pipeline
- Per-customer customization creates unsustainable operational overhead
- You need tenant-aware metrics, billing, and operational visibility

## When NOT to Choose This

- The product is a one-off system for a single organization (internal tooling)
- Regulatory or contractual requirements mandate completely separate, customer-controlled environments with no shared infrastructure
- Customer count will remain permanently small (< 5) and each requires deep customization
- You are building infrastructure, not application software (use cell-based instead)

---

## Core Concepts

### SaaS is a Business Model

Defining what it means to be SaaS starts with agreeing on one key principle: SaaS is driven by business objectives, not technology choices.

Key business objectives:
- **Agility** — continually adapt to market, customer, and competitive dynamics
- **Operational efficiency** — promote scale and rapid release cycles through a unified operational footprint
- **Frictionless onboarding** — decrease time-to-value for every new tenant
- **Innovation** — foundational elements enable rapid response to customer needs
- **Market response** — react to market dynamics in near real-time instead of quarterly release cycles
- **Growth** — align agility and efficiency to target a growth model

### You're a Service, Not a Product

In a service-centric model, the focus shifts from features and functions to the **experience** customers have with your service. How quickly are customers onboarded? How fast do they achieve value? How rapidly are their needs addressed? The *as-a-service* model puts experience attributes on equal or higher footing than features.

### Control Plane vs. Application Plane

Every SaaS environment decomposes into two distinct planes:

```
┌─────────────────────────────────────────────────────────────┐
│                     Control Plane                            │
│  ┌──────────┐ ┌────────┐ ┌──────────┐ ┌─────────┐          │
│  │Onboarding│ │Identity│ │  Billing │ │ Metrics │          │
│  └──────────┘ └────────┘ └──────────┘ └─────────┘          │
│  ┌──────────┐ ┌────────────────────┐                        │
│  │  Tenant  │ │Admin User Mgmt     │                        │
│  └──────────┘ └────────────────────┘                        │
├─────────────────────────────────────────────────────────────┤
│                   Application Plane                          │
│  ┌─────────────────────────────────────────────────┐        │
│  │         Tenant Provisioning                      │        │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐           │        │
│  │  │Service A│ │Service B│ │Service C│           │        │
│  │  └─────────┘ └─────────┘ └─────────┘           │        │
│  └─────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**Control Plane** — services that onboard, authenticate, manage, operate, and analyze the multi-tenant environment. These are NOT multi-tenant themselves; they are global to all tenants. Includes: onboarding, tenant management, identity, billing, metrics, admin user management.

**Application Plane** — where the multi-tenant functionality of your application resides. Includes: your business logic microservices, tenant provisioning, and the actual resources tenants consume.

### Core Services (Control Plane)

- **Onboarding** — frictionless mechanism for introducing new tenants. Orchestrates user creation, tenant creation, isolation policies, and per-tenant resource provisioning.
- **Tenant** — centralizes policies, attributes, and state of tenants. A tenant is not an individual user; a tenant is associated with many users.
- **Identity** — connects users to tenant context. Influences authentication, authorization, and the overall management of user profiles.
- **Billing** — integrates with billing providers, collects consumption and activity data, generates bills per tenant.
- **Metrics** — captures how tenants use the system, how they consume resources, and how they engage. Shapes operational, product, and business strategies.
- **Admin user management** — supports the SaaS provider's operational experience for monitoring and managing the environment.

---

## Deployment Models: Silo and Pool

Instead of the confusing term "single-tenant" vs. "multi-tenant", use **silo** and **pool**:

- **Silo** — a resource is dedicated to a given tenant
- **Pool** — a resource is shared by tenants

These are NOT all-or-nothing concepts. They apply selectively to individual layers:

| Service | Compute | Storage | Pattern |
|---------|---------|---------|---------|
| Order service | Siloed (per-tenant deployment) | Pooled (shared DB, tenant partition key) | Mixed |
| Product service | Pooled (shared compute) | Pooled (shared storage) | Full pool |
| Invoice service | Pooled (shared compute) | Siloed (per-tenant DB) | Mixed |

### Full Stack Silo and Pool

At the macro level, you may have:

- **Full stack pool** — all tenants share all resources (basic tier)
- **Full stack silo** — a tenant gets a completely dedicated stack (premium tier)
- **Mixed** — basic tenants pooled, premium tenants siloed

Even in full-stack silo, all tenants run the same version, deployed by the same pipeline, and are managed through the same control plane. No one-off customization.

---

## SaaS Identity

Every user token must carry **both user identity and tenant identity**. This *SaaS identity* flows through every microservice and is used to:

- Create tenant-aware logs
- Record per-tenant metrics
- Meter billing
- Enforce tenant isolation
- Scope data access

Never rely on separate, standalone mechanisms that map users to tenants. This undermines security and creates architectural bottlenecks.

---

## Tenant Isolation

Tenant isolation is **separate from authentication and authorization**. A user can be authenticated and authorized yet still access another tenant's resources if isolation is not explicitly enforced.

Isolation uses tenant context to limit resource access:
- **Silo isolation** — entire stacks dedicated to a tenant; network or coarse-grained policies prevent cross-tenant access
- **Pool isolation** — shared resources (e.g., DynamoDB table items) require fine-grained policies that scope access to the current tenant's partition

### Isolation vs. Security

| Mechanism | Purpose |
|-----------|---------|
| Authentication | Verify identity |
| Authorization | Control access to functionality |
| Tenant isolation | Limit access to tenant-scoped resources |

All three are required. None is a substitute for the others.

---

## Data Partitioning

Data partitioning describes how tenant data is stored. It is separate from isolation (how access is controlled):

- **Siloed data** — separate storage construct per tenant (e.g., separate DynamoDB table per tenant)
- **Pooled data** — co-mingled data partitioned by tenant identifier (e.g., tenant ID as partition key in a shared table)

The partitioning strategy is influenced by isolation requirements, noisy-neighbor concerns, and compliance needs.

---

## Tiering

SaaS environments commonly support multiple tiers that map to silo/pool decisions:

| Tier | Deployment Model | Characteristics |
|------|-----------------|-----------------|
| Basic | Full stack pool | Shared resources, lower cost, standard SLAs |
| Advanced | Mixed | Some services siloed (e.g., dedicated DB) |
| Premium | Full stack silo | Dedicated stack, highest SLA, dedicated resources |

Tiers drive pricing, isolation, performance guarantees, and operational priorities.

---

## Metering, Metrics, and Billing

Three distinct concepts:

- **Metering** — instrumentation that captures tenant activity/consumption to generate bills (number of requests, active users, storage consumed)
- **Metrics** — all data captured to analyze trends across business, operations, and technology domains (per-tenant and aggregate)
- **Billing** — the mechanism that aggregates metering events and generates invoices through a billing provider

---

## SaaS Migration

When migrating from installed software to SaaS:

1. **Start with business strategy**, not technology — what segments, tiers, service experience?
2. **Build shared services first** — identity, onboarding, metrics, billing, operations (the control plane)
3. **Land any application model** in the middle — even full-stack silo is valid SaaS if managed collectively
4. **Iterate toward pooling** — modernize the application plane over time based on customer feedback

The shared services provide the SaaS experience from day one, even if the underlying application is initially siloed per tenant.

---

## SaaS vs. Managed Service Provider (MSP)

| Aspect | SaaS | MSP |
|--------|------|-----|
| Version | All tenants run same version | Different versions per customer |
| Operations | Single unified operations experience | Operationally separate environments |
| Customization | No one-off customization | May allow per-customer customization |
| Onboarding | Frictionless, automated | Manual provisioning with automation |
| Business proximity | Provider deeply connected to metrics, tenant activity | Often a level removed |

Automating the install of environments does not make you SaaS. SaaS requires unified management, single version, shared services, and collective operations.

---

## Skill Impact Map

When this pattern is adopted, the following skills change behavior:

| Skill | Impact |
|-------|--------|
| `/design` | Design must address: control plane vs. application plane separation, silo/pool decisions per service, tenant isolation strategy, SaaS identity propagation, tiering model |
| `/design` (API) | APIs must be tenant-aware: tenant context in every request, scoped data access, per-tenant rate limiting, tiered throttling |
| `/design` (Threat Model) | Threat model must include: cross-tenant access vectors, isolation boundary failures, tenant impersonation, noisy-neighbor DoS, data co-mingling risks |
| `/build` | Code must propagate tenant context through all layers. Logging, metrics, and data access must be tenant-scoped. Never rely on implicit tenant resolution. |
| `/deploy` | Single pipeline deploys to all tenants (pooled) and all silo environments. No per-tenant versions. Canary/progressive deployment must consider per-tenant health metrics. |
| `/operate` | Dashboards must show per-tenant AND aggregate metrics. Alarms must detect noisy neighbors. Onboarding service health is critical-path. Billing accuracy is operational. |
| `/operate` (ORR) | ORR must verify: tenant isolation tested, noisy-neighbor detection in place, onboarding flow exercised, tenant-aware runbooks exist |
| `/spec` | Every spec for a SaaS workload must declare its silo/pool model and how tenant context flows through the feature |

---

## Key Decisions Checklist

Use during `/design` for any SaaS workload:

- [ ] Control plane services identified (onboarding, identity, tenant, billing, metrics, admin)
- [ ] Silo vs. pool decided per service and per resource layer (compute, storage, queues)
- [ ] Tiering model defined (which tiers, what silo/pool mapping per tier)
- [ ] SaaS identity design: how tenant context is embedded in tokens and propagated
- [ ] Tenant isolation strategy per deployment model (silo: network policies; pool: fine-grained access policies)
- [ ] Data partitioning strategy (separate stores vs. tenant partition keys)
- [ ] Noisy-neighbor mitigation (throttling, resource limits, monitoring)
- [ ] Onboarding automation (zero-friction path from sign-up to first value)
- [ ] Metering instrumentation for billing and operational metrics
- [ ] Single-version deployment: no per-tenant customization, no per-tenant versions

---

## Trade-offs

| Dimension | Pool (shared) | Silo (dedicated) |
|-----------|--------------|-----------------|
| Cost efficiency | Higher — shared resources, better utilization | Lower — dedicated resources per tenant |
| Isolation strength | Requires explicit fine-grained policies | Naturally isolated via separation |
| Noisy neighbor risk | Higher — tenants compete for resources | Lower — blast radius contained |
| Operational complexity | Lower — fewer environments to manage | Higher — more environments to deploy/monitor |
| Onboarding speed | Fast — add a row, not an environment | Slower — must provision infrastructure |
| Compliance | May not satisfy strict data residency | Easier to demonstrate separation |

Most SaaS environments use a **mix** of silo and pool based on the needs of each service, data sensitivity, tier, and customer requirements.

---

## References

- [SaaS Architecture Fundamentals (AWS Whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/saas-architecture-fundamentals.html)
- [SaaS Lens — AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html)
- [AWS SaaS Factory](https://aws.amazon.com/partners/programs/saas-factory/)
- [Tenant Isolation Strategies (AWS Blog)](https://aws.amazon.com/blogs/apn/isolating-saas-tenants-with-dynamically-generated-iam-policies/)

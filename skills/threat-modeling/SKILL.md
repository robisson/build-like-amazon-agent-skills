---
name: Threat Modeling
description: Security threat modeling using STRIDE methodology adapted for cloud services. Covers data classification, IAM boundaries, encryption requirements, blast radius analysis, and systematic identification of attack vectors before code is written.
leadership_principles:
  - Customer Obsession
  - Ownership
  - Insist on the Highest Standards
  - Dive Deep
  - Earn Trust
---

# Threat Modeling

## Overview

Threat modeling is the systematic identification of security threats to a system BEFORE the system is built. It answers four questions: What are we building? What can go wrong? What are we going to do about it? Did we do a good enough job? You cannot secure a system by adding security after the fact—security must be designed in. Threat modeling is how you design it in.

A threat model is not a penetration test. Penetration testing finds bugs in implementation. Threat modeling finds flaws in design. A perfectly implemented system with a flawed design is still insecure. You do threat modeling at design time; you do pen testing at implementation time. Both are required; neither replaces the other.

## When to Use

- During the design phase of any new service or feature
- When adding new data flows (especially customer data or credentials)
- When changing authentication or authorization mechanisms
- When adding new external-facing endpoints (API, web, mobile)
- When integrating with a new third-party service
- When changing trust boundaries (new service-to-service communication)
- When an incident reveals a class of vulnerability (model similar systems)
- Before any Design Bar Raiser review for systems handling sensitive data

## Agent Persona

Load `agents/security-guardian.md` when reviewing the threat model. Use it to challenge trust boundaries, data classification, least privilege, encryption, blast radius, and missing abuse cases.

## Amazon Context

Threat models are living documents maintained alongside design documents. They are updated when the system changes, when new threat intelligence emerges, or when incidents reveal gaps. Every system that handles customer data, credentials, or payment information requires a formal threat model reviewed by security teams before launch.

The principle of "blast radius minimization" is paramount: design systems so that a compromise of one component cannot cascade to compromise the entire system. This drives decisions about service boundaries, IAM scope, encryption key separation, and network isolation.

## The Process

### 1. Data Classification

Before identifying threats, classify the data your system handles:

| Classification | Definition | Examples | Requirements |
|---------------|-----------|----------|-------------|
| **Restricted** | Compromise causes severe harm to customers or business. Regulatory implications. | Payment card numbers, SSNs, authentication credentials, encryption keys | Encrypted at rest AND in transit. Access logged. Minimal retention. Need-to-know access. Annual audit. |
| **Confidential** | Internal business data. Competitive advantage if disclosed. | Customer PII (name, email, address), internal financial data, unreleased product plans | Encrypted at rest AND in transit. Access controlled by role. Retention policy enforced. |
| **Internal** | Not public but low sensitivity. Operational data. | Service metrics, internal documentation, team rosters, non-sensitive logs | Encrypted in transit. Access controlled by team. Standard retention. |
| **Public** | Intended for public consumption. | Marketing content, public documentation, open-source code | Integrity protection (prevent tampering). No confidentiality requirements. |

**Rule**: A system's classification is determined by the HIGHEST classification of data it handles. A service that processes one Restricted field is a Restricted service.

### 2. System Decomposition

Create a Data Flow Diagram (DFD) that identifies:

#### Elements

- **External entities**: Users, third-party services, partner systems (outside your trust boundary)
- **Processes**: Your services, Lambda functions, containers, batch jobs
- **Data stores**: Databases, caches, S3 buckets, queues, logs
- **Data flows**: Every arrow between elements (API calls, events, file transfers)

#### Trust Boundaries

Draw lines around components that share the same trust level:

```
┌─────────────────────── Internet (Untrusted) ───────────────────────┐
│  [Browser]    [Mobile App]    [Partner API]                        │
└──────────────────────────┬─────────────────────────────────────────┘
                           │ TLS
┌──────────────────────────┼─── Public Subnet ───────────────────────┐
│                    [API Gateway + WAF]                              │
└──────────────────────────┬─────────────────────────────────────────┘
                           │ IAM Auth
┌──────────────────────────┼─── Private Subnet ──────────────────────┐
│                    [Application Service]                            │
│                           │                                        │
│              ┌────────────┼────────────┐                           │
│              ▼            ▼            ▼                           │
│        [DynamoDB]   [S3 Bucket]  [SQS Queue]                      │
└────────────────────────────────────────────────────────────────────┘
                           │ Cross-account role
┌──────────────────────────┼─── Separate Account ────────────────────┐
│                    [Audit Log Store]                                │
└────────────────────────────────────────────────────────────────────┘
```

Every crossing of a trust boundary is a potential attack surface.

### 3. STRIDE Analysis

For each element and data flow in the DFD, systematically analyze threats using STRIDE:

| Category | Threat | Question to Ask | Example |
|----------|--------|----------------|---------|
| **S**poofing | Identity falsification | Can an attacker pretend to be someone/something else? | Attacker forges JWT to impersonate another user |
| **T**ampering | Data modification | Can an attacker modify data in transit or at rest? | Man-in-the-middle modifies API request; attacker modifies S3 object |
| **R**epudiation | Denying actions | Can an actor deny performing an action with no proof? | Admin deletes records with no audit trail |
| **I**nformation Disclosure | Data leakage | Can an attacker access data they shouldn't? | Error messages expose internal system details; logs contain PII |
| **D**enial of Service | Availability disruption | Can an attacker make the system unavailable? | Unbounded request causes OOM; regex DoS; resource exhaustion |
| **E**levation of Privilege | Unauthorized access escalation | Can an attacker gain higher privileges? | SSRF to access instance metadata; SQL injection to admin role |

#### STRIDE Per Element

For each component in your DFD, fill in:

```
Component: [Name]
Trust Level: [What trust boundary is it in?]
Data Classification: [Highest classification of data it touches]

| STRIDE | Applicable? | Threat Scenario | Likelihood | Impact | Mitigation |
|--------|-------------|----------------|-----------|--------|-----------|
| Spoofing | Yes/No | [Specific scenario] | H/M/L | H/M/L | [Control] |
| Tampering | Yes/No | [Specific scenario] | H/M/L | H/M/L | [Control] |
| Repudiation | Yes/No | [Specific scenario] | H/M/L | H/M/L | [Control] |
| Info Disclosure | Yes/No | [Specific scenario] | H/M/L | H/M/L | [Control] |
| DoS | Yes/No | [Specific scenario] | H/M/L | H/M/L | [Control] |
| EoP | Yes/No | [Specific scenario] | H/M/L | H/M/L | [Control] |
```

### 4. IAM Boundary Design

#### Principles

1. **Each service has its own IAM role.** No shared roles between services.
2. **Roles are scoped to minimum needed actions and resources.** Use IAM Access Analyzer.
3. **Cross-service access uses role assumption**, not shared credentials.
4. **Human access to production is time-bounded and audited.** No persistent admin access.
5. **Separate accounts for separate blast radii.** Production, staging, and security tooling in different accounts.

#### IAM Threat Patterns

| Pattern | Threat | Mitigation |
|---------|--------|-----------|
| Shared IAM role across services | Compromise of one service = compromise of all | Separate role per service, minimum permissions |
| Wildcard resource in policy | Any resource accessible, not just intended ones | Explicit ARNs; use conditions for dynamic resources |
| No MFA on privileged operations | Credential theft = full access | Require MFA for all human privileged operations |
| Long-lived access keys | Keys leaked in code/logs = persistent access | Use IAM roles with temporary credentials; rotate keys <90 days |
| Instance metadata accessible | SSRF → credential theft via 169.254.169.254 | IMDSv2 (require token); restrict network access to metadata |
| Over-scoped Lambda execution role | Compromised function has broad access | Least privilege per function; separate roles per Lambda |

### 5. Encryption Requirements

#### Encryption Decision Matrix

| Data State | Classification: Restricted | Classification: Confidential | Classification: Internal |
|-----------|---------------------------|-----------------------------|-----------------------|
| At rest | KMS CMK (team-managed key), key rotation enabled | KMS CMK or AWS-managed key | AWS-managed key or SSE-S3 |
| In transit | TLS 1.2+ (mandatory) | TLS 1.2+ (mandatory) | TLS 1.2+ (recommended) |
| In memory | Clear from memory after use; don't log | Standard precautions | Standard precautions |
| In backups | Same encryption as primary | Same encryption as primary | AWS-managed encryption |
| In logs | MUST NOT appear in logs | Mask/redact; tokenize | Acceptable in logs |

#### Key Management

- **Key per service**: Each service has its own KMS key. Compromise of one service's key doesn't expose another service's data.
- **Key per data classification**: Restricted and Confidential data use different keys.
- **Key rotation**: Automatic annual rotation enabled. Manual rotation immediately on suspected compromise.
- **Key access policy**: Only the owning service's role can use the key for Encrypt/Decrypt. Admin access (for rotation, deletion) is a separate role.
- **Cross-account key access**: Grant via key policy, not IAM policy. Explicit deny for any principal not explicitly allowed.

### 6. Blast Radius Analysis

Blast radius = the extent of damage if a single component is fully compromised.

#### Analysis Process

For each component, answer:
1. **If this component is fully compromised (attacker has complete control), what can they access?**
2. **What other systems trust this component?** (follow the trust relationships)
3. **What data can be exfiltrated?** (follow the data flows)
4. **Can the attacker move laterally?** (check network access, shared credentials, role chaining)
5. **What's the recovery time?** (how long to detect, contain, and recover)

#### Blast Radius Containment Strategies

| Strategy | Implementation | Reduces Blast Radius By |
|----------|---------------|------------------------|
| Service isolation | Separate IAM roles per service | Prevents lateral movement via credentials |
| Network segmentation | Security groups with explicit allow lists | Prevents network-based lateral movement |
| Account boundaries | Separate AWS accounts for different trust levels | Hard boundary; cross-account requires explicit grant |
| Data compartmentalization | Different encryption keys per data domain | Compromised key exposes only one domain |
| Privilege separation | Read and write through different roles/paths | Compromised read path can't modify data |
| Secret rotation | Automated, frequent rotation of all secrets | Limits window of exposure for leaked secrets |
| Circuit breakers | Rate limits between services | Prevents cascading resource exhaustion |

#### Blast Radius Scoring

Rate each component:

| Score | Blast Radius | Criteria |
|-------|-------------|----------|
| Critical | System-wide compromise | Component has admin access, cross-service credentials, or access to encryption keys for multiple services |
| High | Multiple services affected | Component can access data or systems beyond its own boundary |
| Medium | Single service affected | Compromise is contained to this service's data and functionality |
| Low | Minimal impact | Component is stateless, has no persistent data access, and is easily replaced |

Any component scoring "Critical" must be re-architected to reduce blast radius.

### 7. Common Attack Patterns (Cloud-Specific)

| Attack | Vector | Mitigation |
|--------|--------|-----------|
| SSRF to metadata | Application fetches attacker-controlled URL → 169.254.169.254 | IMDSv2; block metadata IP in application egress |
| Confused deputy | Attacker tricks your service into acting on their behalf | External ID in cross-account roles; validate caller identity |
| S3 bucket enumeration | Predictable bucket names → unauthorized access | Random bucket name suffixes; block public access; bucket policies |
| Lambda event injection | Malicious input in event payload | Validate and sanitize all event fields; treat events as untrusted |
| IAM privilege escalation | iam:PassRole + lambda:CreateFunction = arbitrary code execution as any role | Restrict iam:PassRole to specific role ARNs; permissions boundaries |
| Supply chain attack | Compromised dependency in build pipeline | Pin dependencies; verify checksums; scan for vulnerabilities; use private registry |
| Log injection | Attacker injects malicious content into logs → exploits log viewers | Sanitize log output; structured logging; separate log viewers from production |

## Mechanisms Over Good Intentions

| Intention | Mechanism |
|-----------|-----------|
| "I'll encrypt sensitive data" | KMS key policies that deny unencrypted writes; S3 bucket policies that require SSE |
| "I'll follow least privilege" | IAM Access Analyzer reviews weekly; over-permissioned roles auto-generate tickets |
| "I'll audit access to sensitive data" | CloudTrail data events mandatory for all Restricted/Confidential data stores |
| "I'll keep secrets safe" | Secrets Manager with automated rotation; credential scanning in CI blocks commits with secrets |
| "I'll limit blast radius" | Separate AWS accounts per trust boundary; network isolation verified by automated tests |

## Common Rationalizations

| What They Say | Why It's Wrong | What To Do Instead |
|---------------|---------------|-------------------|
| "We'll add security later, we need to ship fast" | Security bolted on after the fact is expensive and incomplete. Architecture decisions made without threat modeling create vulnerabilities that require re-architecture to fix. | Threat model during design. It takes 2-4 hours. Re-architecting for security later takes weeks. |
| "We're not a target; attackers focus on bigger companies" | Automated attacks don't discriminate. Bots scan every public endpoint. Supply chain attacks target small components. You ARE a target the moment you have a public endpoint or store customer data. | Model threats regardless of perceived risk. The model will tell you which threats are low-likelihood. Don't skip the analysis. |
| "Our data isn't that sensitive" | Have you classified it? PII includes name + email. Payment data includes partial card numbers. Internal data includes access patterns that reveal business strategy. | Classify your data formally. You may be surprised what's actually Confidential when you apply the classification framework. |
| "IAM is too complex; we'll use broad permissions and tighten later" | Tightening permissions breaks things. Teams never tighten. Broad permissions persist forever and become the assumed blast radius. | Start with zero permissions. Add one permission at a time. Use IAM Access Analyzer to verify you're not over-provisioned. |
| "Encryption at rest doesn't matter if the network is secure" | Networks are breached. Insiders exist. Backups are stolen. Disks are improperly decommissioned. Encryption at rest is defense in depth, not redundancy. | Encrypt at rest. Always. The cost is negligible. The protection is essential. |

## Red Flags

- No threat model exists for a service handling customer data
- Threat model was written once and never updated (system has changed significantly since)
- STRIDE analysis is superficial ("Spoofing: N/A" for an authentication system)
- IAM policies use `Resource: "*"` with no documented justification
- Same encryption key used across multiple services
- No data classification has been performed; team can't articulate what classification their data falls under
- Blast radius analysis shows a single component compromise = system-wide breach
- Secrets (API keys, passwords, tokens) found in code repositories, config files, or logs
- No audit logging for access to Restricted or Confidential data
- Trust boundaries aren't defined; all services communicate freely without authentication
- No automated credential scanning in the CI pipeline
- IMDSv1 is enabled (allows SSRF-based credential theft)

## Verification

- [ ] Data classification is documented for all data the system handles
- [ ] Data Flow Diagram exists showing all components, data stores, and trust boundaries
- [ ] STRIDE analysis completed for every component crossing a trust boundary
- [ ] IAM roles follow least privilege (verified by IAM Access Analyzer)
- [ ] Encryption requirements match data classification (see matrix above)
- [ ] Blast radius analysis completed; no "Critical" components exist without documented mitigation plan
- [ ] Secrets are stored in Secrets Manager/Parameter Store, never in code or config files
- [ ] Automated credential scanning runs in CI pipeline
- [ ] Audit logging enabled for all access to Restricted/Confidential data
- [ ] IMDSv2 enforced on all EC2 instances
- [ ] Network segmentation verified (security groups have explicit allow lists, not 0.0.0.0/0)
- [ ] Threat model reviewed by AppSec for any system handling Restricted data
- [ ] Threat model update schedule defined (at minimum: every major feature addition)

## Tenets

1. **Security is designed in, not bolted on.** Threat modeling happens at design time. If you're threat modeling after launch, you're patching, not designing.
2. **Blast radius above all.** The most important security property is containment. A compromised component must not cascade. Design for breach, not just prevention.
3. **Data classification drives everything.** Encryption, access control, logging, retention—all determined by data classification. Classify first, then secure.
4. **Assume breach.** Design every component as if the adjacent component is already compromised. This drives proper authentication, authorization, and isolation between every boundary.
5. **Least privilege is the default.** Zero permissions until explicitly granted. Every grant is documented, justified, scoped, and auditable.

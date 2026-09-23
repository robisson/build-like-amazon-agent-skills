# Threat Model: [System or Feature Name]

## Instructions

This is the artefact `/design` Step 3 produces and `agents/security-guardian.md` writes: the design-time
answer to *what can go wrong*, while the design is still cheap to change. A threat model written after
launch is a patch list.

Derive every section from `skills/threat-modeling/SKILL.md`. It owns the classification table, the STRIDE
question set, the IAM threat patterns, the encryption matrix and the blast-radius scoring. This template
only **records the decisions** — do not restate the skill in it.

**The bar:** every component that crosses a trust boundary has a STRIDE row, and every row you marked
applicable has a named mitigation. A row with no mitigation and no accepted-risk row is an **open
finding** — it holds the Step 3 gate; it does not quietly become a note.

**Severities are this file's own `Critical` / `High` / `Medium` / `Low`**, written exactly as
`agents/security-guardian.md` writes them, with the CWE reference kept in the finding text. They map to
the canonical levels in `AGENTS.md` → *One Severity Scale and One Verdict Scale* (`Critical` and `High`
both map to BLOCKING, without becoming interchangeable). **Introduce no new label.** `Status` values are
the ones in `skills/code-review-bar-raising/SKILL.md` → *Finding lifecycle in a persisted report*.

**Size:** 2–4 hours for one service. If it is taking a day, you have started designing, not modelling.

---

## 1. Scope and Data Classification

**System:** [name] — **Design doc:** [path] — **Author:** [name] — **Date:** [date] — **Reviewer:** [name]

| Data | Classification | Where it rests | Where it flows | Retention |
|---|---|---|---|---|
| [field or dataset] | Restricted / Confidential / Internal / Public | [store] | [consumers] | [period] |

**System classification:** [the HIGHEST above — one Restricted field makes this a Restricted system]

*Good: `card_last4` — Confidential — DynamoDB table `orders`, KMS CMK — flows only to the receipt renderer — 7 years.*

*Bad: we store some customer data, so: Confidential.*

## 2. Trust Boundaries

A diagram is welcome. The list is mandatory, because section 3 indexes it.

| # | Boundary | What crosses it | Authentication at the crossing |
|---|---|---|---|
| B1 | Internet → public subnet | [browser → API Gateway] | [TLS 1.2+, WAF, JWT] |
| B2 | [service → separate account] | [PutLogEvents] | [cross-account role with external ID] |

*Good: B2 — app service → audit account; crossed by PutLogEvents; cross-account role, external ID, no inbound path back.*

*Bad: internal services talk to each other.*

## 3. STRIDE per Boundary-Crossing Component

One table per component named in a crossing above. `N/A` is an answer only with a reason beside it —
`Spoofing: N/A` on an authentication surface is a red flag, not an analysis.

**Component:** [name] — **Trust level:** [boundary] — **Data classification:** [highest it touches]

| ID | STRIDE | Threat scenario | Likelihood | Severity | Mitigation | Status |
|---|---|---|---|---|---|---|
| F-01 | Spoofing | [one concrete line] | H / M / L | Critical / High / Medium / Low | [the named control] | OPEN |
| F-02 | Tampering | | | | | FIXED |
| F-03 | Repudiation | | | | | |
| F-04 | Info disclosure | | | | | |
| F-05 | DoS | | | | | |
| F-06 | Elevation of privilege | | | | | |

*Good: F-04 — Info disclosure — High (CWE-209) — stack traces returned to the client expose the ORM and the table names — mitigation: error mapper returns `error_code` plus `request_id` only, stack traces to the log sink.*

*Bad: F-04 — Info disclosure — Medium — we should be careful with error messages — mitigation: review logging.*

## 4. IAM Boundary

| Principal | Role | Actions granted | Resources | Why this is the minimum |
|---|---|---|---|---|
| [service or human] | [one role per service] | [explicit actions] | [explicit ARNs] | [the operation that needs it] |

Wildcards get their own line: every `Resource: "*"` or `Action: "*"` left in the design is a finding in
section 3 with an ID, not a footnote here.

## 5. Encryption per Classification

| Data (from section 1) | At rest | In transit | In logs | Key owner and rotation |
|---|---|---|---|---|
| [dataset] | [KMS CMK / AWS-managed / SSE-S3] | [TLS 1.2+] | [MUST NOT appear / masked / acceptable] | [role, annual] |

The skill's decision matrix is the authority. A cell that disagrees with it needs a reason in this row,
not a softer cell.

## 6. Blast Radius

| Component | Score | If fully compromised, the attacker reaches | Lateral path | Containment in place |
|---|---|---|---|---|
| [name] | Critical / High / Medium / Low | [data and systems] | [how they move] | [isolation, separate key, separate account] |

**Any component scoring `Critical` must be re-architected or carry an accepted-risk row below.** A
`Critical` blast radius with neither is an open BLOCKING finding.

## 7. Accepted Risks

Same four columns the ORR checklist uses. A risk with no owner and no date is not accepted, it is
forgotten (`AGENTS.md` → Operating Behavior 3).

| Item # | Mitigation | Resolution Owner | Target Date |
|---|---|---|---|
| [F-0N, and the checkpoint it was accepted against] | [what reduces the exposure meanwhile, or "none"] | [name] | [date] |

## Verification

- [ ] Every dataset in section 1 has a classification, and the system classification is the highest one
- [ ] Every trust boundary in section 2 names what crosses it and how the crossing is authenticated
- [ ] Every boundary-crossing component has a section 3 table with all six STRIDE rows answered
- [ ] No applicable STRIDE row is missing a mitigation, or it appears in section 7 with an owner and a date
- [ ] No `Critical` blast-radius component is left without a re-architecture or an accepted-risk row
- [ ] Secrets are in Secrets Manager or Parameter Store — none in code, config or logs
- [ ] The update trigger is stated: this model is revisited on [event], at minimum every major feature
- [ ] Reviewed by AppSec if any data is Restricted

---

The file ends with the terminal verdict block from `agents/security-guardian.md`, and nothing after it:

```markdown
Verdict: NOT APPROVED (local: open Critical finding)
Report: .bla/design/<feature-name>/threat-model.md
Findings: BLOCKING 3 (Critical 1, High 2) · IMPORTANT 4 (Medium 4) · MINOR 2 (Low 2) · QUESTION 0
```

# Authorization Decision Memorandum

> Fictional example built from [`templates/ato_memo.md`](../../templates/ato_memo.md).
> Not a real authorization. All names are fictional.

**MEMORANDUM FOR:** Dana Ruiz, Director of HR Operations, Acme Defense Fabrication
**FROM:** Morgan Lee, Chief Information Officer and Authorizing Official
**DATE:** 2026-11-02
**SUBJECT:** Authorization decision for Acme HR Portal (AHR)

## 1. Decision

**Authorization to Operate (ATO)**, with the terms and conditions in Section 4.

## 2. System

| Field | Value |
|---|---|
| System name / ID | Acme HR Portal (AHR) |
| Security categorization | `SC Acme HR Portal = {(confidentiality, MODERATE), (integrity, MODERATE), (availability, LOW)}` |
| Authorization boundary | SSP Section 3.3 |
| Package version reviewed | SSP v1.0, SAR v1.0, POA&M dated 2026-11-02 |

## 3. Basis for the decision

I reviewed the SSP, the independent SAR, and the POA&M. The assessment found no High-risk
weaknesses. The four open items are process gaps with funded milestones, and the one
configuration weakness was corrected and verified during the assessment. The portal replaces
emailed PDF pay statements, which carry more disclosure risk than the residual risk described
here. I find the residual risk acceptable to Acme Defense Fabrication.

## 4. Terms and conditions

1. POAM-0001 and POAM-0002 (Moderate) must close by their scheduled dates. A slip of more than
   30 days must be reported to me with a revised plan.
2. Monthly ConMon reports go to the ISSM and to me, as described in the ConMon plan.
3. No new external interconnection or new information type is added without a security impact
   analysis and my approval.
4. Rollout past the 200-user pilot may proceed once POAM-0001 milestone M2 is complete.

## 5. Authorization period

- Authorization termination date: **2029-11-02**, unless superseded by a move to ongoing
  authorization based on ConMon results.
- Reauthorization triggers: significant change (see ConMon plan Section 5), a new High finding
  not fixed within its deadline, a security incident involving PII, or a material change in
  threat.

## 6. Accepted risks

| POA&M ID | Control | Risk rating | Accepted until |
|---|---|---|---|
| POAM-0003 | CP-4 | Low | 2027-02-26 |
| POAM-0004 | AU-6 | Low | 2026-12-31 |

## 7. Signature

| Authorizing official | Signature | Date |
|---|---|---|
| Morgan Lee, CIO | /s/ Morgan Lee (fictional) | 2026-11-02 |

CC: Priya Natarajan (ISSM), Sam Okafor (ISSO), Chief Information Security Officer

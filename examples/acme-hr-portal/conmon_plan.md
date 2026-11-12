# Continuous Monitoring Plan: Acme HR Portal

> Fictional example built from [`templates/conmon_plan.md`](../../templates/conmon_plan.md).

| Field | Value |
|---|---|
| System | Acme HR Portal (AHR) |
| Categorization | `SC Acme HR Portal = {(confidentiality, MODERATE), (integrity, MODERATE), (availability, LOW)}` |
| Plan owner | Sam Okafor, ISSO (fictional) |
| Approved by | Morgan Lee, AO, 2026-11-02 |
| Version | 1.0 |

## 1. Purpose

Keep the AO current on the portal's security posture between authorizations. The plan
focuses on the areas that matter most for a Moderate PII system: who has access, whether
known flaws get fixed on time, and whether the system still matches its approved configuration.

## 2. Roles

| Role | ConMon responsibility |
|---|---|
| System owner (Dana Ruiz) | Funds remediation; approves changes; owns CP-4 testing |
| ISSO (Sam Okafor) | Runs reviews, keeps the POA&M current, writes monthly report |
| System administrators | Patch, scan, and fix configuration drift |
| Control assessor (Internal Audit) | Annual reassessment of rotating control subset |
| AO (Morgan Lee) | Reviews reports; decides on risk acceptance and reauthorization |

## 3. Monitoring activities

| Activity | Controls supported | Frequency | Tool / evidence | Owner |
|---|---|---|---|---|
| Authenticated OS vulnerability scan | RA-5, SI-2 | Weekly | Scanner reports | Sysadmins |
| Dependency scan in CI | RA-5, SI-2, SA-11 | Every build | Pipeline logs | App team |
| CIS benchmark compliance scan | CM-6, CM-7 | Monthly | Compliance report | Sysadmins |
| TLS configuration scan | SC-8, CM-6 | Monthly | Scan output | ISSO |
| Portal-specific audit log review | AU-6 | Weekly | Recurring review ticket | ISSO |
| Privileged role and inactive account review | AC-2, AC-2(3), AC-6 | Quarterly (automated daily check after POAM-0001) | Review sign-off | ISSO, HR admin |
| POA&M review | CA-5 | Monthly | `poam.csv` | ISSO |
| Contingency plan test | CP-4 | Annually | After-action report | System owner |
| Control reassessment (1/3 of controls per year) | CA-2, CA-7 | Annually | SAR addendum | Internal Audit |

## 4. Remediation timelines

| Severity | Remediate within |
|---|---|
| Critical | 15 days |
| High | 30 days |
| Moderate | 60 days |
| Low | 90 days |

## 5. Change management and security impact analysis

- Every change request in the change system includes a short security impact analysis
  completed by the ISSO.
- Significant changes, which need the AO's attention and may require reassessment:
  - a new external interconnection
  - a new information type, especially one that could raise the categorization
  - moving to a different hosting platform or region
  - replacing the authentication method
  - major application rewrites

## 6. Reporting

| Report | Audience | Frequency | Contents |
|---|---|---|---|
| ConMon status report | AO, ISSM | Monthly | Scan trend, overdue items, POA&M changes, significant changes, incidents |
| Annual security review | AO | Annually (each November) | Reassessment results, updated risk determination, recommendation on ongoing authorization |

## 7. Reauthorization triggers

- Any significant change listed in Section 5
- A High finding not fixed within 30 days
- A security incident involving employee PII
- A material change in threat or in Acme's risk tolerance

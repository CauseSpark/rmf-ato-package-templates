# FIPS 199 Security Categorization Worksheet: Acme HR Portal

> Fictional example built from [`templates/fips199_categorization.md`](../../templates/fips199_categorization.md).
> Generated values can be reproduced with
> `python src/categorize.py examples/acme-hr-portal/categorization_input.json`.

| Field | Value |
|---|---|
| System name | Acme HR Portal |
| System acronym / ID | AHR |
| Organization | Acme Defense Fabrication (fictional) |
| System owner | Dana Ruiz, Director of HR Operations (fictional) |
| Prepared by | Sam Okafor, ISSO (fictional) |
| Date | 2026-07-14 |
| Version | 1.0 |

## 1. System description

The Acme HR Portal is a web application where about 1,200 employees view pay statements,
update contact and direct-deposit details, and enroll in benefits, and where 15 HR staff
manage personnel records. The boundary covers the web tier, application tier, database, and
the portal's admin jump host in Acme's commercial IaaS tenant. Enterprise SSO, payroll
processing, and the benefits carrier are outside the boundary.

## 2. Information types

| # | Information type | Source / reference | C | I | A | Adjustment rationale |
|---|---|---|---|---|---|---|
| 1 | Employee personnel records | Org-defined (HR management family, SP 800-60 approach) | MODERATE | MODERATE | LOW | SSNs and home addresses; disclosure enables identity theft. HR can work from exports during an outage. |
| 2 | Payroll and compensation | Org-defined | MODERATE | MODERATE | LOW | Tampering with direct deposit could redirect pay. Payroll runs in a separate provider system. |
| 3 | Benefits enrollment | Org-defined | MODERATE | LOW | LOW | The carrier confirms elections before they take effect. |
| 4 | Public job postings | Org-defined | NOT APPLICABLE | LOW | LOW | Already public on the careers site. |
| 5 | Authentication and audit records | Org-defined | MODERATE | MODERATE | LOW | Log tampering would hide misuse. |

## 3. System categorization (high-water mark)

| Objective | System impact | Driven by information type(s) |
|---|---|---|
| Confidentiality | MODERATE | 1, 2, 3, 5 |
| Integrity | MODERATE | 1, 2, 5 |
| Availability | LOW | all |

**Security category:**
`SC Acme HR Portal = {(confidentiality, MODERATE), (integrity, MODERATE), (availability, LOW)}`

**Overall impact level:** MODERATE
**Initial SP 800-53B baseline:** Moderate

## 4. Special considerations

- Privacy: yes, the system processes employee PII. The Privacy Officer reviewed it on
  2026-07-10, and a privacy impact assessment is attached to the SSP (Attachment F).
- Aggregation: combining SSN, home address, and bank details in one record supports keeping
  confidentiality at MODERATE. The team considered HIGH and rejected it: the data covers
  employees only, at a scale of about 1,200 records.
- Dependencies: the portal inherits identity controls from the Acme Enterprise Identity
  Service, which has its own authorization.

## 5. Review and approval

| Role | Name | Decision | Date |
|---|---|---|---|
| System owner | Dana Ruiz | Concur | 2026-07-15 |
| ISSO / ISSM | Sam Okafor / Priya Natarajan | Concur | 2026-07-15 |
| Authorizing official | Morgan Lee, CIO (fictional) | Approved | 2026-07-18 |

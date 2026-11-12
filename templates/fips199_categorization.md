# FIPS 199 Security Categorization Worksheet

> Template, personal study material. Replace everything in `<angle brackets>`.
> Method: [FIPS 199](https://csrc.nist.gov/pubs/fips/199/final) for impact levels,
> [FIPS 200](https://csrc.nist.gov/pubs/fips/200/final) for the high-water mark, and
> [SP 800-60 Vol. 1 Rev. 1](https://csrc.nist.gov/pubs/sp/800/60/v1/r1/final) for identifying
> information types. You can check the math with `python src/categorize.py <input.json>`.

| Field | Value |
|---|---|
| System name | `<system name>` |
| System acronym / ID | `<ID>` |
| Organization | `<organization>` |
| System owner | `<name, title>` |
| Prepared by | `<name, role>` |
| Date | `<YYYY-MM-DD>` |
| Version | `<x.y>` |

## 1. System description

`<Two or three sentences: what the system does, who uses it, and where its boundary is.>`

## 2. Information types

List every information type the system stores, processes, or transmits. For each one, record
the provisional impact level, any adjustment, and the reason. "N/A" is allowed for
confidentiality only, and only for public information.

| # | Information type | Source / reference | C | I | A | Adjustment rationale |
|---|---|---|---|---|---|---|
| 1 | `<type>` | `<SP 800-60 type or org-defined>` | `<L/M/H/NA>` | `<L/M/H>` | `<L/M/H>` | `<why>` |
| 2 | | | | | | |

## 3. System categorization (high-water mark)

| Objective | System impact | Driven by information type(s) |
|---|---|---|
| Confidentiality | `<L/M/H>` | `<#>` |
| Integrity | `<L/M/H>` | `<#>` |
| Availability | `<L/M/H>` | `<#>` |

**Security category:**
`SC <system> = {(confidentiality, <impact>), (integrity, <impact>), (availability, <impact>)}`

**Overall impact level:** `<LOW / MODERATE / HIGH>`
**Initial SP 800-53B baseline:** `<Low / Moderate / High>`

## 4. Special considerations

- Privacy: does the system process PII? `<yes/no, privacy officer consulted on YYYY-MM-DD>`
- Aggregation: does combining data raise impact above any single type? `<notes>`
- Dependencies: other systems whose impact this one inherits or affects. `<notes>`

## 5. Review and approval

| Role | Name | Decision | Date |
|---|---|---|---|
| System owner | | Concur / Non-concur | |
| ISSO / ISSM | | Concur / Non-concur | |
| Authorizing official or designee | | Approved / Returned | |

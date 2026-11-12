# Continuous Monitoring (ConMon) Plan

> Template, personal study material. Builds on the Monitor step in
> [SP 800-37 Rev. 2](https://csrc.nist.gov/pubs/sp/800/37/r2/final) and the program guidance in
> [SP 800-137](https://csrc.nist.gov/pubs/sp/800/137/final). The frequencies are placeholders;
> set them from your organization's ConMon strategy and the system's risk.

| Field | Value |
|---|---|
| System | `<name / ID>` |
| Categorization | `<SC string>` |
| Plan owner | `<ISSO name>` |
| Approved by | `<AO or designee>`, `<date>` |
| Version | |

## 1. Purpose

`<One paragraph: keep the AO informed about the system's security posture between
authorizations, and catch drift early.>`

## 2. Roles

| Role | ConMon responsibility |
|---|---|
| System owner | |
| ISSO | |
| System administrators | |
| Control assessor | |
| Authorizing official | |

## 3. Monitoring activities

| Activity | Controls supported | Frequency | Tool / evidence | Owner |
|---|---|---|---|---|
| Authenticated vulnerability scanning | RA-5, SI-2 | `<weekly>` | | |
| Configuration compliance scan | CM-6, CM-7 | `<monthly>` | | |
| Audit log review | AU-6 | `<weekly>` | | |
| Account review | AC-2 | `<quarterly>` | | |
| POA&M review and update | CA-5 | `<monthly>` | | |
| Contingency plan test | CP-4 | `<annually>` | | |
| Control subset reassessment | CA-2, CA-7 | `<annually, rotating 1/3 of controls>` | | |

## 4. Remediation timelines

| Severity | Remediate within |
|---|---|
| Critical | `<n> days` |
| High | `<n> days` |
| Moderate | `<n> days` |
| Low | `<n> days` |

## 5. Change management and security impact analysis

- Every change request gets a security impact analysis before approval.
- Significant changes (examples: `<new interconnection, new data type, platform migration>`)
  are reported to the AO and may require reassessment or reauthorization.

## 6. Reporting

| Report | Audience | Frequency | Contents |
|---|---|---|---|
| ConMon status report | AO, ISSM | `<monthly>` | scan trends, POA&M status, changes, incidents |
| Annual security review | AO | `<annually>` | reassessment results, updated risk determination |

## 7. Reauthorization triggers

- `<Significant change to the system or its environment>`
- `<New High-risk finding not remediated within the timeline>`
- `<Security incident affecting the system>`
- `<Change in threat or in organizational risk tolerance>`

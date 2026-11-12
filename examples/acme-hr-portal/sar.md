# Security Assessment Report: Acme HR Portal

> Fictional example built from [`templates/sar.md`](../../templates/sar.md).

| Field | Value |
|---|---|
| System | Acme HR Portal (AHR) |
| Categorization | `SC Acme HR Portal = {(confidentiality, MODERATE), (integrity, MODERATE), (availability, LOW)}` |
| Assessment type | Initial |
| Assessment window | 2026-09-28 to 2026-10-09 |
| Lead assessor | Jordan Pike, Acme Internal Audit (fictional) |
| Independence | Internal Audit reports to the Audit Committee, not to IT or HR |
| Report date / version | 2026-10-16, v1.0 |

## 1. Executive summary

The assessment team tested the system-specific and hybrid controls of the tailored Moderate
baseline. It accepted inherited controls based on the providers' current authorizations. Most
controls are satisfied. Five findings came up: one was corrected during the assessment, and
four remain open, two rated Moderate and two Low. None are High. The open items are process
gaps (account deactivation, patch timeliness, contingency testing, log review records), not
architectural weaknesses. In the assessor's view, the system's controls are generally effective.

| Result | Count |
|---|---|
| Controls assessed (system-specific and hybrid) | 142 |
| Satisfied | 137 |
| Other than satisfied | 5 |
| Findings: High / Moderate / Low | 0 / 2 / 3 (1 corrected) |

## 2. Scope and methodology

- Controls in scope: all system-specific and hybrid controls in SSP v0.9.
- Methods: examined the SSP, plans, tickets, and configuration exports. Interviewed the system
  owner, ISSO, two system administrators, and one HR administrator. Tested with authenticated
  vulnerability scans, a TLS configuration scan, an account inactivity query, and role-based
  access tests with test accounts.
- Limitations: the restore test was not observed because no test had been run yet (see AHR-2026-003).

## 3. Risk rating method

Likelihood × impact matrix from the template, with impact anchored to the system's
MODERATE confidentiality and integrity.

## 4. Findings

```
Finding ID:        AHR-2026-001
Control:           AC-2(3) Disable Accounts
Method:            Test
Observation:       6 local and service accounts showed no activity for 41 to 97 days and
                   were still enabled.
Requirement gap:   The SSP sets a 35-day inactivity limit; enforcement is a manual monthly review
                   that missed these accounts.
Likelihood:        Moderate
Impact:            Moderate
Risk rating:       Moderate
Recommendation:    Automate disabling at 35 days and alert the ISSO on exceptions.
Status at report:  Open
```

```
Finding ID:        AHR-2026-002
Control:           SI-2 Flaw Remediation
Method:            Test
Observation:       Two moderate-severity vulnerabilities in application dependencies were
                   78 and 85 days old.
Requirement gap:   The organization requires moderate-severity flaws to be fixed within 60 days.
Likelihood:        Moderate
Impact:            Moderate
Risk rating:       Moderate
Recommendation:    Update the dependencies, and fail CI builds on findings past their deadline.
Status at report:  Open
```

```
Finding ID:        AHR-2026-003
Control:           CP-4 Contingency Plan Testing
Method:            Examine, interview
Observation:       The contingency plan is approved but has never been tested.
Requirement gap:   The plan requires an annual test before or within the first year of operation.
Likelihood:        Low
Impact:            Low (availability is LOW)
Risk rating:       Low
Recommendation:    Run a tabletop exercise and a database restore test, and record the results.
Status at report:  Open
```

```
Finding ID:        AHR-2026-004
Control:           AU-6 Audit Record Review, Analysis, and Reporting
Method:            Examine, interview
Observation:       Weekly ISSO reviews were recorded for 5 of the last 12 weeks.
Requirement gap:   The SSP commits to weekly documented review.
Likelihood:        Moderate
Impact:            Low (SOC alerting still active)
Risk rating:       Low
Recommendation:    Use a recurring ticket with a checklist so every review leaves a record.
Status at report:  Open
```

```
Finding ID:        AHR-2026-005
Control:           CM-6 Configuration Settings
Method:            Test
Observation:       The load balancer accepted TLS 1.0 and 1.1.
Requirement gap:   The SSP requires TLS 1.2 or higher.
Likelihood:        Low
Impact:            Moderate
Risk rating:       Low
Recommendation:    Apply a TLS 1.2+ policy.
Status at report:  Corrected during assessment
```

## 5. Controls corrected during assessment

| Finding ID | Control | Correction | Verified by / date |
|---|---|---|---|
| AHR-2026-005 | CM-6 | Load balancer policy changed to TLS 1.2+ only | J. Pike, rescan 2026-10-07 |

## 6. Assessor statement

The assessment team assessed the controls listed in Section 2 with the stated methods. Apart
from the four open findings above, the controls are implemented correctly, operating as
intended, and producing the desired outcome. The authorization decision rests with the AO.

| Lead assessor signature | Date |
|---|---|
| /s/ Jordan Pike (fictional) | 2026-10-16 |

# System Security Plan: Acme HR Portal

> Fictional example built from [`templates/ssp_outline.md`](../../templates/ssp_outline.md).
> A real Moderate SSP covers every control in the tailored baseline. This example shows the
> full structure with a **representative set** of implementation statements, chosen to line up
> with the SAR findings, so it stays readable.

## Document control

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 0.1 | 2026-07-21 | Sam Okafor | Initial draft after categorization |
| 0.9 | 2026-09-12 | Sam Okafor | Implementation statements complete; ready for assessment |
| 1.0 | 2026-10-20 | Sam Okafor | Updated for SAR results and corrected CM-6 finding |

## 1. System identification

| Field | Value |
|---|---|
| System name / ID | Acme HR Portal (AHR) |
| Operational status | Operational (pilot, 200 users) pending authorization |
| System type | Major application |
| Security categorization | `SC Acme HR Portal = {(confidentiality, MODERATE), (integrity, MODERATE), (availability, LOW)}` |
| Control baseline | SP 800-53B Moderate, tailored per Section 4 |
| Authorization status | ATO granted 2026-11-02 (see `ato_memo.md`) |

## 2. Roles and contacts

All names are fictional.

| Role | Name | Organization |
|---|---|---|
| Authorizing official | Morgan Lee, CIO | Acme Defense Fabrication |
| System owner | Dana Ruiz, Director of HR Operations | Human Resources |
| Information owner | Dana Ruiz | Human Resources |
| ISSM | Priya Natarajan | Information Security Office |
| ISSO | Sam Okafor | Information Security Office |
| Control assessor | Jordan Pike, Lead Assessor | Acme Internal Audit (independent of IT) |

## 3. System description

### 3.1 Purpose
Employee self-service for HR data, plus a back office for HR staff. It replaces emailed PDF
pay statements and paper benefits forms.

### 3.2 Users and roles
| Role | Count | Access |
|---|---|---|
| Employee | ~1,200 | Own records only |
| HR specialist | 12 | Personnel and benefits records |
| HR administrator | 3 | Above plus role assignment |
| System administrator | 4 | Infrastructure only, through the jump host; no HR application role |

### 3.3 Authorization boundary
Inside the boundary: load balancer, two web/app VMs, a managed PostgreSQL instance, the admin
jump host, and the portal's object storage bucket for document uploads, all in one virtual
network in Acme's commercial IaaS tenant. Outside: Acme Enterprise Identity Service (SSO and
MFA), Acme SOC log platform, the payroll provider, and the benefits carrier.

### 3.4 Data flows
| # | Source → Destination | Protocol / port | Protection |
|---|---|---|---|
| 1 | User browser → load balancer | HTTPS 443 | TLS 1.2+ |
| 2 | Load balancer → app VMs | HTTPS 8443 | TLS 1.2+, private subnet |
| 3 | App VMs → PostgreSQL | 5432 | TLS, private subnet, encryption at rest |
| 4 | App → Enterprise Identity Service | SAML 2.0 over HTTPS | Signed assertions |
| 5 | Payroll provider → App (pay statements) | SFTP 22 | Key-based auth, PGP-encrypted files |
| 6 | App → benefits carrier (elections) | HTTPS API | Mutual TLS |
| 7 | All components → SOC log platform | Syslog over TLS 6514 | TLS |

### 3.5 Inventory
Kept in the CMDB, export attached as Attachment C. Summary: 4 VMs (hardened Linux image),
1 managed database, 1 load balancer, 1 storage bucket, application release 2.3.

### 3.6 Interconnections
| Connected system | Owner | Direction | Data | Agreement |
|---|---|---|---|---|
| Bayline Payroll Services (fictional) | External vendor | Inbound | Pay statements | Contract + ISA-2026-04 |
| Harborview Benefits (fictional) | External carrier | Outbound | Benefit elections | Contract + ISA-2026-05 |
| Acme Enterprise Identity Service | Acme IT | Bidirectional | Authentication | Internal MOU |

### 3.7 Applicable requirements
Acme Information Security Policy v4; state breach-notification laws for employee PII. (This is a
fictional corporate system, so FISMA doesn't apply. Acme uses the RMF voluntarily.)

## 4. Control baseline and tailoring

| Tailoring action | Control(s) | Rationale |
|---|---|---|
| Inherited (Enterprise Identity Service) | IA-2, IA-2(1), IA-2(2), IA-5, AC-7 | SSO and MFA enforced by the enterprise IdP |
| Inherited (IaaS provider) | PE family, MA family (physical) | Provider data centers; provider authorization reviewed |
| Hybrid | AU-6, IR-4, SI-4 | SOC monitors centrally; the ISSO reviews portal-specific events |
| Scoped out | AC-18, AC-19 for the system boundary | No wireless or mobile components inside the boundary; endpoints covered by the enterprise program |
| Organization-defined parameter | AC-2(3) | Disable accounts after 35 days of inactivity |

## 5. Control implementation statements (representative set)

```
Control:            AC-2 Account Management
Implementation:     Implemented
Origination:        Hybrid (identity lifecycle inherited; application roles system-specific)
Responsible role:   HR administrator; ISSO
Description:        Employee accounts are created automatically from the HR system of record
                    and removed at termination via the IdP. HR roles are granted only through
                    an approved ticket. The ISSO reviews privileged roles quarterly.
Evidence:           Role-change tickets; quarterly review sign-off
```

```
Control:            AC-2(3) Disable Accounts
Implementation:     Partially implemented
Origination:        System-specific
Parameter values:   35 days of inactivity
Description:        Local break-glass and service accounts are reviewed by hand monthly.
                    Automated disabling is planned (POAM-0001).
Evidence:           Monthly review checklist
```

```
Control:            AC-6 Least Privilege
Implementation:     Implemented
Origination:        System-specific
Description:        System administrators have no HR application role. HR specialists cannot
                    assign roles. Database access is limited to the application service
                    identity and two named DBAs via the jump host.
Evidence:           Role matrix; database grants export
```

```
Control:            AU-2 / AU-12 Event Logging
Implementation:     Implemented
Origination:        System-specific
Description:        The application logs sign-ins, record views of SSN fields, record changes,
                    role changes, and exports. OS and database logs are forwarded to the SOC.
Evidence:           Logging configuration; sample events
```

```
Control:            AU-6 Audit Record Review, Analysis, and Reporting
Implementation:     Partially implemented
Origination:        Hybrid
Description:        The SOC alerts on correlated events. The ISSO reviews portal-specific
                    reports weekly, but the review was not consistently recorded (POAM-0004).
Evidence:           SOC alert tickets; ISSO review log (incomplete)
```

```
Control:            CM-6 Configuration Settings
Implementation:     Implemented
Origination:        System-specific
Description:        VMs are built from a hardened image scanned against the CIS benchmark
                    monthly. The load balancer TLS policy allows TLS 1.2+ only (corrected
                    during assessment, finding AHR-2026-005).
Evidence:           Monthly compliance scan; load balancer policy export
```

```
Control:            CP-4 Contingency Plan Testing
Implementation:     Planned
Origination:        System-specific
Description:        The contingency plan was approved 2026-08-30. A tabletop and restore test
                    are scheduled (POAM-0003).
Evidence:           Approved contingency plan
```

```
Control:            RA-5 Vulnerability Monitoring and Scanning
Implementation:     Implemented
Origination:        System-specific
Description:        Weekly authenticated OS scans, and a dependency scan on every build in the
                    CI pipeline. Results feed the POA&M via the ISSO.
Evidence:           Scan reports; CI pipeline logs
```

```
Control:            SC-8 / SC-28 Transmission and At-Rest Confidentiality
Implementation:     Implemented
Origination:        Hybrid (provider-managed keys for storage; app-managed TLS)
Description:        All flows in Section 3.4 use TLS 1.2+. The database and storage bucket are
                    encrypted at rest with keys in the provider key service, rotated yearly.
Evidence:           TLS scan results; key policy export
```

```
Control:            SI-2 Flaw Remediation
Implementation:     Partially implemented
Origination:        System-specific
Parameter values:   Critical 15 days, High 30 days, Moderate 60 days, Low 90 days
Description:        OS patches are applied monthly. Application dependency updates fell
                    behind the timeline (POAM-0002).
Evidence:           Patch records; dependency scan history
```

## 6. Continuous monitoring

See [`conmon_plan.md`](conmon_plan.md). In short: weekly scans, monthly POA&M and
configuration review, quarterly account review, and annual reassessment of one third of the
controls.

## 7. Attachments (not reproduced in this example)

A. FIPS 199 worksheet ([`fips199_categorization.md`](fips199_categorization.md)) · B. Boundary
and data flow diagrams · C. Inventory export · D. ISAs · E. Contingency, incident response, and
configuration management plans · F. Privacy impact assessment

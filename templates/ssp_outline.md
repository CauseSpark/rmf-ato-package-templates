# System Security Plan (SSP): Outline

> Template, personal study material. This is my own outline for a readable SSP, loosely
> informed by [SP 800-18 Rev. 1](https://csrc.nist.gov/pubs/sp/800/18/r1/final) and the RMF
> Select and Implement steps in [SP 800-37 Rev. 2](https://csrc.nist.gov/pubs/sp/800/37/r2/final).
> Control IDs refer to [SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final).
> Real SSPs often live in a GRC tool or in OSCAL format; this outline shows the content they need.

## Document control

| Version | Date | Author | Summary of change |
|---|---|---|---|
| `<0.1>` | `<YYYY-MM-DD>` | `<name>` | `<initial draft>` |

## 1. System identification

| Field | Value |
|---|---|
| System name / ID | |
| Operational status | `<operational / under development / major modification>` |
| System type | `<major application / general support system / cloud service>` |
| Security categorization | `<SC string from FIPS 199 worksheet>` |
| Control baseline | `<Low / Moderate / High>` + tailoring reference |
| Authorization status | `<none / ATO / ongoing authorization>` and date |

## 2. Roles and contacts

| Role | Name | Organization | Contact |
|---|---|---|---|
| Authorizing official | | | |
| System owner | | | |
| Information owner | | | |
| ISSM / ISSO | | | |
| Control assessor | | | |

## 3. System description

### 3.1 Purpose and mission or business function
### 3.2 Users and roles (internal, external, privileged)
### 3.3 Authorization boundary
`<Diagram reference plus a narrative of what is in and out of scope.>`
### 3.4 Network architecture and data flows
`<Diagram reference; list each flow with source, destination, protocol/port, and encryption.>`
### 3.5 Hardware and software inventory
`<Reference an attached inventory, or summarize components here.>`
### 3.6 Interconnections and external services
| Connected system | Owner | Direction | Data | Agreement (ISA/MOU/contract) |
|---|---|---|---|---|

### 3.7 Laws, regulations, and policies that apply

## 4. Control baseline and tailoring

| Tailoring action | Control(s) | Rationale |
|---|---|---|
| Scoped out (not applicable) | | |
| Inherited from common control provider | | |
| Added (overlay or organization-specific) | | |
| Compensating control | | |

## 5. Control implementation statements

Repeat this block for each control and enhancement in the tailored baseline.

```
Control:            <ID and short name, e.g., AC-2 Account Management>
Implementation:     <implemented / partially implemented / planned / inherited / not applicable>
Origination:        <system-specific / hybrid / inherited (provider)>
Responsible role:   <who operates it>
Parameter values:   <organization-defined values, e.g., inactive after 35 days>
Description:        <how the control is actually met, written so an assessor can test it>
Evidence:           <where proof lives: config export, ticket queue, log query>
```

## 6. Continuous monitoring

Reference the ConMon plan and summarize assessment frequency by control family.

## 7. Attachments

- A. FIPS 199 categorization worksheet
- B. Boundary and data flow diagrams
- C. Hardware and software inventory
- D. Interconnection agreements
- E. Contingency plan, incident response plan, configuration management plan
- F. Privacy threshold analysis / privacy impact assessment (if PII)

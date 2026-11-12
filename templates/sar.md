# Security Assessment Report (SAR)

> Template, personal study material. Assessment methods (examine, interview, test) and
> procedures come from [SP 800-53A Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final);
> read the source for actual assessment objectives. Risk ratings below use a simple
> likelihood × impact scheme; replace it with your organization's method.

| Field | Value |
|---|---|
| System | `<name / ID>` |
| Categorization | `<SC string>` |
| Assessment type | `<initial / annual / change-driven>` |
| Assessment window | `<start>` to `<end>` |
| Lead assessor | `<name, organization>` |
| Independence | `<how the assessor is independent of the system team>` |
| Report date / version | |

## 1. Executive summary

`<One paragraph: scope, how many controls were assessed, how many were satisfied versus other
than satisfied, the highest-risk findings, and the assessor's overall view.>`

| Result | Count |
|---|---|
| Controls assessed | |
| Satisfied | |
| Other than satisfied | |
| Findings: High / Moderate / Low | `<# / # / #>` |

## 2. Scope and methodology

- Controls in scope: `<baseline, tailored set, or subset for this cycle>`
- Methods: examine `<documents reviewed>`, interview `<roles interviewed>`, test `<tools and techniques>`
- Tools: `<scanner names and versions, configuration checkers>`
- Limitations: `<anything not tested and why>`

## 3. Risk rating method

| | Low impact | Moderate impact | High impact |
|---|---|---|---|
| **High likelihood** | Moderate | High | High |
| **Moderate likelihood** | Low | Moderate | High |
| **Low likelihood** | Low | Low | Moderate |

## 4. Findings

Repeat for each finding. Every finding that stays open gets a matching POA&M row with the same ID.

```
Finding ID:        <SYS-YYYY-###>
Control:           <ID and short name>
Method:            <examine / interview / test>
Observation:       <what the assessor saw, factually>
Requirement gap:   <what was expected versus what was found>
Likelihood:        <L / M / H>
Impact:            <L / M / H>
Risk rating:       <L / M / H>
Recommendation:    <how to fix it>
Status at report:  <open / corrected during assessment>
```

## 5. Controls corrected during assessment

| Finding ID | Control | Correction | Verified by / date |
|---|---|---|---|

## 6. Assessor statement

`<Plain statement of what was assessed and the assessor's conclusion. The authorization
decision belongs to the AO, not the assessor.>`

| Lead assessor signature | Date |
|---|---|
| | |

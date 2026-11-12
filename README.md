# RMF ATO Package Templates

[![tests](https://github.com/CauseSpark/rmf-ato-package-templates/actions/workflows/tests.yml/badge.svg)](https://github.com/CauseSpark/rmf-ato-package-templates/actions/workflows/tests.yml)

Plain-language templates for a NIST Risk Management Framework (RMF) authorization package,
a complete worked example for a fictional system, and a small tested Python tool for FIPS 199
categorization.

> **Disclaimer.** This is personal study material by Peyton Seay. It is not official guidance
> from NIST, DoD, or any agency, it is not endorsed by any of them, and it does not imply any
> certification. **Acme Defense Fabrication** and the **Acme HR Portal** are fictional. Every
> name, date, vendor, and finding is made up, and nothing comes from any real mission, employer,
> or client. No CUI or classified information is included. The templates summarize ideas in my
> own words and link to the official sources rather than copying them.

## Purpose

An Authorization to Operate (ATO) package is a set of documents that lets a senior official
decide whether a system's risk is acceptable. This repo shows each document in that package,
explains where it comes from in the RMF, and fills one out end to end for a realistic
(but fictional) HR web application.

## Versions referenced (checked November 2026)

| Source | Version used |
|---|---|
| [NIST SP 800-37](https://csrc.nist.gov/pubs/sp/800/37/r2/final): Risk Management Framework | **Revision 2** (Dec 2018), 7 steps: Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor |
| [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final): Security and Privacy Controls | **Revision 5, Release 5.2.0** (Aug 2025) |
| [NIST SP 800-53B](https://csrc.nist.gov/pubs/sp/800/53/b/upd1/final): Control Baselines | Rev. 5 baselines (no baseline changes in Release 5.2.0) |
| [NIST SP 800-53A](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final): Assessment Procedures | Revision 5 |
| [FIPS 199](https://csrc.nist.gov/pubs/fips/199/final): Security Categorization | Feb 2004 (current) |
| [FIPS 200](https://csrc.nist.gov/pubs/fips/200/final): Minimum Security Requirements | Mar 2006 (current) |
| [NIST SP 800-60 Vol. 1 Rev. 1](https://csrc.nist.gov/pubs/sp/800/60/v1/r1/final): Mapping Information Types | Revision 1 |
| [NIST SP 800-18](https://csrc.nist.gov/pubs/sp/800/18/r2/final): Developing Security, Privacy, and C-SCRM Plans | **Revision 2** (June 2026) |
| [NIST SP 800-137](https://csrc.nist.gov/pubs/sp/800/137/final): Continuous Monitoring | Original (2011) |

## What's inside

```
docs/rmf_steps.md            Each RMF step in plain language, with typical outputs
diagrams/rmf_process.mmd     Mermaid diagram of the RMF loop
templates/                   Blank, reusable package templates
  fips199_categorization.md    Categorize
  ssp_outline.md               Select / Implement
  sar.md                       Assess
  poam.csv                     Assess / Monitor
  ato_memo.md                  Authorize
  conmon_plan.md               Monitor
examples/acme-hr-portal/     The templates filled out for a fictional Moderate system
src/categorize.py            FIPS 199 impact levels + FIPS 200 high-water mark
tests/                       pytest suite (categorizer logic + package consistency)
```

The same diagram is embedded in [`docs/rmf_steps.md`](docs/rmf_steps.md), so GitHub renders it
there. You can also paste [`diagrams/rmf_process.mmd`](diagrams/rmf_process.mmd) into
<https://mermaid.live> to view or edit it on its own.

## Quick start

```bash
git clone https://github.com/CauseSpark/rmf-ato-package-templates.git
cd rmf-ato-package-templates
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# Categorize the example system
python src/categorize.py examples/acme-hr-portal/categorization_input.json
python src/categorize.py examples/acme-hr-portal/categorization_input.json --format json

# Run the tests
pytest
```

Sample output:

```
| **System (high-water per objective)** | **MODERATE** | **MODERATE** | **LOW** |

`SC Acme HR Portal = {(confidentiality, MODERATE), (integrity, MODERATE), (availability, LOW)}`

Overall impact level (FIPS 200 high-water mark): **MODERATE**
Starting control baseline (SP 800-53B): **Moderate**
```

To use the templates for your own study system, copy `templates/` and fill in the `<placeholders>`.
To categorize it, copy `categorization_input.json` and edit the information types.

## How the categorizer works

1. Each information type gets LOW, MODERATE, or HIGH for confidentiality, integrity, and
   availability. Confidentiality can be NOT APPLICABLE, but only for public information.
2. The system value for each objective is the highest across its information types,
   never lower than LOW.
3. The overall impact level is the highest of those three values (the FIPS 200 high-water
   mark), and it selects the SP 800-53B baseline.

The tests cover the edge cases: N/A allowed only for confidentiality, a system whose types
each peak on a different objective, the LOW floor, empty input, bad input files, and the CLI.

## What this demonstrates

- **RMF fluency across the full lifecycle.** I can explain each of the seven steps, what it
  produces, and how Monitor loops back into Assess, Authorize, and Categorize.
- **Authorization package writing.** The repo includes a categorization worksheet, an SSP with
  testable implementation statements, a SAR with risk-rated findings, a POA&M with milestones,
  an AO decision memo with conditions, and a ConMon plan with real frequencies and triggers.
- **Traceability.** Each SAR finding maps to a POA&M row and to an SSP control statement, and
  accepted risks in the ATO memo map back to the POA&M. A test enforces this, the way a GRC
  tool or an assessor would.
- **Risk judgment, not just paperwork.** The example records *why* each impact level was
  chosen, why HIGH confidentiality was considered and rejected, and why the AO accepted
  the residual risk.
- **Compliance as code.** It has a small, tested Python tool, a pytest suite, and CI on every
  push in GitHub Actions.
- **Operational grounding.** As a network defender I lean on scanning, log review, and
  configuration baselines, and the ConMon plan reflects how monitoring actually runs.

## Notes for DoD readers

DoD systems follow DoDI 8510.01 and categorize with CNSSI 1253, which keeps separate C/I/A
values instead of collapsing them into one high-water level, and packages usually live in
eMASS. This repo uses the general NIST/FIPS approach so it stays tool-neutral and unclassified.

## License

[MIT](LICENSE) © 2026 Peyton Seay

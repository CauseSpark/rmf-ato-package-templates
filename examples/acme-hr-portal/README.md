# Example package: Acme HR Portal

> **Fictional.** Acme Defense Fabrication, the Acme HR Portal, every person, vendor, date, and
> finding here is made up for study. The portal is scoped to process **no CUI** and no
> classified information. Nothing here is drawn from any real system, employer, or client.

A complete sample authorization package built from the templates in [`../../templates`](../../templates).
Read the documents in this order, which follows the RMF steps:

| # | Document | RMF step | Built from |
|---|---|---|---|
| 1 | [`categorization_input.json`](categorization_input.json) | Categorize | input to `src/categorize.py` |
| 2 | [`fips199_categorization.md`](fips199_categorization.md) | Categorize | `fips199_categorization.md` |
| 3 | [`ssp.md`](ssp.md) | Select, Implement | `ssp_outline.md` |
| 4 | [`sar.md`](sar.md) | Assess | `sar.md` |
| 5 | [`poam.csv`](poam.csv) | Assess, Monitor | `poam.csv` |
| 6 | [`ato_memo.md`](ato_memo.md) | Authorize | `ato_memo.md` |
| 7 | [`conmon_plan.md`](conmon_plan.md) | Monitor | `conmon_plan.md` |

## The scenario in one paragraph

Acme Defense Fabrication is a fictional 1,200-person manufacturer. It decided to run its
internal systems through the NIST RMF as a governance practice. The Acme HR Portal is a web
application where employees view pay stubs, update personal details, and enroll in benefits,
and where HR staff manage personnel records. It handles employee PII, so the categorization
comes out **Moderate**, and the package goes through assessment to an ATO with conditions.

## Reproduce the categorization

```bash
python src/categorize.py examples/acme-hr-portal/categorization_input.json
```

`tests/test_package_consistency.py` checks that the package hangs together: the POA&M columns
match the template, every open SAR finding has a POA&M row, and the categorization in the
worksheet and the ATO memo matches what the script computes.

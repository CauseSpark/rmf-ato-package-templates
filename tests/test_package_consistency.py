"""Checks that the example package agrees with itself and with the templates."""

import csv
import re
from datetime import date
from pathlib import Path

import pytest

import categorize

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
EXAMPLE = ROOT / "examples" / "acme-hr-portal"

VALID_STATUS = {"Open", "In Progress", "Risk Accepted", "Completed"}
VALID_RISK = {"Low", "Moderate", "High"}


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


@pytest.fixture(scope="module")
def poam():
    return read_csv(EXAMPLE / "poam.csv")


@pytest.fixture(scope="module")
def sar_text():
    return (EXAMPLE / "sar.md").read_text(encoding="utf-8")


def sar_findings(text):
    """Map finding ID -> status, parsed from the SAR finding blocks."""
    blocks = re.findall(r"Finding ID:\s+(\S+).*?Status at report:\s+([^\n]+)", text, re.S)
    return {fid: status.strip() for fid, status in blocks}


def test_expected_files_exist():
    for name in ["fips199_categorization.md", "ssp_outline.md", "sar.md", "poam.csv", "ato_memo.md", "conmon_plan.md"]:
        assert (TEMPLATES / name).is_file(), name
    for name in ["fips199_categorization.md", "ssp.md", "sar.md", "poam.csv", "ato_memo.md", "conmon_plan.md"]:
        assert (EXAMPLE / name).is_file(), name


def test_poam_columns_match_template(poam):
    template_cols, _ = read_csv(TEMPLATES / "poam.csv")
    example_cols, _ = poam
    assert example_cols == template_cols


def test_poam_rows_are_well_formed(poam):
    _, rows = poam
    assert rows, "example POA&M should not be empty"
    ids = [r["poam_id"] for r in rows]
    assert len(ids) == len(set(ids)), "POA&M IDs must be unique"
    for r in rows:
        assert r["status"] in VALID_STATUS, r
        assert r["risk_rating"] in VALID_RISK, r
        detected = date.fromisoformat(r["original_detection_date"])
        due = date.fromisoformat(r["scheduled_completion_date"])
        assert due >= detected, r["poam_id"]
        assert r["point_of_contact"].strip(), r["poam_id"]


def test_every_open_sar_finding_has_a_poam_row(poam, sar_text):
    _, rows = poam
    findings = sar_findings(sar_text)
    assert findings, "no findings parsed from SAR"
    poam_findings = {r["finding_id"] for r in rows}
    open_findings = {fid for fid, status in findings.items() if status == "Open"}
    assert open_findings == poam_findings


def test_poam_controls_match_sar(poam, sar_text):
    _, rows = poam
    for r in rows:
        pattern = rf"Finding ID:\s+{re.escape(r['finding_id'])}\s+Control:\s+{re.escape(r['control'])}(?=\s)"
        assert re.search(pattern, sar_text), f"{r['poam_id']} control does not match SAR"


def test_categorization_matches_across_documents():
    result = categorize.load_input(EXAMPLE / "categorization_input.json")
    sc = result.security_category()
    for name in ["fips199_categorization.md", "ssp.md", "sar.md", "ato_memo.md", "conmon_plan.md"]:
        assert sc in (EXAMPLE / name).read_text(encoding="utf-8"), f"{name} has a stale categorization"
    worksheet = (EXAMPLE / "fips199_categorization.md").read_text(encoding="utf-8")
    assert f"**Overall impact level:** {result.overall.label}" in worksheet
    assert f"**Initial SP 800-53B baseline:** {result.baseline}" in worksheet


def test_embedded_diagram_matches_source():
    source = (ROOT / "diagrams" / "rmf_process.mmd").read_text(encoding="utf-8")
    doc = (ROOT / "docs" / "rmf_steps.md").read_text(encoding="utf-8")
    embedded = re.search(r"```mermaid\n(.*?)```", doc, re.S).group(1)

    def nodes_and_edges(text):
        return [line.strip() for line in text.splitlines() if "-->" in line or re.match(r"\s*[A-Z]\[", line)]

    assert nodes_and_edges(embedded) == nodes_and_edges(source)


def test_ato_memo_accepted_risks_exist_in_poam(poam):
    _, rows = poam
    poam_ids = {r["poam_id"] for r in rows}
    memo = (EXAMPLE / "ato_memo.md").read_text(encoding="utf-8")
    referenced = set(re.findall(r"POAM-\d{4}", memo))
    assert referenced and referenced <= poam_ids

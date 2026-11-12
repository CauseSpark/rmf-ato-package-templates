import json
from pathlib import Path

import pytest

import categorize
from categorize import Impact, InformationType, categorize_system, high_water_mark

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "acme-hr-portal" / "categorization_input.json"


def it(name, c, i, a):
    return InformationType(name, c, i, a)


# --- Impact parsing -------------------------------------------------------

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("low", Impact.LOW),
        ("L", Impact.LOW),
        ("Moderate", Impact.MODERATE),
        ("mod", Impact.MODERATE),
        (" HIGH ", Impact.HIGH),
        ("h", Impact.HIGH),
        ("n/a", Impact.NOT_APPLICABLE),
        ("not applicable", Impact.NOT_APPLICABLE),
        (Impact.HIGH, Impact.HIGH),
    ],
)
def test_parse_accepts_common_spellings(raw, expected):
    assert Impact.parse(raw) is expected


@pytest.mark.parametrize("raw", ["", "severe", "medium", "4"])
def test_parse_rejects_unknown_levels(raw):
    with pytest.raises(ValueError):
        Impact.parse(raw)


def test_parse_rejects_non_string():
    with pytest.raises(ValueError):
        Impact.parse(2)


def test_impact_ordering_supports_max():
    assert Impact.NOT_APPLICABLE < Impact.LOW < Impact.MODERATE < Impact.HIGH


# --- Information types ----------------------------------------------------

def test_information_type_normalizes_strings():
    t = it("Payroll", "moderate", "high", "low")
    assert (t.confidentiality, t.integrity, t.availability) == (Impact.MODERATE, Impact.HIGH, Impact.LOW)


def test_confidentiality_may_be_not_applicable_for_public_info():
    t = it("Press releases", "n/a", "low", "low")
    assert t.confidentiality is Impact.NOT_APPLICABLE


@pytest.mark.parametrize("objective", ["integrity", "availability"])
def test_only_confidentiality_may_be_not_applicable(objective):
    values = {"confidentiality": "low", "integrity": "low", "availability": "low", objective: "n/a"}
    with pytest.raises(ValueError, match=objective):
        InformationType("Bad", **values)


def test_information_type_requires_name():
    with pytest.raises(ValueError):
        it("  ", "low", "low", "low")


def test_information_type_sc_string():
    assert it("Payroll", "m", "m", "l").security_category() == (
        "SC Payroll = {(confidentiality, MODERATE), (integrity, MODERATE), (availability, LOW)}"
    )


# --- High-water mark ------------------------------------------------------

def test_high_water_mark_picks_highest():
    assert high_water_mark(["low", "high", "moderate"]) is Impact.HIGH


def test_high_water_mark_empty_raises():
    with pytest.raises(ValueError):
        high_water_mark([])


def test_system_value_is_max_per_objective_not_per_type():
    # No single type is M/M/M, but the system is, because each objective is
    # maxed independently across types.
    result = categorize_system(
        "Demo",
        [it("A", "moderate", "low", "low"), it("B", "low", "moderate", "low"), it("C", "low", "low", "moderate")],
    )
    assert (result.confidentiality, result.integrity, result.availability) == (
        Impact.MODERATE,
        Impact.MODERATE,
        Impact.MODERATE,
    )


def test_overall_is_highest_of_three_objectives():
    result = categorize_system("Demo", [it("A", "low", "low", "high")])
    assert result.overall is Impact.HIGH
    assert result.baseline == "High"


def test_all_low_gives_low_baseline():
    result = categorize_system("Demo", [it("A", "low", "low", "low")])
    assert result.overall is Impact.LOW
    assert result.baseline == "Low"


def test_system_confidentiality_floors_at_low():
    result = categorize_system("Public site", [it("Postings", "n/a", "low", "low")])
    assert result.confidentiality is Impact.LOW
    assert "NOT APPLICABLE" not in result.security_category()


def test_categorize_requires_information_types():
    with pytest.raises(ValueError):
        categorize_system("Empty", [])


def test_driving_types_names_the_types_that_set_the_value():
    result = categorize_system("Demo", [it("A", "high", "low", "low"), it("B", "low", "low", "low")])
    assert result.driving_types("confidentiality") == ["A"]
    with pytest.raises(ValueError):
        result.driving_types("authenticity")


# --- Example package and CLI ---------------------------------------------

def test_acme_example_is_moderate():
    result = categorize.load_input(EXAMPLE)
    assert result.system_name == "Acme HR Portal"
    assert (result.confidentiality, result.integrity, result.availability) == (
        Impact.MODERATE,
        Impact.MODERATE,
        Impact.LOW,
    )
    assert result.overall is Impact.MODERATE
    assert result.baseline == "Moderate"


def test_load_input_reports_missing_fields(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"system_name": "X", "information_types": [{"name": "Y"}]}))
    with pytest.raises(ValueError, match="missing"):
        categorize.load_input(bad)


def test_cli_markdown(capsys):
    assert categorize.main([str(EXAMPLE)]) == 0
    out = capsys.readouterr().out
    assert "Overall impact level (FIPS 200 high-water mark): **MODERATE**" in out
    assert "| Public job postings | NOT APPLICABLE | LOW | LOW |" in out


def test_cli_json(capsys):
    assert categorize.main([str(EXAMPLE), "--format", "json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["overall"] == "MODERATE"
    assert data["baseline"] == "Moderate"
    assert len(data["information_types"]) == 5


def test_cli_bad_path_returns_error_code(capsys):
    assert categorize.main(["does-not-exist.json"]) == 2
    assert "error" in capsys.readouterr().err

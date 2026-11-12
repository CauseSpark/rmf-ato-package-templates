"""FIPS 199 security categorization with the FIPS 200 high-water mark.

Personal study tool. It is not an official NIST or DoD tool.

How it works
------------
1. Each *information type* processed by a system gets a potential impact
   value (LOW, MODERATE, HIGH) for confidentiality, integrity, and
   availability. Confidentiality may also be NOT_APPLICABLE for an
   information type that is public (FIPS 199 allows this for information
   types only, never for a whole system).
2. The *system* value for each security objective is the highest value
   for that objective across all of its information types, with a floor
   of LOW (a system is never "not applicable").
3. The *overall* system impact level is the highest of the three system
   values. FIPS 200 calls this the high-water mark, and it picks the
   SP 800-53B control baseline (Low, Moderate, or High).

References (read the originals; nothing here copies their text):
  FIPS 199    https://csrc.nist.gov/pubs/fips/199/final
  FIPS 200    https://csrc.nist.gov/pubs/fips/200/final
  SP 800-60   https://csrc.nist.gov/pubs/sp/800/60/v1/r1/final
  SP 800-53B  https://csrc.nist.gov/pubs/sp/800/53/b/upd1/final

Usage
-----
    python src/categorize.py examples/acme-hr-portal/categorization_input.json
    python src/categorize.py input.json --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Iterable, Sequence

OBJECTIVES = ("confidentiality", "integrity", "availability")


class Impact(IntEnum):
    """Potential impact levels, ordered so that max() works."""

    NOT_APPLICABLE = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3

    @classmethod
    def parse(cls, value: "str | Impact") -> "Impact":
        """Accept 'low', 'Moderate', 'H', 'n/a', etc."""
        if isinstance(value, Impact):
            return value
        if not isinstance(value, str):
            raise ValueError(f"impact must be a string, got {type(value).__name__}")
        key = value.strip().upper().replace("/", "").replace("-", "_").replace(" ", "_")
        aliases = {
            "L": cls.LOW,
            "LOW": cls.LOW,
            "M": cls.MODERATE,
            "MOD": cls.MODERATE,
            "MODERATE": cls.MODERATE,
            "H": cls.HIGH,
            "HIGH": cls.HIGH,
            "NA": cls.NOT_APPLICABLE,
            "NOT_APPLICABLE": cls.NOT_APPLICABLE,
        }
        if key not in aliases:
            raise ValueError(f"unknown impact level: {value!r}")
        return aliases[key]

    @property
    def label(self) -> str:
        return "NOT APPLICABLE" if self is Impact.NOT_APPLICABLE else self.name


@dataclass(frozen=True)
class InformationType:
    """One information type and its provisional or adjusted impact values."""

    name: str
    confidentiality: Impact
    integrity: Impact
    availability: Impact
    rationale: str = ""

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("information type needs a name")
        for objective in OBJECTIVES:
            object.__setattr__(self, objective, Impact.parse(getattr(self, objective)))
        # FIPS 199 permits NOT APPLICABLE only for confidentiality (public info).
        for objective in ("integrity", "availability"):
            if getattr(self, objective) is Impact.NOT_APPLICABLE:
                raise ValueError(
                    f"{self.name}: {objective} cannot be NOT APPLICABLE; "
                    "only confidentiality may be N/A for public information"
                )

    def security_category(self) -> str:
        return _sc_string(self.name, self.confidentiality, self.integrity, self.availability)


@dataclass(frozen=True)
class SystemCategorization:
    system_name: str
    confidentiality: Impact
    integrity: Impact
    availability: Impact
    information_types: tuple[InformationType, ...]

    @property
    def overall(self) -> Impact:
        """FIPS 200 high-water mark: the highest of the three objectives."""
        return max(self.confidentiality, self.integrity, self.availability)

    @property
    def baseline(self) -> str:
        """Matching SP 800-53B control baseline name."""
        return {Impact.LOW: "Low", Impact.MODERATE: "Moderate", Impact.HIGH: "High"}[self.overall]

    def security_category(self) -> str:
        return _sc_string(self.system_name, self.confidentiality, self.integrity, self.availability)

    def driving_types(self, objective: str) -> list[str]:
        """Names of information types that set the system value for an objective."""
        if objective not in OBJECTIVES:
            raise ValueError(f"unknown objective: {objective!r}")
        target = getattr(self, objective)
        return [t.name for t in self.information_types if getattr(t, objective) == target]

    def to_dict(self) -> dict:
        return {
            "system_name": self.system_name,
            "confidentiality": self.confidentiality.label,
            "integrity": self.integrity.label,
            "availability": self.availability.label,
            "overall": self.overall.label,
            "baseline": self.baseline,
            "security_category": self.security_category(),
            "information_types": [
                {
                    "name": t.name,
                    "confidentiality": t.confidentiality.label,
                    "integrity": t.integrity.label,
                    "availability": t.availability.label,
                    "security_category": t.security_category(),
                }
                for t in self.information_types
            ],
        }


def _sc_string(name: str, c: Impact, i: Impact, a: Impact) -> str:
    return (
        f"SC {name} = {{(confidentiality, {c.label}), "
        f"(integrity, {i.label}), (availability, {a.label})}}"
    )


def high_water_mark(levels: Iterable["Impact | str"]) -> Impact:
    """Highest impact in a collection. Raises on an empty collection."""
    parsed = [Impact.parse(level) for level in levels]
    if not parsed:
        raise ValueError("high_water_mark needs at least one impact level")
    return max(parsed)


def categorize_system(system_name: str, information_types: Sequence[InformationType]) -> SystemCategorization:
    """Roll information types up to a system categorization."""
    if not information_types:
        raise ValueError("a system needs at least one information type to categorize")
    values = {}
    for objective in OBJECTIVES:
        hw = high_water_mark(getattr(t, objective) for t in information_types)
        values[objective] = max(hw, Impact.LOW)  # systems floor at LOW
    return SystemCategorization(
        system_name=system_name,
        information_types=tuple(information_types),
        **values,
    )


def load_input(path: "str | Path") -> SystemCategorization:
    """Load a JSON file shaped like examples/acme-hr-portal/categorization_input.json."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    try:
        types = [
            InformationType(
                name=item["name"],
                confidentiality=item["confidentiality"],
                integrity=item["integrity"],
                availability=item["availability"],
                rationale=item.get("rationale", ""),
            )
            for item in data["information_types"]
        ]
        return categorize_system(data["system_name"], types)
    except KeyError as exc:
        raise ValueError(f"input is missing required field {exc}") from exc


def render_markdown(result: SystemCategorization) -> str:
    lines = [
        f"# FIPS 199 categorization: {result.system_name}",
        "",
        "| Information type | C | I | A |",
        "|---|---|---|---|",
    ]
    for t in result.information_types:
        lines.append(f"| {t.name} | {t.confidentiality.label} | {t.integrity.label} | {t.availability.label} |")
    lines.append(
        f"| **System (high-water per objective)** | **{result.confidentiality.label}** | "
        f"**{result.integrity.label}** | **{result.availability.label}** |"
    )
    lines += [
        "",
        f"`{result.security_category()}`",
        "",
        f"Overall impact level (FIPS 200 high-water mark): **{result.overall.label}**",
        f"Starting control baseline (SP 800-53B): **{result.baseline}**",
    ]
    return "\n".join(lines)


def main(argv: "Sequence[str] | None" = None) -> int:
    parser = argparse.ArgumentParser(description="FIPS 199 categorization with the high-water mark.")
    parser.add_argument("input", help="path to a categorization JSON file")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)
    try:
        result = load_input(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

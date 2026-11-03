"""Runs a unit's own tests from tests/expected.yaml, after ESLint's RuleTester and opa test."""
from pathlib import Path

import yaml

from . import SPIKE
from .artefacts import load_dir
from .glossary import load_default
from .units import UNITS_DIR, by_name


class EmptyRun(Exception):
    """A test file with no cases, which must not pass silently (after OPA's --fail-on-empty)."""


def load_cases(path: Path) -> list[dict]:
    """Cases named under `superseded` are kept but marked, so they are skipped, not deleted."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    cases = data.get("cases") or []
    if not cases:
        raise EmptyRun(f"{path}: no cases")
    superseded = set(data.get("superseded") or [])
    return [dict(c, superseded=True) if c["name"] in superseded else c for c in cases]


def collect_cases() -> list[tuple[str, dict]]:
    out = []
    for unit_dir in sorted(UNITS_DIR.iterdir()):
        unit = by_name(unit_dir.name)
        expected = unit_dir / "tests" / "expected.yaml"
        if unit.check_type == "python" and expected.is_file():
            out += [(unit.name, c) for c in load_cases(expected)]
    return out


def citation(unit_name: str) -> str:
    return by_name(unit_name).citation


def run_case(unit_name: str, case: dict):
    """Returns (findings, info) for one case."""
    unit = by_name(unit_name)
    mod = unit.check_module()
    if case["stage"] in ("plan", "analyze"):
        return mod.check_artefacts(load_dir(SPIKE / case["artefacts"]), load_default(), unit.citation)
    if "file" in case:
        return mod.check_file(SPIKE / case["file"], unit.citation)
    return mod.check_tree(SPIKE / case["repo"], SPIKE / case["subject"], unit.citation)

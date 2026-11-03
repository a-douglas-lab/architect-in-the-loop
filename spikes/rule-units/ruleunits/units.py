"""Rule units: identity, applicability and check, loaded from units/<name>/unit.yaml."""
import importlib.util
from dataclasses import dataclass
from pathlib import Path

import yaml

from . import SPIKE

UNITS_DIR = SPIKE / "units"


@dataclass(frozen=True)
class Unit:
    name: str
    citation: str
    source: str
    text: str
    kind: str
    role: str
    stages: tuple[str, ...]
    terms_any: tuple[str, ...]
    always: bool
    check_type: str
    describes: str
    path: Path

    def check_module(self):
        spec = importlib.util.spec_from_file_location(f"unit_{self.name.replace('-', '_')}", self.path / "check.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


def load(path: Path) -> Unit:
    d = yaml.safe_load((path / "unit.yaml").read_text(encoding="utf-8"))
    applies, check = d["applies"], d["check"]
    return Unit(
        name=path.name,
        citation=d["citation"],
        source=d["source"],
        text=d["text"],
        kind=d["kind"],
        role=d["role"],
        stages=tuple(applies["stages"]),
        terms_any=tuple(applies.get("terms_any", ())),
        always=bool(applies.get("always", False)),
        check_type=check["type"],
        describes=check.get("describes", "").strip(),
        path=path,
    )


def load_all(units_dir: Path = UNITS_DIR) -> list[Unit]:
    return [load(p) for p in sorted(units_dir.iterdir()) if (p / "unit.yaml").is_file()]


def by_name(name: str) -> Unit:
    return load(UNITS_DIR / name)


def build_index(units: list[Unit]) -> list[dict]:
    """The always-present part: identity and applicability, no rule text or check."""
    return [
        {"unit": u.name, "citation": u.citation, "kind": u.kind, "role": u.role,
         "stages": list(u.stages), "terms_any": list(u.terms_any), "always": u.always}
        for u in units
    ]

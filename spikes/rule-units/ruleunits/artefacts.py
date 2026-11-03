"""Loading a feature's spec, plan and tasks."""
import re
from pathlib import Path

import yaml

from . import SPIKE

KINDS = ("spec", "plan", "tasks")


def load_dir(path: Path) -> dict[str, str]:
    return {k: (path / f"{k}.md").read_text(encoding="utf-8") for k in KINDS if (path / f"{k}.md").is_file()}


def labels() -> dict:
    return yaml.safe_load((SPIKE / "labels.yaml").read_text(encoding="utf-8"))["fixtures"]


def fixture_path(name: str) -> Path:
    return (SPIKE / labels()[name]["path"]).resolve()


def load_fixture(name: str) -> dict[str, str]:
    return load_dir(fixture_path(name))


def sentences(arts: dict[str, str]):
    """Yield (artefact, sentence): split on line breaks and on '. '."""
    for kind in KINDS:
        for line in arts.get(kind, "").splitlines():
            for s in re.split(r"(?<=\.)\s+", line):
                if s.strip():
                    yield kind, s.strip()

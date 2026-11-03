"""The glossary: one ubiquitous language per bounded context, in a SKOS-like shape."""
from dataclasses import dataclass, field

import yaml

from . import SPIKE


@dataclass(frozen=True)
class Term:
    id: str
    label: str
    definition: str
    aliases: tuple[str, ...]
    context: str


@dataclass
class Glossary:
    terms: dict[str, Term] = field(default_factory=dict)

    def ids(self) -> list[str]:
        return sorted(self.terms)


def load(paths) -> Glossary:
    g = Glossary()
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for t in data["terms"]:
            if t["id"] in g.terms:
                raise ValueError(f"duplicate term id {t['id']}")
            g.terms[t["id"]] = Term(t["id"], t["label"], t["definition"], tuple(t["aliases"]), data["context"])
    return g


def load_default() -> Glossary:
    return load(sorted((SPIKE / "glossary").glob("*.yaml")))

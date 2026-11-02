"""Deterministic selection: terms and stage to units, and the rules file handed to an agent."""
from .units import Unit


def select(units: list[Unit], terms, stage: str) -> list[str]:
    terms = set(terms)
    return sorted(
        u.name for u in units
        if stage in u.stages and (u.always or terms.intersection(u.terms_any))
    )


def rules_file(units: list[Unit], names: list[str]) -> str:
    """The selected units' text, for an agent to read. Carries no check results."""
    chosen = [u for u in units if u.name in names]
    out = [
        "# Rules that apply to this feature",
        "",
        "Selected deterministically for this feature. Each rule is quoted word for word from its source.",
        "",
    ]
    for u in chosen:
        out += [
            f"## {u.citation}",
            "",
            f"Rule: {u.text}",
            "",
            f"Source: {u.source}",
            "",
            f"Kind: {u.kind}",
            "",
            f"Check: {u.describes}",
            "",
        ]
    return "\n".join(out)

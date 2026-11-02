"""ADR-016@v1 C10: tools that report rule violations MUST report in SARIF."""
import json
import re

from ruleunits.report import Finding, location

# Output formats other than SARIF that a plan might name. A described but unnamed format
# isn't caught (a todo case in tests/expected.yaml).
OTHER_FORMATS = re.compile(
    r"\b(csv|json|xml|html|txt|text file|markdown|spreadsheet|excel|xlsx|log file|database table)\b"
    r"|\.(csv|json|xml|html|txt|md|xlsx)\b",
    re.IGNORECASE,
)
SARIF = re.compile(r"\bsarif\b", re.IGNORECASE)


def check_artefacts(arts, glossary, citation):
    text = "\n".join(arts.values())
    if SARIF.search(text):
        return [], {"sarif_named": True}
    hits = [(kind, m.group(0)) for kind, body in arts.items() for m in OTHER_FORMATS.finditer(body)]
    if not hits:
        return [], {"sarif_named": False, "other_format": None}
    kind, fmt = hits[0]
    msg = f"Rule violations are reported as {fmt!r}, not SARIF. {citation} requires SARIF."
    return [Finding(citation, msg, locations=[location(f"{kind}.md", f"names {fmt!r}")])], {"other_format": fmt}


def check_file(path, citation):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError):
        return [Finding(citation, f"{path.name} is not JSON, so not SARIF.", locations=[location(path.name)])], {}
    schema = data.get("$schema", "") if isinstance(data, dict) else ""
    version = data.get("version") if isinstance(data, dict) else None
    runs = data.get("runs") if isinstance(data, dict) else None
    if "sarif" in str(schema).lower() and isinstance(version, str) and isinstance(runs, list):
        return [], {"sarif_version": version}
    return [Finding(citation, f"{path.name} has no SARIF $schema, version and runs.", locations=[location(path.name)])], {}

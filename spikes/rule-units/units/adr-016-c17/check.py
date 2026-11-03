"""ADR-016@v2 C17: SARIF reports of rule violations MUST use SARIF version 2.1.0."""
import json
import re

from ruleunits.report import Finding, location

SARIF_VERSION = "2.1.0"
ACCEPTED = {"2.1", "2.1.0"}
# "SARIF 1.0", "SARIF v2.1", "SARIF version 2.2". Not caught: a version in words (a todo case
# in tests/expected.yaml), one without a dot ("SARIF version 2"), punctuation between
# ("SARIF: 1.0", "SARIF (2.2)"), "SARIF2.1.0" and schema URLs. The first non-2.1.0 version
# wins, so "convert SARIF 1.0.0 to SARIF 2.1.0" is a finding; "2.1.0-rtm.5" passes as 2.1.0.
NAMED_VERSION = re.compile(r"\bsarif\b\s*(?:v(?:ersion)?\s*)?(\d+(?:\.\d+)+)", re.IGNORECASE)


def check_artefacts(arts, glossary, citation):
    for kind, body in arts.items():
        for m in NAMED_VERSION.finditer(body):
            version = m.group(1)
            if version not in ACCEPTED:
                msg = f"The artefacts name SARIF {version}. {citation} requires SARIF {SARIF_VERSION}."
                return [Finding(citation, msg, locations=[location(f"{kind}.md", f"names SARIF {version}")])], {"named_version": version}
    return [], {"named_version": None}


def check_file(path, citation):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError):
        return [], {}
    if not isinstance(data, dict) or "sarif" not in str(data.get("$schema", "")).lower():
        return [], {}
    version = data.get("version")
    if version != SARIF_VERSION:
        named = f"SARIF {version}" if version is not None else "SARIF with no version field"
        msg = f"{path.name} is {named}, not {SARIF_VERSION}. {citation} requires {SARIF_VERSION}."
        return [Finding(citation, msg, locations=[location(path.name)])], {"sarif_version": version}
    return [], {"sarif_version": version}

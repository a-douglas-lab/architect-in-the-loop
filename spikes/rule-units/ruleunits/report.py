"""One typed record per fixture per run, validated against report.schema.json."""
import json
from dataclasses import dataclass, field

from . import SPIKE

SCHEMA = json.loads((SPIKE / "report.schema.json").read_text(encoding="utf-8"))


@dataclass
class Finding:
    rule_id: str
    message: str
    level: str = "error"
    locations: list = field(default_factory=list)

    def to_sarif(self) -> dict:
        d = {"ruleId": self.rule_id, "level": self.level, "message": {"text": self.message}}
        if self.locations:
            d["locations"] = self.locations
        return d


def location(uri: str, text: str | None = None) -> dict:
    loc = {"physicalLocation": {"artifactLocation": {"uri": uri}}}
    if text:
        loc["message"] = {"text": text}
    return loc


def make_record(fixture, stage, translator, terms, selected, findings, measurements) -> dict:
    return {
        "record_version": "0.1",
        "fixture": fixture,
        "stage": stage,
        "translator": translator,
        "terms": list(terms),
        "selected_units": list(selected),
        "findings": [f.to_sarif() if isinstance(f, Finding) else f for f in findings],
        "measurements": dict(measurements),
    }


_TYPES = {"object": dict, "array": list, "string": str}


def validate(value, schema=SCHEMA, path="$"):
    """A small subset of JSON Schema: type, required, properties, items, enum."""
    t = schema.get("type")
    if t and not isinstance(value, _TYPES[t]):
        raise ValueError(f"{path}: expected {t}")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{path}: {value!r} not in {schema['enum']}")
    if t == "object":
        for key in schema.get("required", []):
            if key not in value:
                raise ValueError(f"{path}: missing {key}")
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                validate(value[key], sub, f"{path}.{key}")
    if t == "array" and "items" in schema:
        for i, item in enumerate(value):
            validate(item, schema["items"], f"{path}[{i}]")

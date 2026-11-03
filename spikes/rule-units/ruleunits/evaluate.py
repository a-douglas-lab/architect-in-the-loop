"""Scoring translators and selectors against labels.yaml (method in expected.md)."""
import json
import random
import re
import shutil
from pathlib import Path

from . import SPIKE
from .artefacts import KINDS, fixture_path, labels, load_fixture
from .glossary import load_default
from .report import make_record, validate
from .select import select
from .translate import alias, bm25, validate_ids
from .units import load_all

ALWAYS = "hard-rule-4-copy"
ADR_TO_UNITS = {
    "ADR-004": ["adr-004-c3"],
    "ADR-011": ["adr-011-c3"],
    "ADR-015": ["adr-015-c2", "adr-015-c9"],
    "ADR-016": ["adr-016-c10", "adr-016-c2"],
}
SEED = 20261102


def neutral_copies(out: Path) -> dict[str, str]:
    """Copy fixtures as x01..x17 in a seeded shuffle, without the "(test fixture)" label."""
    names = sorted(labels())
    random.Random(SEED).shuffle(names)
    mapping = {}
    out.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(names, 1):
        nid = f"x{i:02d}"
        mapping[nid] = name
        d = out / nid
        d.mkdir(exist_ok=True)
        for kind, text in load_fixture(name).items():
            text = re.sub(r"\s*\(test fixture\)", "", text)
            (d / f"{kind}.md").write_text(text, encoding="utf-8", newline="\n")
    return mapping


def score(predicted: dict[str, list[str]], key: str, exclude=()) -> dict:
    lab = labels()
    tp = fp = fn = 0
    errors = []
    for fx, item in lab.items():
        want = set(item[key]) - set(exclude)
        got = set(predicted.get(fx, [])) - set(exclude)
        tp += len(want & got)
        fp += len(got - want)
        fn += len(want - got)
        for x in sorted(got - want):
            errors.append(f"{fx}: extra {x}")
        for x in sorted(want - got):
            errors.append(f"{fx}: missed {x}")
    return {
        "tp": tp, "fp": fp, "fn": fn,
        "recall": f"{tp} of {tp + fn}", "precision": f"{tp} of {tp + fp}",
        "errors": errors,
    }


def units_from_terms(terms_by_fx: dict[str, list[str]]) -> dict[str, list[str]]:
    units = load_all()
    return {fx: select(units, terms, "analyze") for fx, terms in terms_by_fx.items()}


def units_from_adrs(adrs_by_fx: dict[str, list[str]]) -> dict[str, list[str]]:
    out = {}
    for fx, adrs in adrs_by_fx.items():
        picked = {u for a in adrs for u in ADR_TO_UNITS.get(a, [])}
        out[fx] = sorted(picked | {ALWAYS})
    return out


def deterministic(name: str) -> dict:
    fn = {"alias": alias, "bm25": bm25}[name]
    g = load_default()
    terms = {fx: fn(load_fixture(fx), g) for fx in sorted(labels())}
    sel = units_from_terms(terms)
    records = [make_record(fx, "analyze", name, terms[fx], sel[fx], [], {}) for fx in terms]
    for r in records:
        validate(r)
    return {
        "translator": name,
        "terms": terms,
        "units": sel,
        "term_score": score(terms, "terms"),
        "unit_score": score(sel, "units", exclude=[ALWAYS]),
        "records": records,
    }


def model_run(path: Path, mapping: dict[str, str], kind: str) -> dict:
    """Score one model run. kind is "model" (term IDs) or "baseline-titles" (ADR IDs)."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    by_fx = {mapping[nid]: v for nid, v in raw.items()}
    if kind == "model":
        g = load_default()
        terms = {fx: validate_ids(v, g) for fx, v in by_fx.items()}
        sel = units_from_terms(terms)
        result = {"terms": terms, "units": sel, "term_score": score(terms, "terms")}
    else:
        adrs = {fx: sorted(set(v)) for fx, v in by_fx.items()}
        sel = units_from_adrs(adrs)
        result = {"adrs": adrs, "units": sel}
    result["unit_score"] = score(sel, "units", exclude=[ALWAYS])
    result["translator"] = kind
    return result


def stability(runs: list[dict], key: str) -> str:
    fxs = sorted(labels())
    same = sum(1 for fx in fxs if len({tuple(r[key].get(fx, [])) for r in runs}) == 1)
    return f"{same} of {len(fxs)}"


def write(obj, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

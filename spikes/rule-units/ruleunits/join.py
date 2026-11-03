"""The joined step: translate, validate, select, check and report for one feature, in one call.

Called by the MCP server (server.py), which a harness hook or an orchestrator calls. Never
writes to the feature or to .specify/.
"""
import json
import os
import time
from pathlib import Path

from .artefacts import load_dir
from .glossary import load_default
from .report import make_record
from .select import rules_file, select
from .translate import alias
from .translate_model import TranslatorFailed, model
from .units import load_all

# Spec Kit skills that the hook acts on, and the stage each one is.
SKILL_STAGES = {"speckit-plan": "plan", "speckit-analyze": "analyze"}
CONTEXT_LIMIT = 10_000  # Claude Code's cap on one additionalContext string


def translate(arts, g, translator, client):
    """Returns (terms, translator used, fallback reason or None)."""
    if translator == "alias":
        return alias(arts, g), "alias", None
    try:
        return model(arts, g, client), "model", None
    except TranslatorFailed as e:
        return alias(arts, g), "alias", str(e)


def run(feature: Path, stage: str, *, translator: str | None = None, client=None) -> dict:
    start = time.monotonic()
    translator = translator or os.environ.get("RULEUNITS_TRANSLATOR", "auto")
    g, units = load_default(), load_all()
    arts = load_dir(feature)
    terms, used, fallback = translate(arts, g, translator, client)
    names = select(units, terms, stage)
    findings = []
    for u in units:
        if u.name in names and u.check_type == "python" and stage in ("plan", "analyze"):
            found, _ = u.check_module().check_artefacts(arts, g, u.citation)
            findings += found
    measurements = {
        "translator": used,
        "translator_fallback": fallback,
        "duration_ms": int((time.monotonic() - start) * 1000),
    }
    record = make_record(feature.name, stage, used, terms, names, findings, measurements)
    rules = rules_file(units, names)
    return {"record": record, "rules_text": rules, "context": context_text(record, rules)}


def context_text(record: dict, rules: str) -> str:
    """Statements for the agent's context: the rules, then the deterministic check results."""
    translator = record["translator"]
    if record["measurements"]["translator_fallback"]:
        translator += f" (fallback: {record['measurements']['translator_fallback']})"
    head = [
        "Rule units for this feature, from the rule-unit MCP server.",
        f"Stage: {record['stage']}. Translator: {translator}. Terms: {', '.join(record['terms']) or 'none'}.",
        "",
    ]
    results = ["", "## Results of deterministic checks", ""]
    if record["findings"]:
        results += [f"- {f['ruleId']}: {f['message']['text']}" for f in record["findings"]]
    else:
        results.append("- No findings.")
    head_text, tail = "\n".join(head), "\n".join(results)
    text = head_text + rules + tail
    if len(text) > CONTEXT_LIMIT:
        # Shorten the rules first, keeping the check results; if the results alone are too long, cut them too.
        marker = "\n[shortened to fit the 10,000-character limit]\n"
        room = CONTEXT_LIMIT - len(head_text) - len(tail) - len(marker)
        text = head_text + rules[: max(room, 0)] + marker + tail
        text = text[:CONTEXT_LIMIT]
    return text


def feature_dir(project: Path) -> Path | None:
    """As Spec Kit resolves it: SPECIFY_FEATURE_DIRECTORY, then .specify/feature.json. Read only."""
    project = Path(project)
    value = os.environ.get("SPECIFY_FEATURE_DIRECTORY")
    if not value:
        fj = project / ".specify" / "feature.json"
        if not fj.is_file():
            return None
        try:
            value = json.loads(fj.read_text(encoding="utf-8")).get("feature_directory")
        except ValueError:
            return None
        if not value:
            return None
    path = Path(value)
    return (path if path.is_absolute() else project / path).resolve()


def hook_result(skill: str, project_dir, hook_event_name: str, *, translator: str | None = None, client=None):
    """(the JSON a Claude Code mcp_tool hook reads, as text; the record or None). {} when the skill isn't a mapped stage."""
    stage = SKILL_STAGES.get(skill or "")
    if not stage:
        return "{}", None
    feature = feature_dir(Path(project_dir))
    record = None
    if feature is None or not feature.is_dir():
        ctx = ("Rule units: no feature folder was found (SPECIFY_FEATURE_DIRECTORY is unset and "
               ".specify/feature.json names none), so no rules were selected.")
    else:
        res = run(feature, stage, translator=translator, client=client)
        ctx, record = res["context"], res["record"]
    return json.dumps({"hookSpecificOutput": {"hookEventName": hook_event_name, "additionalContext": ctx}}), record


def hook_output(skill: str, project_dir, hook_event_name: str, **kw) -> str:
    return hook_result(skill, project_dir, hook_event_name, **kw)[0]

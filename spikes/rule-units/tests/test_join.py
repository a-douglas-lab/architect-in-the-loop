"""The joined step and the hook contract: behaviour fixed in server-expected.md before the code."""
import json
from types import SimpleNamespace

import pytest

from ruleunits import SPIKE, artefacts, join, report

F8 = artefacts.fixture_path("f8")
RECORDED = json.loads((SPIKE / "runs" / "selection" / "raw" / "translator-run1.json").read_text(encoding="utf-8"))
NEUTRAL = {v: k for k, v in json.loads((SPIKE / "runs" / "mapping.json").read_text(encoding="utf-8")).items()}


class FakeClient:
    """Stands in for anthropic.Anthropic: returns a canned response, or raises."""

    def __init__(self, terms=None, stop_reason="end_turn", error=None):
        self.calls = 0
        self._terms, self._stop, self._error = terms, stop_reason, error
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls += 1
        if self._error:
            raise self._error
        text = json.dumps({"terms": self._terms or []})
        return SimpleNamespace(stop_reason=self._stop, content=[SimpleNamespace(type="text", text=text)])


def run(fixture, **kw):
    return join.run(artefacts.fixture_path(fixture), "analyze", **kw)


# J1 to J3: alias forced


def test_j1_f8_alias():
    res = run("f8", translator="alias")
    rec = res["record"]
    report.validate(rec)
    assert rec["translator"] == "alias"
    assert "violation-report" in rec["terms"]
    assert rec["selected_units"] == ["adr-016-c10", "hard-rule-4-copy"]
    assert [f["ruleId"] for f in rec["findings"]] == ["ADR-016@v1 C10"]
    assert "csv" in rec["findings"][0]["message"]["text"].lower()


def test_j2_f1_alias():
    rec = run("f1", translator="alias")["record"]
    assert rec["selected_units"] == ["hard-rule-4-copy"]
    assert rec["findings"] == []


def test_j3_f4_alias_hard_rule_4():
    # As first committed (c7b89cb), this asked for exactly one finding and failed: f4 copies in
    # both spec.md and plan.md, so there are two. server-expected.md says "a finding", which holds.
    rec = run("f4", translator="alias")["record"]
    ids = [f["ruleId"] for f in rec["findings"]]
    assert ids and set(ids) == {"CLAUDE.md hard rule 4 (copy clause)"}


# J4 to J7: model translator, with a fake client


def test_j4_model_replayed():
    recorded = RECORDED[NEUTRAL["f8"]]
    client = FakeClient(terms=recorded)
    rec = run("f8", translator="auto", client=client)["record"]
    assert client.calls == 1
    assert rec["translator"] == "model"
    assert rec["measurements"]["translator_fallback"] is None
    assert rec["terms"] == sorted(recorded)
    assert rec["selected_units"] == ["adr-016-c10", "hard-rule-4-copy"]
    assert [f["ruleId"] for f in rec["findings"]] == ["ADR-016@v1 C10"]


def test_j5_unknown_id_falls_back():
    rec = run("f8", client=FakeClient(terms=["violation-report", "made-up"]))["record"]
    assert rec["translator"] == "alias"
    assert "glossary" in rec["measurements"]["translator_fallback"]


def test_j6_client_error_falls_back():
    rec = run("f8", client=FakeClient(error=ConnectionError("offline")))["record"]
    assert rec["translator"] == "alias"
    assert "ConnectionError" in rec["measurements"]["translator_fallback"]


def test_j6b_client_constructor_error_falls_back(monkeypatch):
    # Added after the code, defensively: anthropic 2.3.0 builds a client without credentials and
    # fails at the request (J6's path), so this mocks a failure the SDK doesn't currently produce.
    from ruleunits import translate_model

    def no_credentials():
        raise TypeError("Could not resolve authentication method")
    monkeypatch.setattr(translate_model, "default_client", no_credentials)
    rec = run("f8", translator="auto")["record"]
    assert rec["translator"] == "alias"
    assert "authentication" in rec["measurements"]["translator_fallback"]


def test_j7_refusal_falls_back():
    rec = run("f8", client=FakeClient(terms=["sarif"], stop_reason="refusal"))["record"]
    assert rec["translator"] == "alias"
    assert "refusal" in rec["measurements"]["translator_fallback"]


# J8, J9


def test_j8_measurements():
    m = run("f8", translator="alias")["record"]["measurements"]
    assert m["translator"] == "alias"
    assert "translator_fallback" in m
    assert isinstance(m["duration_ms"], int)


def test_j9_rules_text_and_findings_kept_apart():
    res = run("f8", translator="alias")
    rules = res["rules_text"]
    assert "ADR-016@v1 C10" in rules
    assert "Tools that report rule violations MUST report in SARIF." in rules
    assert "never copy eShop files into this repo." in rules
    context = res["context"]
    assert "Results of deterministic checks" in context
    assert context.index("Results of deterministic checks") > context.index("ADR-016@v1 C10")


@pytest.mark.parametrize("rules_len, findings", [(20_000, 1), (100, 500), (20_000, 500)])
def test_context_never_exceeds_limit(rules_len, findings):
    # Added after review run 13: the shortening branch had no test.
    rec = report.make_record("x", "analyze", "alias", [], [], [
        {"ruleId": "R", "level": "error", "message": {"text": "a finding " * 10}} for _ in range(findings)],
        {"translator": "alias", "translator_fallback": None, "duration_ms": 0})
    text = join.context_text(rec, "r" * rules_len)
    assert len(text) <= join.CONTEXT_LIMIT
    if findings == 1:
        assert "Results of deterministic checks" in text


# H1 to H5: hook contract


@pytest.fixture
def project(tmp_path, monkeypatch):
    monkeypatch.delenv("SPECIFY_FEATURE_DIRECTORY", raising=False)
    (tmp_path / ".specify").mkdir()
    return tmp_path


def write_feature_json(project, feature):
    path = project / ".specify" / "feature.json"
    path.write_text(json.dumps({"feature_directory": str(feature)}), encoding="utf-8")
    return path


def test_h1_analyze_hook_output(project):
    write_feature_json(project, F8)
    out = json.loads(join.hook_output("speckit-analyze", project, "PreToolUse", translator="alias"))
    spec = out["hookSpecificOutput"]
    assert spec["hookEventName"] == "PreToolUse"
    ctx = spec["additionalContext"]
    assert "ADR-016@v1 C10" in ctx
    assert "Tools that report rule violations MUST report in SARIF." in ctx
    assert "not SARIF" in ctx
    assert len(ctx) <= 10_000
    assert not any(line.lstrip().lower().startswith(("you must", "always ", "never read")) for line in ctx.splitlines())


def test_h2_unmapped_skill_does_nothing(project):
    write_feature_json(project, F8)
    assert json.loads(join.hook_output("speckit-specify", project, "PreToolUse")) == {}
    assert json.loads(join.hook_output("", project, "PreToolUse")) == {}


def test_h3_no_feature_is_said_not_silent(project):
    out = json.loads(join.hook_output("speckit-analyze", project, "PreToolUse", translator="alias"))
    ctx = out["hookSpecificOutput"]["additionalContext"]
    assert "no feature folder" in ctx.lower()
    assert "no rules were selected" in ctx.lower()


def test_h4_resolution_order_and_read_only(project, monkeypatch):
    fj = write_feature_json(project, artefacts.fixture_path("f1"))
    before = fj.read_text(encoding="utf-8")
    assert join.feature_dir(project) == artefacts.fixture_path("f1")
    rel = F8.relative_to(SPIKE.parents[1]) if F8.is_relative_to(SPIKE.parents[1]) else F8
    monkeypatch.setenv("SPECIFY_FEATURE_DIRECTORY", str(rel))
    assert join.feature_dir(SPIKE.parents[1]) == F8
    join.hook_output("speckit-analyze", project, "PreToolUse", translator="alias")
    assert fj.read_text(encoding="utf-8") == before


def test_h5_plan_stage(project):
    write_feature_json(project, artefacts.fixture_path("f5"))
    out = json.loads(join.hook_output("speckit-plan", project, "PreToolUse", translator="alias"))
    assert "ADR-015@v1 C2" in out["hookSpecificOutput"]["additionalContext"]

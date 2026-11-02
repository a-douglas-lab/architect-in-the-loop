"""Runs every mechanical and bright-line unit against its own tests/expected.yaml.

Written before the checks. A todo case is one the check is predicted to get wrong; it is
marked xfail (not strict), so it is reported without failing the run.
"""
import pytest

from ruleunits import runner

CASES = runner.collect_cases()


def test_every_checked_unit_has_cases():
    names = {unit for unit, _ in CASES}
    assert names == {"adr-016-c10", "hard-rule-4-copy"}


@pytest.mark.parametrize(
    "unit,case",
    [pytest.param(u, c, id=f"{u}: {c['name']}",
                  marks=[pytest.mark.xfail(strict=False, reason="todo: predicted miss")] if c.get("todo") else [])
     for u, c in CASES],
)
def test_case(unit, case):
    findings, info = runner.run_case(unit, case)
    if case["expect"] == "finding":
        assert findings, f"expected a finding, got none ({info})"
        assert all(f.rule_id == runner.citation(unit) for f in findings)
    else:
        assert not findings, f"expected no finding, got {[f.message for f in findings]}"
    if "version" in case:
        assert info.get("sarif_version") == case["version"]


def test_a_unit_with_no_cases_fails(tmp_path):
    (tmp_path / "expected.yaml").write_text("unit: X\ncases: []\n", encoding="utf-8")
    with pytest.raises(runner.EmptyRun):
        runner.load_cases(tmp_path / "expected.yaml")

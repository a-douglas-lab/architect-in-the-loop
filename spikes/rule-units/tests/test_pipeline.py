"""Translate, select and report: behaviour fixed before the code was written."""
import pytest

from ruleunits import artefacts, glossary, report, select, translate, units

G = glossary.load_default()
UNITS = units.load_all()
F8 = artefacts.load_fixture("f8")


def test_glossary_contexts_are_separate():
    assert G.terms["violation-report"].context == "capability"
    assert G.terms["subject-system"].context == "subject"


def test_one_preferred_label_per_term_and_unique_aliases():
    seen = {}
    for term in G.terms.values():
        for alias in term.aliases:
            assert alias.lower() not in seen, f"{alias!r} in {term.id} and {seen.get(alias.lower())}"
            seen[alias.lower()] = term.id


def test_alias_translator_finds_f8_violation_report():
    assert "violation-report" in translate.alias(F8, G)


@pytest.mark.parametrize("name", ["alias", "bm25"])
def test_deterministic_translators_are_deterministic(name):
    fn = getattr(translate, name)
    assert fn(F8, G) == fn(F8, G)


def test_validator_rejects_unknown_ids():
    with pytest.raises(ValueError):
        translate.validate_ids(["violation-report", "made-up"], G)
    assert translate.validate_ids(["sarif", "violation-report"], G) == ["sarif", "violation-report"]


def test_selection_is_ordered_and_stage_filtered():
    picked = select.select(UNITS, ["violation-report"], "analyze")
    assert picked == sorted(picked)
    assert "adr-016-c10" in picked
    assert "adr-015-c2" not in select.select(UNITS, ["outcome-split"], "implement")


def test_bright_line_is_always_selected():
    assert "hard-rule-4-copy" in select.select(UNITS, [], "analyze")


def test_decoys_are_never_checked():
    assert all(u.check_type == "none" for u in UNITS if u.role == "decoy")


def test_index_lists_every_unit_without_bodies():
    index = units.build_index(UNITS)
    assert {e["unit"] for e in index} == {u.name for u in UNITS}
    assert all("text" not in e for e in index)


def test_rules_file_carries_unit_text_not_findings():
    text = select.rules_file(UNITS, ["adr-016-c10", "hard-rule-4-copy"])
    assert "ADR-016@v1 C10" in text
    assert "Tools that report rule violations MUST report in SARIF." in text
    assert "finding" not in text.lower().split("check:")[0]


def test_report_record_validates_and_bad_record_fails():
    rec = report.make_record("f8", "analyze", "alias", ["violation-report"], ["adr-016-c10"], [], {})
    report.validate(rec)
    bad = dict(rec, stage="deploy")
    with pytest.raises(ValueError):
        report.validate(bad)

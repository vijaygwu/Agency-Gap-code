"""Unit tests for the four-property classifier (Chapter 2 §2.2)."""
from four_property_test import (
    CANONICAL_VERDICTS,
    FourPropertyAnswer,
    classify,
)


def test_all_properties_true_is_agent() -> None:
    a = FourPropertyAnswer(True, True, True, True)
    assert classify(a) == "agent"


def test_canonical_named_patterns() -> None:
    name_index = {
        "persistent_state": 0,
        "tool_access": 1,
        "planning_loop": 2,
        "environmental_feedback": 3,
    }
    for missing, expected_verdict in CANONICAL_VERDICTS.items():
        flags = [True, True, True, True]
        for prop in missing:
            flags[name_index[prop]] = False
        a = FourPropertyAnswer(*flags)
        assert classify(a) == expected_verdict


def test_non_canonical_returns_missing_list() -> None:
    a = FourPropertyAnswer(False, False, False, True)
    verdict = classify(a)
    assert verdict.startswith("not an agent: missing")
    assert "persistent_state" in verdict
    assert "tool_access" in verdict
    assert "planning_loop" in verdict

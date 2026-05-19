"""Four-property test for "is this an agent or a workflow?"

Runnable companion for Chapter 2 §2.2 of "Engineering AI Agents." Asks four
yes/no questions about a candidate system and prints a verdict.

Usage:
    python four_property_test.py         # interactive CLI
    pytest four_property_test.py         # auto-discovers test_classify()

Pedagogical, not load-bearing. The questions match the operational
definition in §2.2; the verdict matches the DAG test in §2.3.
"""
from dataclasses import dataclass


# Canonical named patterns from §2.3. Shared by classify() and
# test_classify() so the verdict strings cannot drift between code and test.
# Key: frozenset of missing property names. Value: verdict string.
CANONICAL_VERDICTS: dict[frozenset[str], str] = {
    frozenset({"persistent_state", "planning_loop", "environmental_feedback"}):
        "retrieval pipeline (not an agent)",
    frozenset({"persistent_state", "tool_access", "environmental_feedback"}):
        "chain-of-thought reasoner (not an agent)",
    frozenset({"persistent_state", "environmental_feedback"}):
        "workflow with embedded inference (not an agent)",
}

_PROPERTY_NAMES = (
    "persistent_state",
    "tool_access",
    "planning_loop",
    "environmental_feedback",
)


@dataclass
class FourPropertyAnswer:
    persistent_state: bool       # state survives across turns/invocations
    tool_access: bool            # interacts with something outside model weights
    planning_loop: bool          # next action depends on intermediate results
    environmental_feedback: bool # loop reads/conditions on environment at inference


def classify(a: FourPropertyAnswer) -> str:
    """Return the system's category per the book's definition.

    Collects every missing property up front so the verdict names all of
    them. Named-pattern labels (retrieval pipeline, chain-of-thought
    reasoner, workflow with embedded inference) come from the shared
    CANONICAL_VERDICTS map and apply only when the missing-property set
    matches the canonical pattern exactly.
    """
    flags = (
        a.persistent_state,
        a.tool_access,
        a.planning_loop,
        a.environmental_feedback,
    )
    missing = [name for name, val in zip(_PROPERTY_NAMES, flags) if not val]
    if not missing:
        return "agent"
    named = CANONICAL_VERDICTS.get(frozenset(missing))
    if named is not None:
        return named
    return "not an agent: missing " + ", ".join(missing)


def test_classify() -> None:
    """Exercise the 16 truth-table rows of classify().

    pytest discovers this automatically (file ends in `_test.py`, function
    starts with `test_`). Silent on success; raises AssertionError on a
    failed row. Can also be invoked as
    `python -c "from four_property_test import test_classify; test_classify()"`.
    """
    from itertools import product

    for flags in product([False, True], repeat=4):
        verdict = classify(FourPropertyAnswer(*flags))
        missing = frozenset(
            name for name, val in zip(_PROPERTY_NAMES, flags) if not val
        )
        if not missing:
            assert verdict == "agent", (
                f"All-true should classify as 'agent', got {verdict!r}"
            )
        elif missing in CANONICAL_VERDICTS:
            assert verdict == CANONICAL_VERDICTS[missing], (
                f"Expected {CANONICAL_VERDICTS[missing]!r}, got {verdict!r} "
                f"for {flags}"
            )
        else:
            assert verdict.startswith("not an agent: missing"), (
                f"Expected missing-list verdict, got {verdict!r} for {flags}"
            )


def ask_yes_no(prompt: str) -> bool:
    while True:
        try:
            raw = input(f"{prompt} [y/n]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            raise SystemExit(1)
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("  Please answer y or n.")


def main() -> None:
    print("Four-property test (Chapter 2 §2.2)\n")
    a = FourPropertyAnswer(
        persistent_state=ask_yes_no(
            "1. Does the system have persistent state that survives across "
            "turns or invocations (not just conversation history)?"
        ),
        tool_access=ask_yes_no(
            "2. Does the system reach outside the model's context window "
            "(tools, APIs, file systems, databases)?"
        ),
        planning_loop=ask_yes_no(
            "3. Does the system select its NEXT action based on the RESULT "
            "of a previous action, in a way that cannot be drawn as a fixed "
            "DAG at design time?"
        ),
        environmental_feedback=ask_yes_no(
            "4. Does the loop read and condition on environmental feedback "
            "AT INFERENCE TIME (not just during training)?"
        ),
    )
    verdict = classify(a)
    print(f"\nVerdict: this is a {verdict}.")
    if verdict == "agent":
        print("Proceed to Chapter 10's six-decision framework.")
    else:
        print("Workflow/pipeline architectures are usually cheaper and safer.")
        print("See Chapter 10 §10.1 for the agent-vs-workflow decision.")


if __name__ == "__main__":
    main()

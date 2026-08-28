#!/usr/bin/env python3
"""Adversarial selftest for the WAIT / Autonomous Patience prototype."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATOR_PATH = HERE / "validate_wait_state.py"
spec = importlib.util.spec_from_file_location("validate_wait_state", VALIDATOR_PATH)
assert spec is not None and spec.loader is not None
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

resolve_case = validator.resolve_case
load_jsonl = validator.load_jsonl
POSTURES = validator.POSTURES


def assert_resolution(case: dict, expected: str, expected_posture: str | None = None) -> None:
    resolution, posture, diagnostics = resolve_case(case)
    assert resolution == expected, (resolution, posture, diagnostics, case)
    if expected_posture is not None:
        assert posture == expected_posture, (resolution, posture, diagnostics, case)


def main() -> int:
    fixture_path = HERE.parent / "fixtures" / "wait-state-cases.jsonl"
    rows = load_jsonl(fixture_path)
    assert rows, "fixture corpus must not be empty"

    # Existing corpus is an open-cardinality regression set: every represented
    # expected result must be reproduced, but the selftest does not assert an
    # exact number of cases as architectural ontology.
    for row in rows:
        resolution, posture, diagnostics = resolve_case(row["case"])
        assert resolution == row["expected_resolution"], (row["case_id"], resolution, diagnostics)
        assert posture == row["expected_posture"], (row["case_id"], posture, diagnostics)

    base = {
        "eval_time": "2026-08-26T10:20:00Z",
        "wait": {
            "wait_id": "ADV-1",
            "reason": "await callback",
            "entered_at": "2026-08-26T10:00:00Z",
            "wake_condition": {"type": "EVENT", "ref": "callback:X"},
            "deadline_at": "2026-08-26T10:30:00Z",
        },
    }

    # Silence is not failure and does not authorize re-execution.
    assert_resolution(base, "WAITING", POSTURES["WAITING"])

    # Wake at the exact deadline is still a represented wake under WS-R06.
    wake_on_deadline = deepcopy(base)
    wake_on_deadline["eval_time"] = "2026-08-26T10:40:00Z"
    wake_on_deadline["wait"]["wake_observation"] = {
        "type": "EVENT",
        "ref": "callback:X",
        "observed_at": "2026-08-26T10:30:00Z",
    }
    assert_resolution(wake_on_deadline, "WAKE_READY", POSTURES["WAKE_READY"])

    # A wake after the deadline cannot resurrect the expired wait horizon.
    late_wake = deepcopy(wake_on_deadline)
    late_wake["wait"]["wake_observation"]["observed_at"] = "2026-08-26T10:31:00Z"
    assert_resolution(late_wake, "TIMEOUT_REACHED", POSTURES["TIMEOUT_REACHED"])

    # Cancellation before a later wake/deadline ends the wait without claiming
    # task completion.
    cancelled_first = deepcopy(wake_on_deadline)
    cancelled_first["wait"]["cancelled_at"] = "2026-08-26T10:10:00Z"
    assert_resolution(cancelled_first, "CANCELLED", POSTURES["CANCELLED"])

    # Wake before a later cancellation remains the first material transition.
    wake_first = deepcopy(wake_on_deadline)
    wake_first["wait"]["wake_observation"]["observed_at"] = "2026-08-26T10:08:00Z"
    wake_first["wait"]["cancelled_at"] = "2026-08-26T10:10:00Z"
    assert_resolution(wake_first, "WAKE_READY", POSTURES["WAKE_READY"])

    # Future occurrence claims are invalid in the evaluated snapshot.
    future_cancel = deepcopy(base)
    future_cancel["wait"]["cancelled_at"] = "2026-08-26T10:25:00Z"
    assert_resolution(future_cancel, "INVALID_RECORD", POSTURES["INVALID_RECORD"])

    # TIME wakes are self-resolved from the declared clock boundary; attaching a
    # second external wake observation would create contradictory time sources.
    time_with_observation = deepcopy(base)
    time_with_observation["wait"]["wake_condition"] = {
        "type": "TIME",
        "at": "2026-08-26T10:10:00Z",
    }
    time_with_observation["wait"]["wake_observation"] = {
        "type": "TIME",
        "observed_at": "2026-08-26T10:11:00Z",
    }
    assert_resolution(time_with_observation, "INVALID_RECORD", POSTURES["INVALID_RECORD"])

    # An open-ended wait remains valid; whether it is acceptable for a material
    # obligation is explicitly a Host/consequence decision rather than a schema
    # timer mandate.
    open_ended = deepcopy(base)
    del open_ended["wait"]["deadline_at"]
    open_ended["eval_time"] = "2026-09-26T10:20:00Z"
    assert_resolution(open_ended, "WAITING", POSTURES["WAITING"])

    # Dependency pointers do not change resolution and cannot manufacture
    # effect settlement or authority validity.
    dependency_refs = deepcopy(base)
    dependency_refs["wait"]["related_effect_refs"] = ["E1"]
    dependency_refs["wait"]["related_authority_refs"] = ["G1"]
    assert_resolution(dependency_refs, "WAITING", POSTURES["WAITING"])

    print("PASS: WAIT adversarial and chronology selftest")
    print("WAKE_READY!=AUTHORIZED_TO_RESUME")
    print("TIMEOUT_REACHED!=RETRY_EFFECT")
    print("WAITING!=COMPLETED")
    print("CANCELLED!=COMPLETED")
    print("OPEN_ENDED_WAIT=REPRESENTABLE_WITH_HOST_CONSEQUENCE_BOUNDARY")
    print("FIXTURE_CARDINALITY=OPEN")
    print("CURRENT_CHANGE=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

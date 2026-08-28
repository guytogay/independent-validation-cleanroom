#!/usr/bin/env python3
"""Validate and resolve the WAIT / Autonomous Patience research prototype.

Verification scope: represented wait chronology plus deterministic wake/cancel/
timeout resolution. This tool does not prove external event authenticity, Host
timer liveness, effect settlement, current authority, or timeout-policy fitness.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
from typing import Any

WAKE_TYPES = {"EVIDENCE", "EVENT", "TIME", "MANUAL"}
RESOLUTIONS = {
    "WAITING",
    "WAKE_READY",
    "TIMEOUT_REACHED",
    "CANCELLED",
    "INVALID_RECORD",
}
POSTURES = {
    "WAITING": "DO_NOT_REEXECUTE_JUST_BECAUSE_NOTHING_HAPPENED",
    "WAKE_READY": "REVALIDATE_DEPENDENCIES_BEFORE_RESUME",
    "TIMEOUT_REACHED": "APPLY_TIMEOUT_POLICY_NO_IMPLICIT_RETRY",
    "CANCELLED": "STOP_WAIT_WITHOUT_COMPLETION_CLAIM",
    "INVALID_RECORD": "REJECT_INCONSISTENT_WAIT_RECORD",
}


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    # Do not compare naive and offset-aware times inside one record.
    if parsed.tzinfo is None:
        return None
    return parsed


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_ref_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and all(_nonempty_string(item) for item in value)
        and len(value) == len(set(value))
    )


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise SystemExit(f"{path}:{lineno}: row must be object")
        rows.append(row)
    return rows


def validate_wait_record(wait: Any, eval_time: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(wait, dict):
        return ["wait must be object"]

    for field in ("wait_id", "reason"):
        if not _nonempty_string(wait.get(field)):
            errors.append(f"{field} required")

    entered_at = parse_time(wait.get("entered_at"))
    evaluated_at = parse_time(eval_time)
    if entered_at is None:
        errors.append("entered_at must be offset-aware ISO datetime")
    if evaluated_at is None:
        errors.append("eval_time must be offset-aware ISO datetime")
    if entered_at is not None and evaluated_at is not None and evaluated_at < entered_at:
        errors.append("eval_time precedes entered_at")

    condition = wait.get("wake_condition")
    if not isinstance(condition, dict):
        errors.append("wake_condition must be object")
        condition = {}

    wake_type = condition.get("type")
    if wake_type not in WAKE_TYPES:
        errors.append("wake_condition.type invalid")
    elif wake_type == "TIME":
        wake_at = parse_time(condition.get("at"))
        if wake_at is None:
            errors.append("TIME wake_condition requires offset-aware ISO at")
        elif entered_at is not None and wake_at < entered_at:
            errors.append("TIME wake condition precedes entered_at")
        if "ref" in condition and condition.get("ref") is not None and not _nonempty_string(condition.get("ref")):
            errors.append("wake_condition.ref must be non-empty string when present")
    else:
        if not _nonempty_string(condition.get("ref")):
            errors.append(f"{wake_type or 'non-TIME'} wake_condition requires ref")
        if "at" in condition and condition.get("at") is not None:
            errors.append("non-TIME wake_condition must not carry at")

    deadline_raw = wait.get("deadline_at")
    deadline_at = parse_time(deadline_raw) if deadline_raw is not None else None
    if deadline_raw is not None and deadline_at is None:
        errors.append("deadline_at must be offset-aware ISO datetime when present")
    if entered_at is not None and deadline_at is not None and deadline_at < entered_at:
        errors.append("deadline_at precedes entered_at")

    cancelled_raw = wait.get("cancelled_at")
    cancelled_at = parse_time(cancelled_raw) if cancelled_raw is not None else None
    if cancelled_raw is not None and cancelled_at is None:
        errors.append("cancelled_at must be offset-aware ISO datetime when present")
    if entered_at is not None and cancelled_at is not None and cancelled_at < entered_at:
        errors.append("cancelled_at precedes entered_at")
    if evaluated_at is not None and cancelled_at is not None and cancelled_at > evaluated_at:
        errors.append("cancelled_at is in the future relative to eval_time")

    observation = wait.get("wake_observation")
    if observation is not None:
        if not isinstance(observation, dict):
            errors.append("wake_observation must be object when present")
        else:
            observed_type = observation.get("type")
            if observed_type != wake_type:
                errors.append("wake_observation.type does not match wake_condition.type")
            observed_at = parse_time(observation.get("observed_at"))
            if observed_at is None:
                errors.append("wake_observation.observed_at must be offset-aware ISO datetime")
            else:
                if entered_at is not None and observed_at < entered_at:
                    errors.append("wake observation precedes entered_at")
                if evaluated_at is not None and observed_at > evaluated_at:
                    errors.append("wake observation is in the future relative to eval_time")
            if wake_type == "TIME":
                # TIME wakes are resolved from the declared time itself; an external
                # observation is unnecessary and would create two clocks for one cue.
                errors.append("TIME wake_condition must not carry wake_observation")
            elif isinstance(condition, dict) and observation.get("ref") != condition.get("ref"):
                errors.append("wake_observation.ref does not match wake_condition.ref")

    for field in ("related_effect_refs", "related_authority_refs"):
        value = wait.get(field)
        if value is not None and not _valid_ref_list(value):
            errors.append(f"{field} must be a unique string array when present")

    note = wait.get("note")
    if note is not None and not _nonempty_string(note):
        errors.append("note must be non-empty string when present")

    return errors


def resolve_case(case: Any) -> tuple[str, str, list[str]]:
    """Return (resolution, posture, diagnostics) for represented state only."""
    if not isinstance(case, dict):
        return ("INVALID_RECORD", POSTURES["INVALID_RECORD"], ["CASE_NOT_OBJECT"])

    eval_raw = case.get("eval_time")
    wait = case.get("wait")
    errors = validate_wait_record(wait, eval_raw)
    if errors:
        return ("INVALID_RECORD", POSTURES["INVALID_RECORD"], errors)

    assert isinstance(wait, dict)
    eval_time = parse_time(eval_raw)
    entered_at = parse_time(wait["entered_at"])
    assert eval_time is not None and entered_at is not None

    condition = wait["wake_condition"]
    wake_type = condition["type"]
    deadline_at = parse_time(wait.get("deadline_at"))
    cancelled_at = parse_time(wait.get("cancelled_at"))

    wake_at: datetime | None = None
    if wake_type == "TIME":
        wake_at = parse_time(condition["at"])
    else:
        observation = wait.get("wake_observation")
        if isinstance(observation, dict):
            wake_at = parse_time(observation["observed_at"])

    # Resolution is occurrence-sensitive, not merely evaluation-time-sensitive.
    # Explicit cancellation wins a tie because the represented actor withdrew
    # the wait at that instant. A wake at the exact deadline remains WAKE_READY
    # per WS-R06 (wake before/equal deadline may wake).
    occurred_cancel = cancelled_at if cancelled_at is not None and cancelled_at <= eval_time else None
    occurred_wake = wake_at if wake_at is not None and wake_at <= eval_time else None
    occurred_deadline = deadline_at if deadline_at is not None and deadline_at <= eval_time else None

    if occurred_cancel is not None:
        if occurred_wake is None or occurred_cancel <= occurred_wake:
            if occurred_deadline is None or occurred_cancel <= occurred_deadline:
                return ("CANCELLED", POSTURES["CANCELLED"], [])

    if occurred_wake is not None:
        if occurred_deadline is None or occurred_wake <= occurred_deadline:
            if occurred_cancel is None or occurred_wake < occurred_cancel:
                return ("WAKE_READY", POSTURES["WAKE_READY"], [])

    if occurred_deadline is not None:
        if occurred_cancel is None or occurred_deadline < occurred_cancel:
            return ("TIMEOUT_REACHED", POSTURES["TIMEOUT_REACHED"], [])

    # A later cancellation/wake/deadline cannot affect the current snapshot.
    return ("WAITING", POSTURES["WAITING"], [])


def main() -> int:
    parser = argparse.ArgumentParser()
    default_cases = Path(__file__).resolve().parents[1] / "fixtures" / "wait-state-cases.jsonl"
    parser.add_argument("--cases", type=Path, default=default_cases)
    args = parser.parse_args()

    rows = load_jsonl(args.cases)
    failures: list[str] = []
    seen: set[str] = set()
    counts = {state: 0 for state in RESOLUTIONS}

    for row in rows:
        case_id = row.get("case_id")
        if not _nonempty_string(case_id):
            failures.append("case without valid case_id")
            continue
        if case_id in seen:
            failures.append(f"duplicate case_id: {case_id}")
            continue
        seen.add(case_id)

        expected_resolution = row.get("expected_resolution")
        expected_posture = row.get("expected_posture")
        if expected_resolution not in RESOLUTIONS or not _nonempty_string(expected_posture):
            failures.append(f"{case_id}: malformed expected result")
            continue

        resolution, posture, diagnostics = resolve_case(row.get("case"))
        counts[resolution] += 1
        if resolution != expected_resolution:
            failures.append(
                f"{case_id}: resolution expected={expected_resolution} actual={resolution} diagnostics={diagnostics}"
            )
        if posture != expected_posture:
            failures.append(
                f"{case_id}: posture expected={expected_posture} actual={posture} diagnostics={diagnostics}"
            )

    print(f"cases={len(rows)} " + " ".join(f"{key.lower()}={counts[key]}" for key in sorted(counts)))
    if failures:
        print(f"FAIL: {len(failures)} WAIT fixture mismatch(es)")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: all WAIT fixtures matched represented reference rules")
    print("verification_scope=REPRESENTED_WAIT_WAKE_CANCEL_TIMEOUT_CONSISTENCY_ONLY")
    print("external_event_authenticity=UNPROVEN")
    print("host_timer_liveness=UNPROVEN")
    print("effect_settlement=SEPARATE_ORGAN")
    print("resume_authority=SEPARATE_ORGAN")
    print("timeout_policy_fitness=HOST_CONSEQUENCE_BOUNDARY")
    print("fixture_cardinality=OPEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

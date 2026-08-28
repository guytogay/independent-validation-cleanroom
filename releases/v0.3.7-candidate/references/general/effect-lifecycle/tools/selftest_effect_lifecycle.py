#!/usr/bin/env python3
"""Portable adversarial selftest for Effect Lifecycle research prototype."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from validate_effect_lifecycle import load_jsonl, next_action, validate_record  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> int:
    validator = TOOLS / "validate_effect_lifecycle.py"
    cases_path = ROOT / "fixtures" / "effect-lifecycle-cases.jsonl"

    proc = subprocess.run(
        [sys.executable, str(validator), "--cases", str(cases_path)],
        text=True,
        capture_output=True,
    )
    print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    require(proc.returncode == 0, "authored fixture corpus does not match validator")

    rows = load_jsonl(cases_path)
    require(bool(rows), "effect fixture corpus must not be empty")
    by_id = {row["case_id"]: row for row in rows}
    require(len(rows) == len(by_id), "fixture case_id values must be unique")
    required_ids = {"EL-001", "EL-003", "EL-008", "EL-009"}
    require(required_ids <= set(by_id), f"missing targeted regression fixtures: {sorted(required_ids - set(by_id))}")

    # Mutation 1: same effect identity, different material parameters.
    mutated = deepcopy(by_id["EL-001"]["record"])
    mutated["attempts"][0]["material_parameters_digest"] = "sha256:DIFFERENT"
    errors = validate_record(mutated)
    require(
        any("material parameter digest differs" in error for error in errors),
        "validator missed effect-id/material-parameter rebinding",
    )
    require(
        next_action(mutated, errors) == "REJECT_INCONSISTENT_RECORD",
        "inconsistent parameter rebinding did not reject",
    )
    print("PASS: catches same-effect material parameter mutation")

    # Mutation 2: fork copies one indivisible commitment into two ACTIVE owners.
    mutated = deepcopy(by_id["EL-008"]["record"])
    mutated["commitments"][0]["executor_assignments"][1]["status"] = "ACTIVE"
    errors = validate_record(mutated)
    require(
        any("multiple ACTIVE executors" in error for error in errors),
        "validator missed forked double execution ownership",
    )
    print("PASS: catches forked duplicate ACTIVE commitment ownership")

    # Mutation 3: local workflow marks settlement complete without settlement receipt.
    mutated = deepcopy(by_id["EL-003"]["record"])
    mutated["receipts"] = []
    mutated["commitments"][0]["status"] = "SETTLED"
    mutated["commitments"][0]["settlement_receipt_refs"] = []
    errors = validate_record(mutated)
    require(
        any("SETTLED requires settlement receipt refs" in error for error in errors),
        "validator missed receipt-free settlement claim",
    )
    print("PASS: catches receipt-free commitment settlement")

    # Mutation 4: a later REALIZE occurs after a represented COMMITTED receipt.
    mutated = deepcopy(by_id["EL-003"]["record"])
    mutated["attempts"].append(
        {
            "attempt_id": "A2",
            "effect_id": "E1",
            "kind": "REALIZE",
            "material_parameters_digest": "sha256:x",
            "outcome": "ACKNOWLEDGED",
            "sequence": 3,
        }
    )
    errors = validate_record(mutated)
    require(
        any("REALIZE occurs after known terminal receipt" in error for error in errors),
        "validator missed post-settlement realization replay",
    )
    print("PASS: catches REALIZE after known committed receipt")

    control = deepcopy(by_id["EL-009"]["record"])
    errors = validate_record(control)
    require(not errors, f"read-only false-BLOCK: {errors}")
    require(
        next_action(control, errors) == "REALIZE_NEW_INTENT",
        "read-only control did not remain executable",
    )
    print("PASS: read-only/no-idempotency false-BLOCK control")

    print("PASS: effect-lifecycle portable adversarial selftest")
    print(f"observed_fixture_count={len(rows)}")
    print("fixture_cardinality=OPEN_WITH_TARGETED_REGRESSION_DEPENDENCIES")
    print("verification_scope=REPRESENTED_LIFECYCLE_RULES_AND_SELFTEST_MUTATIONS_ONLY")
    print("external_receipt_authenticity=UNPROVEN")
    print("exactly_once=NOT_CLAIMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

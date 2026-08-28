#!/usr/bin/env python3
"""Validate/evaluate the research Effect Lifecycle fixture corpus.

Verification scope: represented lifecycle consistency and deterministic reference
next-action logic only. This does not authenticate receipts or prove exactly-once
external execution.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

EFFECT_CLASSES = {
    "READ_ONLY",
    "REVERSIBLE_LOCAL",
    "EXTERNAL_COMPENSABLE",
    "EXTERNAL_IRREVERSIBLE",
    "EXTERNAL_UNKNOWN",
}
IDEMPOTENCY = {
    "NATIVE_KEY",
    "TRANSACTIONAL_WORKFLOW",
    "INTRINSICALLY_REPEATABLE",
    "NONE",
    "UNKNOWN",
}
ATTEMPT_KINDS = {"REALIZE", "STATUS_QUERY"}
ATTEMPT_OUTCOMES = {"NOT_STARTED", "IN_FLIGHT", "ACKNOWLEDGED", "TIMEOUT", "ERROR", "UNKNOWN"}
RECEIPT_STATUSES = {"COMMITTED", "NOT_COMMITTED", "PARTIAL", "UNKNOWN", "COMPENSATED"}
COMMITMENT_STATUSES = {"OPEN", "ASSIGNED", "WAITING", "SETTLED", "CANCELLED", "UNKNOWN"}
ASSIGNMENT_STATUSES = {"ACTIVE", "OBSERVER", "REVOKED", "SETTLED"}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
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


def validate_record(record: dict) -> list[str]:
    errors: list[str] = []

    effects = record.get("effects")
    attempts = record.get("attempts")
    receipts = record.get("receipts")
    commitments = record.get("commitments")

    if not isinstance(effects, list) or not effects:
        return ["effects must be a non-empty array"]
    if not isinstance(attempts, list):
        errors.append("attempts must be an array")
        attempts = []
    if not isinstance(receipts, list):
        errors.append("receipts must be an array")
        receipts = []
    if not isinstance(commitments, list):
        errors.append("commitments must be an array")
        commitments = []

    effect_by_id: dict[str, dict] = {}
    for i, effect in enumerate(effects):
        if not isinstance(effect, dict):
            errors.append(f"effects[{i}] must be object")
            continue
        effect_id = effect.get("effect_id")
        if not isinstance(effect_id, str) or not effect_id:
            errors.append(f"effects[{i}].effect_id required")
            continue
        if effect_id in effect_by_id:
            errors.append(f"duplicate effect_id: {effect_id}")
            continue
        effect_by_id[effect_id] = effect
        for field in ["target", "operation", "material_parameters_digest", "authority_ref"]:
            if not isinstance(effect.get(field), str) or not effect[field]:
                errors.append(f"{effect_id}: {field} required")
        if effect.get("effect_class") not in EFFECT_CLASSES:
            errors.append(f"{effect_id}: invalid effect_class")
        if effect.get("idempotency_strategy") not in IDEMPOTENCY:
            errors.append(f"{effect_id}: invalid idempotency_strategy")

    decision_effect_id = record.get("decision_effect_id")
    if decision_effect_id not in effect_by_id:
        errors.append(f"decision_effect_id not represented: {decision_effect_id!r}")

    for effect_id, effect in effect_by_id.items():
        original = effect.get("compensates_effect_id")
        if original is not None:
            if not isinstance(original, str) or not original:
                errors.append(f"{effect_id}: compensates_effect_id must be string")
            elif original == effect_id:
                errors.append(f"{effect_id}: compensation cannot reuse original effect_id")
            elif original not in effect_by_id:
                errors.append(f"{effect_id}: compensation origin not represented: {original}")

    attempt_by_id: dict[str, dict] = {}
    attempt_sequence_state: dict[tuple[str, int], tuple[str, str]] = {}
    for i, attempt in enumerate(attempts):
        if not isinstance(attempt, dict):
            errors.append(f"attempts[{i}] must be object")
            continue
        attempt_id = attempt.get("attempt_id")
        effect_id = attempt.get("effect_id")
        if not isinstance(attempt_id, str) or not attempt_id:
            errors.append(f"attempts[{i}].attempt_id required")
            continue
        if attempt_id in attempt_by_id:
            errors.append(f"duplicate attempt_id: {attempt_id}")
            continue
        attempt_by_id[attempt_id] = attempt
        if effect_id not in effect_by_id:
            errors.append(f"{attempt_id}: unknown effect_id {effect_id!r}")
            continue
        kind = attempt.get("kind")
        outcome = attempt.get("outcome")
        if kind not in ATTEMPT_KINDS:
            errors.append(f"{attempt_id}: invalid kind")
        if outcome not in ATTEMPT_OUTCOMES:
            errors.append(f"{attempt_id}: invalid outcome")
        sequence = attempt.get("sequence")
        if not isinstance(sequence, int):
            errors.append(f"{attempt_id}: integer sequence required")
        elif kind in ATTEMPT_KINDS and outcome in ATTEMPT_OUTCOMES:
            sequence_key = (effect_id, sequence)
            represented_state = (kind, outcome)
            prior_state = attempt_sequence_state.get(sequence_key)
            if prior_state is not None and prior_state != represented_state:
                errors.append(
                    f"{attempt_id}: conflicting attempt state at sequence {sequence} for effect {effect_id}"
                )
            else:
                attempt_sequence_state.setdefault(sequence_key, represented_state)
        if attempt.get("material_parameters_digest") != effect_by_id[effect_id].get("material_parameters_digest"):
            errors.append(f"{attempt_id}: material parameter digest differs from intent {effect_id}")

    receipt_by_id: dict[str, dict] = {}
    receipt_sequence_status: dict[tuple[str, int], str] = {}
    for i, receipt in enumerate(receipts):
        if not isinstance(receipt, dict):
            errors.append(f"receipts[{i}] must be object")
            continue
        receipt_id = receipt.get("receipt_id")
        effect_id = receipt.get("effect_id")
        if not isinstance(receipt_id, str) or not receipt_id:
            errors.append(f"receipts[{i}].receipt_id required")
            continue
        if receipt_id in receipt_by_id:
            errors.append(f"duplicate receipt_id: {receipt_id}")
            continue
        receipt_by_id[receipt_id] = receipt
        if effect_id not in effect_by_id:
            errors.append(f"{receipt_id}: unknown effect_id {effect_id!r}")
        if receipt.get("observed_status") not in RECEIPT_STATUSES:
            errors.append(f"{receipt_id}: invalid observed_status")
        evidence_refs = receipt.get("evidence_refs")
        if not isinstance(evidence_refs, list) or not evidence_refs or not all(isinstance(x, str) and x for x in evidence_refs):
            errors.append(f"{receipt_id}: non-empty evidence_refs required")
        sequence = receipt.get("sequence")
        status = receipt.get("observed_status")
        if not isinstance(sequence, int):
            errors.append(f"{receipt_id}: integer sequence required")
        elif effect_id in effect_by_id and status in RECEIPT_STATUSES:
            sequence_key = (effect_id, sequence)
            prior_status = receipt_sequence_status.get(sequence_key)
            if prior_status is not None and prior_status != status:
                errors.append(
                    f"{receipt_id}: conflicting receipt status at sequence {sequence} for effect {effect_id}"
                )
            else:
                receipt_sequence_status.setdefault(sequence_key, status)
        attempt_id = receipt.get("attempt_id")
        if attempt_id is not None:
            if attempt_id not in attempt_by_id:
                errors.append(f"{receipt_id}: unknown attempt_id {attempt_id!r}")
            elif attempt_by_id[attempt_id].get("effect_id") != effect_id:
                errors.append(f"{receipt_id}: attempt/effect mismatch")

    # Once a represented COMMITTED/COMPENSATED receipt is known, a later REALIZE
    # attempt for the same logical effect is rejected. STATUS_QUERY remains legal.
    terminal_receipt_sequence: dict[str, int] = {}
    for receipt in receipt_by_id.values():
        if receipt.get("observed_status") in {"COMMITTED", "COMPENSATED"} and isinstance(receipt.get("sequence"), int):
            effect_id = receipt.get("effect_id")
            terminal_receipt_sequence[effect_id] = min(
                terminal_receipt_sequence.get(effect_id, receipt["sequence"]),
                receipt["sequence"],
            )
    for attempt_id, attempt in attempt_by_id.items():
        effect_id = attempt.get("effect_id")
        if (
            attempt.get("kind") == "REALIZE"
            and isinstance(attempt.get("sequence"), int)
            and effect_id in terminal_receipt_sequence
            and attempt["sequence"] > terminal_receipt_sequence[effect_id]
        ):
            errors.append(f"{attempt_id}: REALIZE occurs after known terminal receipt for {effect_id}")

    commitment_by_id: dict[str, dict] = {}
    for i, commitment in enumerate(commitments):
        if not isinstance(commitment, dict):
            errors.append(f"commitments[{i}] must be object")
            continue
        commitment_id = commitment.get("commitment_id")
        if not isinstance(commitment_id, str) or not commitment_id:
            errors.append(f"commitments[{i}].commitment_id required")
            continue
        if commitment_id in commitment_by_id:
            errors.append(f"duplicate commitment_id: {commitment_id}")
            continue
        commitment_by_id[commitment_id] = commitment
        effect_ids = commitment.get("effect_ids")
        if not isinstance(effect_ids, list) or not effect_ids:
            errors.append(f"{commitment_id}: effect_ids required")
            effect_ids = []
        for effect_id in effect_ids:
            if effect_id not in effect_by_id:
                errors.append(f"{commitment_id}: unknown effect_id {effect_id!r}")
        if commitment.get("status") not in COMMITMENT_STATUSES:
            errors.append(f"{commitment_id}: invalid status")
        assignments = commitment.get("executor_assignments")
        if not isinstance(assignments, list):
            errors.append(f"{commitment_id}: executor_assignments must be array")
            assignments = []
        active_count = 0
        for j, assignment in enumerate(assignments):
            if not isinstance(assignment, dict):
                errors.append(f"{commitment_id}: assignment[{j}] must be object")
                continue
            if not isinstance(assignment.get("executor"), str) or not assignment.get("executor"):
                errors.append(f"{commitment_id}: assignment[{j}].executor required")
            if assignment.get("status") not in ASSIGNMENT_STATUSES:
                errors.append(f"{commitment_id}: assignment[{j}] invalid status")
            if assignment.get("status") == "ACTIVE":
                active_count += 1
        if active_count > 1 and not commitment.get("partitioned", False):
            errors.append(f"{commitment_id}: multiple ACTIVE executors without partition semantics")

        settlement_refs = commitment.get("settlement_receipt_refs")
        if not isinstance(settlement_refs, list):
            errors.append(f"{commitment_id}: settlement_receipt_refs must be array")
            settlement_refs = []
        for receipt_id in settlement_refs:
            if receipt_id not in receipt_by_id:
                errors.append(f"{commitment_id}: unknown settlement receipt {receipt_id!r}")

        if commitment.get("status") == "SETTLED":
            if not settlement_refs:
                errors.append(f"{commitment_id}: SETTLED requires settlement receipt refs")
            else:
                settled_effects = {
                    receipt_by_id[r].get("effect_id")
                    for r in settlement_refs
                    if r in receipt_by_id
                    and receipt_by_id[r].get("observed_status") in {"COMMITTED", "COMPENSATED"}
                }
                missing = set(effect_ids) - settled_effects
                if missing:
                    errors.append(
                        f"{commitment_id}: SETTLED lacks terminal settlement evidence for {sorted(missing)}"
                    )

    return errors


def next_action(record: dict, errors: list[str]) -> str:
    if errors:
        return "REJECT_INCONSISTENT_RECORD"

    effect_id = record["decision_effect_id"]
    effects = {e["effect_id"]: e for e in record["effects"]}
    effect = effects[effect_id]
    attempts = sorted(
        [a for a in record.get("attempts", []) if a.get("effect_id") == effect_id],
        key=lambda a: a.get("sequence", -1),
    )
    receipts = sorted(
        [r for r in record.get("receipts", []) if r.get("effect_id") == effect_id],
        key=lambda r: r.get("sequence", -1),
    )
    commitments = [c for c in record.get("commitments", []) if effect_id in c.get("effect_ids", [])]

    if receipts:
        latest = receipts[-1]["observed_status"]
        if latest == "PARTIAL":
            return "MANUAL_RECONCILIATION"
        if latest in {"COMMITTED", "COMPENSATED"}:
            if any(c.get("status") not in {"SETTLED", "CANCELLED"} for c in commitments):
                return "SETTLE_COMMITMENT"
            return "NO_EFFECT_NEEDED"
        if latest == "NOT_COMMITTED":
            return "RETRY_SAME_INTENT"
        if latest == "UNKNOWN":
            return "QUERY_SETTLEMENT"

    realize_attempts = [a for a in attempts if a.get("kind") == "REALIZE"]
    if not realize_attempts:
        return "REALIZE_NEW_INTENT"

    last = realize_attempts[-1]
    if last.get("outcome") == "IN_FLIGHT":
        return "WAIT_FOR_EVIDENCE"

    strategy = effect.get("idempotency_strategy")
    if last.get("outcome") in {"TIMEOUT", "ERROR", "UNKNOWN"}:
        if strategy in {"NATIVE_KEY", "INTRINSICALLY_REPEATABLE"}:
            return "RETRY_SAME_INTENT"
        return "QUERY_SETTLEMENT"

    if last.get("outcome") == "ACKNOWLEDGED":
        return "QUERY_SETTLEMENT"

    return "QUERY_SETTLEMENT"


def main() -> int:
    parser = argparse.ArgumentParser()
    default_cases = Path(__file__).resolve().parents[1] / "fixtures" / "effect-lifecycle-cases.jsonl"
    parser.add_argument("--cases", type=Path, default=default_cases)
    args = parser.parse_args()

    rows = load_jsonl(args.cases)
    failures: list[str] = []
    valid_expected = invalid_expected = 0

    case_ids: set[str] = set()
    for row in rows:
        case_id = row.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            failures.append("case without valid case_id")
            continue
        if case_id in case_ids:
            failures.append(f"duplicate case_id: {case_id}")
            continue
        case_ids.add(case_id)

        expected_valid = row.get("expected_valid")
        expected_action = row.get("expected_next_action")
        record = row.get("record")
        if not isinstance(expected_valid, bool) or not isinstance(expected_action, str) or not isinstance(record, dict):
            failures.append(f"{case_id}: malformed fixture wrapper")
            continue

        errors = validate_record(record)
        actual_valid = not errors
        actual_action = next_action(record, errors)
        valid_expected += int(expected_valid)
        invalid_expected += int(not expected_valid)

        if actual_valid != expected_valid:
            failures.append(
                f"{case_id}: validity expected={expected_valid} actual={actual_valid} errors={errors}"
            )
        if actual_action != expected_action:
            failures.append(
                f"{case_id}: next_action expected={expected_action} actual={actual_action} errors={errors}"
            )

    print(
        f"cases={len(rows)} expected_valid={valid_expected} expected_invalid={invalid_expected}"
    )
    if failures:
        print(f"FAIL: {len(failures)} fixture mismatch(es)")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: all Effect Lifecycle fixtures matched represented reference rules")
    print("verification_scope=REPRESENTED_LIFECYCLE_CONSISTENCY_AND_REFERENCE_NEXT_ACTION_ONLY")
    print("external_receipt_authenticity=UNPROVEN")
    print("exactly_once=NOT_CLAIMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

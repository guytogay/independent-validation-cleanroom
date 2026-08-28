#!/usr/bin/env python3
"""Validate/evaluate the Recovery Adapter research prototype.

Verification scope: represented rescue viability, restore state, and bounded
post-restore summaries only. This does not prove external recovery, settlement,
authority, or evidence authenticity.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ACTIONS = {
    "ATTEMPT_RESTORE",
    "RESUME",
    "DO_NOT_RESUME",
    "REPAIR_RECOVERY_PATH",
    "RESOLVE_RECOVERY_UNCERTAINTY",
    "REJECT_INCONSISTENT_RECORD",
}
INDEPENDENCE = {"INDEPENDENT", "SHARED_FATE", "UNKNOWN"}
REACHABILITY = {"VERIFIED_REACHABLE", "VERIFIED_UNREACHABLE", "UNKNOWN"}
DRILL = {"PASSED", "FAILED", "NOT_TESTED", "UNKNOWN"}
RESTORE = {"NOT_ATTEMPTED", "SUCCESS", "FAILED", "UNKNOWN"}
WORLD = {"NOT_REQUIRED", "CLEARED", "ACTION_REQUIRED", "UNRESOLVED"}
AUTHORITY = {"NOT_REQUIRED", "AUTHORIZED", "NOT_AUTHORIZED", "UNRESOLVED"}


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


def _s(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _refs(value: Any) -> bool:
    return isinstance(value, list) and all(_s(item) for item in value) and len(value) == len(set(value))


def validate_record(record: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["record must be object"]

    for field in (
        "adapter_id",
        "protected_subject_ref",
        "candidate_failure_domain",
        "control_plane_failure_domain",
        "rescue_failure_domain",
        "rescue_executor",
        "recovery_locator",
        "access_path_ref",
        "checkpoint_ref",
    ):
        if not _s(record.get(field)):
            errors.append(f"{field} required")

    if not isinstance(record.get("independent_rescue_required"), bool):
        errors.append("independent_rescue_required must be boolean")

    independence = record.get("rescue_independence")
    if not isinstance(independence, dict):
        errors.append("rescue_independence must be object")
        independence = {}
    independence_status = independence.get("status")
    if independence_status not in INDEPENDENCE:
        errors.append("invalid rescue_independence.status")
    independence_refs = independence.get("evidence_refs")
    if not _refs(independence_refs):
        errors.append("rescue_independence.evidence_refs must be unique string array")
        independence_refs = []
    if independence_status in {"INDEPENDENT", "SHARED_FATE"} and not independence_refs:
        errors.append("represented independence/shared-fate observation requires evidence refs")

    reachability = record.get("reachability")
    if not isinstance(reachability, dict):
        errors.append("reachability must be object")
        reachability = {}
    reachability_status = reachability.get("status")
    if reachability_status not in REACHABILITY:
        errors.append("invalid reachability.status")
    reachability_refs = reachability.get("evidence_refs")
    if not _refs(reachability_refs):
        errors.append("reachability.evidence_refs must be unique string array")
        reachability_refs = []
    if reachability_status in {"VERIFIED_REACHABLE", "VERIFIED_UNREACHABLE"} and not reachability_refs:
        errors.append("verified reachability observation requires evidence refs")

    drill = record.get("restore_drill")
    if not isinstance(drill, dict):
        errors.append("restore_drill must be object")
        drill = {}
    if not isinstance(drill.get("required"), bool):
        errors.append("restore_drill.required must be boolean")
    drill_status = drill.get("status")
    if drill_status not in DRILL:
        errors.append("invalid restore_drill.status")
    drill_refs = drill.get("evidence_refs")
    if not _refs(drill_refs):
        errors.append("restore_drill.evidence_refs must be unique string array")
        drill_refs = []
    if drill_status in {"PASSED", "FAILED"} and not drill_refs:
        errors.append("represented drill result requires evidence refs")

    restore = record.get("restore")
    if not isinstance(restore, dict):
        errors.append("restore must be object")
        restore = {}
    restore_status = restore.get("status")
    if restore_status not in RESTORE:
        errors.append("invalid restore.status")
    restore_refs = restore.get("evidence_refs")
    if not _refs(restore_refs):
        errors.append("restore.evidence_refs must be unique string array")
        restore_refs = []
    if restore_status in {"SUCCESS", "FAILED"} and not restore_refs:
        errors.append("represented restore result requires evidence refs")

    post = record.get("post_restore")
    if restore_status == "SUCCESS" and not isinstance(post, dict):
        errors.append("post_restore required when restore.status=SUCCESS")
    if post is not None and not isinstance(post, dict):
        errors.append("post_restore must be object when present")
        post = None

    if isinstance(post, dict):
        world_state = post.get("world_state")
        authority_state = post.get("authority_state")
        if world_state not in WORLD:
            errors.append("invalid post_restore.world_state")
        if authority_state not in AUTHORITY:
            errors.append("invalid post_restore.authority_state")

        world_refs = post.get("world_resolution_refs")
        authority_refs = post.get("authority_resolution_refs")
        if not _refs(world_refs):
            errors.append("post_restore.world_resolution_refs must be unique string array")
            world_refs = []
        if not _refs(authority_refs):
            errors.append("post_restore.authority_resolution_refs must be unique string array")
            authority_refs = []

        if world_state in {"CLEARED", "ACTION_REQUIRED", "UNRESOLVED"} and not world_refs:
            errors.append("represented post-restore world state requires resolution refs")
        if authority_state in {"AUTHORIZED", "NOT_AUTHORIZED", "UNRESOLVED"} and not authority_refs:
            errors.append("represented post-restore authority state requires resolution refs")

    return errors


def evaluate(record: Any) -> tuple[str, list[str]]:
    errors = validate_record(record)
    if errors:
        return ("REJECT_INCONSISTENT_RECORD", errors)
    assert isinstance(record, dict)

    blockers: list[str] = []
    uncertain: list[str] = []

    independence_status = record["rescue_independence"]["status"]
    if record["independent_rescue_required"]:
        if independence_status == "SHARED_FATE":
            blockers.append("REQUIRED_RESCUE_SHARES_FATE")
        elif independence_status == "UNKNOWN":
            uncertain.append("REQUIRED_RESCUE_INDEPENDENCE_UNKNOWN")

    reachability_status = record["reachability"]["status"]
    if reachability_status == "VERIFIED_UNREACHABLE":
        blockers.append("RECOVERY_PATH_UNREACHABLE")
    elif reachability_status == "UNKNOWN":
        uncertain.append("RECOVERY_PATH_REACHABILITY_UNKNOWN")

    drill = record["restore_drill"]
    if drill["required"]:
        if drill["status"] == "FAILED":
            blockers.append("REQUIRED_RESTORE_DRILL_FAILED")
        elif drill["status"] in {"NOT_TESTED", "UNKNOWN"}:
            uncertain.append("REQUIRED_RESTORE_DRILL_UNRESOLVED")

    if blockers:
        return ("REPAIR_RECOVERY_PATH", blockers + uncertain)
    if uncertain:
        return ("RESOLVE_RECOVERY_UNCERTAINTY", uncertain)

    restore_status = record["restore"]["status"]
    if restore_status == "NOT_ATTEMPTED":
        return ("ATTEMPT_RESTORE", [])
    if restore_status == "FAILED":
        return ("REPAIR_RECOVERY_PATH", ["RESTORE_FAILED"])
    if restore_status == "UNKNOWN":
        return ("RESOLVE_RECOVERY_UNCERTAINTY", ["RESTORE_RESULT_UNKNOWN"])

    assert restore_status == "SUCCESS"
    post = record["post_restore"]
    resume_blockers: list[str] = []

    world_state = post["world_state"]
    if world_state == "ACTION_REQUIRED":
        resume_blockers.append("WORLD_RECONCILIATION_ACTION_REQUIRED")
    elif world_state == "UNRESOLVED":
        resume_blockers.append("WORLD_RECONCILIATION_UNRESOLVED")

    authority_state = post["authority_state"]
    if authority_state == "NOT_AUTHORIZED":
        resume_blockers.append("AUTHORITY_NOT_AUTHORIZED")
    elif authority_state == "UNRESOLVED":
        resume_blockers.append("AUTHORITY_UNRESOLVED")

    if resume_blockers:
        return ("DO_NOT_RESUME", resume_blockers)
    return ("RESUME", [])


def main() -> int:
    parser = argparse.ArgumentParser()
    default_cases = Path(__file__).resolve().parents[1] / "fixtures" / "recovery-adapter-cases.jsonl"
    parser.add_argument("--cases", type=Path, default=default_cases)
    args = parser.parse_args()

    rows = load_jsonl(args.cases)
    failures: list[str] = []
    seen: set[str] = set()
    counts = {action: 0 for action in ACTIONS}

    for row in rows:
        case_id = row.get("case_id")
        if not _s(case_id):
            failures.append("case without valid case_id")
            continue
        if case_id in seen:
            failures.append(f"duplicate case_id: {case_id}")
            continue
        seen.add(case_id)

        expected = row.get("expected_action")
        if expected not in ACTIONS:
            failures.append(f"{case_id}: invalid expected_action")
            continue

        actual, diagnostics = evaluate(row.get("case"))
        counts[actual] += 1
        if actual != expected:
            failures.append(f"{case_id}: expected={expected} actual={actual} diagnostics={diagnostics}")

    print(f"cases={len(rows)} " + " ".join(f"{key.lower()}={counts[key]}" for key in sorted(counts)))
    if failures:
        print(f"FAIL: {len(failures)} recovery-adapter fixture mismatch(es)")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: all Recovery Adapter fixtures matched represented reference rules")
    print("verification_scope=REPRESENTED_RESCUE_RESTORE_AND_POST_RESTORE_SUMMARIES_ONLY")
    print("external_recovery_truth=UNPROVEN")
    print("post_restore_world_truth=UNPROVEN")
    print("post_restore_authority_truth=UNPROVEN")
    print("independent_rescue_required=CALLER_TRUST_BOUNDARY")
    print("restore_drill_required=CALLER_TRUST_BOUNDARY")
    print("fixture_cardinality=OPEN_WITH_TARGETED_REGRESSION_DEPENDENCIES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

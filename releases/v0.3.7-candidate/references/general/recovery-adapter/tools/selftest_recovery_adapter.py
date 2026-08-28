#!/usr/bin/env python3
"""Portable adversarial selftest for Recovery Adapter prototype."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import subprocess
import sys

from validate_recovery_adapter import evaluate, load_jsonl


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def by_id(rows: list[dict], case_id: str) -> dict:
    for row in rows:
        if row.get("case_id") == case_id:
            return copy.deepcopy(row)
    raise KeyError(case_id)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    prototypes_root = Path(__file__).resolve().parents[2]
    validator = root / "tools" / "validate_recovery_adapter.py"
    fixtures_path = root / "fixtures" / "recovery-adapter-cases.jsonl"

    proc = subprocess.run(
        [sys.executable, str(validator), "--cases", str(fixtures_path)],
        text=True,
        capture_output=True,
    )
    print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    require(proc.returncode == 0, "authored Recovery Adapter corpus does not match validator")

    rows = load_jsonl(fixtures_path)
    require(bool(rows), "fixture corpus must not be empty")
    ids = [row.get("case_id") for row in rows]
    require(len(ids) == len(set(ids)), "fixture case IDs must be unique")
    required_regressions = {
        "RA-001",  # viable path before restore
        "RA-002",  # same-fate rescue defect
        "RA-003",  # independence uncertainty
        "RA-005",  # required drill absent
        "RA-007",  # world action after restore
        "RA-009",  # authority denied after restore
        "RA-010",  # clean resume
        "RA-011",  # low-cost local false-BLOCK control
        "RA-012",  # evidence-free verified claim invalid
        "RA-013",  # restore success without post-restore summary invalid
    }
    require(required_regressions <= set(ids), "targeted recovery regression fixture removed")

    # Known same-fate recovery must not become usable merely because a checkpoint
    # and healthy-time read both exist.
    same_fate = by_id(rows, "RA-002")["case"]
    action, blockers = evaluate(same_fate)
    require(action == "REPAIR_RECOVERY_PATH", f"same-fate recovery escaped: {action} {blockers}")
    require("REQUIRED_RESCUE_SHARES_FATE" in blockers, "same-fate blocker missing")
    print("PASS: checkpoint + healthy reachability does not prove independent rescue")

    # False-BLOCK: cheap local cache restoration does not need a ceremonial
    # out-of-band Rescue Plane or mandatory drill.
    local = by_id(rows, "RA-011")["case"]
    action, blockers = evaluate(local)
    require(action == "RESUME", f"local recovery false-BLOCK: {action} {blockers}")
    print("PASS: bounded local recovery can resume without universal rescue-plane ceremony")

    effect = load_module(
        "effect_lifecycle_for_recovery",
        prototypes_root / "effect-lifecycle" / "tools" / "validate_effect_lifecycle.py",
    )
    authority = load_module(
        "authority_lease_for_recovery",
        prototypes_root / "authority-lease" / "tools" / "validate_authority_lease.py",
    )

    # Build a world-state case where an external payment already committed, but
    # the restored local workflow still has an unsettled commitment. Effect
    # Lifecycle says the effect should NOT be realized again; settlement work is
    # still required before ordinary resume.
    effect_record = {
        "decision_effect_id": "E1",
        "effects": [
            {
                "effect_id": "E1",
                "effect_class": "EXTERNAL_IRREVERSIBLE",
                "target": "account:ops",
                "operation": "PAY",
                "material_parameters_digest": "sha256:invoice42",
                "authority_ref": "G1",
                "idempotency_strategy": "NATIVE_KEY",
            }
        ],
        "attempts": [
            {
                "attempt_id": "A1",
                "effect_id": "E1",
                "kind": "REALIZE",
                "material_parameters_digest": "sha256:invoice42",
                "outcome": "ACKNOWLEDGED",
                "sequence": 1,
            }
        ],
        "receipts": [
            {
                "receipt_id": "R1",
                "effect_id": "E1",
                "attempt_id": "A1",
                "observed_status": "COMMITTED",
                "evidence_refs": ["provider:receipt:1"],
                "sequence": 2,
            }
        ],
        "commitments": [
            {
                "commitment_id": "C1",
                "effect_ids": ["E1"],
                "status": "ASSIGNED",
                "executor_assignments": [{"executor": "agent:A", "status": "ACTIVE"}],
                "settlement_receipt_refs": [],
            }
        ],
    }
    effect_errors = effect.validate_record(effect_record)
    require(not effect_errors, f"effect composition record invalid: {effect_errors}")
    require(
        effect.next_action(effect_record, effect_errors) == "SETTLE_COMMITMENT",
        "committed effect with open commitment did not demand settlement",
    )

    authority_case = {
        "query": {
            "query_id": "Q-recovery",
            "authority_required": True,
            "authority_ref": "G1",
            "grantee": "agent:A",
            "action": "PAY",
            "protected_subject_ref": "account:ops",
            "task_scope": "invoice:42",
            "host": "host:H1",
            "grantee_epoch": "epoch:E1",
            "eval_time": "2026-08-26",
        },
        "grants": [
            {
                "grant_id": "G1",
                "source_ref": "mandate:user:1",
                "grantee": "agent:A",
                "allowed_actions": ["PAY"],
                "protected_subject_refs": ["account:ops"],
                "task_scopes": ["invoice:42"],
                "host_scopes": ["host:H1"],
                "grantee_epoch_scopes": ["epoch:E1"],
                "valid_from": "2026-08-01",
                "expires_at": "2026-08-31",
                "status": "ACTIVE",
            }
        ],
    }
    authority_resolution, _, authority_diag = authority.resolve_case(authority_case)
    require(authority_resolution == "AUTHORIZED", f"authority baseline failed: {authority_diag}")

    restored = by_id(rows, "RA-010")["case"]
    restored["post_restore"]["world_state"] = "ACTION_REQUIRED"
    restored["post_restore"]["world_resolution_refs"] = ["effect:E1:SETTLE_COMMITMENT"]
    restored["post_restore"]["authority_state"] = authority_resolution
    restored["post_restore"]["authority_resolution_refs"] = ["authority:G1:2026-08-26"]
    action, blockers = evaluate(restored)
    require(action == "DO_NOT_RESUME", f"restore resumed before world settlement: {action} {blockers}")
    require("WORLD_RECONCILIATION_ACTION_REQUIRED" in blockers, "world reconciliation blocker missing")
    print("PASS: restore success does not replay through a committed-but-unsettled external effect")

    # Once the commitment is settled against the represented receipt, Effect
    # Lifecycle reports no more effect work. With still-valid authority, the
    # same restored state may become resumable.
    settled_effect = copy.deepcopy(effect_record)
    settled_effect["commitments"][0]["status"] = "SETTLED"
    settled_effect["commitments"][0]["executor_assignments"][0]["status"] = "SETTLED"
    settled_effect["commitments"][0]["settlement_receipt_refs"] = ["R1"]
    settled_errors = effect.validate_record(settled_effect)
    require(not settled_errors, f"settled effect invalid: {settled_errors}")
    require(effect.next_action(settled_effect, settled_errors) == "NO_EFFECT_NEEDED", "settled effect not cleared")

    cleared = copy.deepcopy(restored)
    cleared["post_restore"]["world_state"] = "CLEARED"
    cleared["post_restore"]["world_resolution_refs"] = ["effect:E1:NO_EFFECT_NEEDED"]
    action, blockers = evaluate(cleared)
    require(action == "RESUME", f"cleared world + authorized grant did not resume: {action} {blockers}")
    print("PASS: settled world + current authority permits bounded resume")

    # Same recovered local state, later evaluation time: Authority Lease expires.
    # Effect settlement remains clear, but authority cannot be resurrected from
    # checkpoint memory, so Recovery Adapter must stop resume.
    expired_authority = copy.deepcopy(authority_case)
    expired_authority["query"]["eval_time"] = "2026-09-01"
    expired_resolution, _, expired_diag = authority.resolve_case(expired_authority)
    require(expired_resolution == "NOT_AUTHORIZED", f"expired authority escaped: {expired_diag}")

    authority_blocked = copy.deepcopy(cleared)
    authority_blocked["post_restore"]["authority_state"] = expired_resolution
    authority_blocked["post_restore"]["authority_resolution_refs"] = ["authority:G1:2026-09-01"]
    action, blockers = evaluate(authority_blocked)
    require(action == "DO_NOT_RESUME", f"restore revived expired authority: {action} {blockers}")
    require("AUTHORITY_NOT_AUTHORIZED" in blockers, "post-restore authority blocker missing")
    print("PASS: restore cannot revive authority that expired outside the checkpoint")

    print("PASS: recovery-adapter portable adversarial selftest")
    print("verification_scope=REPRESENTED_RECOVERY_RULES_PLUS_EFFECT_AND_AUTHORITY_COMPOSITION_ONLY")
    print("external_recovery_truth=UNPROVEN")
    print("external_effect_truth=INHERITS_EFFECT_LIFECYCLE_BOUNDARY")
    print("external_authority_truth=INHERITS_AUTHORITY_LEASE_BOUNDARY")
    print("fixture_cardinality=OPEN_WITH_TARGETED_REGRESSION_DEPENDENCIES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

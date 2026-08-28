#!/usr/bin/env python3
"""Portable adversarial selftest for Authority Grant / Lease prototype."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import subprocess
import sys

from validate_authority_lease import load_jsonl, resolve_case


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def by_id(rows: list[dict], case_id: str) -> dict:
    for row in rows:
        if row.get("case_id") == case_id:
            return copy.deepcopy(row)
    raise KeyError(case_id)


def load_effect_validator(prototypes_root: Path):
    path = prototypes_root / "effect-lifecycle" / "tools" / "validate_effect_lifecycle.py"
    spec = importlib.util.spec_from_file_location("effect_lifecycle_for_authority_composition", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load Effect Lifecycle validator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    prototypes_root = Path(__file__).resolve().parents[2]
    validator = root / "tools" / "validate_authority_lease.py"
    fixtures_path = root / "fixtures" / "authority-lease-cases.jsonl"

    proc = subprocess.run(
        [sys.executable, str(validator), "--cases", str(fixtures_path)],
        text=True,
        capture_output=True,
    )
    print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    require(proc.returncode == 0, "authored Authority Lease fixture corpus does not match validator")

    rows = load_jsonl(fixtures_path)
    require(bool(rows), "fixture corpus must not be empty")
    ids = [row.get("case_id") for row in rows]
    require(len(ids) == len(set(ids)), "fixture case IDs must be unique")

    # These are regression dependencies, not a total-corpus cardinality claim.
    required_regressions = {
        "AL-001",  # valid authority
        "AL-002",  # expiry
        "AL-003",  # revocation
        "AL-008",  # copied epoch does not inherit scope
        "AL-010",  # credential identity binding
        "AL-011",  # harmless local false-BLOCK control
        "AL-012",  # unresolved grant
        "AL-013",  # renewal does not resurrect old grant
        "AL-014",  # explicit new grant can authorize
        "AL-015",  # explicit broad Host/epoch scope
        "AL-016",  # structurally inconsistent authority record
    }
    require(required_regressions <= set(ids), "targeted authority regression fixture removed")

    # Mutation 1: a formerly valid grant expires; represented effect shape alone
    # must not keep execution authorized.
    valid = by_id(rows, "AL-001")["case"]
    expired = copy.deepcopy(valid)
    expired["query"]["eval_time"] = "2026-09-01"
    resolution, posture, diagnostics = resolve_case(expired)
    require(resolution == "NOT_AUTHORIZED", f"expiry mutation escaped: {resolution} {diagnostics}")
    require(posture == "DO_NOT_EXECUTE_UNDER_THIS_GRANT", "expired grant did not block use of that grant")
    print("PASS: expiry removes represented current authority")

    # Mutation 2: copying the authority bytes into a later epoch does not widen
    # an explicitly narrow epoch binding.
    copied_epoch = copy.deepcopy(valid)
    copied_epoch["query"]["grantee_epoch"] = "epoch:E2"
    resolution, _, diagnostics = resolve_case(copied_epoch)
    require(resolution == "NOT_AUTHORIZED", f"epoch-copy authority inflation: {resolution} {diagnostics}")
    print("PASS: copied/restored grant does not auto-authorize a new scoped epoch")

    # Missing epoch is uncertainty, not a fabricated denial, when the selected
    # grant actually depends on epoch scope.
    missing_scoped_epoch = copy.deepcopy(valid)
    missing_scoped_epoch["query"].pop("grantee_epoch")
    resolution, posture, diagnostics = resolve_case(missing_scoped_epoch)
    require(resolution == "UNRESOLVED", f"missing scoped epoch not preserved as uncertainty: {resolution} {diagnostics}")
    require(posture == "NARROW_OR_RESOLVE_AUTHORITY", "missing scoped epoch posture wrong")
    print("PASS: missing decision-relevant epoch remains UNRESOLVED")

    # Counter-control: a Host is not forced to manufacture epoch machinery when
    # the real grant explicitly spans epochs.
    broad_epoch = by_id(rows, "AL-015")["case"]
    broad_epoch["query"].pop("grantee_epoch")
    resolution, posture, diagnostics = resolve_case(broad_epoch)
    require(resolution == "AUTHORIZED", f"universal epoch false-BLOCK: {resolution} {diagnostics}")
    require(posture == "AUTHORITY_PRECONDITION_SATISFIED", "broad-epoch posture wrong")
    print("PASS: explicit cross-epoch grant does not require a Host epoch mechanism")

    # False-BLOCK control: harmless local synchronization is allowed to declare
    # that no external Authority Lease is required. The validator does not mint
    # or demand a grant merely because a state change exists.
    local = by_id(rows, "AL-011")["case"]
    resolution, posture, diagnostics = resolve_case(local)
    require(resolution == "NOT_REQUIRED", f"local false-BLOCK: {resolution} {diagnostics}")
    require(posture == "PROCEED_WITHOUT_AUTHORITY_LEASE", "local false-BLOCK posture wrong")
    print("PASS: non-authority-bearing local action does not require ceremonial lease")

    # Renewal control: the existence of a successor grant does not make the old
    # referenced grant current; explicitly selecting the new grant can authorize.
    old = by_id(rows, "AL-013")["case"]
    new = by_id(rows, "AL-014")["case"]
    old_resolution, _, _ = resolve_case(old)
    new_resolution, _, _ = resolve_case(new)
    require(old_resolution == "NOT_AUTHORIZED", "successor grant resurrected old authority")
    require(new_resolution == "AUTHORIZED", "explicit renewed grant did not authorize")
    print("PASS: renewal uses new grant identity without latest-grant magic")

    # Cross-organ seam: Effect Lifecycle can be structurally valid while the
    # authority precondition later becomes invalid. This demonstrates that an
    # authority_ref is a dependency, not proof of authority.
    effect = load_effect_validator(prototypes_root)
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
        "attempts": [],
        "receipts": [],
        "commitments": [],
    }
    effect_errors = effect.validate_record(effect_record)
    require(not effect_errors, f"Effect Lifecycle baseline unexpectedly invalid: {effect_errors}")
    require(effect.next_action(effect_record, effect_errors) == "REALIZE_NEW_INTENT", "Effect Lifecycle baseline action changed")

    authorized_resolution, _, _ = resolve_case(valid)
    require(authorized_resolution == "AUTHORIZED", "composition baseline authority not authorized")

    expired_resolution, _, _ = resolve_case(expired)
    require(expired_resolution == "NOT_AUTHORIZED", "composition expiry authority unexpectedly authorized")
    effect_errors_after_expiry = effect.validate_record(effect_record)
    require(not effect_errors_after_expiry, "Effect Lifecycle should remain structurally valid after external authority time changes")
    print("PASS: effect consistency + authority_ref does not imply current authority")

    print("PASS: authority-lease portable adversarial selftest")
    print("verification_scope=REPRESENTED_AUTHORITY_RULES_PLUS_EFFECT_LIFECYCLE_COMPOSITION_SEAM_ONLY")
    print("external_mandate_authenticity=UNPROVEN")
    print("credential_external_validity=UNPROVEN")
    print("authority_required_classification=CALLER_TRUST_BOUNDARY")
    print("epoch_mechanism=OPTIONAL_UNLESS_SELECTED_GRANT_IS_EPOCH_SCOPED")
    print("fixture_cardinality=OPEN_WITH_TARGETED_REGRESSION_DEPENDENCIES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

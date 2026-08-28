#!/usr/bin/env python3
"""Validate the research-only ENA Evidence Envelope prototype.

This validates represented consistency and a few derived claim-strength rules.
It does NOT prove evidence truth, witness independence, transfer validity,
projection completeness, or real activation/effect occurrence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path}: expected JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise SystemExit(f"{path}:{lineno}: expected object")
        rows.append(value)
    return rows


def require_string(value: Any, label: str, errors: list[str]) -> bool:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} must be a non-empty string")
        return False
    return True


def require_string_list(value: Any, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
        errors.append(f"{label} must be array[non-empty string]")
        return []
    return value


def validate_envelope(envelope: dict[str, Any], contract: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []

    require_string(envelope.get("envelope_id"), "envelope_id", errors)

    subject = envelope.get("subject")
    if not isinstance(subject, dict):
        errors.append("subject must be an object")
        subject = {}
    require_string(subject.get("subject_ref"), "subject.subject_ref", errors)
    require_string(subject.get("subject_type"), "subject.subject_type", errors)
    subject_failure_domain = subject.get("failure_domain_ref")
    if subject_failure_domain is not None:
        require_string(subject_failure_domain, "subject.failure_domain_ref", errors)

    claim = envelope.get("claim")
    if not isinstance(claim, dict):
        errors.append("claim must be an object")
        claim = {}
    require_string(claim.get("claim_ref"), "claim.claim_ref", errors)
    require_string(claim.get("claim_type"), "claim.claim_type", errors)

    evidence = envelope.get("evidence")
    if not isinstance(evidence, dict):
        errors.append("evidence must be an object")
        evidence = {}
    evidence_refs = require_string_list(evidence.get("evidence_refs", []), "evidence.evidence_refs", errors)
    observation_refs = require_string_list(
        evidence.get("observation_or_activity_refs", []),
        "evidence.observation_or_activity_refs",
        errors,
    )
    if not evidence_refs and not observation_refs:
        errors.append("evidence must contain at least one evidence or observation/activity ref")

    support = envelope.get("support")
    if not isinstance(support, dict):
        errors.append("support must be an object")
        support = {}
    support_basis = support.get("basis")
    if support_basis not in set(contract["support_basis"]):
        errors.append(f"support.basis invalid: {support_basis!r}")
    support_status = support.get("status", "UNKNOWN")
    if support_status not in set(contract["support_status"]):
        errors.append(f"support.status invalid: {support_status!r}")
    require_string_list(support.get("limitations", []), "support.limitations", errors)

    dependency_map_ref = support.get("dependency_map_ref")
    if dependency_map_ref is not None:
        require_string(dependency_map_ref, "support.dependency_map_ref", errors)
    if support_basis == "CORROBORATION" and not isinstance(dependency_map_ref, str):
        errors.append("CORROBORATION requires support.dependency_map_ref")

    applicability = envelope.get("applicability")
    effective_applicability = "UNKNOWN"
    changed_dimensions: list[str] = []
    transfer_basis_refs: list[str] = []
    if applicability is not None:
        if not isinstance(applicability, dict):
            errors.append("applicability must be an object when present")
            applicability = {}
        status = applicability.get("status")
        if status not in set(contract["applicability_status"]):
            errors.append(f"applicability.status invalid: {status!r}")
        else:
            effective_applicability = status
        evaluated = applicability.get("evaluated_dimensions", {})
        if not isinstance(evaluated, dict):
            errors.append("applicability.evaluated_dimensions must be an object")
        changed_dimensions = require_string_list(
            applicability.get("changed_dimensions", []),
            "applicability.changed_dimensions",
            errors,
        )
        transfer_basis_refs = require_string_list(
            applicability.get("transfer_or_invariance_basis_refs", []),
            "applicability.transfer_or_invariance_basis_refs",
            errors,
        )
        if status == "EXPLICIT_MATCH" and changed_dimensions:
            errors.append("EXPLICIT_MATCH cannot coexist with represented changed_dimensions")
        if status == "TRANSFER_WITH_BASIS" and not transfer_basis_refs:
            errors.append("TRANSFER_WITH_BASIS requires transfer_or_invariance_basis_refs")
        if support_status == "EXPIRED" and status in {"EXPLICIT_MATCH", "TRANSFER_WITH_BASIS"}:
            errors.append("EXPIRED support cannot silently retain current EXPLICIT_MATCH/TRANSFER_WITH_BASIS")

    provenance = envelope.get("provenance")
    if provenance is not None:
        if not isinstance(provenance, dict):
            errors.append("provenance must be an object when present")
        else:
            for key in ("producer_or_actor_ref", "activity_or_transformation_ref"):
                if provenance.get(key) is not None:
                    require_string(provenance.get(key), f"provenance.{key}", errors)
            require_string_list(provenance.get("source_refs", []), "provenance.source_refs", errors)
            access = provenance.get("access", "UNKNOWN")
            if access not in set(contract["provenance_access"]):
                errors.append(f"provenance.access invalid: {access!r}")

    witness = envelope.get("witness")
    if witness is not None:
        if not isinstance(witness, dict):
            errors.append("witness must be an object when present")
        else:
            witness_ref = witness.get("witness_ref")
            if witness_ref is not None:
                require_string(witness_ref, "witness.witness_ref", errors)
            witness_domain = witness.get("failure_domain_ref")
            if witness_domain is not None:
                require_string(witness_domain, "witness.failure_domain_ref", errors)
            independence = witness.get("independence_claim", "UNKNOWN")
            if independence not in set(contract["witness_independence"]):
                errors.append(f"witness.independence_claim invalid: {independence!r}")
            survivability = witness.get("survivability", "UNKNOWN")
            if survivability not in set(contract["witness_survivability"]):
                errors.append(f"witness.survivability invalid: {survivability!r}")
            if subject_failure_domain and witness_domain == subject_failure_domain:
                if independence == "CLAIMED":
                    errors.append("same represented failure domain cannot claim independent witness")
                if survivability == "EXTERNAL_DOMAIN":
                    errors.append("same represented failure domain cannot claim EXTERNAL_DOMAIN survivability")

    completeness = envelope.get("completeness")
    if completeness is not None:
        if not isinstance(completeness, dict):
            errors.append("completeness must be an object when present")
        else:
            if "complete" in completeness:
                errors.append("universal completeness.complete is not supported; use dimension-scoped claims")
            require_string_list(
                completeness.get("claimed_complete_dimensions", []),
                "completeness.claimed_complete_dimensions",
                errors,
            )
            require_string_list(
                completeness.get("known_missing_or_unknown", []),
                "completeness.known_missing_or_unknown",
                errors,
            )

    projection = envelope.get("projection")
    if projection is not None:
        if not isinstance(projection, dict):
            errors.append("projection must be an object when present")
        else:
            require_string_list(projection.get("source_subject_refs", []), "projection.source_subject_refs", errors)
            material_omissions = require_string_list(
                projection.get("material_omissions", []),
                "projection.material_omissions",
                errors,
            )
            preservation_basis_refs = require_string_list(
                projection.get("preservation_basis_refs", []),
                "projection.preservation_basis_refs",
                errors,
            )
            if (
                material_omissions
                and not preservation_basis_refs
                and effective_applicability in {"EXPLICIT_MATCH", "TRANSFER_WITH_BASIS"}
            ):
                errors.append(
                    "material projection omissions without preservation basis cannot silently retain strong applicability"
                )

    activation = envelope.get("activation")
    if activation is not None:
        if not isinstance(activation, dict):
            errors.append("activation must be an object when present")
        else:
            level = activation.get("claimed_level")
            if level not in set(contract["activation_levels"]):
                errors.append(f"activation.claimed_level invalid: {level!r}")
            else:
                required = contract["derived_semantics"]["activation"][level]
                for key in required:
                    if not isinstance(activation.get(key), str) or not activation.get(key):
                        errors.append(f"activation level {level} requires {key}")

    derived = {
        "effective_applicability": effective_applicability,
        "support_status": support_status,
        "represented_valid": not errors,
    }
    return errors, derived


def main() -> int:
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--contract", type=Path, default=root / "evidence-envelope.v0.1.json")
    parser.add_argument("--fixtures", type=Path, default=root / "fixtures" / "evidence-envelope-cases.jsonl")
    parser.add_argument("--show-all", action="store_true")
    args = parser.parse_args()

    contract = load_json(args.contract)
    fixtures = load_jsonl(args.fixtures)

    seen: set[str] = set()
    mismatches: list[str] = []
    expected_valid_count = 0
    expected_invalid_count = 0

    for row in fixtures:
        case_id = row.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise SystemExit("every fixture requires non-empty string case_id")
        if case_id in seen:
            raise SystemExit(f"duplicate case_id: {case_id}")
        seen.add(case_id)

        expected_valid = row.get("expected_valid")
        if not isinstance(expected_valid, bool):
            raise SystemExit(f"{case_id}: expected_valid must be boolean")
        expected_valid_count += int(expected_valid)
        expected_invalid_count += int(not expected_valid)

        envelope = row.get("envelope")
        if not isinstance(envelope, dict):
            raise SystemExit(f"{case_id}: envelope must be object")

        errors, derived = validate_envelope(envelope, contract)
        actual_valid = not errors
        expected_applicability = row.get("expected_effective_applicability")

        if actual_valid != expected_valid:
            mismatches.append(
                f"{case_id}: validity expected={expected_valid} actual={actual_valid} errors={errors}"
            )
        if expected_applicability != derived["effective_applicability"]:
            mismatches.append(
                f"{case_id}: applicability expected={expected_applicability!r} actual={derived['effective_applicability']!r}"
            )

        if args.show_all or actual_valid != expected_valid:
            print(
                f"{case_id}: expected_valid={expected_valid} actual_valid={actual_valid} "
                f"effective_applicability={derived['effective_applicability']} errors={len(errors)}"
            )
            for error in errors:
                print(f"  - {error}")

    print(
        "fixture summary:",
        f"total={len(fixtures)}",
        f"expected_valid={expected_valid_count}",
        f"expected_invalid={expected_invalid_count}",
        f"mismatches={len(mismatches)}",
    )

    if mismatches:
        print("FAIL: evidence-envelope fixture mismatch")
        for mismatch in mismatches:
            print(f"- {mismatch}")
        return 1

    print("PASS: evidence-envelope represented-consistency fixtures")
    print("verification_scope=REPRESENTED_CONSISTENCY_AND_DERIVED_CLAIM_STRENGTH_ONLY")
    print("external_truth=UNPROVEN")
    print("current_change=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

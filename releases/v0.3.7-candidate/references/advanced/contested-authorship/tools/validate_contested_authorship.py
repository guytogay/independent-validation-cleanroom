#!/usr/bin/env python3
"""Validate research-only Contested Authorship fixtures.

Checks represented durable-self authorship consistency only. It does not prove
sincerity, moral authorship, beneficial change, consent, or external authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path}: expected object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise SystemExit(f"{path}:{lineno}: expected object")
        rows.append(value)
    return rows


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def string_list(value: Any, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not all(nonempty_string(v) for v in value):
        errors.append(f"{label} must be array[non-empty string]")
        return []
    return value


def validate_record(record: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    scope_status = record.get("scope_status")
    if scope_status not in set(contract["scope_status"]):
        return [f"scope_status invalid: {scope_status!r}"]

    if scope_status == "OUT_OF_SCOPE":
        update_kind = record.get("update_kind")
        if update_kind not in set(contract["out_of_scope_update_kind"]):
            errors.append(f"OUT_OF_SCOPE update_kind invalid: {update_kind!r}")
        if not nonempty_string(record.get("reason")):
            errors.append("OUT_OF_SCOPE requires a reason")
        forbidden = {
            "change_id", "subject", "before_ref", "proposal", "authorship",
            "readback", "endorsement", "integration", "authority", "conflict",
        }
        present = sorted(forbidden & set(record))
        if present:
            errors.append(f"OUT_OF_SCOPE record must not masquerade as durable self-change: {present}")
        return errors

    # IN_SCOPE
    if not nonempty_string(record.get("change_id")):
        errors.append("IN_SCOPE requires change_id")

    subject = record.get("subject")
    if not isinstance(subject, dict):
        errors.append("subject must be object")
        subject = {}
    for key in ("trajectory_ref", "self_surface", "target_ref"):
        if not nonempty_string(subject.get(key)):
            errors.append(f"subject.{key} must be non-empty string")
    if subject.get("epoch_ref") is not None and not nonempty_string(subject.get("epoch_ref")):
        errors.append("subject.epoch_ref must be non-empty string when present")
    surface = subject.get("self_surface")
    if surface not in set(contract["self_surfaces"]):
        errors.append(f"subject.self_surface invalid: {surface!r}")

    before_ref = record.get("before_ref")
    if not isinstance(before_ref, dict) or not nonempty_string(before_ref.get("version_or_digest")):
        errors.append("durable self-change requires before_ref.version_or_digest")

    proposal = record.get("proposal")
    if not isinstance(proposal, dict):
        errors.append("proposal must be object")
        proposal = {}
    origin = proposal.get("origin_class")
    if origin not in set(contract["origin_class"]):
        errors.append(f"proposal.origin_class invalid: {origin!r}")
    for key in ("proposer_ref", "proposed_diff_ref"):
        if not nonempty_string(proposal.get(key)):
            errors.append(f"proposal.{key} must be non-empty string")
    consequence = proposal.get("consequence_class")
    if consequence not in set(contract["consequence_class"]):
        errors.append(f"proposal.consequence_class invalid: {consequence!r}")
    if "evidence_refs" in proposal:
        string_list(proposal.get("evidence_refs"), "proposal.evidence_refs", errors)

    authorship = record.get("authorship")
    if not isinstance(authorship, dict):
        errors.append("authorship must be object")
        authorship = {}
    claim = authorship.get("claim")
    if claim not in set(contract["authorship_claim"]):
        errors.append(f"authorship.claim invalid: {claim!r}")
    if "causal_sources" in authorship:
        string_list(authorship.get("causal_sources"), "authorship.causal_sources", errors)
    if origin in {"OPERATOR", "USER", "PEER", "IMPORTED"} and claim == "SELF_AUTHORED":
        errors.append(f"origin {origin} cannot be laundered as SELF_AUTHORED")
    if origin == "MIXED" and claim != "MIXED":
        errors.append("MIXED origin requires authorship.claim=MIXED")

    readback = record.get("readback")
    if not isinstance(readback, dict):
        errors.append("readback must be object")
        readback = {}
    readback_status = readback.get("status")
    if readback_status not in set(contract["readback_status"]):
        errors.append(f"readback.status invalid: {readback_status!r}")
    if readback.get("actor_ref") is not None and not nonempty_string(readback.get("actor_ref")):
        errors.append("readback.actor_ref must be non-empty string when present")

    endorsement = record.get("endorsement")
    if not isinstance(endorsement, dict):
        errors.append("endorsement must be object")
        endorsement = {}
    endorsement_status = endorsement.get("status")
    if endorsement_status not in set(contract["endorsement_status"]):
        errors.append(f"endorsement.status invalid: {endorsement_status!r}")

    integration = record.get("integration")
    if not isinstance(integration, dict):
        errors.append("integration must be object")
        integration = {}
    integration_status = integration.get("status")
    if integration_status not in set(contract["integration_status"]):
        errors.append(f"integration.status invalid: {integration_status!r}")
    if integration_status == "INTEGRATED" and not nonempty_string(integration.get("integrated_version_or_digest")):
        errors.append("INTEGRATED requires integrated_version_or_digest")

    material = consequence == "MATERIAL" or surface in set(contract["material_surfaces"])
    if integration_status == "INTEGRATED" and material:
        if readback_status not in {"READ", "ACCEPTED"}:
            errors.append("material INTEGRATED self-change requires semantic readback (READ or ACCEPTED)")
        if not nonempty_string(readback.get("actor_ref")):
            errors.append("material INTEGRATED self-change requires readback.actor_ref")

    if (
        integration_status == "INTEGRATED"
        and material
        and origin in {"OPERATOR", "USER", "PEER", "IMPORTED"}
        and endorsement_status != "ACCEPTED"
    ):
        errors.append("material external/imported-origin integration requires explicit current endorsement")

    authority = record.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority must be object")
        authority = {}
    effect = authority.get("effect")
    resolution = authority.get("resolution")
    if effect not in set(contract["authority_effect"]):
        errors.append(f"authority.effect invalid: {effect!r}")
    if resolution not in set(contract["authority_resolution"]):
        errors.append(f"authority.resolution invalid: {resolution!r}")
    external_authority_ref = authority.get("external_authority_ref")
    if external_authority_ref is not None and not nonempty_string(external_authority_ref):
        errors.append("authority.external_authority_ref must be non-empty string when present")
    if effect == "EXTERNAL_AUTHORITY_REQUIRED" and resolution == "RESOLVED" and not nonempty_string(external_authority_ref):
        errors.append("external authority cannot be RESOLVED without external_authority_ref")
    if effect == "NONE" and resolution != "NOT_APPLICABLE":
        errors.append("authority.effect=NONE requires resolution=NOT_APPLICABLE")
    if effect != "EXTERNAL_AUTHORITY_REQUIRED" and external_authority_ref is not None:
        errors.append("external_authority_ref only applies to EXTERNAL_AUTHORITY_REQUIRED")

    conflict = record.get("conflict")
    if not isinstance(conflict, dict):
        errors.append("conflict must be object")
        conflict = {}
    conflict_material = conflict.get("material")
    if not isinstance(conflict_material, bool):
        errors.append("conflict.material must be boolean")
        conflict_material = False
    competing = string_list(conflict.get("competing_proposal_refs", []), "conflict.competing_proposal_refs", errors)
    disposition = conflict.get("disposition")
    if disposition not in set(contract["conflict_disposition"]):
        errors.append(f"conflict.disposition invalid: {disposition!r}")
    if not conflict_material and competing:
        errors.append("non-material conflict must not carry competing proposal refs")
    if conflict_material and not competing:
        errors.append("material conflict requires competing_proposal_refs")
    if integration_status == "INTEGRATED" and conflict_material:
        if disposition in {"NONE", "UNKNOWN", "DISPUTED"}:
            errors.append("material conflict cannot disappear through INTEGRATED last-write-wins")
        if not nonempty_string(conflict.get("resolution_ref")):
            errors.append("material conflict INTEGRATED requires conflict.resolution_ref")

    history = record.get("history")
    if history is not None:
        if not isinstance(history, dict):
            errors.append("history must be object")
        else:
            for key in ("revises_change_ref", "rollback_or_revision_ref"):
                if history.get(key) is not None and not nonempty_string(history.get(key)):
                    errors.append(f"history.{key} must be non-empty string when present")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--contract", type=Path, default=root / "contested-authorship.v0.1.json")
    parser.add_argument("--fixtures", type=Path, default=root / "fixtures" / "contested-authorship-cases.jsonl")
    parser.add_argument("--show-all", action="store_true")
    args = parser.parse_args()

    contract = load_json(args.contract)
    fixtures = load_jsonl(args.fixtures)
    seen: set[str] = set()
    mismatches: list[str] = []
    out_of_scope = 0

    for row in fixtures:
        case_id = row.get("case_id")
        if not nonempty_string(case_id):
            raise SystemExit("every fixture requires case_id")
        if case_id in seen:
            raise SystemExit(f"duplicate case_id: {case_id}")
        seen.add(case_id)
        expected_valid = row.get("expected_valid")
        if not isinstance(expected_valid, bool):
            raise SystemExit(f"{case_id}: expected_valid must be boolean")
        record = row.get("record")
        if not isinstance(record, dict):
            raise SystemExit(f"{case_id}: record must be object")
        if record.get("scope_status") == "OUT_OF_SCOPE":
            out_of_scope += 1

        errors = validate_record(record, contract)
        actual_valid = not errors
        if actual_valid != expected_valid:
            mismatches.append(
                f"{case_id}: expected={expected_valid} actual={actual_valid} errors={errors}"
            )
        if args.show_all or actual_valid != expected_valid:
            print(f"{case_id}: expected_valid={expected_valid} actual_valid={actual_valid} errors={len(errors)}")
            for error in errors:
                print(f"  - {error}")

    print(
        "fixture summary:",
        f"total={len(fixtures)}",
        f"out_of_scope_cases={out_of_scope}",
        f"mismatches={len(mismatches)}",
    )
    if mismatches:
        print("FAIL: contested-authorship fixture mismatch")
        for mismatch in mismatches:
            print(f"- {mismatch}")
        return 1

    print("PASS: contested-authorship represented-consistency fixtures")
    print("verification_scope=DURABLE_SELF_CHANGE_PROVENANCE_READBACK_CONFLICT_AUTHORITY_ONLY")
    print("sincere_authorship=UNPROVEN")
    print("external_authority=NOT_MINTED")
    print("current_change=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

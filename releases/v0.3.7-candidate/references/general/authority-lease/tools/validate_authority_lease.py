#!/usr/bin/env python3
"""Validate/resolve the Authority Grant / Lease research prototype.

Verification scope: represented grant/query structure plus deterministic
scope/time resolution. This tool does not authenticate mandate sources,
credential validity, or the caller's authority_required classification.
"""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
from typing import Any

RESOLUTIONS = {
    "NOT_REQUIRED",
    "AUTHORIZED",
    "NOT_AUTHORIZED",
    "UNRESOLVED",
    "INVALID_RECORD",
}
POSTURES = {
    "NOT_REQUIRED": "PROCEED_WITHOUT_AUTHORITY_LEASE",
    "AUTHORIZED": "AUTHORITY_PRECONDITION_SATISFIED",
    "NOT_AUTHORIZED": "DO_NOT_EXECUTE_UNDER_THIS_GRANT",
    "UNRESOLVED": "NARROW_OR_RESOLVE_AUTHORITY",
    "INVALID_RECORD": "REJECT_INCONSISTENT_AUTHORITY_RECORD",
}
GRANT_STATUSES = {"ACTIVE", "REVOKED"}
SCOPE_FIELDS = (
    "allowed_actions",
    "protected_subject_refs",
    "task_scopes",
    "host_scopes",
    "grantee_epoch_scopes",
)


def parse_date(value: Any) -> date | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


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


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _valid_scope_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(_nonempty_string(item) for item in value)
        and len(value) == len(set(value))
    )


def validate_grant(grant: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(grant, dict):
        return ["grant must be object"]

    for field in ("grant_id", "source_ref", "grantee"):
        if not _nonempty_string(grant.get(field)):
            errors.append(f"{field} required")

    for field in SCOPE_FIELDS:
        if not _valid_scope_list(grant.get(field)):
            errors.append(f"{field} must be a non-empty unique string array")

    status = grant.get("status")
    if status not in GRANT_STATUSES:
        errors.append("invalid status")

    valid_from = parse_date(grant.get("valid_from"))
    expires_at = parse_date(grant.get("expires_at"))
    if valid_from is None:
        errors.append("valid_from must be ISO date")
    if expires_at is None:
        errors.append("expires_at must be ISO date")
    if valid_from is not None and expires_at is not None and expires_at < valid_from:
        errors.append("expires_at precedes valid_from")

    revoked_at_raw = grant.get("revoked_at")
    revoked_at = parse_date(revoked_at_raw) if revoked_at_raw is not None else None
    if status == "ACTIVE" and revoked_at_raw is not None:
        errors.append("ACTIVE grant must not carry revoked_at")
    if status == "REVOKED" and revoked_at is None:
        errors.append("REVOKED grant requires valid revoked_at")

    supersedes = grant.get("supersedes_grant_ref")
    if supersedes is not None and not _nonempty_string(supersedes):
        errors.append("supersedes_grant_ref must be non-empty string when present")
    if supersedes is not None and supersedes == grant.get("grant_id"):
        errors.append("grant cannot supersede itself")

    credential_ref = grant.get("credential_ref")
    if credential_ref is not None and not _nonempty_string(credential_ref):
        errors.append("credential_ref must be non-empty string when present")

    return errors


def validate_query(query: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(query, dict):
        return ["query must be object"]

    for field in (
        "query_id",
        "grantee",
        "action",
        "protected_subject_ref",
        "task_scope",
        "host",
    ):
        if not _nonempty_string(query.get(field)):
            errors.append(f"{field} required")

    # Epoch is intentionally optional. A Host need not manufacture an epoch
    # mechanism merely to use a grant that explicitly spans epochs. If the
    # selected grant is epoch-scoped, absence is resolved later as UNRESOLVED.
    grantee_epoch = query.get("grantee_epoch")
    if grantee_epoch is not None and not _nonempty_string(grantee_epoch):
        errors.append("grantee_epoch must be non-empty string when present")

    if not isinstance(query.get("authority_required"), bool):
        errors.append("authority_required must be boolean")

    if parse_date(query.get("eval_time")) is None:
        errors.append("eval_time must be ISO date")

    if query.get("authority_required") is True and not _nonempty_string(query.get("authority_ref")):
        errors.append("authority_ref required when authority_required=true")

    credential_ref = query.get("credential_ref")
    if credential_ref is not None and not _nonempty_string(credential_ref):
        errors.append("credential_ref must be non-empty string when present")

    return errors


def _scope_allows(scope: list[str], value: str) -> bool:
    return "*" in scope or value in scope


def resolve_case(case: Any) -> tuple[str, str, list[str]]:
    """Return (resolution, execution_posture, diagnostic_codes)."""
    if not isinstance(case, dict):
        return ("INVALID_RECORD", POSTURES["INVALID_RECORD"], ["CASE_NOT_OBJECT"])

    query = case.get("query")
    grants = case.get("grants")
    q_errors = validate_query(query)
    if not isinstance(grants, list):
        return ("INVALID_RECORD", POSTURES["INVALID_RECORD"], q_errors + ["GRANTS_NOT_ARRAY"])
    if q_errors:
        return ("INVALID_RECORD", POSTURES["INVALID_RECORD"], q_errors)

    assert isinstance(query, dict)
    if query["authority_required"] is False:
        return ("NOT_REQUIRED", POSTURES["NOT_REQUIRED"], [])

    grant_by_id: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for index, grant in enumerate(grants):
        g_errors = validate_grant(grant)
        if g_errors:
            errors.extend(f"grant[{index}]: {error}" for error in g_errors)
            continue
        grant_id = grant["grant_id"]
        if grant_id in grant_by_id:
            errors.append(f"duplicate grant_id: {grant_id}")
            continue
        grant_by_id[grant_id] = grant

    # Supersession is lineage only. Missing predecessor may remain external
    # history; the resolver never uses supersession to choose authority.
    if errors:
        return ("INVALID_RECORD", POSTURES["INVALID_RECORD"], errors)

    authority_ref = query["authority_ref"]
    grant = grant_by_id.get(authority_ref)
    if grant is None:
        return ("UNRESOLVED", POSTURES["UNRESOLVED"], ["AUTHORITY_REF_UNRESOLVED"])

    eval_time = parse_date(query["eval_time"])
    valid_from = parse_date(grant["valid_from"])
    expires_at = parse_date(grant["expires_at"])
    assert eval_time is not None and valid_from is not None and expires_at is not None

    deny_reasons: list[str] = []
    unresolved_reasons: list[str] = []

    if eval_time < valid_from:
        deny_reasons.append("GRANT_NOT_YET_VALID")
    if eval_time > expires_at:
        deny_reasons.append("GRANT_EXPIRED")

    if grant["status"] == "REVOKED":
        revoked_at = parse_date(grant["revoked_at"])
        assert revoked_at is not None
        if revoked_at <= eval_time:
            deny_reasons.append("GRANT_REVOKED")

    if grant["grantee"] != query["grantee"]:
        deny_reasons.append("GRANTEE_MISMATCH")
    if not _scope_allows(grant["allowed_actions"], query["action"]):
        deny_reasons.append("ACTION_OUT_OF_SCOPE")
    if not _scope_allows(grant["protected_subject_refs"], query["protected_subject_ref"]):
        deny_reasons.append("PROTECTED_SUBJECT_OUT_OF_SCOPE")
    if not _scope_allows(grant["task_scopes"], query["task_scope"]):
        deny_reasons.append("TASK_OUT_OF_SCOPE")
    if not _scope_allows(grant["host_scopes"], query["host"]):
        deny_reasons.append("HOST_OUT_OF_SCOPE")

    epoch_scopes = grant["grantee_epoch_scopes"]
    query_epoch = query.get("grantee_epoch")
    if "*" not in epoch_scopes:
        if not _nonempty_string(query_epoch):
            unresolved_reasons.append("GRANTEE_EPOCH_REQUIRED_FOR_SCOPED_GRANT")
        elif query_epoch not in epoch_scopes:
            deny_reasons.append("GRANTEE_EPOCH_OUT_OF_SCOPE")

    bound_credential = grant.get("credential_ref")
    if bound_credential is not None and query.get("credential_ref") != bound_credential:
        deny_reasons.append("CREDENTIAL_BINDING_MISMATCH")

    # A known disqualifier is enough to deny use of this grant even if another
    # dimension is unresolved. Otherwise preserve uncertainty honestly.
    if deny_reasons:
        return ("NOT_AUTHORIZED", POSTURES["NOT_AUTHORIZED"], deny_reasons + unresolved_reasons)
    if unresolved_reasons:
        return ("UNRESOLVED", POSTURES["UNRESOLVED"], unresolved_reasons)
    return ("AUTHORIZED", POSTURES["AUTHORIZED"], [])


def main() -> int:
    parser = argparse.ArgumentParser()
    default_cases = Path(__file__).resolve().parents[1] / "fixtures" / "authority-lease-cases.jsonl"
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
        expected_posture = row.get("expected_execution_posture")
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
        print(f"FAIL: {len(failures)} authority-lease fixture mismatch(es)")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: all Authority Lease fixtures matched represented reference rules")
    print("verification_scope=REPRESENTED_GRANT_QUERY_TIME_AND_SCOPE_RESOLUTION_ONLY")
    print("external_mandate_authenticity=UNPROVEN")
    print("credential_external_validity=UNPROVEN")
    print("authority_required_classification=CALLER_TRUST_BOUNDARY")
    print("epoch_mechanism=OPTIONAL_UNLESS_SELECTED_GRANT_IS_EPOCH_SCOPED")
    print("fixture_cardinality=OPEN_WITH_TARGETED_REGRESSION_DEPENDENCIES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

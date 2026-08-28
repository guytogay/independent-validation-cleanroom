#!/usr/bin/env python3
"""Minimal ENA v0.3.7 candidate v2 evolution helper.

This tool deliberately does not recreate the legacy ena_evolve.py state
machine. It orchestrates the candidate-local v2 evolution-record semantics and
adds only the packet-v2 mechanics that the candidate package needs as a
practical path.

Boundaries:
- evolution-record semantic consistency is delegated to this candidate's
  validate_evolution_record_v2.py;
- packet-v2 validation is schema + canonical digest + represented source-history
  shape/snapshot consistency;
- imported source selection/evidence never becomes receiver-local selection;
- external authenticity, authority, effect settlement, and evidence truth are
  not established by this helper.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import FormatChecker
from jsonschema.validators import Draft202012Validator

PACKAGE = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = PACKAGE / "templates" / "evolution-record.v2.json"
PACKET_SCHEMA_PATH = PACKAGE / "schemas" / "adaptation-packet.v2.schema.json"
RECORD_VALIDATOR_PATH = PACKAGE / "tools" / "validate_evolution_record_v2.py"
TRANSFER_STATUS = "TRANSFERRED_SOURCE_EVIDENCE_NOT_LOCAL_PROOF"
SOURCE_AUTHENTICATION = "NOT_AUTHENTICATED_BY_THIS_PACKET"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def canonical_digest(value: dict[str, Any]) -> str:
    base = dict(value)
    base.pop("content_sha256", None)
    payload = json.dumps(base, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _load_candidate_record_validator_module():
    spec = importlib.util.spec_from_file_location("ena_candidate_record_v2_validator", RECORD_VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load candidate evolution-record v2 validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_record_v2(record: dict[str, Any]) -> list[str]:
    return list(_load_candidate_record_validator_module().validate_record(record))


def validate_transferred_source_history(packet: dict[str, Any]) -> list[str]:
    return list(_load_candidate_record_validator_module().validate_transferred_source_history(packet))


def require_valid_record(record: dict[str, Any]) -> None:
    errors = validate_record_v2(record)
    if errors:
        raise ValueError("Invalid evolution-record v2: " + " | ".join(errors))


def build_latent_record(
    candidate_id: str,
    hypothesis: str,
    change: str,
    *,
    variation_space: str | None = None,
    evolutionary_subject: str = "",
    signal_refs: list[str] | None = None,
    mutation_pressure_refs: list[str] | None = None,
    protected_subjects: list[str] | None = None,
    environment: dict[str, Any] | None = None,
    dependencies: list[str] | None = None,
    unknowns: list[str] | None = None,
    expected_outcomes: list[str] | None = None,
    observation_plan: str = "",
) -> dict[str, Any]:
    record = copy.deepcopy(load_json(TEMPLATE_PATH))
    record.update(
        {
            "candidate_id": candidate_id,
            "created_at": now(),
            "origin": "LOCAL_VARIATION",
            "lifecycle_state": "PROPOSED",
            "expression_state": "LATENT",
            "selection_state": "UNASSESSED",
            "signal_refs": list(signal_refs or []),
            "mutation_pressure_refs": list(mutation_pressure_refs or []),
            "triggered_obligation_refs": [],
            "hypothesis": hypothesis,
            "change": change,
            "expected_outcomes": list(expected_outcomes or []),
            "variation_space": variation_space,
            "evolutionary_subject": evolutionary_subject,
            "protected_subjects": list(protected_subjects or []),
            "environment": dict(environment or {}),
            "dependencies": list(dependencies or []),
            "unknowns": list(unknowns or []),
            "observation_plan": observation_plan,
            "experiments": [],
            "evaluations": [],
            "expression_history": [],
            "integration_history": [],
            "archive": None,
            "migration": None,
        }
    )
    require_valid_record(record)
    return record


def packet_purpose(selection: str) -> str:
    if selection in {"SUPPORTED", "PARTIAL"}:
        return "ADAPTATION_CANDIDATE"
    if selection in {"NOT_SUPPORTED", "HARMFUL"}:
        return "NEGATIVE_EVIDENCE"
    return "UNRESOLVED_VARIATION"


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _last_expressed_at(history: list[dict[str, Any]]) -> str | None:
    expressed = [item for item in history if item.get("state") == "EXPRESSED"]
    if not expressed:
        return None
    latest = max(expressed, key=lambda item: _parse_time(str(item["time"])))
    return str(latest["time"])


def _negative_lineage_refs(record: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    migration = record.get("migration")
    if isinstance(migration, dict):
        refs.extend(str(x) for x in migration.get("source_negative_lineage_refs", []) or [])
    for evaluation in record.get("evaluations", []) or []:
        refs.extend(str(x) for x in evaluation.get("negative_evidence", []) or [])
    seen: set[str] = set()
    out: list[str] = []
    for ref in refs:
        if ref and ref not in seen:
            seen.add(ref)
            out.append(ref)
    return out


def export_packet_v2(record: dict[str, Any]) -> dict[str, Any]:
    require_valid_record(record)
    history = copy.deepcopy(record.get("expression_history", []) or [])
    packet: dict[str, Any] = {
        "packet_schema": "ena-adaptation-packet.v2",
        "exported_at": now(),
        "packet_purpose": packet_purpose(str(record["selection_state"])),
        "source_candidate_id": record["candidate_id"],
        "source_origin": record.get("origin"),
        "source_lifecycle_state": record["lifecycle_state"],
        "source_expression_state": record["expression_state"],
        "source_selection_state": record["selection_state"],
        "hypothesis": record.get("hypothesis"),
        "change": record.get("change"),
        "expected_outcomes": copy.deepcopy(record.get("expected_outcomes", []) or []),
        "source_variation_space": record.get("variation_space"),
        "evolutionary_subject": record.get("evolutionary_subject"),
        "protected_subjects": copy.deepcopy(record.get("protected_subjects", []) or []),
        "source_environment": copy.deepcopy(record.get("environment", {}) or {}),
        "dependencies": copy.deepcopy(record.get("dependencies", []) or []),
        "source_experiments": copy.deepcopy(record.get("experiments", []) or []),
        "source_evaluations": copy.deepcopy(record.get("evaluations", []) or []),
        "source_expression_history": history,
        "source_last_expressed_at": _last_expressed_at(history),
        "source_integration_history": copy.deepcopy(record.get("integration_history", []) or []),
        "source_archive": copy.deepcopy(record.get("archive")),
        "source_migration": copy.deepcopy(record.get("migration")),
        "source_negative_lineage_refs": _negative_lineage_refs(record),
        "unknowns": copy.deepcopy(record.get("unknowns", []) or []),
        "transfer_status": TRANSFER_STATUS,
        "source_authentication": SOURCE_AUTHENTICATION,
    }
    packet["content_sha256"] = canonical_digest(packet)
    require_valid_packet_v2(packet)
    return packet


def validate_packet_v2(packet: dict[str, Any]) -> list[str]:
    schema = load_json(PACKET_SCHEMA_PATH)
    errors = [
        f"schema: {error.message}"
        for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(packet)
    ]
    claimed = packet.get("content_sha256")
    if isinstance(claimed, str) and claimed != canonical_digest(packet):
        errors.append("digest: content_sha256 does not match canonical packet content")

    for required_context in ("source_variation_space", "evolutionary_subject", "protected_subjects"):
        if required_context not in packet:
            errors.append(f"consistency: packet must represent {required_context} even when empty/null")

    errors.extend(validate_transferred_source_history(packet))

    history = packet.get("source_expression_history") or []
    if isinstance(history, list) and history:
        try:
            parsed_history = [(_parse_time(str(item["time"])), item) for item in history]
            max_time = max(stamp for stamp, _ in parsed_history)
            latest_items = [item for stamp, item in parsed_history if stamp == max_time]
            if len(latest_items) != 1:
                errors.append("consistency: source_expression_history has tied latest timestamps")
            else:
                latest = latest_items[0]
                if latest.get("state") != packet.get("source_expression_state"):
                    errors.append("consistency: latest source expression state must match source_expression_state")
            expected_last = _last_expressed_at(history)
            if packet.get("source_last_expressed_at") != expected_last:
                errors.append("consistency: source_last_expressed_at must match latest represented EXPRESSED occurrence")
        except Exception as exc:
            errors.append(f"consistency: invalid source expression history time: {exc}")
    elif packet.get("source_last_expressed_at") is not None:
        errors.append("consistency: source_last_expressed_at requires represented source expression history")
    return errors


def require_valid_packet_v2(packet: dict[str, Any]) -> None:
    errors = validate_packet_v2(packet)
    if errors:
        raise ValueError("Invalid adaptation-packet v2: " + " | ".join(errors))


def import_packet_v2(
    packet: dict[str, Any],
    candidate_id: str,
    *,
    packet_ref: str = "inline:adaptation-packet-v2",
    evolutionary_subject: str = "",
    environment: dict[str, Any] | None = None,
    protected_subjects: list[str] | None = None,
    unknowns: list[str] | None = None,
    observation_plan: str = "",
) -> dict[str, Any]:
    require_valid_packet_v2(packet)
    hypothesis = packet.get("hypothesis") or "Imported unresolved source variation."
    change = packet.get("change") or "Imported source change retained for local evaluation."
    record = build_latent_record(
        candidate_id,
        str(hypothesis),
        str(change),
        variation_space=None,
        evolutionary_subject=evolutionary_subject,
        protected_subjects=protected_subjects,
        environment=environment,
        dependencies=copy.deepcopy(packet.get("dependencies", []) or []),
        unknowns=list(packet.get("unknowns", []) or []) + list(unknowns or []),
        expected_outcomes=copy.deepcopy(packet.get("expected_outcomes", []) or []),
        observation_plan=observation_plan,
    )
    record["origin"] = "MIGRATION_CANDIDATE"
    record["source_packet"] = packet_ref
    record["source_packet_sha256"] = packet["content_sha256"]
    record["source_candidate_id"] = packet["source_candidate_id"]
    record["migration"] = {
        "source_candidate_id": packet["source_candidate_id"],
        "source_selection_state": packet["source_selection_state"],
        "source_lifecycle_state": packet["source_lifecycle_state"],
        "packet_purpose": packet["packet_purpose"],
        "transfer_status": "TRANSFERRED_NOT_LOCALLY_VALIDATED",
        "source_authentication": packet["source_authentication"],
        "packet_sha256": packet["content_sha256"],
        "source_negative_lineage_refs": copy.deepcopy(packet.get("source_negative_lineage_refs", []) or []),
        "source_variation_space": copy.deepcopy(packet.get("source_variation_space")),
        "source_evolutionary_subject": copy.deepcopy(packet.get("evolutionary_subject")),
        "source_protected_subjects": copy.deepcopy(packet.get("protected_subjects", []) or []),
        "material_differences": [],
        "source_environment": copy.deepcopy(packet.get("source_environment", {}) or {}),
        "source_experiments": copy.deepcopy(packet.get("source_experiments", []) or []),
        "source_evaluations": copy.deepcopy(packet.get("source_evaluations", []) or []),
        "source_integration_history": copy.deepcopy(packet.get("source_integration_history", []) or []),
        "source_archive": copy.deepcopy(packet.get("source_archive")),
        "source_migration": copy.deepcopy(packet.get("source_migration")),
        "source_expression_state": packet["source_expression_state"],
        "source_expression_history": copy.deepcopy(packet.get("source_expression_history", []) or []),
        "source_last_expressed_at": packet.get("source_last_expressed_at"),
    }
    require_valid_record(record)
    return record


def _parse_kv(items: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"Expected KEY=VALUE, got {item!r}")
        key, value = item.split("=", 1)
        if not key:
            raise SystemExit(f"Empty key in {item!r}")
        result[key] = value
    return result


def _candidate_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def cmd_new_latent(args: argparse.Namespace) -> None:
    record = build_latent_record(
        args.candidate_id or _candidate_id("var"),
        args.hypothesis,
        args.change,
        variation_space=args.variation_space,
        evolutionary_subject=args.evolutionary_subject,
        signal_refs=args.signal,
        mutation_pressure_refs=args.mutation_pressure,
        protected_subjects=args.protected_subject,
        environment=_parse_kv(args.environment),
        dependencies=args.dependency,
        unknowns=args.unknown,
        expected_outcomes=args.expected,
        observation_plan=args.observe,
    )
    write_json(Path(args.output), record)
    print(json.dumps({"result": "WROTE_LATENT_V2", "output": args.output, "candidate_id": record["candidate_id"], "variation_space": record["variation_space"]}))


def cmd_export(args: argparse.Namespace) -> None:
    packet = export_packet_v2(load_json(Path(args.record)))
    write_json(Path(args.output), packet)
    print(json.dumps({"result": "WROTE_PACKET_V2", "output": args.output, "content_sha256": packet["content_sha256"]}))


def cmd_import(args: argparse.Namespace) -> None:
    record = import_packet_v2(
        load_json(Path(args.packet)),
        args.candidate_id or _candidate_id("mig"),
        packet_ref=args.packet,
        evolutionary_subject=args.evolutionary_subject,
        environment=_parse_kv(args.environment),
        protected_subjects=args.protected_subject,
        unknowns=args.unknown,
        observation_plan=args.observe,
    )
    write_json(Path(args.output), record)
    print(json.dumps({"result": "WROTE_MIGRATION_CANDIDATE_V2", "output": args.output, "candidate_id": record["candidate_id"], "local_selection": record["selection_state"]}))


def cmd_validate_record(args: argparse.Namespace) -> None:
    errors = validate_record_v2(load_json(Path(args.record)))
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


def cmd_validate_packet(args: argparse.Namespace) -> None:
    errors = validate_packet_v2(load_json(Path(args.packet)))
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ena_evolve_v2.py", description="Minimal ENA v0.3.7 candidate v2 record/packet helper")
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("new-latent")
    c.add_argument("--candidate-id")
    c.add_argument("--hypothesis", required=True)
    c.add_argument("--change", required=True)
    c.add_argument("--variation-space")
    c.add_argument("--evolutionary-subject", default="")
    c.add_argument("--signal", action="append", default=[])
    c.add_argument("--mutation-pressure", action="append", default=[])
    c.add_argument("--protected-subject", action="append", default=[])
    c.add_argument("--environment", action="append", default=[])
    c.add_argument("--dependency", action="append", default=[])
    c.add_argument("--unknown", action="append", default=[])
    c.add_argument("--expected", action="append", default=[])
    c.add_argument("--observe", default="")
    c.add_argument("--output", required=True)
    c.set_defaults(func=cmd_new_latent)

    c = sub.add_parser("export-packet")
    c.add_argument("record")
    c.add_argument("--output", required=True)
    c.set_defaults(func=cmd_export)

    c = sub.add_parser("import-packet")
    c.add_argument("packet")
    c.add_argument("--candidate-id")
    c.add_argument("--evolutionary-subject", default="")
    c.add_argument("--environment", action="append", default=[])
    c.add_argument("--protected-subject", action="append", default=[])
    c.add_argument("--unknown", action="append", default=[])
    c.add_argument("--observe", default="")
    c.add_argument("--output", required=True)
    c.set_defaults(func=cmd_import)

    c = sub.add_parser("validate-record")
    c.add_argument("record")
    c.set_defaults(func=cmd_validate_record)

    c = sub.add_parser("validate-packet")
    c.add_argument("packet")
    c.set_defaults(func=cmd_validate_packet)
    return p


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

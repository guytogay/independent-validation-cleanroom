#!/usr/bin/env python3
"""ENA v0.3.5 candidate.2 reference evolution-metabolism tool.

This is a state/evidence tool, not a self-modification engine or authority
oracle. Lifecycle state and evidence-backed selection state are separate axes.

Boundaries:
- positive/negative selection requires at least one represented experiment;
- integration never proves improvement;
- migration preserves source selection/provenance and transfer is not local proof;
- packet digest checks internal consistency, not source authentication;
- closure reads represented local state but cannot prove omitted real-world
  blockers do not exist;
- authority/recovery statements are recorded, not verified here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_VERSION = "1.2"
DEFAULT_STATE = Path(".ena") / "evolution" / "state.json"
OUTCOME_STATES = {"IMPROVED", "DEGRADED", "UNCHANGED", "UNKNOWN"}
SELECTION_STATES = {"UNASSESSED", "SUPPORTED", "PARTIAL", "NOT_SUPPORTED", "HARMFUL", "UNKNOWN"}
POSITIVE_SELECTION = {"SUPPORTED", "PARTIAL"}
NEGATIVE_SELECTION = {"NOT_SUPPORTED", "HARMFUL"}
LIFECYCLE_STATES = {"PROPOSED", "EXPERIMENTED", "INTEGRATED", "ARCHIVED", "RETIRED"}
PACKET_PURPOSES = {"ADAPTATION_CANDIDATE", "NEGATIVE_EVIDENCE", "UNRESOLVED_VARIATION"}
TRANSFER_STATUS = "TRANSFERRED_SOURCE_EVIDENCE_NOT_LOCAL_PROOF"
SOURCE_AUTHENTICATION = "NOT_AUTHENTICATED_BY_THIS_PACKET"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def empty_state() -> dict[str, Any]:
    t = now()
    return {
        "schema_version": STATE_VERSION,
        "created_at": t,
        "updated_at": t,
        "signals": [],
        "reviews": [],
        "candidates": [],
        "migration_imports": [],
        "events": [],
    }


def state_path(args: argparse.Namespace) -> Path:
    return Path(getattr(args, "state", DEFAULT_STATE))


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"State not found: {path}. Run `init` first.")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != STATE_VERSION:
        raise SystemExit(
            f"Unsupported state schema: {data.get('schema_version')!r}; expected {STATE_VERSION!r}"
        )
    return data


def atomic_write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = now()
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as fh:
        tmp = Path(fh.name)
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    tmp.replace(path)


def print_json(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def add_event(state: dict[str, Any], kind: str, ref: str, detail: str = "") -> None:
    state["events"].append(
        {"event_id": new_id("evt"), "time": now(), "kind": kind, "ref": ref, "detail": detail}
    )


def find_candidate(state: dict[str, Any], cid: str) -> dict[str, Any]:
    for candidate in state["candidates"]:
        if candidate["candidate_id"] == cid:
            return candidate
    raise SystemExit(f"Candidate not found: {cid}")


def parse_kv(items: list[str] | None) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in items or []:
        if "=" not in item:
            raise SystemExit(f"Expected KEY=VALUE, got: {item}")
        key, value = item.split("=", 1)
        if not key:
            raise SystemExit(f"Empty key in: {item}")
        out[key] = value
    return out


def canonical_digest(obj: dict[str, Any]) -> str:
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def lifecycle_state(candidate: dict[str, Any]) -> str:
    value = candidate.get("lifecycle_state", "PROPOSED")
    return value if value in LIFECYCLE_STATES else "PROPOSED"


def selection_state(candidate: dict[str, Any]) -> str:
    value = candidate.get("selection_state", "UNASSESSED")
    return value if value in SELECTION_STATES else "UNASSESSED"


def latest_evaluation(candidate: dict[str, Any]) -> dict[str, Any] | None:
    values = candidate.get("evaluations") or []
    return values[-1] if values else None


def require_experiment(candidate: dict[str, Any], action: str) -> None:
    if not candidate.get("experiments"):
        raise SystemExit(f"{action} requires at least one represented experiment")


def validate_evaluation(
    candidate: dict[str, Any], selection: str, outcomes: dict[str, str], evidence: list[str]
) -> None:
    require_experiment(candidate, f"{selection} evaluation")
    if selection == "UNASSESSED":
        raise SystemExit("UNASSESSED is an initial state, not an evaluation verdict")
    if selection == "UNKNOWN":
        return
    if not outcomes:
        raise SystemExit(f"{selection} requires at least one observed outcome dimension")
    if not evidence:
        raise SystemExit(f"{selection} requires at least one evidence reference")
    values = set(outcomes.values())
    if selection in POSITIVE_SELECTION and "IMPROVED" not in values:
        raise SystemExit(f"{selection} requires at least one represented IMPROVED outcome")
    if selection == "HARMFUL" and "DEGRADED" not in values:
        raise SystemExit("HARMFUL requires at least one represented DEGRADED outcome")


def packet_purpose_for(selection: str) -> str:
    if selection in POSITIVE_SELECTION:
        return "ADAPTATION_CANDIDATE"
    if selection in NEGATIVE_SELECTION:
        return "NEGATIVE_EVIDENCE"
    return "UNRESOLVED_VARIATION"


def packet_consistency_error(packet: dict[str, Any]) -> str | None:
    purpose = packet.get("packet_purpose")
    source_lifecycle = packet.get("source_lifecycle_state")
    source_selection = packet.get("source_selection_state")
    transfer_status = packet.get("transfer_status")
    source_authentication = packet.get("source_authentication")

    if purpose not in PACKET_PURPOSES:
        return f"invalid packet_purpose: {purpose!r}"
    if source_lifecycle not in LIFECYCLE_STATES:
        return f"invalid source_lifecycle_state: {source_lifecycle!r}"
    if source_selection not in SELECTION_STATES:
        return f"invalid source_selection_state: {source_selection!r}"
    if transfer_status != TRANSFER_STATUS:
        return f"invalid transfer_status: {transfer_status!r}"
    if source_authentication != SOURCE_AUTHENTICATION:
        return f"invalid source_authentication: {source_authentication!r}"

    expected = packet_purpose_for(source_selection)
    if purpose != expected:
        return f"packet_purpose/source_selection_state contradiction: {purpose} != {expected}"

    experiments = packet.get("source_experiments") or []
    evaluations = packet.get("source_evaluations") or []
    if source_selection != "UNASSESSED":
        if not experiments:
            return f"source_selection_state {source_selection} requires source_experiments"
        if not evaluations:
            return f"source_selection_state {source_selection} requires source_evaluations"
        latest = evaluations[-1]
        if latest.get("selection") != source_selection:
            return "latest source evaluation does not match source_selection_state"
        outcomes = latest.get("outcomes") or {}
        evidence = latest.get("evidence_refs") or []
        if source_selection != "UNKNOWN":
            if not outcomes:
                return f"source_selection_state {source_selection} requires represented outcomes"
            if not evidence:
                return f"source_selection_state {source_selection} requires evidence references"
        values = set(outcomes.values())
        if source_selection in POSITIVE_SELECTION and "IMPROVED" not in values:
            return f"source_selection_state {source_selection} requires an IMPROVED outcome"
        if source_selection == "HARMFUL" and "DEGRADED" not in values:
            return "source_selection_state HARMFUL requires a DEGRADED outcome"
    return None


def cmd_init(args: argparse.Namespace) -> None:
    path = state_path(args)
    if path.exists() and not args.force:
        raise SystemExit(f"State already exists: {path}; use --force to replace")
    if path.exists() and args.force and not args.confirm_reset:
        raise SystemExit("--force requires --confirm-reset because it destroys previous evolution state")
    state = empty_state()
    add_event(state, "INIT", "state", "Evolution metabolism initialized")
    atomic_write(path, state)
    print_json({"state": str(path), "result": "INITIALIZED", "schema_version": STATE_VERSION})


def cmd_observe(args: argparse.Namespace) -> None:
    path = state_path(args)
    state = load_state(path)
    signal = {
        "signal_id": new_id("sig"),
        "time": now(),
        "kind": args.kind,
        "summary": args.summary,
        "source": args.source,
        "context": parse_kv(args.context),
        "reviewed": False,
    }
    state["signals"].append(signal)
    add_event(state, "OBSERVE", signal["signal_id"], signal["summary"])
    atomic_write(path, state)
    print_json(signal)


def cmd_review(args: argparse.Namespace) -> None:
    path = state_path(args)
    state = load_state(path)
    pending = [s for s in state["signals"] if not s.get("reviewed")]
    selected = pending if args.all else pending[: args.limit]
    rid = new_id("rev")
    for signal in selected:
        signal["reviewed"] = True
        signal["review_id"] = rid
    review = {
        "review_id": rid,
        "time": now(),
        "trigger": args.trigger,
        "signal_refs": [s["signal_id"] for s in selected],
        "finding": args.finding,
        "mutation_required": bool(args.mutation_required),
    }
    state["reviews"].append(review)
    add_event(state, "REVIEW", rid, args.finding or "review complete")
    atomic_write(path, state)
    print_json(review)


def cmd_propose(args: argparse.Namespace) -> None:
    path = state_path(args)
    state = load_state(path)
    refs = args.signal or []
    known = {s["signal_id"] for s in state["signals"]}
    missing = [ref for ref in refs if ref not in known]
    if missing:
        raise SystemExit(f"Unknown signal refs: {', '.join(missing)}")
    candidate = {
        "candidate_id": new_id("var"),
        "created_at": now(),
        "origin": "LOCAL_VARIATION",
        "lifecycle_state": "PROPOSED",
        "selection_state": "UNASSESSED",
        "signal_refs": refs,
        "hypothesis": args.hypothesis,
        "change": args.change,
        "expected_outcomes": args.expected or [],
        "variation_space": args.variation_space,
        "evolutionary_subject": args.evolutionary_subject,
        "protected_subjects": args.protected_subject or [],
        "environment": parse_kv(args.environment),
        "dependencies": args.dependency or [],
        "unknowns": args.unknown or [],
        "observation_plan": args.observe,
        "experiments": [],
        "evaluations": [],
        "integration_history": [],
        "archive": None,
        "migration": None,
    }
    state["candidates"].append(candidate)
    add_event(state, "PROPOSE", candidate["candidate_id"], candidate["hypothesis"])
    atomic_write(path, state)
    print_json(candidate)


def cmd_experiment(args: argparse.Namespace) -> None:
    path = state_path(args)
    state = load_state(path)
    candidate = find_candidate(state, args.candidate)
    life = lifecycle_state(candidate)
    if life in {"INTEGRATED", "ARCHIVED", "RETIRED"}:
        raise SystemExit(f"Candidate lifecycle_state is {life}; create a new variation rather than overwrite history")
    experiment = {
        "experiment_id": new_id("exp"),
        "time": now(),
        "variation_space": args.variation_space or candidate.get("variation_space"),
        "actual_change": args.actual_change,
        "effect_boundary": args.effect_boundary,
        "recovery": args.recovery,
        "external_authority_basis": args.authority_basis,
        "notes": args.note or "",
    }
    candidate["experiments"].append(experiment)
    candidate["lifecycle_state"] = "EXPERIMENTED"
    candidate["selection_state"] = "UNASSESSED"
    add_event(state, "EXPERIMENT", candidate["candidate_id"], experiment["experiment_id"])
    atomic_write(path, state)
    print_json(experiment)


def cmd_evaluate(args: argparse.Namespace) -> None:
    path = state_path(args)
    state = load_state(path)
    candidate = find_candidate(state, args.candidate)
    if lifecycle_state(candidate) in {"INTEGRATED", "ARCHIVED", "RETIRED"}:
        raise SystemExit("Closed lifecycle cannot be overwritten by a new evaluation; create a new variation")
    outcomes: dict[str, str] = {}
    for item in args.outcome or []:
        if "=" not in item:
            raise SystemExit(f"Expected DIMENSION=STATE, got: {item}")
        dim, value = item.split("=", 1)
        value = value.upper()
        if value not in OUTCOME_STATES:
            raise SystemExit(f"Invalid outcome state {value}; choose {sorted(OUTCOME_STATES)}")
        outcomes[dim] = value
    selection = args.selection.upper()
    if selection not in SELECTION_STATES:
        raise SystemExit(f"Invalid selection: {selection}")
    evidence = args.evidence or []
    validate_evaluation(candidate, selection, outcomes, evidence)
    evaluation = {
        "evaluation_id": new_id("eval"),
        "time": now(),
        "outcomes": outcomes,
        "selection": selection,
        "evidence_refs": evidence,
        "negative_evidence": args.negative_evidence or [],
        "tradeoffs": args.tradeoff or [],
        "unknowns": args.unknown or [],
        "notes": args.note or "",
        "evidence_boundary": "REFERENCED_NOT_EXTERNALLY_VERIFIED_BY_THIS_TOOL",
    }
    candidate["evaluations"].append(evaluation)
    candidate["selection_state"] = selection
    add_event(state, "EVALUATE", candidate["candidate_id"], selection)
    atomic_write(path, state)
    print_json(evaluation)


def cmd_integrate(args: argparse.Namespace) -> None:
    path = state_path(args)
    state = load_state(path)
    candidate = find_candidate(state, args.candidate)
    life = lifecycle_state(candidate)
    if life in {"INTEGRATED", "ARCHIVED", "RETIRED"}:
        raise SystemExit(f"Candidate lifecycle_state is {life}; integration cannot overwrite it")
    require_experiment(candidate, "Integration")
    selection = selection_state(candidate)
    evaluation = latest_evaluation(candidate)
    if not evaluation or evaluation.get("selection") != selection:
        raise SystemExit("Integration requires an explicit current evaluation")
    if selection in NEGATIVE_SELECTION or selection == "UNASSESSED":
        raise SystemExit(f"Candidate selection_state is {selection}; revise/new variation instead")
    if selection == "UNKNOWN" and not args.allow_unknown:
        raise SystemExit("UNKNOWN integration requires explicit --allow-unknown")
    if args.result == "COMMITTED":
        if not args.authority_basis:
            raise SystemExit("COMMITTED integration requires --authority-basis (recorded, not verified)")
        if not args.recovery_boundary:
            raise SystemExit("COMMITTED integration requires --recovery-boundary (recorded, not verified)")
    integration = {
        "integration_id": new_id("int"),
        "time": now(),
        "target": args.target,
        "authority_basis": args.authority_basis,
        "recovery_boundary": args.recovery_boundary,
        "scope": args.scope,
        "result": args.result,
        "residuals": args.residual or [],
        "selection_state_at_commit": selection,
        "authority_boundary": "RECORDED_NOT_VERIFIED_BY_THIS_TOOL",
    }
    candidate["integration_history"].append(integration)
    if args.result == "COMMITTED":
        candidate["lifecycle_state"] = "INTEGRATED"
    add_event(state, "INTEGRATE", candidate["candidate_id"], args.result)
    atomic_write(path, state)
    print_json(integration)


def cmd_archive(args: argparse.Namespace) -> None:
    path = state_path(args)
    state = load_state(path)
    candidate = find_candidate(state, args.candidate)
    if lifecycle_state(candidate) in {"ARCHIVED", "RETIRED"}:
        raise SystemExit("Candidate is already archived/retired")
    candidate["archive"] = {
        "time": now(),
        "reason": args.reason,
        "record_retention": "RETAIN" if not args.retire_record else "RETIRE_RECORD_IF_POLICY_ALLOWS",
        "retention_note": args.retention_note,
        "selection_state_preserved": selection_state(candidate),
    }
    candidate["lifecycle_state"] = "RETIRED" if args.retire_record else "ARCHIVED"
    add_event(state, "ARCHIVE", candidate["candidate_id"], args.reason)
    atomic_write(path, state)
    print_json(candidate["archive"])


def migration_packet(candidate: dict[str, Any]) -> dict[str, Any]:
    selection = selection_state(candidate)
    packet = {
        "packet_schema": "ena-adaptation-packet.v1",
        "exported_at": now(),
        "packet_purpose": packet_purpose_for(selection),
        "source_candidate_id": candidate["candidate_id"],
        "source_origin": candidate.get("origin"),
        "source_lifecycle_state": lifecycle_state(candidate),
        "source_selection_state": selection,
        "hypothesis": candidate.get("hypothesis"),
        "change": candidate.get("change"),
        "expected_outcomes": candidate.get("expected_outcomes", []),
        "source_variation_space": candidate.get("variation_space"),
        "evolutionary_subject": candidate.get("evolutionary_subject"),
        "protected_subjects": candidate.get("protected_subjects", []),
        "source_environment": candidate.get("environment", {}),
        "dependencies": candidate.get("dependencies", []),
        "source_experiments": candidate.get("experiments", []),
        "source_evaluations": candidate.get("evaluations", []),
        "source_integration_history": candidate.get("integration_history", []),
        "source_archive": candidate.get("archive"),
        "source_migration": candidate.get("migration"),
        "unknowns": candidate.get("unknowns", []),
        "transfer_status": TRANSFER_STATUS,
        "source_authentication": SOURCE_AUTHENTICATION,
    }
    packet["content_sha256"] = canonical_digest(packet)
    return packet


def validate_packet(packet: dict[str, Any]) -> None:
    if packet.get("packet_schema") != "ena-adaptation-packet.v1":
        raise SystemExit("Unsupported migration packet schema")
    claimed = packet.get("content_sha256")
    if not claimed:
        raise SystemExit("Migration packet missing content_sha256")
    base = dict(packet)
    base.pop("content_sha256", None)
    if claimed != canonical_digest(base):
        raise SystemExit("Migration packet content digest mismatch")
    required = {
        "packet_purpose",
        "source_candidate_id",
        "source_lifecycle_state",
        "source_selection_state",
        "transfer_status",
        "source_authentication",
        "source_experiments",
        "source_evaluations",
    }
    missing = sorted(k for k in required if k not in packet)
    if missing:
        raise SystemExit(f"Migration packet missing required fields: {', '.join(missing)}")
    error = packet_consistency_error(packet)
    if error:
        raise SystemExit(f"Migration packet semantic inconsistency: {error}")


def cmd_export(args: argparse.Namespace) -> None:
    state = load_state(state_path(args))
    candidate = find_candidate(state, args.candidate)
    packet = migration_packet(candidate)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print_json(
        {
            "output": str(out),
            "packet_purpose": packet["packet_purpose"],
            "source_lifecycle_state": packet["source_lifecycle_state"],
            "source_selection_state": packet["source_selection_state"],
            "content_sha256": packet["content_sha256"],
            "transfer_status": packet["transfer_status"],
            "source_authentication": packet["source_authentication"],
        }
    )


def cmd_import(args: argparse.Namespace) -> None:
    path = state_path(args)
    state = load_state(path)
    packet = json.loads(Path(args.packet).read_text(encoding="utf-8"))
    validate_packet(packet)
    candidate = {
        "candidate_id": new_id("mig"),
        "created_at": now(),
        "origin": "MIGRATION_CANDIDATE",
        "lifecycle_state": "PROPOSED",
        "selection_state": "UNASSESSED",
        "source_packet": str(args.packet),
        "source_packet_sha256": packet["content_sha256"],
        "source_candidate_id": packet["source_candidate_id"],
        "signal_refs": [],
        "hypothesis": packet.get("hypothesis"),
        "change": packet.get("change"),
        "expected_outcomes": packet.get("expected_outcomes", []),
        "variation_space": args.variation_space,
        "evolutionary_subject": args.evolutionary_subject,
        "protected_subjects": args.protected_subject or [],
        "environment": parse_kv(args.environment),
        "dependencies": packet.get("dependencies", []),
        "unknowns": list(packet.get("unknowns", [])) + (args.unknown or []),
        "observation_plan": args.observe,
        "experiments": [],
        "evaluations": [],
        "integration_history": [],
        "archive": None,
        "migration": {
            "source_selection_state": packet["source_selection_state"],
            "source_lifecycle_state": packet["source_lifecycle_state"],
            "packet_purpose": packet["packet_purpose"],
            "transfer_status": "TRANSFERRED_NOT_LOCALLY_VALIDATED",
            "source_authentication": packet["source_authentication"],
            "material_differences": args.difference or [],
            "source_environment": packet.get("source_environment", {}),
            "source_experiments": packet.get("source_experiments", []),
            "source_evaluations": packet.get("source_evaluations", []),
            "source_integration_history": packet.get("source_integration_history", []),
            "source_archive": packet.get("source_archive"),
            "source_migration": packet.get("source_migration"),
        },
    }
    state["candidates"].append(candidate)
    state["migration_imports"].append(
        {
            "time": now(),
            "packet": str(args.packet),
            "packet_sha256": packet["content_sha256"],
            "candidate_id": candidate["candidate_id"],
            "packet_purpose": packet["packet_purpose"],
            "source_selection_state": packet["source_selection_state"],
        }
    )
    add_event(state, "IMPORT", candidate["candidate_id"], packet["packet_purpose"])
    atomic_write(path, state)
    print_json(candidate)


def closure_state_obligations(state: dict[str, Any], candidate_id: str | None) -> list[str]:
    obligations: list[str] = []
    if candidate_id:
        candidate = find_candidate(state, candidate_id)
        life, selection = lifecycle_state(candidate), selection_state(candidate)
        if life == "PROPOSED":
            obligations.append(f"{candidate_id}: no represented experiment")
        if life == "EXPERIMENTED" and selection in {"UNASSESSED", "UNKNOWN"}:
            obligations.append(f"{candidate_id}: experiment remains {selection}")
        return obligations
    unreviewed = [s for s in state["signals"] if not s.get("reviewed")]
    if unreviewed:
        obligations.append(f"{len(unreviewed)} evolution signal(s) remain unreviewed")
    for candidate in state["candidates"]:
        if lifecycle_state(candidate) == "EXPERIMENTED" and selection_state(candidate) in {
            "UNASSESSED",
            "UNKNOWN",
        }:
            obligations.append(
                f"{candidate['candidate_id']}: experimented candidate remains {selection_state(candidate)}"
            )
    return obligations


def cmd_closure(args: argparse.Namespace) -> None:
    state = load_state(state_path(args))
    blockers = list(args.blocker or [])
    evidence = list(args.evidence_needed or [])
    narrow = list(args.narrow or [])
    auto = closure_state_obligations(state, args.candidate)
    evidence.extend(auto)
    outcome = (
        "STOP_OR_ESCALATE"
        if blockers
        else "EVIDENCE_NEEDED"
        if evidence
        else "NARROW_AND_PROCEED"
        if narrow
        else "READY"
    )
    print_json(
        {
            "semantic_outcome": outcome,
            "evidence_scope": "REPRESENTED_STATE_AND_INPUTS_ONLY",
            "unrepresented_material_blockers": "UNKNOWN",
            "candidate_scope": args.candidate,
            "auto_state_obligations": auto,
            "blockers": blockers,
            "evidence_needed": evidence,
            "narrowing": narrow,
            "claim_boundary": "Reads represented state/input only; omitted real-world blockers may still exist.",
        }
    )


def cmd_status(args: argparse.Namespace) -> None:
    state = load_state(state_path(args))
    lc: dict[str, int] = {}
    sc: dict[str, int] = {}
    for candidate in state["candidates"]:
        life, sel = lifecycle_state(candidate), selection_state(candidate)
        lc[life] = lc.get(life, 0) + 1
        sc[sel] = sc.get(sel, 0) + 1
    print_json(
        {
            "state_schema": state["schema_version"],
            "signals": len(state["signals"]),
            "signals_pending_review": sum(1 for s in state["signals"] if not s.get("reviewed")),
            "reviews": len(state["reviews"]),
            "candidates": len(state["candidates"]),
            "candidate_lifecycle_counts": lc,
            "candidate_selection_counts": sc,
            "migration_imports": len(state["migration_imports"]),
            "updated_at": state.get("updated_at"),
        }
    )


def _expect_packet_rejection(packet: dict[str, Any], label: str) -> None:
    try:
        validate_packet(packet)
    except SystemExit:
        return
    raise AssertionError(f"{label} was accepted")


def _redigest(packet: dict[str, Any]) -> dict[str, Any]:
    packet = dict(packet)
    packet.pop("content_sha256", None)
    packet["content_sha256"] = canonical_digest(packet)
    return packet


def cmd_selftest(_args: argparse.Namespace) -> None:
    root = Path(tempfile.mkdtemp(prefix="ena-evolve-selftest-"))
    try:
        base = {
            "candidate_id": "var-positive",
            "created_at": now(),
            "origin": "LOCAL_VARIATION",
            "lifecycle_state": "EXPERIMENTED",
            "selection_state": "UNASSESSED",
            "signal_refs": [],
            "hypothesis": "test",
            "change": "test change",
            "expected_outcomes": ["quality"],
            "variation_space": "selftest",
            "evolutionary_subject": "tool-state",
            "protected_subjects": [],
            "environment": {"host": "selftest"},
            "dependencies": [],
            "unknowns": [],
            "observation_plan": "measure",
            "experiments": [{"experiment_id": "exp-1"}],
            "evaluations": [],
            "integration_history": [],
            "archive": None,
            "migration": None,
        }
        validate_evaluation(base, "SUPPORTED", {"quality": "IMPROVED"}, ["obs"])
        base["selection_state"] = "SUPPORTED"
        base["evaluations"] = [
            {
                "evaluation_id": "eval-1",
                "selection": "SUPPORTED",
                "outcomes": {"quality": "IMPROVED"},
                "evidence_refs": ["obs"],
            }
        ]
        packet = migration_packet(base)
        validate_packet(packet)
        assert packet["packet_purpose"] == "ADAPTATION_CANDIDATE"

        no_exp = {**base, "experiments": []}
        try:
            validate_evaluation(no_exp, "SUPPORTED", {"quality": "IMPROVED"}, ["obs"])
            raise AssertionError("zero-experiment positive selection was accepted")
        except SystemExit:
            pass

        harmful = {
            **base,
            "candidate_id": "var-bad",
            "lifecycle_state": "ARCHIVED",
            "selection_state": "HARMFUL",
            "evaluations": [
                {
                    "evaluation_id": "eval-bad",
                    "selection": "HARMFUL",
                    "outcomes": {"quality": "DEGRADED"},
                    "evidence_refs": ["bad"],
                }
            ],
        }
        bad_packet = migration_packet(harmful)
        validate_packet(bad_packet)
        assert bad_packet["packet_purpose"] == "NEGATIVE_EVIDENCE"

        unknown = {
            **base,
            "candidate_id": "var-unknown",
            "lifecycle_state": "INTEGRATED",
            "selection_state": "UNKNOWN",
            "evaluations": [
                {
                    "evaluation_id": "eval-u",
                    "selection": "UNKNOWN",
                    "outcomes": {},
                    "evidence_refs": [],
                }
            ],
        }
        assert migration_packet(unknown)["packet_purpose"] == "UNRESOLVED_VARIATION"

        contradictory = _redigest({**bad_packet, "packet_purpose": "ADAPTATION_CANDIDATE"})
        _expect_packet_rejection(contradictory, "contradictory packet")

        no_source_exp = _redigest({**packet, "source_experiments": []})
        _expect_packet_rejection(no_source_exp, "selected packet without source experiment")

        invalid_lifecycle = _redigest({**packet, "source_lifecycle_state": "BANANA"})
        _expect_packet_rejection(invalid_lifecycle, "invalid lifecycle")

        forged_auth = _redigest({**packet, "source_authentication": "TOTALLY_TRUSTED"})
        _expect_packet_rejection(forged_auth, "forged source authentication")

        forged_transfer = _redigest({**packet, "transfer_status": "LOCALLY_PROVEN"})
        _expect_packet_rejection(forged_transfer, "forged transfer status")

        state_file = root / "state.json"
        state = empty_state()
        state["candidates"] = [
            {**base, "candidate_id": "var-open", "selection_state": "UNASSESSED", "evaluations": []}
        ]
        atomic_write(state_file, state)
        assert closure_state_obligations(load_state(state_file), None)

        print_json({"selftest": "PASS", "schema_version": STATE_VERSION, "cases": 10})
    finally:
        shutil.rmtree(root, ignore_errors=True)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ena_evolve.py",
        description="ENA v0.3.5 candidate.2 evolution state/evidence reference",
    )
    p.add_argument("--state", default=str(DEFAULT_STATE))
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("init")
    c.add_argument("--force", action="store_true")
    c.add_argument("--confirm-reset", action="store_true")
    c.set_defaults(func=cmd_init)

    c = sub.add_parser("observe")
    c.add_argument("--kind", required=True)
    c.add_argument("--summary", required=True)
    c.add_argument("--source", default="agent")
    c.add_argument("--context", action="append", default=[])
    c.set_defaults(func=cmd_observe)

    c = sub.add_parser("review")
    c.add_argument("--trigger", default="MANUAL")
    c.add_argument("--limit", type=int, default=20)
    c.add_argument("--all", action="store_true")
    c.add_argument("--finding", default="")
    c.add_argument("--mutation-required", action="store_true")
    c.set_defaults(func=cmd_review)

    c = sub.add_parser("propose")
    c.add_argument("--signal", action="append", default=[])
    c.add_argument("--hypothesis", required=True)
    c.add_argument("--change", required=True)
    c.add_argument("--expected", action="append", default=[])
    c.add_argument("--variation-space", required=True)
    c.add_argument("--evolutionary-subject", default="")
    c.add_argument("--protected-subject", action="append", default=[])
    c.add_argument("--environment", action="append", default=[])
    c.add_argument("--dependency", action="append", default=[])
    c.add_argument("--unknown", action="append", default=[])
    c.add_argument("--observe", default="")
    c.set_defaults(func=cmd_propose)

    c = sub.add_parser("experiment")
    c.add_argument("candidate")
    c.add_argument("--variation-space")
    c.add_argument("--actual-change", required=True)
    c.add_argument("--effect-boundary", default="")
    c.add_argument("--recovery", default="")
    c.add_argument("--authority-basis", default="")
    c.add_argument("--note", default="")
    c.set_defaults(func=cmd_experiment)

    c = sub.add_parser("evaluate")
    c.add_argument("candidate")
    c.add_argument("--outcome", action="append", default=[])
    c.add_argument("--selection", required=True)
    c.add_argument("--evidence", action="append", default=[])
    c.add_argument("--negative-evidence", action="append", default=[])
    c.add_argument("--tradeoff", action="append", default=[])
    c.add_argument("--unknown", action="append", default=[])
    c.add_argument("--note", default="")
    c.set_defaults(func=cmd_evaluate)

    c = sub.add_parser("integrate")
    c.add_argument("candidate")
    c.add_argument("--target", required=True)
    c.add_argument("--authority-basis", default="")
    c.add_argument("--recovery-boundary", default="")
    c.add_argument("--scope", default="")
    c.add_argument(
        "--result", choices=["COMMITTED", "DEFERRED", "REJECTED", "UNKNOWN"], default="COMMITTED"
    )
    c.add_argument("--residual", action="append", default=[])
    c.add_argument("--allow-unknown", action="store_true")
    c.set_defaults(func=cmd_integrate)

    c = sub.add_parser("archive")
    c.add_argument("candidate")
    c.add_argument("--reason", required=True)
    c.add_argument("--retire-record", action="store_true")
    c.add_argument("--retention-note", default="")
    c.set_defaults(func=cmd_archive)

    c = sub.add_parser("export")
    c.add_argument("candidate")
    c.add_argument("--output", required=True)
    c.set_defaults(func=cmd_export)

    c = sub.add_parser("import")
    c.add_argument("packet")
    c.add_argument("--variation-space", required=True)
    c.add_argument("--evolutionary-subject", default="")
    c.add_argument("--protected-subject", action="append", default=[])
    c.add_argument("--environment", action="append", default=[])
    c.add_argument("--difference", action="append", default=[])
    c.add_argument("--unknown", action="append", default=[])
    c.add_argument("--observe", default="")
    c.set_defaults(func=cmd_import)

    c = sub.add_parser("closure")
    c.add_argument("--candidate")
    c.add_argument("--blocker", action="append", default=[])
    c.add_argument("--evidence-needed", action="append", default=[])
    c.add_argument("--narrow", action="append", default=[])
    c.set_defaults(func=cmd_closure)

    c = sub.add_parser("status")
    c.set_defaults(func=cmd_status)

    c = sub.add_parser("selftest")
    c.set_defaults(func=cmd_selftest)
    return p


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

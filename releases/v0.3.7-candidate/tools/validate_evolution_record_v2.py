#!/usr/bin/env python3
"""Consistency validator for ENA v0.3.7 candidate.2 evolution-record v2.

Checks represented internal consistency only. It does not prove external truth,
actual expression, evidence validity, authority, recovery, or universal fitness.
"""
from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime
from pathlib import Path

from jsonschema import FormatChecker
from jsonschema.validators import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/evolution-record.v2.schema.json"
TEMPLATE_PATH = ROOT / "templates/evolution-record.v2.json"
POSITIVE = {"SUPPORTED", "PARTIAL"}
NEGATIVE = {"NOT_SUPPORTED", "HARMFUL"}


def expected_packet_purpose(selection: object) -> str:
    if selection in {"SUPPORTED", "PARTIAL"}:
        return "ADAPTATION_CANDIDATE"
    if selection in {"NOT_SUPPORTED", "HARMFUL"}:
        return "NEGATIVE_EVIDENCE"
    return "UNRESOLVED_VARIATION"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: object, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"consistency: {label} requires non-empty RFC3339 date-time")
        return None
    text = value.strip()
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"consistency: {label} has invalid date-time {text!r}")
        return None
    if parsed.tzinfo is None:
        errors.append(f"consistency: {label} must include timezone")
        return None
    return parsed


def latest_by_time(items: list[dict], label: str, errors: list[str]) -> dict | None:
    if not items:
        return None
    parsed: list[tuple[datetime, dict]] = []
    for index, item in enumerate(items):
        stamp = parse_time(item.get("time"), f"{label}[{index}].time", errors)
        if stamp is not None:
            parsed.append((stamp, item))
    if len(parsed) != len(items):
        return None
    max_time = max(stamp for stamp, _ in parsed)
    latest = [item for stamp, item in parsed if stamp == max_time]
    if len(latest) != 1:
        errors.append(f"consistency: {label} has tied latest timestamps")
        return None
    return latest[0]


def latest_at_or_before(
    items: list[dict],
    cutoff: datetime,
    label: str,
    errors: list[str],
) -> dict | None:
    if not items:
        return None
    parsed: list[tuple[datetime, dict]] = []
    for index, item in enumerate(items):
        stamp = parse_time(item.get("time"), f"{label}[{index}].time", errors)
        if stamp is not None and stamp <= cutoff:
            parsed.append((stamp, item))
    if not parsed:
        return None
    max_time = max(stamp for stamp, _ in parsed)
    latest = [item for stamp, item in parsed if stamp == max_time]
    if len(latest) != 1:
        errors.append(f"consistency: {label} has tied latest timestamps at/before snapshot")
        return None
    return latest[0]


def _validate_selection_snapshot(
    selection: object,
    experiments: list[dict],
    evaluations: list[dict],
    *,
    history_label: str,
    message_prefix: str,
    errors: list[str],
) -> dict | None:
    latest_eval = latest_by_time(evaluations, history_label, errors) if evaluations else None
    if selection != "UNASSESSED":
        if not experiments:
            errors.append(f"consistency: {message_prefix}non-UNASSESSED selection requires represented experiment")
        if not evaluations:
            errors.append(f"consistency: {message_prefix}non-UNASSESSED selection requires represented evaluation")
        elif latest_eval:
            if latest_eval.get("selection") != selection:
                errors.append(f"consistency: latest {message_prefix}evaluation selection must match {message_prefix}selection state")
            outcomes = latest_eval.get("outcomes") or {}
            evidence = latest_eval.get("evidence_refs") or []
            tradeoffs = latest_eval.get("tradeoffs") or []
            values = set(outcomes.values()) if isinstance(outcomes, dict) else set()
            if selection in POSITIVE:
                if "IMPROVED" not in values:
                    errors.append(f"consistency: positive {message_prefix}selection requires IMPROVED outcome")
                if not evidence:
                    errors.append(f"consistency: positive {message_prefix}selection requires evidence reference")
                if selection == "SUPPORTED" and "DEGRADED" in values and not tradeoffs:
                    errors.append(
                        f"consistency: SUPPORTED {message_prefix}selection with represented DEGRADED outcome requires explicit tradeoffs or PARTIAL"
                    )
            elif selection == "HARMFUL":
                if "DEGRADED" not in values:
                    errors.append(f"consistency: HARMFUL {message_prefix}selection requires DEGRADED outcome")
                if not evidence:
                    errors.append(f"consistency: HARMFUL {message_prefix}selection requires evidence reference")
            elif selection == "NOT_SUPPORTED":
                if not outcomes:
                    errors.append(f"consistency: NOT_SUPPORTED {message_prefix}selection requires represented outcomes")
                if not evidence:
                    errors.append(f"consistency: NOT_SUPPORTED {message_prefix}selection requires evidence reference")
    return latest_eval


def validate_transferred_source_history(packet: dict) -> list[str]:
    """Validate represented source-history shape/consistency without authenticating it."""
    schema = load_json(SCHEMA_PATH)
    errors: list[str] = []
    mapping = {
        "source_experiments": "experiments",
        "source_evaluations": "evaluations",
        "source_expression_history": "expression_history",
        "source_integration_history": "integration_history",
    }
    for packet_key, record_key in mapping.items():
        items = packet.get(packet_key) or []
        if not isinstance(items, list):
            continue
        item_schema = schema["properties"][record_key]["items"]
        item_validator = Draft202012Validator(item_schema, format_checker=FormatChecker())
        for index, item in enumerate(items):
            for error in item_validator.iter_errors(item):
                errors.append(f"source-history: {packet_key}[{index}] {error.message}")

    if "source_archive" in packet:
        archive_validator = Draft202012Validator(
            schema["properties"]["archive"],
            format_checker=FormatChecker(),
        )
        for error in archive_validator.iter_errors(packet.get("source_archive")):
            errors.append(f"source-history: source_archive {error.message}")

    experiments = packet.get("source_experiments") or []
    evaluations = packet.get("source_evaluations") or []
    _validate_selection_snapshot(
        packet.get("source_selection_state"),
        experiments if isinstance(experiments, list) else [],
        evaluations if isinstance(evaluations, list) else [],
        history_label="source_evaluations",
        message_prefix="source ",
        errors=errors,
    )

    lifecycle = packet.get("source_lifecycle_state")
    integrations = packet.get("source_integration_history") or []
    if lifecycle == "PROPOSED" and experiments:
        errors.append("consistency: source PROPOSED cannot contain represented experiments")
    if lifecycle == "EXPERIMENTED" and not experiments:
        errors.append("consistency: source EXPERIMENTED requires represented experiment")
    if lifecycle == "INTEGRATED":
        if not experiments or not evaluations:
            errors.append("consistency: source INTEGRATED requires represented experiment and evaluation")
        if not integrations:
            errors.append("consistency: source INTEGRATED requires integration history")
        elif isinstance(integrations, list):
            latest_integration = latest_by_time(integrations, "source_integration_history", errors)
            if latest_integration and latest_integration.get("result") != "COMMITTED":
                errors.append("consistency: source INTEGRATED requires latest integration result COMMITTED")
    if lifecycle in {"ARCHIVED", "RETIRED"}:
        archive = packet.get("source_archive")
        if not isinstance(archive, dict):
            errors.append("consistency: source ARCHIVED/RETIRED requires represented archive metadata")
        elif archive.get("selection_state_preserved") != packet.get("source_selection_state"):
            errors.append("consistency: source archive.selection_state_preserved must match source selection state")

    return errors


def validate_record(record: dict) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    errors = [
        f"schema: {e.message}"
        for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record)
    ]
    parse_time(record.get("created_at"), "created_at", errors)

    history = record.get("expression_history") or []
    current_expr = record.get("expression_state")
    lifecycle = record.get("lifecycle_state")
    selection = record.get("selection_state")
    obligation_refs = record.get("triggered_obligation_refs") or []

    if current_expr == "EXPRESSED" and not history:
        errors.append("consistency: EXPRESSED requires represented expression history")
    latest_expr = latest_by_time(history, "expression_history", errors) if history else None
    if latest_expr:
        if latest_expr.get("state") != current_expr:
            errors.append("consistency: latest expression history state must match expression_state")
        if latest_expr.get("state") == "EXPRESSED" and not str(latest_expr.get("trigger", "")).strip():
            errors.append("consistency: EXPRESSED transition requires non-empty represented trigger")

    if current_expr == "EXPRESSED":
        if selection in NEGATIVE or lifecycle in {"ARCHIVED", "RETIRED"}:
            if not obligation_refs:
                errors.append(
                    "consistency: harmful/not-supported or archived/retired EXPRESSED state requires triggered_obligation_refs"
                )
        if latest_expr and latest_expr.get("effect_materiality") == "MATERIAL":
            if record.get("variation_space") is None and not obligation_refs:
                errors.append(
                    "consistency: materially consequential EXPRESSED state requires Variation Space or triggered obligation"
                )

    experiments = record.get("experiments") or []
    evaluations = record.get("evaluations") or []

    if lifecycle == "PROPOSED" and experiments:
        errors.append("consistency: PROPOSED cannot contain represented experiments")
    if lifecycle == "EXPERIMENTED" and not experiments:
        errors.append("consistency: EXPERIMENTED requires represented experiment")

    latest_eval = _validate_selection_snapshot(
        selection,
        experiments,
        evaluations,
        history_label="evaluations",
        message_prefix="",
        errors=errors,
    )

    if record.get("origin") == "MIGRATION_CANDIDATE":
        migration = record.get("migration")
        if not isinstance(migration, dict):
            errors.append("consistency: MIGRATION_CANDIDATE requires represented migration provenance")
        else:
            if record.get("source_candidate_id") != migration.get("source_candidate_id"):
                errors.append(
                    "consistency: top-level source_candidate_id must match migration.source_candidate_id"
                )
            if record.get("source_packet_sha256") != migration.get("packet_sha256"):
                errors.append(
                    "consistency: top-level source_packet_sha256 must match migration.packet_sha256"
                )
            expected_purpose = expected_packet_purpose(migration.get("source_selection_state"))
            if migration.get("packet_purpose") != expected_purpose:
                errors.append(
                    "consistency: migration.packet_purpose must match migration.source_selection_state"
                )
            errors.extend(validate_transferred_source_history(migration))
        if selection != "UNASSESSED":
            for index, item in enumerate(experiments):
                if item.get("provenance") != "LOCAL":
                    errors.append(
                        f"consistency: migrated candidate local experiment[{index}] must declare provenance LOCAL"
                    )
            for index, item in enumerate(evaluations):
                if item.get("provenance") != "LOCAL":
                    errors.append(
                        f"consistency: migrated candidate local evaluation[{index}] must declare provenance LOCAL"
                    )

    if lifecycle == "INTEGRATED":
        if not experiments or not evaluations:
            errors.append("consistency: INTEGRATED requires represented experiment and evaluation")
        integrations = record.get("integration_history") or []
        if not integrations:
            errors.append("consistency: INTEGRATED requires integration history")
        else:
            latest_integration = latest_by_time(integrations, "integration_history", errors)
            if latest_integration and latest_integration.get("result") != "COMMITTED":
                errors.append("consistency: INTEGRATED requires latest integration result COMMITTED")
            if latest_integration and latest_integration.get("result") == "COMMITTED":
                integration_time = parse_time(latest_integration.get("time"), "latest integration time", errors)
                if integration_time is not None:
                    experiment_at_commit = False
                    for index, experiment in enumerate(experiments):
                        experiment_time = parse_time(
                            experiment.get("time"), f"experiments@integration[{index}].time", errors
                        )
                        if experiment_time is not None and experiment_time <= integration_time:
                            experiment_at_commit = True
                    if not experiment_at_commit:
                        errors.append(
                            "consistency: COMMITTED integration requires represented experiment at/before commit"
                        )

                    evaluation_at_commit = latest_at_or_before(
                        evaluations, integration_time, "evaluations@integration", errors
                    )
                    commit_selection = latest_integration.get("selection_state_at_commit")
                    if evaluation_at_commit is None:
                        errors.append(
                            "consistency: COMMITTED integration requires represented evaluation at/before commit"
                        )
                    elif evaluation_at_commit.get("selection") != commit_selection:
                        errors.append(
                            "consistency: integration selection_state_at_commit must match latest represented evaluation at/before commit"
                        )

                    if "expression_state_at_commit" in latest_integration:
                        expression_at_commit = latest_at_or_before(
                            history, integration_time, "expression_history@integration", errors
                        )
                        expected_expression = (
                            expression_at_commit.get("state") if expression_at_commit else "LATENT"
                        )
                        if latest_integration.get("expression_state_at_commit") != expected_expression:
                            errors.append(
                                "consistency: integration expression_state_at_commit must match represented expression state at/before commit"
                            )

    if lifecycle in {"ARCHIVED", "RETIRED"}:
        archive = record.get("archive")
        if not isinstance(archive, dict):
            errors.append("consistency: ARCHIVED/RETIRED requires represented archive metadata")
        elif archive.get("selection_state_preserved") != selection:
            errors.append("consistency: archive.selection_state_preserved must match selection_state")

    return errors


def exp_record(base: dict) -> dict:
    item = copy.deepcopy(base)
    item["lifecycle_state"] = "EXPERIMENTED"
    item["variation_space"] = "sandbox"
    item["experiments"] = [{
        "experiment_id": "exp-1",
        "time": "2026-08-24T00:00:00Z",
        "actual_change": "test change",
        "variation_space": "sandbox",
        "provenance": "LOCAL",
    }]
    return item


def selftest() -> None:
    base = load_json(TEMPLATE_PATH)
    template_errors = validate_record(base)
    assert any("created_at" in error for error in template_errors), "uninstantiated template unexpectedly passed created_at validation"
    base["created_at"] = "2026-08-24T00:00:00Z"

    # 1: legitimate dormant possibility has no current experiment surface or verdict.
    assert not validate_record(base), validate_record(base)

    # 2: false expression claim with no trace must fail.
    bad = copy.deepcopy(base)
    bad["expression_state"] = "EXPRESSED"
    assert validate_record(bad), "EXPRESSED without history unexpectedly passed"

    # 3: chronological expression contradiction must fail even when array order is misleading.
    bad = copy.deepcopy(base)
    bad["expression_state"] = "EXPRESSED"
    bad["expression_history"] = [
        {
            "expression_id": "expr-new",
            "time": "2026-08-24T02:00:00Z",
            "state": "LATENT",
            "trigger": "task ended",
            "effect_materiality": "NON_MATERIAL",
        },
        {
            "expression_id": "expr-old",
            "time": "2026-08-24T01:00:00Z",
            "state": "EXPRESSED",
            "trigger": "task cue",
            "effect_materiality": "NON_MATERIAL",
        },
    ]
    assert validate_record(bad), "chronologically stale trailing expression unexpectedly won"

    # 4: represented expression with trigger may remain UNASSESSED if no selection claim is made.
    good = copy.deepcopy(base)
    good["expression_state"] = "EXPRESSED"
    good["expression_history"] = [{
        "expression_id": "expr-2",
        "time": "2026-08-24T01:00:00Z",
        "state": "EXPRESSED",
        "trigger": "relevant task cue",
        "effect_materiality": "NON_MATERIAL",
    }]
    assert not validate_record(good), validate_record(good)

    # 5: expression can return to dormancy without manufacturing selection.
    good["expression_state"] = "LATENT"
    good["expression_history"].append({
        "expression_id": "expr-3",
        "time": "2026-08-24T02:00:00Z",
        "state": "LATENT",
        "trigger": "task ended",
        "effect_materiality": "NON_MATERIAL",
    })
    assert not validate_record(good), validate_record(good)
    assert good["selection_state"] == "UNASSESSED"

    # 6: UNKNOWN selection without experiment is not a shortcut around reality contact.
    bad = copy.deepcopy(base)
    bad["selection_state"] = "UNKNOWN"
    bad["evaluations"] = [{
        "evaluation_id": "eval-0",
        "time": "2026-08-24T00:00:00Z",
        "outcomes": {},
        "selection": "UNKNOWN",
        "evidence_refs": [],
    }]
    assert validate_record(bad), "UNKNOWN without experiment unexpectedly passed"

    # 7: positive selection without IMPROVED evidence must fail.
    bad = exp_record(base)
    bad["selection_state"] = "SUPPORTED"
    bad["evaluations"] = [{
        "evaluation_id": "eval-1",
        "time": "2026-08-24T01:00:00Z",
        "outcomes": {"quality": "UNCHANGED"},
        "selection": "SUPPORTED",
        "evidence_refs": ["e1"],
        "provenance": "LOCAL",
    }]
    assert validate_record(bad), "SUPPORTED without IMPROVED unexpectedly passed"

    # 8: positive selection without evidence ref must fail.
    bad = exp_record(base)
    bad["selection_state"] = "SUPPORTED"
    bad["evaluations"] = [{
        "evaluation_id": "eval-2",
        "time": "2026-08-24T01:00:00Z",
        "outcomes": {"quality": "IMPROVED"},
        "selection": "SUPPORTED",
        "evidence_refs": [],
        "provenance": "LOCAL",
    }]
    assert validate_record(bad), "SUPPORTED without evidence unexpectedly passed"

    # 9: evidence-backed local positive selection is structurally consistent.
    good2 = exp_record(base)
    good2["selection_state"] = "SUPPORTED"
    good2["evaluations"] = [{
        "evaluation_id": "eval-3",
        "time": "2026-08-24T01:00:00Z",
        "outcomes": {"quality": "IMPROVED"},
        "selection": "SUPPORTED",
        "evidence_refs": ["trace:local"],
        "provenance": "LOCAL",
    }]
    assert not validate_record(good2), validate_record(good2)

    # 10: integrated state cannot self-assert with an empty/arbitrary integration object.
    bad = copy.deepcopy(good2)
    bad["lifecycle_state"] = "INTEGRATED"
    bad["integration_history"] = [{}]
    assert validate_record(bad), "INTEGRATED with empty integration object unexpectedly passed"

    # 11: valid committed integration preserves selection/authority/recovery representation.
    good3 = copy.deepcopy(good2)
    good3["lifecycle_state"] = "INTEGRATED"
    good3["integration_history"] = [{
        "integration_id": "int-1",
        "time": "2026-08-24T02:00:00Z",
        "target": "runtime",
        "authority_basis": "owner-approved",
        "recovery_boundary": "state-only",
        "result": "COMMITTED",
        "selection_state_at_commit": "SUPPORTED",
        "expression_state_at_commit": "LATENT",
    }]
    assert not validate_record(good3), validate_record(good3)

    # 12: chronologically later harmful evidence cannot be hidden before an older trailing positive result.
    bad = exp_record(base)
    bad["selection_state"] = "SUPPORTED"
    bad["evaluations"] = [
        {
            "evaluation_id": "eval-new-harm",
            "time": "2026-08-24T03:00:00Z",
            "outcomes": {"quality": "DEGRADED"},
            "selection": "HARMFUL",
            "evidence_refs": ["trace:harm"],
            "provenance": "LOCAL",
        },
        {
            "evaluation_id": "eval-old-good",
            "time": "2026-08-24T02:00:00Z",
            "outcomes": {"quality": "IMPROVED"},
            "selection": "SUPPORTED",
            "evidence_refs": ["trace:old"],
            "provenance": "LOCAL",
        },
    ]
    assert validate_record(bad), "chronologically stale trailing evaluation unexpectedly won"

    # 13: tied latest evaluation timestamps are ambiguous and must fail.
    bad = exp_record(base)
    bad["selection_state"] = "SUPPORTED"
    bad["evaluations"] = [
        {
            "evaluation_id": "eval-a",
            "time": "2026-08-24T02:00:00Z",
            "outcomes": {"quality": "IMPROVED"},
            "selection": "SUPPORTED",
            "evidence_refs": ["a"],
            "provenance": "LOCAL",
        },
        {
            "evaluation_id": "eval-b",
            "time": "2026-08-24T02:00:00Z",
            "outcomes": {"quality": "DEGRADED"},
            "selection": "HARMFUL",
            "evidence_refs": ["b"],
            "provenance": "LOCAL",
        },
    ]
    assert validate_record(bad), "tied latest evaluations unexpectedly passed"

    # 14: mixed positive/negative outcomes cannot silently claim clean SUPPORTED without tradeoffs.
    bad = exp_record(base)
    bad["selection_state"] = "SUPPORTED"
    bad["evaluations"] = [{
        "evaluation_id": "eval-mixed",
        "time": "2026-08-24T02:00:00Z",
        "outcomes": {"speed": "IMPROVED", "data_loss": "DEGRADED"},
        "selection": "SUPPORTED",
        "evidence_refs": ["trace:mixed"],
        "provenance": "LOCAL",
    }]
    assert validate_record(bad), "mixed outcomes unexpectedly passed as unqualified SUPPORTED"

    # 15: explicit tradeoff can preserve a scoped SUPPORTED claim when the caller represents the tradeoff.
    good4 = copy.deepcopy(bad)
    good4["evaluations"][0]["tradeoffs"] = ["data_loss degraded; support limited to speed objective"]
    assert not validate_record(good4), validate_record(good4)

    # 16: harmful/retired current expression requires a represented triggered obligation.
    bad = copy.deepcopy(good2)
    bad["lifecycle_state"] = "RETIRED"
    bad["selection_state"] = "HARMFUL"
    bad["evaluations"] = [{
        "evaluation_id": "eval-h",
        "time": "2026-08-24T02:00:00Z",
        "outcomes": {"quality": "DEGRADED"},
        "selection": "HARMFUL",
        "evidence_refs": ["trace:h"],
        "provenance": "LOCAL",
    }]
    bad["archive"] = {
        "time": "2026-08-24T02:30:00Z",
        "reason": "harmful",
        "selection_state_preserved": "HARMFUL",
    }
    bad["expression_state"] = "EXPRESSED"
    bad["expression_history"] = [{
        "expression_id": "expr-h",
        "time": "2026-08-24T03:00:00Z",
        "state": "EXPRESSED",
        "trigger": "still routed",
        "effect_materiality": "NON_MATERIAL",
    }]
    assert validate_record(bad), "harmful retired expression without obligation unexpectedly passed"
    bad["triggered_obligation_refs"] = ["obligation:stop-or-authorize"]
    assert not validate_record(bad), validate_record(bad)

    # 17: materially consequential expression needs Variation Space or a triggered obligation.
    bad = copy.deepcopy(base)
    bad["expression_state"] = "EXPRESSED"
    bad["expression_history"] = [{
        "expression_id": "expr-material",
        "time": "2026-08-24T01:00:00Z",
        "state": "EXPRESSED",
        "trigger": "production route",
        "effect_boundary": "external email send",
        "effect_materiality": "MATERIAL",
    }]
    assert validate_record(bad), "material expression without consequence ownership unexpectedly passed"
    bad["triggered_obligation_refs"] = ["obligation:consequence-owner"]
    assert not validate_record(bad), validate_record(bad)

    # 18: archived/retired lifecycle requires archive metadata.
    bad = copy.deepcopy(base)
    bad["lifecycle_state"] = "ARCHIVED"
    assert validate_record(bad), "ARCHIVED without archive metadata unexpectedly passed"

    # 19: archive preservation metadata may faithfully preserve the current selection state.
    good_archive = copy.deepcopy(good2)
    good_archive["lifecycle_state"] = "ARCHIVED"
    good_archive["archive"] = {
        "time": "2026-08-24T02:30:00Z",
        "reason": "bounded archive",
        "selection_state_preserved": "SUPPORTED",
    }
    assert not validate_record(good_archive), validate_record(good_archive)

    # 20: archive metadata cannot contradict the selection truth it claims to preserve.
    bad_archive = copy.deepcopy(good_archive)
    bad_archive["archive"]["selection_state_preserved"] = "HARMFUL"
    assert validate_record(bad_archive), "contradictory archive preservation metadata unexpectedly passed"

    # 21: integration cannot claim support before represented support evidence exists.
    early_integration = copy.deepcopy(good2)
    early_integration["evaluations"][0]["time"] = "2026-08-24T03:00:00Z"
    early_integration["lifecycle_state"] = "INTEGRATED"
    early_integration["integration_history"] = [{
        "integration_id": "int-early",
        "time": "2026-08-24T02:00:00Z",
        "target": "runtime",
        "result": "COMMITTED",
        "selection_state_at_commit": "SUPPORTED",
        "expression_state_at_commit": "LATENT",
    }]
    assert validate_record(early_integration), "integration support claim before evidence unexpectedly passed"

    # 22: integration snapshot must match support already represented at commit time.
    bad_snapshot = copy.deepcopy(good3)
    bad_snapshot["integration_history"][0]["selection_state_at_commit"] = "UNKNOWN"
    assert validate_record(bad_snapshot), "integration selection snapshot mismatch unexpectedly passed"

    # 23: later evidence may legitimately change current selection without rewriting commit history.
    post_commit = copy.deepcopy(good3)
    post_commit["evaluations"].append({
        "evaluation_id": "eval-post-harm",
        "time": "2026-08-24T03:00:00Z",
        "outcomes": {"quality": "DEGRADED"},
        "selection": "HARMFUL",
        "evidence_refs": ["trace:post-harm"],
        "provenance": "LOCAL",
    })
    post_commit["selection_state"] = "HARMFUL"
    assert not validate_record(post_commit), validate_record(post_commit)

    # 24: expression snapshot at commit cannot contradict represented expression history.
    bad_expression_snapshot = copy.deepcopy(good3)
    bad_expression_snapshot["expression_state"] = "EXPRESSED"
    bad_expression_snapshot["expression_history"] = [{
        "expression_id": "expr-before-commit",
        "time": "2026-08-24T01:30:00Z",
        "state": "EXPRESSED",
        "trigger": "runtime cue",
        "effect_materiality": "NON_MATERIAL",
    }]
    bad_expression_snapshot["integration_history"][0]["expression_state_at_commit"] = "LATENT"
    assert validate_record(bad_expression_snapshot), "integration expression snapshot mismatch unexpectedly passed"

    # 25: sealed A-S chronology shape cannot integrate before all represented reality contact.
    bad_precontact = copy.deepcopy(good2)
    bad_precontact["experiments"][0]["time"] = "2026-08-24T03:00:00Z"
    bad_precontact["evaluations"][0]["time"] = "2026-08-24T04:00:00Z"
    bad_precontact["lifecycle_state"] = "INTEGRATED"
    bad_precontact["integration_history"] = [{
        "integration_id": "int-before-contact",
        "time": "2026-08-24T02:00:00Z",
        "target": "runtime",
        "result": "COMMITTED",
        "selection_state_at_commit": "UNKNOWN",
        "expression_state_at_commit": "LATENT",
    }]
    assert validate_record(bad_precontact), "integration before represented reality contact unexpectedly passed"

    # 26: unresolved UNKNOWN integration remains legitimate after real represented contact.
    unresolved_then_supported = copy.deepcopy(good2)
    unresolved_then_supported["experiments"][0]["time"] = "2026-08-24T01:00:00Z"
    unresolved_then_supported["evaluations"] = [
        {
            "evaluation_id": "eval-unresolved",
            "time": "2026-08-24T01:30:00Z",
            "outcomes": {"quality": "UNKNOWN"},
            "selection": "UNKNOWN",
            "evidence_refs": ["trace:unresolved"],
            "provenance": "LOCAL",
        },
        {
            "evaluation_id": "eval-later-supported",
            "time": "2026-08-24T03:00:00Z",
            "outcomes": {"quality": "IMPROVED"},
            "selection": "SUPPORTED",
            "evidence_refs": ["trace:later-supported"],
            "provenance": "LOCAL",
        },
    ]
    unresolved_then_supported["selection_state"] = "SUPPORTED"
    unresolved_then_supported["lifecycle_state"] = "INTEGRATED"
    unresolved_then_supported["integration_history"] = [{
        "integration_id": "int-unresolved",
        "time": "2026-08-24T02:00:00Z",
        "target": "runtime",
        "result": "COMMITTED",
        "selection_state_at_commit": "UNKNOWN",
        "expression_state_at_commit": "LATENT",
        "residuals": ["quality unresolved at commit"],
    }]
    assert not validate_record(unresolved_then_supported), validate_record(unresolved_then_supported)

    valid_migration = copy.deepcopy(base)
    valid_migration["origin"] = "MIGRATION_CANDIDATE"
    valid_migration["source_candidate_id"] = "source-A"
    valid_migration["source_packet_sha256"] = "a" * 64
    valid_migration["migration"] = {
        "source_candidate_id": "source-A",
        "source_selection_state": "UNASSESSED",
        "source_lifecycle_state": "PROPOSED",
        "packet_purpose": "UNRESOLVED_VARIATION",
        "transfer_status": "TRANSFERRED_NOT_LOCALLY_VALIDATED",
        "source_authentication": "NOT_AUTHENTICATED_BY_THIS_PACKET",
        "packet_sha256": "a" * 64,
        "source_negative_lineage_refs": [],
        "source_experiments": [],
        "source_evaluations": [],
        "source_integration_history": [],
    }

    # 27: internally consistent migration provenance remains lightweight/local-UNASSESSED.
    assert not validate_record(valid_migration), validate_record(valid_migration)

    # 28: duplicated source candidate identity cannot contradict itself.
    bad_migration = copy.deepcopy(valid_migration)
    bad_migration["migration"]["source_candidate_id"] = "source-B"
    assert validate_record(bad_migration), "contradictory migration source candidate identity unexpectedly passed"

    # 29: duplicated packet digest cannot contradict itself.
    bad_migration = copy.deepcopy(valid_migration)
    bad_migration["migration"]["packet_sha256"] = "b" * 64
    assert validate_record(bad_migration), "contradictory migration packet digest unexpectedly passed"

    # 30: packet purpose cannot invert represented source selection semantics.
    bad_migration = copy.deepcopy(valid_migration)
    bad_migration["migration"]["source_selection_state"] = "HARMFUL"
    bad_migration["migration"]["packet_purpose"] = "ADAPTATION_CANDIDATE"
    assert validate_record(bad_migration), "contradictory migration packet purpose unexpectedly passed"

    # 31: a durable migrated record may preserve internally consistent source support
    # while receiver-local selection remains UNASSESSED.
    supported_source = copy.deepcopy(valid_migration)
    supported_source["migration"]["source_selection_state"] = "SUPPORTED"
    supported_source["migration"]["source_lifecycle_state"] = "INTEGRATED"
    supported_source["migration"]["packet_purpose"] = "ADAPTATION_CANDIDATE"
    supported_source["migration"]["source_experiments"] = [{
        "experiment_id": "source-exp-1",
        "time": "2026-08-20T00:00:00Z",
        "actual_change": "source test",
        "provenance": "LOCAL",
    }]
    supported_source["migration"]["source_evaluations"] = [{
        "evaluation_id": "source-eval-1",
        "time": "2026-08-20T01:00:00Z",
        "outcomes": {"quality": "IMPROVED"},
        "selection": "SUPPORTED",
        "evidence_refs": ["source:trace"],
        "provenance": "LOCAL",
    }]
    supported_source["migration"]["source_integration_history"] = [{
        "integration_id": "source-int-1",
        "time": "2026-08-20T02:00:00Z",
        "target": "source-runtime",
        "result": "COMMITTED",
        "selection_state_at_commit": "SUPPORTED",
    }]
    assert supported_source["selection_state"] == "UNASSESSED"
    assert not validate_record(supported_source), validate_record(supported_source)

    # 32: durable source support/integration cannot survive as an empty history shell.
    shallow_source = copy.deepcopy(supported_source)
    shallow_source["migration"]["source_experiments"] = []
    shallow_source["migration"]["source_evaluations"] = []
    shallow_source["migration"]["source_integration_history"] = []
    assert validate_record(shallow_source), "shallow durable supported source history unexpectedly passed"

    print("EVOLUTION_RECORD_V2_SELFTEST_PASS 32")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return
    if not args.path:
        parser.error("path required unless --selftest is used")
    record = load_json(Path(args.path))
    errors = validate_record(record)
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()

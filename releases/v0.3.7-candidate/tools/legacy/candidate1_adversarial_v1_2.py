#!/usr/bin/env python3
"""Legacy v1.2 candidate.1 adversarial regression probes.

These are regression tests for independently reproduced v0.3.5 frozen-candidate
failures. They exercise the explicitly legacy v1.2 tool and do not prove
external authority/evidence/recovery truth or v0.3.7 v2 parity.
"""
from __future__ import annotations
import importlib.util
import json
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "ena_evolve_v1_2.py"

spec = importlib.util.spec_from_file_location("ena_evolve_candidate1_v1_2", TOOL)
ee = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(ee)

def expect_system_exit(fn, label: str) -> None:
    try:
        fn()
    except SystemExit:
        return
    raise AssertionError(f"expected rejection: {label}")

def base_candidate(selection="UNASSESSED", lifecycle="EXPERIMENTED"):
    return {
        "candidate_id": "var-test",
        "created_at": ee.now(),
        "origin": "LOCAL_VARIATION",
        "lifecycle_state": lifecycle,
        "selection_state": selection,
        "signal_refs": [],
        "hypothesis": "test",
        "change": "test change",
        "expected_outcomes": ["quality"],
        "variation_space": "sandbox",
        "evolutionary_subject": "test-subject",
        "protected_subjects": [],
        "environment": {"host": "probe"},
        "dependencies": [],
        "unknowns": [],
        "observation_plan": "observe quality",
        "experiments": [{"experiment_id": "exp-1", "time": ee.now(), "actual_change": "change"}],
        "evaluations": [],
        "integration_history": [],
        "archive": None,
        "migration": None,
    }

def main() -> int:
    results = {}

    zero = base_candidate()
    zero["experiments"] = []
    expect_system_exit(
        lambda: ee.validate_evaluation(zero, "SUPPORTED", {"quality": "IMPROVED"}, ["claim"]),
        "zero-experiment SUPPORTED",
    )
    results["zero_experiment_positive_rejected"] = True

    harmful = base_candidate("HARMFUL", "ARCHIVED")
    harmful["evaluations"] = [{
        "evaluation_id": "eval-harm",
        "time": ee.now(),
        "outcomes": {"quality": "DEGRADED"},
        "selection": "HARMFUL",
        "evidence_refs": ["harm-observation"],
    }]
    packet = ee.migration_packet(harmful)
    ee.validate_packet(packet)
    assert packet["packet_purpose"] == "NEGATIVE_EVIDENCE"
    assert packet["source_selection_state"] == "HARMFUL"
    assert packet["source_lifecycle_state"] == "ARCHIVED"
    results["archive_preserves_harmful_selection"] = True

    unknown = base_candidate("UNKNOWN", "INTEGRATED")
    unknown["evaluations"] = [{
        "evaluation_id": "eval-u",
        "time": ee.now(),
        "outcomes": {},
        "selection": "UNKNOWN",
        "evidence_refs": [],
    }]
    up = ee.migration_packet(unknown)
    ee.validate_packet(up)
    assert up["packet_purpose"] == "UNRESOLVED_VARIATION"
    assert up["source_selection_state"] == "UNKNOWN"
    results["integrated_unknown_stays_unresolved"] = True

    contradictory = dict(packet)
    contradictory["packet_purpose"] = "ADAPTATION_CANDIDATE"
    contradictory.pop("content_sha256")
    contradictory["content_sha256"] = ee.canonical_digest(contradictory)
    expect_system_exit(lambda: ee.validate_packet(contradictory), "contradictory migration packet")
    results["contradictory_packet_rejected"] = True

    with tempfile.TemporaryDirectory(prefix="ena-c1-probe-") as td:
        td = Path(td)
        state_path = td / "state.json"
        ee.atomic_write(state_path, ee.empty_state())
        packet_path = td / "harmful.json"
        packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        args = type("Args", (), {
            "state": str(state_path),
            "packet": str(packet_path),
            "variation_space": "receiver-sandbox",
            "evolutionary_subject": "receiver",
            "protected_subject": [],
            "environment": [],
            "difference": [],
            "unknown": [],
            "observe": "local observation",
        })()
        ee.cmd_import(args)
        imported = ee.load_state(state_path)["candidates"][0]
        assert imported["selection_state"] == "UNASSESSED"
        assert imported["migration"]["source_selection_state"] == "HARMFUL"
        expect_system_exit(
            lambda: ee.validate_evaluation(imported, "SUPPORTED", {"quality": "IMPROVED"}, ["local-claim"]),
            "imported negative evidence promoted without local experiment",
        )
    results["negative_transfer_requires_local_experiment_for_positive_reselection"] = True

    state = ee.empty_state()
    state["candidates"] = [base_candidate("UNASSESSED", "EXPERIMENTED")]
    assert ee.closure_state_obligations(state, None)
    results["closure_reads_unresolved_state"] = True

    print(json.dumps({"candidate1_adversarial_v1_2": "PASS", "results": results}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

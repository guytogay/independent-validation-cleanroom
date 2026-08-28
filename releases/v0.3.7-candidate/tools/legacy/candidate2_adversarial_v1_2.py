#!/usr/bin/env python3
"""Legacy v1.2 candidate.2 adversarial regressions.

These probes retain residual N1/N2 and adjacent packet-consistency regressions
against the explicitly legacy v1.2 tool. They do not prove external source
identity, authority, evidence, recovery truth, or v0.3.7 v2 parity.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "ena_evolve_v1_2.py"

spec = importlib.util.spec_from_file_location("ena_evolve_candidate2_v1_2", TOOL)
ee = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(ee)


def expect_reject(packet: dict, label: str) -> None:
    packet = dict(packet)
    packet.pop("content_sha256", None)
    packet["content_sha256"] = ee.canonical_digest(packet)
    try:
        ee.validate_packet(packet)
    except SystemExit:
        return
    raise AssertionError(f"expected rejection: {label}")


def main() -> int:
    candidate = {
        "candidate_id": "var-c2",
        "created_at": ee.now(),
        "origin": "LOCAL_VARIATION",
        "lifecycle_state": "EXPERIMENTED",
        "selection_state": "SUPPORTED",
        "signal_refs": [],
        "hypothesis": "candidate.2 packet guard",
        "change": "test",
        "expected_outcomes": ["quality"],
        "variation_space": "sandbox",
        "evolutionary_subject": "test",
        "protected_subjects": [],
        "environment": {"host": "probe"},
        "dependencies": [],
        "unknowns": [],
        "observation_plan": "observe",
        "experiments": [{"experiment_id": "exp-1", "time": ee.now(), "actual_change": "test"}],
        "evaluations": [{
            "evaluation_id": "eval-1",
            "time": ee.now(),
            "outcomes": {"quality": "IMPROVED"},
            "selection": "SUPPORTED",
            "evidence_refs": ["obs-1"],
        }],
        "integration_history": [],
        "archive": None,
        "migration": None,
    }

    packet = ee.migration_packet(candidate)
    ee.validate_packet(packet)

    expect_reject({**packet, "source_lifecycle_state": "BANANA"}, "invalid lifecycle enum")
    expect_reject({**packet, "source_authentication": "TOTALLY_TRUSTED"}, "forged source authentication")
    expect_reject({**packet, "transfer_status": "LOCALLY_PROVEN"}, "forged transfer status")

    assert packet["source_authentication"] == "NOT_AUTHENTICATED_BY_THIS_PACKET"
    assert packet["transfer_status"] == "TRANSFERRED_SOURCE_EVIDENCE_NOT_LOCAL_PROOF"

    print(json.dumps({
        "candidate2_adversarial_v1_2": "PASS",
        "results": {
            "invalid_lifecycle_rejected_by_cli": True,
            "forged_source_authentication_rejected_by_cli": True,
            "forged_transfer_status_rejected_by_cli": True,
        },
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

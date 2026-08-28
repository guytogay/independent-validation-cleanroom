#!/usr/bin/env python3
"""Portable adversarial selftest for Evidence Envelope research prototype."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            rows.append(json.loads(raw))
    return rows


def run(cmd: list[str], expect: int) -> None:
    print("+", " ".join(cmd))
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    if proc.returncode != expect:
        raise SystemExit(
            f"expected exit {expect}, got {proc.returncode}: {' '.join(cmd)}"
        )


def write_one(path: Path, row: dict) -> None:
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")


def by_id(rows: list[dict], case_id: str) -> dict:
    for row in rows:
        if row.get("case_id") == case_id:
            return copy.deepcopy(row)
    raise KeyError(case_id)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    validator = root / "tools" / "validate_evidence_envelope.py"
    fixtures = root / "fixtures" / "evidence-envelope-cases.jsonl"

    run([sys.executable, str(validator)], expect=0)
    rows = load_jsonl(fixtures)
    assert rows, "evidence-envelope fixture corpus must not be empty"
    ids = [row.get("case_id") for row in rows]
    assert len(ids) == len(set(ids)), "duplicate case_id"
    required_ids = {"EE-001", "EE-002", "EE-009", "EE-015", "EE-017"}
    assert required_ids <= set(ids), f"missing targeted regression fixtures: {sorted(required_ids - set(ids))}"

    with tempfile.TemporaryDirectory(prefix="ena-evidence-envelope-") as tmp:
        tmpdir = Path(tmp)

        row = by_id(rows, "EE-002")
        row["envelope"]["applicability"]["changed_dimensions"] = ["model:M1->M2"]
        path = tmpdir / "changed-dimension.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "EE-009")
        row["envelope"]["activation"]["claimed_level"] = "INVOKED"
        path = tmpdir / "activation-upgrade.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "EE-015")
        row["envelope"]["witness"]["failure_domain_ref"] = "HOST-X"
        path = tmpdir / "same-domain-witness.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "EE-017")
        del row["envelope"]["support"]["dependency_map_ref"]
        path = tmpdir / "corroboration-without-dependency.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "EE-001")
        row["envelope"]["completeness"] = {
            "complete": True,
            "claimed_complete_dimensions": ["all"],
            "known_missing_or_unknown": [],
        }
        path = tmpdir / "universal-complete.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

    print("PASS: evidence-envelope portable adversarial selftest")
    print(f"observed_fixture_count={len(rows)}")
    print("fixture_cardinality=OPEN_WITH_TARGETED_REGRESSION_DEPENDENCIES")
    print("verification_scope=REPRESENTED_CONSISTENCY_MUTATION_TESTS_ONLY")
    print("mechanism_retention=APPLICABILITY,PROJECTION,ACTIVATION,WITNESS,DEPENDENCY")
    print("external_truth=UNPROVEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

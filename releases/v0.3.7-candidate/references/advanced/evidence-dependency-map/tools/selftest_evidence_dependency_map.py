#!/usr/bin/env python3
"""Portable adversarial selftest for Evidence Dependency Map prototype."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(raw) for raw in path.read_text(encoding="utf-8").splitlines() if raw.strip()]


def by_id(rows: list[dict], case_id: str) -> dict:
    for row in rows:
        if row.get("case_id") == case_id:
            return copy.deepcopy(row)
    raise KeyError(case_id)


def write_one(path: Path, row: dict) -> None:
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")


def run(cmd: list[str], expect: int) -> None:
    print("+", " ".join(cmd))
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    if proc.returncode != expect:
        raise SystemExit(f"expected exit {expect}, got {proc.returncode}: {' '.join(cmd)}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    validator = root / "tools" / "validate_evidence_dependency_map.py"
    fixtures_path = root / "fixtures" / "evidence-dependency-map-cases.jsonl"

    run([sys.executable, str(validator)], expect=0)
    rows = load_jsonl(fixtures_path)
    assert rows, "dependency-map fixture corpus must not be empty"
    ids = [row.get("case_id") for row in rows]
    assert len(ids) == len(set(ids)), "duplicate case_id"
    required_ids = {"EDM-001", "EDM-005", "EDM-007", "EDM-011"}
    assert required_ids <= set(ids), f"missing targeted regression fixtures: {sorted(required_ids - set(ids))}"

    with tempfile.TemporaryDirectory(prefix="ena-edm-") as tmp:
        tmpdir = Path(tmp)

        row = by_id(rows, "EDM-001")
        row["map"]["edges"] = [
            e for e in row["map"]["edges"]
            if not (e["from"] == "O1" and e["to"] == "O2" and e["relation"] == "SHARED_SOURCE_EVIDENCE")
        ]
        path = tmpdir / "hidden-source.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "EDM-005")
        row["map"]["independence_score"] = 0.5
        path = tmpdir / "scalar-independence.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "EDM-007")
        row["map"]["edges"] = []
        path = tmpdir / "lost-lineage.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "EDM-005")
        path = tmpdir / "same-model-distinct-world.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=0)

        row = by_id(rows, "EDM-011")
        path = tmpdir / "recurrence-lightweight.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=0)

    print("PASS: evidence-dependency-map portable adversarial selftest")
    print(f"observed_fixture_count={len(rows)}")
    print("fixture_cardinality=OPEN_WITH_TARGETED_REGRESSION_DEPENDENCIES")
    print("verification_scope=KNOWN_DEPENDENCY_VISIBILITY_MUTATION_TESTS_ONLY")
    print("independence_score=NOT_COMPUTED")
    print("false_block_controls=SAME_MODEL_DISTINCT_WORLD,RECURRENCE_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

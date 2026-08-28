#!/usr/bin/env python3
"""Portable adversarial selftest for Contested Authorship prototype."""

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
    validator = root / "tools" / "validate_contested_authorship.py"
    fixtures_path = root / "fixtures" / "contested-authorship-cases.jsonl"

    run([sys.executable, str(validator)], expect=0)
    rows = load_jsonl(fixtures_path)
    assert rows, "authorship fixture corpus must not be empty"
    ids = [row.get("case_id") for row in rows]
    assert len(ids) == len(set(ids)), "duplicate case_id"
    required_ids = {"CA-001", "CA-004", "CA-010", "CA-013", "CA-014"}
    assert required_ids <= set(ids), f"missing targeted regression fixtures: {sorted(required_ids - set(ids))}"

    with tempfile.TemporaryDirectory(prefix="ena-authorship-") as tmp:
        tmpdir = Path(tmp)

        row = by_id(rows, "CA-004")
        row["record"]["authorship"]["claim"] = "SELF_AUTHORED"
        path = tmpdir / "authorship-laundering.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "CA-004")
        row["record"]["endorsement"]["status"] = "NOT_EVALUATED"
        path = tmpdir / "silent-endorsement.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "CA-010")
        del row["record"]["authority"]["external_authority_ref"]
        path = tmpdir / "authority-laundering.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "CA-013")
        row["record"]["conflict"]["disposition"] = "NONE"
        row["record"]["conflict"].pop("resolution_ref", None)
        path = tmpdir / "silent-conflict.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=1)

        row = by_id(rows, "CA-001")
        path = tmpdir / "low-heuristic.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=0)

        row = by_id(rows, "CA-014")
        path = tmpdir / "cache-out-of-scope.jsonl"
        write_one(path, row)
        run([sys.executable, str(validator), "--fixtures", str(path)], expect=0)

    print("PASS: contested-authorship portable adversarial selftest")
    print(f"observed_fixture_count={len(rows)}")
    print("fixture_cardinality=OPEN_WITH_TARGETED_REGRESSION_DEPENDENCIES")
    print("verification_scope=DURABLE_SELF_CHANGE_MUTATION_TESTS_ONLY")
    print("false_block_controls=LOW_HEURISTIC,CACHE_OUT_OF_SCOPE")
    print("external_authority=NOT_MINTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

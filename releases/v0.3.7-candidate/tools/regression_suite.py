#!/usr/bin/env python3
"""Inherited deterministic composed-validator regression suite.

This file intentionally exercises the byte-inherited v0.3.3/v0.3.4
`validate_contracts.py` implementation surface. Passing this suite proves
regression preservation only; it does NOT prove coverage of new v0.3.5
semantics such as evolution metabolism, migration, emergence, continuity, or
language portability.
"""
import sys, json
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import validate_contracts as vc

FIXTURES_V1 = HERE / "contract-fixtures.v1.json"
FIXTURES_V2 = HERE / "contract-fixtures.v2.json"
FIXTURES_V21 = HERE / "contract-fixtures.v2.1.json"


def run_fixture_file(path: Path, label: str):
    res = vc.run_selftest(str(path))
    results = res["results"]
    corpus = json.loads(path.read_text(encoding="utf-8"))
    cases_by_id = {c["id"]: c for c in corpus["cases"]}
    by_prov = {}
    unexpected = []
    exceptions = []
    verdicts = Counter()
    for r in results:
        case = cases_by_id.get(r["id"], {})
        prov = case.get("provenance", "UNKNOWN")
        by_prov.setdefault(prov, {"total": 0, "ok": 0})
        by_prov[prov]["total"] += 1
        if r["passed"]:
            by_prov[prov]["ok"] += 1
        else:
            unexpected.append(r)
        actual = r.get("actual") or {}
        verdicts[actual.get("verdict")] += 1
        if actual.get("verdict") == "EXCEPTION" or "EVALUATOR_FAULT" in str(actual.get("codes", [])):
            exceptions.append(r["id"])
    return {"label": label, "total": len(results), "failed": len(unexpected),
            "by_prov": by_prov, "unexpected": unexpected, "exceptions": exceptions,
            "verdicts": dict(verdicts)}


def main() -> int:
    print("=" * 100)
    print("V0.3.5 CURRENT INHERITED COMPOSED-VALIDATOR REGRESSION SUITE")
    print("=" * 100)

    v1 = run_fixture_file(FIXTURES_V1, "migrated v0.3.2 selftests")
    v2 = run_fixture_file(FIXTURES_V2, "inherited 164-case corpus")
    v21 = run_fixture_file(FIXTURES_V21, "successor closure corpus (PR#38 + D controls)")

    print("migrated v0.3.2 selftests : %d/%d passed" % (v1["total"] - v1["failed"], v1["total"]))
    print("inherited 164-case corpus : %d/%d passed (ZERO flips required)" % (v2["total"] - v2["failed"], v2["total"]))
    print("successor closure corpus  : %d/%d passed" % (v21["total"] - v21["failed"], v21["total"]))
    print()
    print("--- by provenance (inherited + closure) ---")
    for f in (v2, v21):
        for prov in sorted(f["by_prov"]):
            b = f["by_prov"][prov]
            print("  %-32s %d/%d passed" % (prov, b["ok"], b["total"]))
    print()
    all_unexpected = v1["unexpected"] + v2["unexpected"] + v21["unexpected"]
    all_exceptions = v1["exceptions"] + v2["exceptions"] + v21["exceptions"]
    print("--- unexpected verdicts / failures ---")
    for r in all_unexpected:
        a = r.get("actual") or {}
        print("  %-46s expected=%s actual=%s codes=%s" % (
            r["id"], json.dumps(r.get("expected")), a.get("verdict"), a.get("codes")))
    print()
    total_verdicts = Counter()
    for f in (v1, v2, v21):
        total_verdicts.update(f["verdicts"])
    print("verdict counts            : %s" % dict(total_verdicts))
    print("unexpected verdicts       : %d" % len(all_unexpected))
    print("uncaught exceptions       : %d" % len(all_exceptions))
    print()
    ok = (not all_unexpected) and (not all_exceptions)
    print("RESULT: %s" % ("PASS - inherited implementation regression preserved"
                          if ok else "FAIL"))

    out = {
        "implementation_surface": "releases/current/tools/validate_contracts.py",
        "implementation_lineage": "inherited validator surface released through v0.3.5 candidate.2 lineage",
        "coverage_boundary": "INHERITED_COMPOSED_VALIDATOR_ONLY_NOT_V035_NEW_SEMANTICS",
        "migrated_v032_selftest": {"total": v1["total"], "passed": v1["total"] - v1["failed"]},
        "inherited_v2": {"total": v2["total"], "passed": v2["total"] - v2["failed"]},
        "closure_v21": {"total": v21["total"], "passed": v21["total"] - v21["failed"]},
        "by_provenance": {prov: b for f in (v2, v21) for prov, b in f["by_prov"].items()},
        "verdict_counts": dict(total_verdicts),
        "unexpected_verdicts": [{"id": r["id"], "expected": r.get("expected"),
                                 "actual_verdict": (r.get("actual") or {}).get("verdict"),
                                 "actual_codes": (r.get("actual") or {}).get("codes")} for r in all_unexpected],
        "uncaught_exceptions": all_exceptions,
        "passed": ok,
    }
    (HERE / "regression-results-v033.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print()
    print("regression-results-v033.json written")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate research-only Evidence Dependency Map fixtures.

This checks represented common-cause visibility. It does not prove causal
independence/dependence or compute an independence score.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path}: expected object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise SystemExit(f"{path}:{lineno}: expected object")
        rows.append(value)
    return rows


def string_list(value: Any, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
        errors.append(f"{label} must be array[non-empty string]")
        return []
    return value


def nested_get(obj: dict[str, Any], path: str) -> Any:
    current: Any = obj
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def has_forbidden_key(value: Any, forbidden: set[str], found: list[str], prefix: str = "") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            if key in forbidden:
                found.append(path)
            has_forbidden_key(child, forbidden, found, path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            has_forbidden_key(child, forbidden, found, f"{prefix}[{index}]")


def edge_present(edge_set: set[tuple[str, str, str]], a: str, b: str, relation: str) -> bool:
    return (a, b, relation) in edge_set or (b, a, relation) in edge_set


def connected_components(nodes: list[str], edges: list[dict[str, Any]]) -> int:
    adjacency = {node: set() for node in nodes}
    for edge in edges:
        a = edge.get("from")
        b = edge.get("to")
        if a in adjacency and b in adjacency and a != b:
            adjacency[a].add(b)
            adjacency[b].add(a)
    seen: set[str] = set()
    count = 0
    for node in adjacency:
        if node in seen:
            continue
        count += 1
        stack = [node]
        seen.add(node)
        while stack:
            cur = stack.pop()
            for nxt in adjacency[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return count


def validate_map(depmap: dict[str, Any], contract: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []

    for key in ("map_id", "claim_ref"):
        if not isinstance(depmap.get(key), str) or not depmap.get(key):
            errors.append(f"{key} must be a non-empty string")

    purpose = depmap.get("purpose")
    if purpose not in set(contract["purpose_values"]):
        errors.append(f"purpose invalid: {purpose!r}")

    forbidden_found: list[str] = []
    has_forbidden_key(depmap, set(contract["forbidden_scalar_fields"]), forbidden_found)
    for path in forbidden_found:
        errors.append(f"forbidden universal independence scalar: {path}")

    observations = depmap.get("observations")
    if not isinstance(observations, list) or not observations:
        errors.append("observations must be a non-empty array")
        observations = []

    obs_by_id: dict[str, dict[str, Any]] = {}
    duplicate_obs: list[str] = []
    for index, obs in enumerate(observations):
        if not isinstance(obs, dict):
            errors.append(f"observations[{index}] must be an object")
            continue
        obs_id = obs.get("observation_id")
        if not isinstance(obs_id, str) or not obs_id:
            errors.append(f"observations[{index}].observation_id must be non-empty string")
            continue
        if obs_id in obs_by_id:
            duplicate_obs.append(obs_id)
        obs_by_id[obs_id] = obs
        if obs.get("claim_ref") != depmap.get("claim_ref"):
            errors.append(f"{obs_id}: claim_ref must match map claim_ref")

        for section in ("producer", "inputs", "execution", "provenance"):
            if section in obs and not isinstance(obs.get(section), dict):
                errors.append(f"{obs_id}.{section} must be object")

        producer = obs.get("producer", {}) if isinstance(obs.get("producer", {}), dict) else {}
        inputs = obs.get("inputs", {}) if isinstance(obs.get("inputs", {}), dict) else {}
        execution = obs.get("execution", {}) if isinstance(obs.get("execution", {}), dict) else {}
        provenance = obs.get("provenance", {}) if isinstance(obs.get("provenance", {}), dict) else {}

        for key in ("evidence_source_refs", "retrieval_run_refs"):
            if key in inputs:
                string_list(inputs.get(key), f"{obs_id}.inputs.{key}", errors)
        if "toolchain_refs" in execution:
            string_list(execution.get("toolchain_refs"), f"{obs_id}.execution.toolchain_refs", errors)
        if "derived_from_observation_refs" in provenance:
            string_list(
                provenance.get("derived_from_observation_refs"),
                f"{obs_id}.provenance.derived_from_observation_refs",
                errors,
            )
        if "unknown_dimensions" in obs:
            string_list(obs.get("unknown_dimensions"), f"{obs_id}.unknown_dimensions", errors)

        # Optional scalar refs, when present, must be non-empty strings.
        for section_obj, section_name, keys in (
            (producer, "producer", ("agent_or_validator_ref", "model_family", "model_checkpoint_ref", "prompt_lineage_ref")),
            (inputs, "inputs", ("fixture_or_task_ref",)),
            (execution, "execution", ("host_ref", "code_or_validator_ref", "environment_ref", "witness_ref")),
            (provenance, "provenance", ("reviewer_instruction_ref",)),
        ):
            for key in keys:
                value = section_obj.get(key)
                if value is not None and (not isinstance(value, str) or not value):
                    errors.append(f"{obs_id}.{section_name}.{key} must be non-empty string when present")

    for obs_id in duplicate_obs:
        errors.append(f"duplicate observation_id: {obs_id}")

    edges = depmap.get("edges")
    if not isinstance(edges, list):
        errors.append("edges must be an array")
        edges = []

    valid_relations = set(contract["relations"])
    edge_set: set[tuple[str, str, str]] = set()
    duplicate_edges: list[tuple[str, str, str]] = []
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"edges[{index}] must be object")
            continue
        a = edge.get("from")
        b = edge.get("to")
        relation = edge.get("relation")
        if not isinstance(a, str) or not isinstance(b, str):
            errors.append(f"edges[{index}] from/to must be strings")
            continue
        if a not in obs_by_id or b not in obs_by_id:
            errors.append(f"edge refers to unknown observation: {a}->{b}")
        if a == b:
            errors.append(f"self dependency edge not allowed: {a} {relation}")
        if relation not in valid_relations:
            errors.append(f"edge relation invalid: {relation!r}")
            continue
        key = (a, b, relation)
        if key in edge_set:
            duplicate_edges.append(key)
        edge_set.add(key)
    for edge in duplicate_edges:
        errors.append(f"duplicate edge: {edge}")

    # Derived lineage is directional and must be explicit regardless of purpose.
    for obs_id, obs in obs_by_id.items():
        provenance = obs.get("provenance", {}) if isinstance(obs.get("provenance", {}), dict) else {}
        for source_id in provenance.get("derived_from_observation_refs", []) or []:
            if source_id not in obs_by_id:
                errors.append(f"{obs_id}: derived_from refers to unknown observation {source_id}")
            elif (obs_id, source_id, "DERIVED_FROM") not in edge_set:
                errors.append(f"{obs_id}: missing DERIVED_FROM edge to {source_id}")

    # For material corroboration, exact represented shared causes must not disappear.
    if purpose == "MATERIAL_CORROBORATION":
        relation_map: dict[str, str] = contract["shared_dimension_relation_map"]
        for a_id, b_id in itertools.combinations(sorted(obs_by_id), 2):
            a = obs_by_id[a_id]
            b = obs_by_id[b_id]
            for path, relation in relation_map.items():
                av = nested_get(a, path)
                bv = nested_get(b, path)
                shared = False
                if isinstance(av, str) and av and isinstance(bv, str) and bv and av == bv:
                    shared = True
                elif isinstance(av, list) and isinstance(bv, list):
                    shared = bool(set(av) & set(bv))
                if shared and not edge_present(edge_set, a_id, b_id, relation):
                    errors.append(
                        f"{a_id}/{b_id}: known shared dimension {path} requires {relation} edge"
                    )

    components = connected_components(sorted(obs_by_id), edges)
    return errors, {
        "observation_count": len(obs_by_id),
        "edge_count": len(edge_set),
        "dependency_components": components,
        "represented_valid": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--contract", type=Path, default=root / "evidence-dependency-map.v0.1.json")
    parser.add_argument("--fixtures", type=Path, default=root / "fixtures" / "evidence-dependency-map-cases.jsonl")
    parser.add_argument("--show-all", action="store_true")
    args = parser.parse_args()

    contract = load_json(args.contract)
    fixtures = load_jsonl(args.fixtures)
    seen: set[str] = set()
    mismatches: list[str] = []

    for row in fixtures:
        case_id = row.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise SystemExit("every fixture requires case_id")
        if case_id in seen:
            raise SystemExit(f"duplicate fixture case_id: {case_id}")
        seen.add(case_id)
        expected_valid = row.get("expected_valid")
        expected_components = row.get("expected_components")
        if not isinstance(expected_valid, bool) or not isinstance(expected_components, int):
            raise SystemExit(f"{case_id}: invalid expected fields")
        depmap = row.get("map")
        if not isinstance(depmap, dict):
            raise SystemExit(f"{case_id}: map must be object")

        errors, derived = validate_map(depmap, contract)
        actual_valid = not errors
        if actual_valid != expected_valid:
            mismatches.append(
                f"{case_id}: validity expected={expected_valid} actual={actual_valid} errors={errors}"
            )
        if derived["dependency_components"] != expected_components:
            mismatches.append(
                f"{case_id}: components expected={expected_components} actual={derived['dependency_components']}"
            )
        if args.show_all or actual_valid != expected_valid:
            print(
                f"{case_id}: expected_valid={expected_valid} actual_valid={actual_valid} "
                f"obs={derived['observation_count']} edges={derived['edge_count']} components={derived['dependency_components']} errors={len(errors)}"
            )
            for error in errors:
                print(f"  - {error}")

    print(f"fixture summary: total={len(fixtures)} mismatches={len(mismatches)}")
    if mismatches:
        print("FAIL: evidence-dependency-map fixture mismatch")
        for mismatch in mismatches:
            print(f"- {mismatch}")
        return 1

    print("PASS: evidence-dependency-map represented dependency fixtures")
    print("verification_scope=KNOWN_DEPENDENCY_VISIBILITY_AND_LINEAGE_ONLY")
    print("independence_score=NOT_COMPUTED")
    print("current_change=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

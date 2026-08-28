## v0.3.7 candidate.1 — WORKING_CANDIDATE / NOT_CURRENT / NOT_FROZEN

Candidate.1 succeeds frozen candidate.0 after blind fresh Phase A (`5ba3d241efa460fe170253860ad67045aa1d96a5`) and Phase-B reconciliation classified four deterministic candidate-byte defects as shared blind spots missed by author validation.

Targeted corrections:

- preserve source Variation Space, Evolutionary Subject, and Protected Subjects in imported migration provenance while keeping receiver-local state separate;
- reject tied latest packet expression timestamps rather than using array order as chronology;
- require `archive.selection_state_preserved` to match represented selection truth;
- require instantiated record `created_at` to be timezone-aware date-time syntax and make the shipped template placeholder explicitly uninstantiated.

Candidate.1 does not repeat or overwrite fresh Phase A. It uses targeted successor regression plus inherited regression, preserves false-BLOCK escape behavior, and keeps still-open Phase-A attack branches visible for further falsification/reconciliation.

Current remains v0.3.6.

---

# ENA Changelog

## v0.3.7 candidate.0 — WORKING_CANDIDATE / NOT_CURRENT / NOT_FROZEN

Base Current: v0.3.6 tree `7dcbb3934883ffa6cc5292a662588cafc1533cff`.

Candidate birth base / merged release-scope checkpoint:

`0ad263178ab8b7c21c150012b3c06a5c41a4f41c`

### Release thesis

v0.3.7 candidate.0 preserves the v0.3.6 semantic trunk and tests a materially more practical Operational Architecture surface.

```text
NEW_CONSTITUTION_IDS = 0
NEW_CORE_SEMANTIC_DELTA_REQUIRED = 0_DEMONSTRATED
PRACTICAL_OPERATIONAL_RELEASE_VALUE = MATERIAL
```

### Operational Architecture

Adds candidate-local:

- consequence-first Cue Index;
- cold HOW Map;
- machine-readable reference index;
- Purpose-Relative Continuity procedure;
- Standing Input procedure;
- Control Retirement procedure;
- Evolution Commons substrate/protocol patterns;
- Host Mapping patterns;
- explicit hot-cue -> cold-HOW traversal.

The package may grow a large HOW library without requiring the active context to grow with it.

`HOT_KERNEL != HOW_LIBRARY`

### Optional reference library

Bundles as optional/default-off reusable references:

General:
- Retrieval Obligation 0.5;
- WAIT;
- Authority Lease;
- Effect Lifecycle;
- Recovery Adapter.

Advanced/specialized:
- Evidence Envelope;
- Evidence Dependency Map;
- Contested Authorship.

All remain `required_for_complete_adoption=false` and `default_activation=false` unless a future governed release-scope decision changes that.

`BUNDLED != REQUIRED != DEFAULT_ACTIVE`

The recovered Commitment/Settlement prototype is retained in research lineage but not bundled in candidate.0 pending fresh independent review or renewed candidate-critical need.

### Practical v2 evolution tooling

Adds candidate-local `tools/ena_evolve_v2.py` as the primary narrow practical path for:

- latent v2 record creation without early Variation Space;
- candidate-local v2 record validation;
- packet-v2 export/import;
- canonical packet digest + narrow represented consistency;
- preserving source selection/evidence as source context rather than receiver-local proof.

The inherited v1.2 tool is retained as `tools/legacy/ena_evolve_v1_2.py` and removed from the candidate default path.

The v2 helper is intentionally not a complete experiment/evaluation/integration lifecycle state machine.

### zh-CN Operational Architecture projection

Adds Simplified Chinese decision-bearing projections for:

- operational entrypoint;
- Cue Index;
- HOW Map;
- three bounded procedures;
- Commons and Host Mapping patterns;
- optional-reference usage guidance.

Machine reference bytes remain single/canonical rather than being duplicated into translated machine implementations.

Adds `language-projections/semantic-fixtures.v3.yaml` with paired English/zh-CN operational scenarios. Fixture count is an observed corpus fact, not an architecture threshold. Structural route parity does not prove behavioral equivalence.

### Assembly machine evidence

Stage 3:
- exact head `8ba109528ecb14f9a22a372c897ac8d9ea1759f3`;
- Assembly Gate run `33004330491` — SUCCESS;
- Current isolation, reference optionality/paths, all bundled reference selftests, candidate-local v2 helper corpus/CLI, tool boundary, Python compile/bytecode hygiene PASS.

Stage 4:
- exact head `7a59ac9b10e18f804ce7141b0beae2aef5e75cf6`;
- Assembly Gate run `33007647412` — SUCCESS;
- zh-CN operational paths, candidate-scoped projection manifest, paired v3 route structure/parity, reference-guide optionality boundaries PASS.

These are author-side machine/packaging facts, not external truth or independent semantic support.

### Candidate state

Still required before freeze:

`identity reconciliation -> author adversarial suite -> exact pre-freeze machine validation -> freeze record -> fresh independent semantic falsification`

No release/promotion claim is made.

---

## v0.3.6 — CURRENT / FIELD_VALIDATION

v0.3.6 remains the active adopter baseline while candidate.0 is evaluated.

### Evolution Ecology

v0.3.6 established:

- `stimulus -> mutation pressure` without forced mutation;
- long-lived latent variation;
- `stored != expressed != applied != selected`;
- separate lifecycle / expression / selection axes;
- environment-local selection rather than universal fitness;
- publisher/receiver autonomy in Evolution Commons;
- popularity/propagation is not proof;
- narrow Rescue Plane semantics;
- governed canonical lineage independent of one metaphysical carrier;
- ecological/minimal-intervention governance.

### Machine representation

v0.3.6 added evolution-record v2 schema/template/validator, chronological v2 consistency, structured migration provenance, archive consistency, mixed-result overclaim protection, expression consequence representation, and adaptation-packet v2 source expression/negative-lineage context.

### v0.3.6 falsification lineage

- candidate.0 frozen source `3cb94d98882621acede189d0d47806efae44fb0f`, fresh independent verdict `NEEDS_REVISION`;
- candidate.1 frozen source `4af5d17a1cedcf2850b2b4dfe5446e132023369a`, same-falsifier targeted verdict `TARGETED_REVALIDATION_PASS_WITH_RESIDUALS`;
- host-side reconciliation concluded `CANDIDATE_SUCCESSION_STOP = YES` and `RELEASE_PREPARATION_SUPPORTED`;
- v0.3.6 was later explicitly packaged/promoted as Current.

All 38 Constitution IDs remained unchanged.

Earlier release/candidate history remains preserved in Git, PRs, and reconciliation records rather than being rewritten by v0.3.7 candidate packaging.

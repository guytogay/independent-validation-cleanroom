# Agent Adoption Instruction — ENA v0.3.7 candidate.2

Status: **CANDIDATE REVIEW / NOT_CURRENT / NOT_FROZEN / DO_NOT_PROMOTE BY INSTRUCTION ALONE**.

The active adopter baseline remains `releases/current/` = v0.3.6.

This file describes how to evaluate the candidate as a complete operational package and, only after an explicit future release decision, how its surfaces are intended to be adopted.

## Candidate review traversal

1. Read `CANDIDATE-BASELINE.yaml` and bind review to exact candidate content, not branch name alone.
2. Read `00-READ-ME-FIRST.md`.
3. Preserve the inherited 38-ID `01-CONSTITUTION.md`; candidate.2 adds no Constitution ID.
4. Use `RUNTIME-ADOPTION-KERNEL.md` as the compact cue surface.
5. When a concrete mechanism is needed, route through `operational/CUE-INDEX.md` -> `operational/HOW-MAP.md` -> exact procedure/reference/Host pattern.
6. Treat `references/REFERENCE-MANIFEST.yaml` as packaging/optionality metadata: bundled references are not complete-adoption requirements and are default-off.
7. Use `tools/ena_evolve_v2.py` as the candidate's narrow practical v2 latent-record/packet path; keep `tools/legacy/ena_evolve_v1_2.py` as explicit compatibility history.
8. For Chinese operation, use `language-projections/zh-CN/operational/` and `REFERENCE-GUIDE.md`; machine reference bytes remain canonical/shared.
9. Record Host/model/language/authority/recovery assumptions when they materially affect applicability.
10. Treat future salience/application and bilingual behavioral equivalence as field/independent evidence; same-session readback is not proof.

## Durable distinctions

Preserve at least:

- `stimulus != mutation != improvement`;
- `stored != expressed != applied != selected`;
- lifecycle != expression != selection;
- `INTEGRATED != SUPPORTED`;
- `ARCHIVED/RETIRED != selection verdict`;
- local success != universal fitness;
- source success != receiver-local proof;
- `PUBLISHED != IMPORTED != EXPRESSED != LOCALLY_SELECTED`;
- capability/credential/identity != current authority;
- attempt/receipt/settlement are distinct;
- state restore != world rollback != restored mandate;
- recurrence/agreement != independent evidence;
- being heard != sovereignty/authority;
- bundled reference != required/default-active;
- `WRITTEN != LOADED != INTERPRETED != SALIENT != APPLIED`.

## Operational applicability rule

Use the lightest mechanism that can change/protect the decision.

Legitimate outcomes include:

`NOT_REQUIRED | NOT_APPLICABLE | WAIT | UNKNOWN | REFUSE`

A Host-native mechanism may satisfy an ENA property without using a bundled reference schema.

## Tool boundary

This candidate formally contains v2 schema/validator/packet representation plus `tools/ena_evolve_v2.py` for a narrow practical path.

The helper does **not** implement the entire evolution lifecycle state machine and does not prove external facts. The inherited v1.2 tool remains non-default legacy compatibility.

## Claim boundary

Do not report that:

- candidate.2 is Current, frozen, released, or independently supported;
- every bundled reference is universally applicable or mandatory;
- machine selftests prove external evidence/authority/recovery/receipt truth;
- a latent variation is an improvement;
- `EXPRESSED` creates authority;
- source selection/popularity creates receiver-local proof;
- cue configuration proves future natural salience;
- paired zh-CN fixtures prove behavioral equivalence;
- GitHub itself is the permanent source of ENA validity.

When making a strong claim, distinguish:

`PROSE_PRESENT | STRUCTURALLY_REPRESENTED | MACHINE_GUARDED | EXECUTED | EXTERNALLY_OBSERVED | INDEPENDENTLY_SUPPORTED`

Do not upgrade one level into another.

**Review the candidate; do not promote it by narration.**

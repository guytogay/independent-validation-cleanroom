# 10. Language Portability and Semantic Projection — v0.3.7 candidate.2

Status: `WORKING_CANDIDATE / OPERATIONAL_LANGUAGE_PROJECTION / NOT_CURRENT / NOT_FROZEN`.

ENA must not depend on English proficiency to remain usable as ENA.

A language version is a **semantic projection** of one candidate/release identity, not a separate Constitution or a second machine implementation.

## 10.1 Stable identity

Across languages:

- inherited `ENA-CON-*`, `ENA-CAP-*`, contract/schema IDs remain stable unless a governed version change explicitly changes them;
- effective-content identity remains traceable;
- a projection declares source identity and language tag;
- wording may differ to preserve decision meaning.

Literal translation is not the goal.

Example:

`capability != authority`

Operational Chinese meaning:

`有能力做到某件事 ≠ 被授权可以这样做`

Other high-risk inherited distinctions include:

`stimulus != mutation != improvement`

`stored != expressed != applied != selected`

`ARCHIVED/RETIRED != selection verdict`

`local selection != universal fitness`

`published != imported != locally selected`

This candidate adds operational distinctions that also require semantic rather than lexical projection:

`bundled reference != required/default-active`

`cue match != applicability proven`

`continuity for one decision != universal same-agent claim`

`being heard != sovereignty/authority`

`no incident != control not needed`

## 10.2 Candidate projection manifest

The zh-CN projection declares candidate source identity, covered semantic/operational surfaces, machine-artifact policy, fixture sets, validation state, and known gaps in:

`language-projections/zh-CN/projection-manifest.yaml`

This candidate is `NOT_CURRENT / NOT_FROZEN`; the projection is therefore also a working candidate projection. If freeze occurs, it must be bound to the exact frozen candidate tree rather than a mutable branch name.

## 10.3 Decision-bearing operational projection

This candidate adds zh-CN paths for:

- operational entrypoint;
- Cue Index;
- HOW Map;
- Purpose-Relative Continuity;
- Standing Input;
- Control Retirement;
- Evolution Commons patterns;
- Host Mapping patterns;
- optional-reference usage guidance.

Root:

`language-projections/zh-CN/operational/`

Reference guide:

`language-projections/zh-CN/REFERENCE-GUIDE.md`

Chinese adopters should be able to reach the practical HOW layer without hidden English-only decision instructions.

## 10.4 One canonical machine surface

This candidate intentionally does **not** translate every machine reference schema/tool/fixture into a second zh-CN implementation.

```text
ONE_MACHINE_SURFACE
+ MULTIPLE_SEMANTIC_USAGE_PROJECTIONS
```

Canonical machine bytes remain under `references/`, `schemas/`, `templates/`, and `tools/`.

This avoids two nominally equivalent machine contracts drifting independently. Chinese usage guidance explains applicability/boundaries while preserving the same machine paths.

## 10.5 Cross-language conformance

Validate **decision meaning**, not literary similarity.

Fixture sets:

- `semantic-fixtures.v1.yaml` — inherited v0.3.5 paired scenarios;
- `semantic-fixtures.v2.yaml` — inherited v0.3.6 ecology scenarios;
- `semantic-fixtures.v3.yaml` — v0.3.7 candidate operational routing/applicability scenarios.

v3 currently exercises Retrieval, WAIT, Authority, Effect, Recovery, Purpose-Relative Continuity, Standing Input, Evidence dependency, Adoption/reference optionality, Commons/Migration, Control Retirement, and Contested Authorship.

The current v3 case count is a corpus fact, not a required minimum or proof that the operational ontology is exhaustive.

Fixture presence/structure and route parity are not behavioral proof. Only observed paired model/Host/language behavior can support behavioral conformance claims.

```text
TRANSLATED != BEHAVIORALLY_EQUIVALENT
FIXTURE_DEFINED != MODEL_PASS
```

## 10.6 Local Projection and applicability

Where language can materially affect interpretation, record as needed:

- operating/adoption language;
- projection identity;
- source semantic identity;
- model/Host/language combination;
- material limitations.

`same model != same semantic performance across languages`

Language change can be an applicability boundary for evidence when it can change a decision.

## 10.7 Candidate evidence status

The Stage-4 Assembly Gate has machine-checked:

- required zh-CN operational files exist;
- projection manifest is candidate-scoped and `not_current=true`;
- machine reference bytes remain single/canonical by policy;
- paired v3 fixtures are structurally valid;
- every expected v3 route resolves in both English and zh-CN HOW maps;
- the zh-CN reference guide preserves optional/default-off/deferred-not-retired boundaries.

This is author-side structural/semantic packaging evidence, not natural bilingual behavior proof.

Predecessor behavioral results remain predecessor evidence with their original scope. Candidate v0.3.7 behavioral semantic conformance is **UNPROVEN / FIELD OR INDEPENDENT EVIDENCE REQUIRED**.

> **Translate wording; preserve decisions.**
>
> **语言是接口，不是 ENA 的身份。**

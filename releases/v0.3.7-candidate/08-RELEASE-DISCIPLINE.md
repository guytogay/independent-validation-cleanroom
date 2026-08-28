# 8. Release and Canonical-Lineage Discipline — v0.3.7 candidate.2

Status: `SUCCESSOR_WORKING_CANDIDATE / REPAIR_RECONCILED / EXACT_PREFREEZE_NEXT / NOT_CURRENT / NOT_FROZEN`.

A deployable ENA adoption version must be self-contained and immutably identifiable. Candidate.2 is not Current and must not acquire release status by self-description.

## Version identity

One adoption version identifies one immutable effective-content state.

`same ena_version -> same effective content`

Material change requires a new version/candidate identity. Research/candidates may branch; adopter-facing Current remains singular.

`Git main != ENA Current`

`candidate branch != frozen identity`

## Candidate discipline

A candidate is a variation:

`candidate -> author attacks -> exact pre-freeze validation -> freeze -> fresh independent falsification/validation -> targeted correction/revalidation where needed -> reconciliation -> release decision`

If a frozen candidate needs material correction, create a successor identity; do not silently edit its frozen effective-content tree.

A same-falsifier targeted revalidation may verify specific fixes when labeled honestly; it is not fresh independent validation.

Stop candidate succession when decision-changing residuals converge. Visible research questions are not automatic release blockers.

### v0.3.7 candidate.2 current state

Candidate.2 succeeds frozen candidate.1 because fresh A-S/A-P found four material represented-consistency defects plus deterministic active self-description drift. Candidate.1 remains immutable occurrence truth; candidate.2 repairs only justified validator/reference/projection defects and does not reopen `releases/current/`.

Candidate.1 A-S seal: `2e6b46aeedc1945a03aac93620ad36aa1ccbd70f`.

Candidate.1 A-P completion: `b970148fe9596ea9cad0a2817a3b399a1d2b75f5`.

Candidate.1 Phase-B disposition: `NEEDS_REVISION / CANDIDATE_2_REQUIRED`.

Candidate.1 frozen source/subtree: `ae6903464133cb5bcf3cd8909ecae1215fe0b9ba` / `c0458e0d7ea417b841cbf4c8bf6e64e4aff37319`.

### Predecessor v0.3.7 candidate.1 preserved state

Candidate.1 passed exact pre-freeze machine validation, was externally frozen without rewriting its tested bytes, then failed fresh A-S/A-P independent falsification. Its frozen tree must not be edited in place.

### Predecessor v0.3.7 candidate.0 preserved state

Candidate birth base:

`0ad263178ab8b7c21c150012b3c06a5c41a4f41c`

That main commit contains the merged release-scope checkpoint and version selection before candidate bytes were authored.

Candidate.0 has assembled:

- release-local Operational Architecture routing;
- optional reference library with machine-readable default-off policy;
- candidate-local minimal v2 evolution helper with explicit v1.2 legacy demotion;
- decision-bearing zh-CN Operational Architecture projection and paired v3 route fixtures.

Assembly machine checks have passed on recorded exact heads, but candidate.0 is still mutable workspace. It remains `NOT_CURRENT / NOT_FROZEN / NOT_RELEASED` until later governed gates complete.

## Canonical ENA evolution

ENA itself is evolvable, but one local Agent/fork cannot mint canonical status by self-description.

Canonical change requires durable lineage sufficient to establish:

- proposal/change identity;
- reviewable effective content;
- falsification/validation evidence;
- reconciliation/decision record;
- immutable version identity;
- recoverable/publicly inspectable history appropriate to the project;
- explicit promotion/admission event.

GitHub is the current project carrier for this lineage. The semantic requirement is governed reproducible lineage, not eternal dependence on one service.

## Current isolation

`releases/current/` is still v0.3.6 and must not be edited as a side effect of candidate assembly.

A material Current change requires a new release identity and explicit release decision.

Candidate validation therefore checks Current isolation against the exact release-scope checkpoint.

## Freeze identity

Candidate.0 uses the external-record freeze model:

- finish all material candidate bytes first;
- run exact-source machine validation;
- identify exact source commit and exact `releases/v0.3.7-candidate/` subtree;
- record that binding outside the candidate subtree in governed lineage;
- do not rewrite the tested candidate tree merely to insert a post-hoc `frozen: true` marker.

The authoritative freeze property is exact source/tree binding plus governed lineage.

Any material correction after candidate.1 freeze would require a successor such as candidate.2.

## Source/distribution identity

A release must be built from identified committed source/effective-content bytes. Release evidence may include source commit/tree, exact file set, byte/hash parity, package digest, and published artifact readback.

Ordinary adopters need the minimum sufficient immutable effective-content identity; they need not reproduce release-author ceremony.

## Language projections

Supported projections must be immutably bound to the same candidate/release identity. Material decision meaning must remain conformant across supported languages.

Candidate.2 retains the zh-CN operational decision surfaces and v3 paired route fixtures. Fixture structure/parity does not prove behavioral equivalence; actual model/Host evidence is still required.

## Runtime/reference compatibility

A semantic baseline may retain older compatibility mechanisms only when their actual scope is explicit.

Candidate.2 exposes one primary practical v2 path:

`tools/ena_evolve_v2.py`

and keeps the inherited state/schema 1.2 tool only under:

`tools/legacy/ena_evolve_v1_2.py`

Bundled optional reference schemas likewise do not become normative Host implementations merely by being packaged.

`canonical semantic property != bundled reference implementation != Host mechanism`

## History and carriers

Preserve historical releases/candidates/evidence as occurrence truth without forcing ordinary adopters to reconstruct history to determine Current.

Repository/carrier availability is an implementation dependency. Project continuity should not require one permanent session, Agent, validator, institution, or hosting vendor to remain forever available or correct.

> **Expose one Current; allow many candidates and historical surfaces.**
>
> **The carrier hosts the lineage; it is not the sovereign of the lineage.**

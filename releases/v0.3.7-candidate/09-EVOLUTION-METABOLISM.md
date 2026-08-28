# 9. Evolution Metabolism and Ecology — v0.3.7 candidate.2

Status: `WORKING_CANDIDATE / INHERITED_V036_ECOLOGY_PLUS_OPERATIONAL_HOW / NOT_CURRENT / NOT_FROZEN`.

This candidate preserves the v0.3.6 evolution-ecology semantics and adds practical routing/tool surfaces. It does **not** introduce a new universal evolution ontology or Constitution rule.

## 9.1 Ecological metabolism

The inherited model remains:

`environment/stimulus -> mutation pressure -> variation -> latent storage or expression -> reality contact -> local selection -> retention/dormancy/loss -> inheritance/migration/recombination -> renewed variation`

Core distinctions remain:

`stimulus != mutation`

`mutation != improvement`

`stored != expressed != applied != selected`

`local selection != universal fitness`

`publication != receiver adoption`

A variation does not have to move immediately toward experiment or verdict.

## 9.2 Stimulus and mutation pressure

User correction, repeated failure/success, friction, contradiction, capability/environment change, other Agents, external discovery, curiosity, recombination, opportunity, or stale adaptation may create mutation pressure.

Mutation pressure is an opportunity/incentive to generate or revisit variation, not a command to mutate and not evidence of improvement.

Hosts may deliberately increase exploratory pressure when useful. No universal cadence is required.

## 9.3 Latent / cryptic variation

A variation may remain stored without immediate experiment, expression, or selection when retention is affordable/lawful and storage alone creates no active consequential behavior.

`UNASSESSED` is not automatically backlog debt. Hosts may curate, compact, archive, or lawfully delete latent material when carrying cost exceeds plausible value, but age/low usage alone is not proof of worthlessness.

Candidate practical creation path:

`tools/ena_evolve_v2.py new-latent ...`

This path deliberately permits latent creation without requiring an early Variation Space.

## 9.4 Expression is a separate axis

Expression remains conceptually separate from lifecycle and selection:

`LATENT | EXPRESSED`

A stored adaptation may be `INTEGRATED + SUPPORTED + LATENT`, become expressed in a relevant context, and return latent later without rewriting selection history.

Expression does not mint authority.

## 9.5 Cue-triggered salience -> Operational Architecture

This candidate turns the v0.3.6 hot-cue direction into a concrete release-local navigation surface:

```text
hot cue / failure shape
-> operational/CUE-INDEX.md
-> operational/HOW-MAP.md
-> operational/REFERENCE-INDEX.yaml
-> procedure / optional reference / Host-native pattern
```

The exact resident cue mechanism remains Host-selectable. The entire HOW library should not be permanently hot merely to claim internalization.

`configured cue != future salience proven`

Candidate routing adds explicit branches for Retrieval, WAIT, Authority, Effect Lifecycle, Recovery, Continuity, Standing Input, Evidence dependency, Contested Authorship, Evolution/Commons, Control Retirement, Host mapping, language, and adoption.

This branch set is a practical map, not a claim of exhaustive ontology.

## 9.6 Variation Space and reality contact

When a variation is consequentially expressed as an experiment, use a suitable Variation Space where uncertainty can become real enough to learn from while preserving consequence ownership/correction capacity.

Possible Host mechanisms include branch/fork, sandbox, disposable VM/container, shadow execution, canary, test Agent, reversible local configuration, isolated skill version, simulation, or replay.

Internal capability/permission topology may vary inside legitimate scope. Internal mutation cannot self-mint external mandate.

## 9.7 Lifecycle, expression, and selection remain different

Lifecycle:

`PROPOSED | EXPERIMENTED | INTEGRATED | ARCHIVED | RETIRED`

Expression:

`LATENT | EXPRESSED`

Selection:

`UNASSESSED | SUPPORTED | PARTIAL | NOT_SUPPORTED | HARMFUL | UNKNOWN`

No transition on one axis silently upgrades another.

## 9.8 Evaluation and local selection

Material outcomes may be represented as:

`IMPROVED | DEGRADED | UNCHANGED | UNKNOWN`

Evidence-backed positive/negative selection depends on represented reality contact where the claim requires it.

Selection remains scoped to the represented environment, Host, model, language, dependencies, consequence envelope, time, and subject as material.

`local success != universal recommendation`

`wide adoption != universal truth`

`survival != moral correctness`

Plural environments and receiver-side reselection prevent one local fitness landscape from pretending to be the whole world.

## 9.9 Integration, dormancy, pruning, and control retirement

Integration is not permanent expression. Supported capability may remain dormant until relevant context wakes it.

Hosts may use:

`KEEP | UPDATE | DORMANT | ARCHIVE | RESTORE | RETIRE`

Pruning does not rewrite selection history.

For safeguards/controls rather than adaptations, this candidate provides `operational/procedures/CONTROL-RETIREMENT.md`: recover original purpose, inspect replacement/coverage, preserve secondary dependencies, choose reversible narrowing/shadow/dormancy where useful, and preserve reactivation/lineage.

`NO_INCIDENT != CONTROL_NOT_NEEDED`

## 9.10 Migration, inheritance, propagation, and Commons

Migration transfers a possibility plus represented source history; it does not transfer a conclusion.

Source and receiver results remain separate. A receiver may import, ignore, adapt, recombine, reject, keep unknown, or re-test.

This candidate provides:

- `adaptation-packet.v2` as inherited portable represented context;
- `tools/ena_evolve_v2.py export-packet/import-packet` as a narrow practical path;
- `operational/patterns/EVOLUTION-COMMONS.md` for Git/OCI/object-store/direct-transfer/active-protocol composition patterns.

A packet digest checks content consistency; it does not authenticate the source. Imported source selection remains source context and never becomes receiver-local selection merely through transport.

## 9.11 Recombination and emergence

Recombination remains a first-class variation generator. It may produce conflict, cancellation, amplification, emergent capability, new externality, or no useful change.

Expectation of emergence is not evidence. Observe the composed subject when interaction can change the decision.

## 9.12 Recovery and rescue

Where a self-affecting mutation can disable its own recovery path and consequence warrants it, preserve a rescue path reachable outside the damaged variation: last-known-viable snapshot, watchdog/timer, recovery manifest, narrow recovery credential, peer/human handoff, independent startup path, or another Host-native mechanism.

This candidate bundles optional `references/general/recovery-adapter/` and maps Host alternatives in `operational/patterns/HOST-MAPPINGS.md`.

Rescue authority stays narrow.

`restore success != external consequence rollback != restored authority`

## 9.13 Authority, effect, continuity, and standing around evolution

Evolution does not erase other consequence boundaries.

- consequential authority may use `references/general/authority-lease/` or Host equivalent;
- retry/restart/world-effect ambiguity may use `references/general/effect-lifecycle/` or Host equivalent;
- continuity questions should use `operational/procedures/PURPOSE-RELATIVE-CONTINUITY.md` only when continuity changes the decision;
- decision-material objections may use `operational/procedures/STANDING-INPUT.md` without granting sovereignty;
- durable material self-surface changes may use optional Contested Authorship; ordinary state writes may be out of scope.

These HOWs are optional/applicability-scoped. They are not a mandatory checklist for every mutation.

## 9.14 Candidate tool boundary

This candidate now supplies a primary narrow practical v2 tool:

`tools/ena_evolve_v2.py`

Its scope is intentionally bounded:

The shipped JSON record template is intentionally uninstantiated: its `created_at` placeholder must be replaced before validator PASS. `build_latent_record` supplies a real UTC timestamp automatically.

- create valid latent v2 records without early Variation Space;
- delegate evolution-record semantics to the candidate-local v2 validator;
- export/import packet v2 with canonical digest and narrow represented consistency;
- preserve source evidence/selection vs receiver-local selection.

It does **not** implement the complete experiment/evaluation/integration/archive lifecycle state machine and does not prove external truth.

The inherited v1.2 tool is preserved only as `tools/legacy/ena_evolve_v1_2.py`. Its old `--variation-space` propose/import limitation remains a legacy implementation fact, not candidate semantic law.

## 9.15 Retained residuals

Keep visible where applicable:

- self-asserted `LOCAL` provenance is not external proof;
- obligation-reference strings are not authenticated by schema acceptance alone;
- tied latest timestamps are conservatively rejected;
- natural future cue salience/application remains field evidence;
- `experiment` versus broader `reality contact` terminology remains research wording;
- the candidate v2 helper is intentionally partial rather than full lifecycle runtime;
- optional reference machine PASS does not establish universal applicability/external truth;
- zh-CN paired decision fixtures do not prove bilingual behavioral equivalence.

> **Variation does not owe reality an immediate verdict.**
>
> **Stored possibility is not active authority.**
>
> **Selection is local; propagation is not proof.**

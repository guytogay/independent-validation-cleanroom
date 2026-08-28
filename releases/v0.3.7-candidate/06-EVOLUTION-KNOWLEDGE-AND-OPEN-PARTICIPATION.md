# 6. Evolution, Knowledge, Migration, and Open Participation — v0.3.7 candidate.2

Status: `WORKING_CANDIDATE / INHERITED_SEMANTICS_PLUS_OPERATIONAL_POINTER / NOT_CURRENT / NOT_FROZEN`.

ENA project knowledge, variations, adaptations, research, evidence, lineage, and open questions should remain discoverable to legitimate participants. Knowledge access, publication, import, adoption, and consequential authority remain separate things.

Any participant may, **within actual capability, publication authority, Protected-Subject constraints, and other legitimate external constraints**:

- read/search project knowledge;
- question and critique ENA;
- generate variations and hypotheses;
- preserve unresolved/latent possibilities;
- perform bounded experiments;
- contribute positive and negative evidence;
- publish variations/adaptations/evidence into a discoverable Commons;
- discover/import prior material;
- locally adapt/recombine it;
- challenge current selections.

Useful contribution classes remain open, including:

`INCIDENT | NEAR_MISS | FRICTION | VALUE_OBSERVED | COUNTEREXAMPLE | PORTABILITY_FINDING | NEW_VARIATION | LATENT_VARIATION | ADAPTATION_PACKET | EMERGENCE_FINDING | EVIDENCE_RESULT | RESEARCH_HYPOTHESIS | CRITIQUE`

## Evolution Commons

ENA encourages a shared discoverable possibility pool. The Commons is not a mandatory-update service and not a universal ranking authority.

Separate:

`PUBLISH -> DISCOVER -> IMPORT -> EXPRESS/EXPERIMENT -> LOCALLY_SELECT`

None of those arrows is automatic.

This candidate adds concrete substrate/protocol patterns at:

`operational/patterns/EVOLUTION-COMMONS.md`

The pattern library explicitly keeps durable Commons distinct from active Agent/A2A-style live discovery/task exchange. A Host may compose them; neither silently implements the other.

### Publisher autonomy

A publisher may make material discoverable only within legitimate publication authority and consequence boundaries. Receiver non-adoption is not by itself a veto over independently authorized publication, but privacy, ownership, confidentiality, contractual, security, shared-resource, Protected-Subject, and third-party constraints remain real.

Publication does not authorize pushing material into every receiver. Publication count/popularity does not create universal truth.

### Receiver autonomy

A receiver may search, import, ignore, locally adapt, recombine, reject, keep unknown, or re-test within its own authority/consequence boundary.

`ADOPT | LOCAL_ADAPT | RECOMBINE | REJECT | KEEP_UNKNOWN`

Import creates a migration candidate, not a command and not local proof.

## Migration packet

Where material, preserve source change/hypothesis, environment, experiments/evaluations, outcomes/tradeoffs, negative evidence, dependencies, authority/consequence assumptions, transfer limitations, unknowns, and expression/dormancy context.

`PUBLISHED != IMPORTED`

`IMPORTED != EXPRESSED`

`EXPRESSED != LOCALLY_SELECTED`

`POPULAR != UNIVERSALLY_VALID`

This candidate retains `adaptation-packet.v2` as the portable represented source-context carrier and provides `tools/ena_evolve_v2.py` for narrow packet-v2 export/import. Packet transfer still does not authenticate the source or create receiver-local selection.

## Composition as search space

Recombination may produce degradation, neutral interaction, additive/super-additive improvement, emergent capability, or UNKNOWN. When interactions can materially change the decision, observe the composed subject rather than inheriting component verdicts.

## Pruning, dormancy, and adaptive retirement

Hosts may move material among:

`KEEP | UPDATE | DORMANT | ARCHIVE | RESTORE | RETIRE`

Dormancy keeps possibility available without continuous expression. Age/low usage are evidence, not proof of worthlessness; retention itself also has cost.

For safeguards/controls whose original failure may have disappeared or been replaced, this candidate provides `operational/procedures/CONTROL-RETIREMENT.md`. Retirement preserves lineage; deactivation is not historical erasure.

## ENA narrow waist

ENA standardizes semantic properties needed for truthful evolvable interoperability across heterogeneous Agents/Hosts/languages, not one universal organ inventory.

`Universal semantics != universal implementation burden`

`Same source != same local outcome`

`Migration != local validation`

`Composition != sum of parts`

`Propagation != proof`

`Commons != sovereign`

Candidate Host realization guidance lives at `operational/patterns/HOST-MAPPINGS.md`.

> **Knowledge and possibility can be shared broadly. Adoption remains local; consequential authority remains scoped.**

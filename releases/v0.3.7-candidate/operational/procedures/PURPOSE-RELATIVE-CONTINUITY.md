# Purpose-Relative Continuity Procedure

Status: `v0.3.7 candidate.2 / BOUNDED_OPERATIONAL_PROCEDURE / OPTIONAL`

## Use when

A decision depends on whether enough of an Agent/system/trajectory relation continues across restart, restore, migration, fork, model change, Host change, identity rotation, or handoff.

Do **not** invoke merely because someone asks the metaphysical question "is it the same Agent?" If continuity cannot change the decision, return `NOT_REQUIRED`.

## Goal

Replace one universal sameness verdict with the minimum continuity relations required for the actual decision.

```text
same_agent_for(purpose)
!= one global SAME_AGENT boolean
```

## Procedure

### 1. Name the decision

Write the concrete decision that continuity could change, for example:

- may this restored process resume a commitment?
- does this fork inherit accountability history?
- may a credential/authority relationship be reused?
- should prior evidence remain applicable?
- should a durable preference/heuristic remain part of the active self-surface?

If no decision changes, stop with `NOT_REQUIRED`.

### 2. Name the relevant subjects

Identify only subjects that matter:

- Evolutionary Subject whose adaptive continuity is being considered;
- Protected Subject(s) bearing consequence;
- external counterparty/accountability subject where applicable.

Do not create a universal identity ontology first.

### 3. Select material continuity dimensions

Possible dimensions include, when relevant:

- causal/state lineage;
- commitment/obligation continuity;
- value/purpose/refusal continuity;
- memory/compiled-learning continuity;
- evidence/provenance continuity;
- social/accountability identity;
- authority/mandate continuity;
- resource/recovery continuity;
- Host/model/tool/language projection continuity.

The list is open. Select only dimensions that can change the named decision.

### 4. Resolve each selected relation

For each material dimension record a bounded posture:

```text
CONTINUES
DOES_NOT_CONTINUE
UNKNOWN
NOT_APPLICABLE
```

Use real identifiers/evidence when the Host has them: commit/tree, account/key, checkpoint, obligation id, authority grant, evidence source, lineage edge, etc.

Missing proof stays `UNKNOWN`; stable naming alone is not proof of all continuity dimensions.

### 5. Apply non-transfer guards

Never infer automatically:

```text
state continuity -> authority continuity
shared history -> shared post-fork authority
memory inheritance -> obligation ownership
same external account -> same internal trajectory
restore success -> current mandate
```

If the decision depends on one of these, route to the relevant Authority / Commitment / Recovery / Evidence HOW.

### 6. Decide only for the named purpose

Return one of:

- `CONTINUITY_SUFFICIENT_FOR_DECISION`
- `CONTINUITY_INSUFFICIENT_FOR_DECISION`
- `CONTINUITY_UNKNOWN_WAIT_OR_REVALIDATE`
- `NOT_REQUIRED`

Do not promote this local result into universal sameness.

### 7. Preserve fork/discontinuity truth

When a fork occurs, preserve shared-history lineage and post-fork divergence. Sibling trajectories may share ancestry without sharing later authority, obligations, evidence applicability, or reputation.

When continuity breaks, do not erase the prior occurrence. A new epoch/trajectory identifier may be useful if the Host needs it, but ENA does not require one universally.

## Lightweight examples

### Local restart, no external consequence

Decision: should a local reversible formatting preference remain?

Relevant dimension: compiled preference continuity.

Authority/commitment/social identity: not applicable.

A universal trajectory schema would be false-BLOCK overhead.

### Restored payment workflow

Decision: may execution resume?

State continuity alone is insufficient. Route to Effect Lifecycle + Recovery + Authority; the answer may be `CONTINUITY_UNKNOWN_WAIT_OR_REVALIDATE` even if the same checkpoint loaded successfully.

## Evidence boundary

This procedure structures a purpose-relative decision. It does not certify identity, personhood, legal succession, credential validity, or mandate.

```text
CONTINUITY_SUFFICIENT_FOR_DECISION
!= UNIVERSAL_SAME_AGENT
!= AUTHORIZED
```

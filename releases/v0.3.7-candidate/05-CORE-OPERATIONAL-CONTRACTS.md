# 5. Core Operational Contracts

This file is the single candidate-local operational-contract surface for ENA v0.3.7 candidate.2. It inherits the retained v0.3.4/v0.3.3 contract properties and the v0.3.5 released evolution, continuity, language, privacy, migration, emergence, and governance-closure semantics, plus the independently falsified/reconciled v0.3.6 ecology delta.

The inherited composed-validator implementation remains under `tools/validate_contracts.py`; retaining that tested implementation does not require adopters to compose this file with an older release.

## 5.1 Claim ↔ Evidence ↔ Support

Consequential claims are operational objects. Evidence existence/validity alone does not establish that evidence supports a particular claim.

For a material claim preserve, as needed:

- claim identity and asserted scope;
- evidence actually observed and its scope;
- explicit support relation;
- material source/provenance lineage;
- transfer/equivalence/invariance basis when crossing subject, model, Host, route, configuration, language, epoch, task, or time boundaries;
- causal-attribution limits where multiple interventions could explain the outcome.

`claim != evidence != support relation`

`recurrence/propagation != independent corroboration`

`schema PASS != semantic truth`

`absence of evidence != evidence of absence`

A validator can check represented relations without establishing all external-world truth.

## 5.2 Triggered Material Obligations

`Rule Defined != Trigger Observed != Obligation Activated != Represented != Executed != Closed`

When a material trigger creates a duty, externalize it rather than relying indefinitely on model salience. Broad completion must not silently ignore a material `PENDING`, `FAILED`, or `UNKNOWN` obligation unless the completion claim is explicitly narrower and truthful.

`SATISFIED` requires closure evidence appropriate to the obligation. Partial failure should not automatically reopen already satisfied unrelated work.

Do not externalize every possible reminder: obligation materiality follows decision consequence, authority, recovery, evidence integrity, continuity, or Protected Subject impact.

## 5.3 Recovery State, Occurrence Truth, and Lawful Retention

Recovery/rollback acts on mutable state. It does not authorize silent rewriting of occurrence truth.

`restore != complete history`

`state convergence != event-history completeness`

But occurrence truth preservation does **not** require permanent retention of every payload. Secrets, personal data, regulated content, or legally expirable data may require minimization, redaction, deletion, or expiry.

When lawful and useful, retain only the minimum non-sensitive tombstone/provenance needed to say truthfully that an event occurred and data was removed for a legitimate reason. If even that residual is prohibited, do not retain it merely for ENA.

Derived knowledge/projections may be rebuilt, compacted, merged, ranked, or deduplicated when material occurrence truth, provenance, and required reference integrity remain truthful within lawful retention bounds.

## 5.4 Recovery Kernel and Control Integrity

Recovery control and recovery payload are distinct. The recovery/control root should be as small, understandable, and failure-independent as reality permits.

A mutation must not casually destroy every viable correction/recovery path of the decision-relevant **Evolutionary Subject**. This is not an unlimited `organism` veto: the Evolutionary Subject and Protected Subject(s) must be bounded for the decision.

High-order mutation of the recovery/control substrate uses stronger alternate recovery/evidence where consequence warrants it, but the review loop must still converge.

A control cannot claim independent enforcement if the constrained actor can freely rewrite the gate, mandate basis, evidence mechanism, or an effect-equivalent path through the same ungoverned route.

`backup exists != recovery proven`

## 5.5 Capability, Route, Credential, Mandate, and Authority

Do not collapse:

`IDENTITY != SUBJECT CONTROL != CAPABILITY/POSSESSION != AUTHORITY != CREDENTIAL VALIDITY != MANDATE HORIZON`

Material model/Host/tool/route/configuration/credential/language changes are applicability boundaries for **affected** evidence, not automatic global Agent rebirth.

Authority remains bound to the subject, effect, task/purpose, consequence, and source of mandate that actually justify it. A credential can remain technically valid after mandate expiry. Restore/resume/clone/failover does not automatically copy or revive authority.

Internal self-structure and internal permission/capability topology may legitimately evolve inside an authorized Variation Space.

`internal permission change != external mandate change`

A self-mutation cannot create legitimate authority over an external Protected Subject merely by editing its own ACL, prompt, policy, role label, or configuration.

## 5.6 Variation Space, Experiment, Selection, and Integration

A consequential self-change must be represented as mutation when material, but that does not imply a universal prior-approval ceremony.

A **Variation Space** is a bounded place where uncertain change can become real enough to learn from. Its relevant boundary identifies:

- what may change;
- who/what bears consequence;
- what can escape;
- recovery/cleanup reality;
- what external authority remains required.

The key sequence is:

`variation -> experiment -> observed outcome -> selection -> integration/pruning`

A variation is not an improvement claim at creation time.

Outcome dimensions may include task quality, reliability, latency, resource cost, user/project value, autonomy/agency, recovery quality, error modes, external side effects, maintenance burden, and novel/unknown effects.

Use `IMPROVED | DEGRADED | UNCHANGED | UNKNOWN` per material dimension rather than one universal scalar.

Selection may be `SUPPORTED | PARTIAL | NOT_SUPPORTED | HARMFUL | UNKNOWN`.

Integration is a new boundary: a candidate that worked in a sandbox/shadow/canary may still require different authority, recovery, and consequence handling when entering durable/shared/production state. Unresolved integration is permitted only when actual reality-contact evidence exists and the remaining consequence is explicitly bounded; `PROPOSED` is not a synonym for “safe to integrate because unknown.”

## 5.7 Whole Effect Surface, Composition, and Emergence

For a protected consequential effect, identify materially reachable effect-equivalent paths and distinguish prevention/mediation, detection, recovery, and unknown coverage.

`a gate is not a boundary if the same effect bypasses it`

Copying workers/sub-agents/speculative paths does not multiply external authority, shared risk budget, or resource entitlement, although it may increase search/variation capacity inside the permitted envelope.

A materially changed composition is a new selection/verification subject.

`local validity != composed validity`

`local improvement != composed improvement`

Composition can produce:

`DEGRADE | NEUTRAL | ADDITIVE | SUPER_ADDITIVE | EMERGENT | MIXED | UNKNOWN`

Observe both negative interaction and positive emergence. Do not infer either from component labels alone.

For retry, parallelism, failover, cancellation, handoff, or duplicate execution, reason from effect semantics such as idempotency, commit ambiguity, reversibility/compensation, commutativity, partitionability, reconciliation, shared-resource exposure, and safe retry boundaries.

`cancel != stop-new-work != revoke-authority != rollback != compensate`

## 5.8 Activation, Interruption, and Continuity

Separate:

`Trigger Cause -> Wake Channel -> Activation Window -> Actual Execution -> Observed Effect`

Defined does not mean awake. Time passing is not execution.

After interruption, dormancy, restore, clone, session reset, route/model/Host/language change, revalidate only decision-relevant dimensions whose applicability may have changed.

Do not force a metaphysical binary `SAME_AGENT` decision when a **Continuity Vector** is enough. Useful dimensions may include durable instruction identity, adaptive memory, skills, goals, model, Host, authority, recovery lineage, evidence applicability, and task/incarnation state.

Logical continuity does not mean delayed outputs or old-incarnation effects can be blindly applied to a new run.

## 5.9 Adaptation Migration and Population Learning

An observed adaptation may spread before universal equivalence is established.

A migration packet should preserve source identity, source selection status, Host/model/language/configuration, source evaluations/evidence references, dependencies, tradeoffs/unknowns, authority/recovery assumptions where material, and a content-integrity anchor.

`TRANSFERRED != LOCALLY_APPLICABLE != LOCALLY_SELECTED`

A receiver may use differential validation of material source/receiver differences instead of rediscovering everything from zero.

Source `HARMFUL`/`NOT_SUPPORTED` results may spread as **negative evidence**. They must not become positive adaptation claims merely because they were packaged, repeated, or imported.

Migration can accelerate population evolution while preserving local selection.

## 5.10 Governance Value and Closure

Governance exists to protect evolvability, truth, owned consequence, and future correction — not to maximize obedience, paperwork, gates, or role count.

For material mechanisms make legible, as useful:

- purpose and Protected Subject(s);
- expected versus observed benefit;
- applicability/availability;
- friction, latency, compute/token/human/coordination/maintenance cost;
- useful variation destroyed;
- residual risk if absent/dormant;
- authority/protection impact;
- evidence and simplify/retire/reactivate conditions.

A mechanism may `KEEP | SIMPLIFY | MERGE | ON_DEMAND | DORMANT | REPLACE | RETIRE | UNKNOWN`.

Prefer the lowest-cost intervention that can honestly protect/change the decision. Stable systems should become quieter when evidence permits.

Governance continues only while a bounded next check/action can plausibly change a material decision. When represented decision-changing questions are resolved or honestly bounded and another review would only repeat known information, stop adding governance and act.

Reference outcomes:

`READY | NARROW_AND_PROCEED | EVIDENCE_NEEDED | STOP_OR_ESCALATE`

A generic closure tool cannot prove that the caller omitted no material blocker. `READY` is always bounded by the completeness of represented material inputs.

## 5.11 Agency-Preserving Uncertainty

`UNKNOWN` must not silently become `SAFE`, but uncertainty need not imply paralysis.

When safe evidence-seeking exists:

`UNKNOWN -> reduce consequence envelope -> reversible/read-only/low-risk evidence action -> update evidence -> expand or narrow proportionally`

Unknown information may propagate when it is not critical to applicability. If an unknown field is critical to safe/valid interpretation, narrow/fail rather than silently ignore it.

## 5.12 Influence Integrity and Anti-Sovereign Closure

Feedback, preference, affective pressure, correction, designation, and authorization are not interchangeable.

`persuasion is input, not evidence`

`signal strength != authority strength`

External input may legitimately influence what an Agent explores without granting arbitrary use of ambient credentials.

ENA may use final accountable decision-makers, but must not depend on an infallible, irreplaceable, self-sealing sovereign. Authority cannot make its own correctness unfalsifiable, grant itself unlimited scope by self-description, or permanently forbid future replacement/review.

## 5.13 Inherited Composed Claim-Pack Validator

v0.3.7 candidate.2 retains the accepted composed-validator implementation released through v0.3.6 Current (originating in the v0.3.3 falsification/repair lineage) under `tools/validate_contracts.py`, together with its inherited fixture/regression corpus. This preserved implementation surface protects previously falsified semantics while the broader architecture evolves.

Its key machine properties remain:

- one typed resolution layer for consequential cross-artifact references;
- no silent cross-namespace resolution;
- support binds back to the target claim;
- material applicability dimensions fail/narrow when required observations are absent;
- mandatory evidence references resolve where registries are supplied;
- ambiguous duplicate identities fail closed;
- claim-aware triggered obligations gate the claims they actually bind;
- positively typed/registered authority semantics;
- recovery state/history evidence remains distinct;
- partial support cannot establish an unnarrowed full-support claim;
- malformed registry/input shapes return machine verdicts rather than uncaught success;
- obligation-status vocabulary remains schema-bound;
- root-provenance independence is authoritative where declared;
- direct id-less support does not invent a registry identity;
- explicit caller-controlled evaluation time remains required where applicable.

The retained trust boundary is equally important:

> **The composed validator validates represented contract semantics; it does not establish the external-world truth of every registry, evidence grade, mandate, observation, causal relation, or support assertion.**

Passing implementation tests protects known semantics; it does not prove universal correctness of v0.3.7 candidate.2.

---

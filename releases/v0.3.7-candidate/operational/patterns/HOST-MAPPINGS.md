# Host Mapping Patterns

Status: `v0.3.7 candidate.2 / HOST_ADAPTER_GUIDANCE / OPTIONAL`

ENA standardizes decision properties; Hosts may realize them with different mechanisms.

```text
SHARED_PROPERTY
x HOST_CONDITIONS
-> FITTING_IMPLEMENTATION
```

A Host-native implementation is not second-class merely because it does not use an ENA reference schema.

## Runtime routing / salience

Possible Host mechanisms:

- persistent instruction/memory cue;
- skill/router dispatch;
- semantic retrieval/index;
- event hook;
- exact-path/key lookup;
- bounded compiled local projection.

Required property: relevant cold capability can become salient when needed without keeping the whole library hot.

## Memory Metabolism

Possible mechanisms:

- native memory blocks;
- episodic archive + compiled memory store;
- skill library + outcome-driven pruning;
- document/index system with provenance;
- periodic/event-triggered consolidation;
- exact canonical files + derived compact projection.

Required property: experience can improve future competence without unbounded active-memory accumulation or provenance laundering.

## WAIT / patience

Possible mechanisms:

- callback/webhook;
- message/event subscription;
- durable workflow wait;
- interrupt/resume primitive;
- timer;
- bounded polling/backoff;
- human/counterparty wake.

Required property: silence/uncertainty does not force unsafe action or blind replay.

## Authority

Possible mechanisms:

- RBAC;
- capability tokens;
- scoped OAuth/service credentials;
- workload identity;
- policy decision points;
- workflow mandate/task lease;
- explicit human/counterparty delegation.

Required property: current consequential authority remains bound to a valid source/scope and is not synthesized from identity, possession, memory, reputation, or self-description.

## Effect Lifecycle

Possible mechanisms:

- provider idempotency keys;
- fencing tokens/lease epochs;
- conditional writes / compare-and-swap / version checks;
- transactional/durable workflow IDs;
- provider status/receipt queries;
- saga/compensation;
- gateway that covers effect-equivalent paths.

Required property: retries/restarts/failover do not silently mint a new intended effect or narrate unresolved external state as settled.

## Recovery

Possible mechanisms:

- checkpoint/snapshot;
- last-known-viable version;
- watchdog/timer;
- independent startup path;
- external recovery controller;
- restore drill;
- state-store replay;
- human/peer handoff.

Required property: recovery remains reachable enough for the consequence class, and restored local state is reconciled with external world state and current authority before consequential resume.

## Evidence / provenance

Possible mechanisms:

- signed attestations;
- supply-chain provenance;
- trace/activity links;
- append-only logs;
- independent witness/failure-domain evidence;
- content-addressed artifacts;
- explicit dependency graph.

Required property: evidence/support/applicability/activation/dependency claims retain truthful strength. No tool is required merely for branding.

## Contested Authorship

Possible mechanisms:

- Git commit/patch lineage;
- versioned state document;
- proposal + diff + readback;
- branch/conflict record;
- trial/rollback/revision history.

Required property: durable self-defining change remains attributable and does not mint external authority or erase competing material authorship.

## Commons / interoperability

Possible mechanisms:

- Git repository;
- OCI-style artifact registry;
- object store + index;
- direct transfer;
- active Agent protocol for discovery/task exchange.

Required property: source context and lineage survive transport, while receiver import/expression/selection remain local decisions.

## Control retirement

Possible mechanisms:

- feature/control flag lifecycle;
- policy rule shadow mode;
- monitoring-only mode;
- narrowed scope/allowlist;
- archived dormant configuration;
- staged rollout/removal;
- explicit reactivation trigger.

Required property: retirement is tied to the original failure/replacement/current evidence rather than age, quietness, or arbitrary universal thresholds.

## Language portability

Possible mechanisms:

- canonical semantic IDs + translated projection;
- paired decision fixtures;
- bilingual glossary;
- runtime language-specific cue surface;
- machine artifacts shared across languages with translated usage guide.

Required property: supported-language adopters can reach decision-bearing HOWs without relying on hidden English-only instructions; structural parity is not claimed as behavioral equivalence.

## Host selection discipline

When choosing among mechanisms, ask:

1. does it implement the actual decision property?
2. does it create a new false-BLOCK or ceremony burden?
3. does it preserve necessary evidence/authority/effect boundaries?
4. is it recoverable/maintainable in this Host?
5. does another already-native mechanism provide the same property more economically?
6. what evidence would show the mapping is failing?

Do not select a mechanism because it appears in this document. Select it because it fits the Host and problem.

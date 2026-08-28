# Evolution Commons Patterns

Status: `v0.3.7 candidate.2 / OPERATIONAL_PATTERN_LIBRARY / OPTIONAL`

Evolution Commons is a discoverable possibility pool. It is **not** one mandated registry product and not an automatic update channel.

```text
PUBLISH != DISCOVER != IMPORT != EXPRESS != EXPERIMENT != LOCALLY_SELECT
```

Each step remains separately authorized and locally evaluated.

## Pattern A — Git / repository Commons

Useful when:

- human/Agent reviewability matters;
- versioned text/code/artifacts fit Git economics;
- pull/review/fork lineage is useful.

Mechanism shape:

```text
content-addressed commit/tree
+ discoverable index/catalog
+ source evidence/context
+ receiver clone/fetch
+ receiver-local review/reselection
```

Do not confuse branch recency or star/popularity with fitness.

## Pattern B — OCI-style content-addressed registry

Useful when adaptations are packaged artifacts and immutable digests, manifests, provenance, promotion channels, and caching matter.

Mechanism shape:

```text
artifact digest
+ metadata/index
+ optional attestations
+ pull by receiver
+ receiver verifies identity/context
+ receiver locally selects
```

A registry signature/attestation can strengthen origin/integrity claims but does not prove local usefulness or authority to apply.

## Pattern C — object store + explicit index

Useful when artifacts are large or do not map naturally to Git/OCI.

Keep discovery metadata separate from payload storage:

```text
object identity/digest
+ index entry
+ source/context/evidence refs
+ access policy
+ receiver-local validation
```

Do not rely on bucket listing order as semantic ranking.

## Pattern D — direct transfer

Useful for bounded peer-to-peer or counterparty exchange where a global registry is unnecessary.

Transfer should still preserve enough source identity/context/negative lineage to prevent a received object from becoming context-free truth.

## Pattern E — active Agent protocol / A2A-style exchange

Useful for live discovery, task delegation, messaging, capability negotiation, or active collaboration.

This solves a different problem from durable Commons storage.

```text
ACTIVE_PROTOCOL != DURABLE_COMMONS
DISCOVER_AGENT != DISCOVER_DURABLE_ADAPTATION
TASK_RESULT != INDEPENDENT_EVIDENCE
```

A Host may compose an active protocol with Git/OCI/object-store Commons, but one does not automatically implement the other.

## Minimum portable adaptation shape

A Commons entry should preserve enough to let a receiver make its own decision. Depending on the adaptation, useful fields/refs include:

- immutable content identity/digest;
- source candidate/adaptation identity;
- hypothesis/change;
- source environment/context;
- source experiments/evaluations;
- source selection posture;
- expression/dormancy context;
- negative evidence/lineage;
- dependencies/unknowns;
- provenance/authentication claims with truthful strength;
- protected-subject / authority limitations when material.

`adaptation-packet.v2` is ENA's portable carrier for a bounded subset of this source context. It is not a complete Commons registry protocol.

## Receiver procedure

```text
DISCOVER
-> verify source/content identity as needed
-> inspect source context + negative lineage
-> decide whether import is authorized/useful
-> import without upgrading source proof
-> choose local expression/experiment surface
-> perform local reality contact when selection is claimed
-> record receiver-local result
```

Source success is evidence about the source environment. It is not automatically receiver applicability.

## Publisher autonomy / receiver autonomy

Publishers may publish when actually authorized and lawful; receivers may ignore or reject without vetoing publication.

Receivers may also re-test an adaptation that failed elsewhere when environments materially differ. Local positive evidence does not erase source negative lineage.

## Security / evidence boundary

Commons mechanisms must not silently upgrade:

```text
digest -> authentication
signature -> authorization
popularity -> fitness
source selection -> receiver selection
transport success -> semantic compatibility
```

Host-specific access control, provenance, scanning, sandboxing, and supply-chain verification may be appropriate, but ENA does not mandate one vendor stack.

## Selection principle

Choose the substrate by artifact type, collaboration model, trust/evidence needs, latency, scale, and Host economics.

No substrate becomes "the ENA Commons" merely because it is currently convenient.

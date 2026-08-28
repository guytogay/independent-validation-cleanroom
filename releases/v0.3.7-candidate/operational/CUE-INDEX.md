# Operational Cue Index — v0.3.7 candidate.2

Status: `WORKING_CANDIDATE / OPERATIONAL_ROUTER / NOT_CURRENT / NOT_FROZEN`

Use this when the Agent knows **what problem it has** but does not yet know which ENA mechanism to retrieve.

This is a cue surface, not a universal keyword classifier. Host-native routers, skills, memory indexes, event hooks, or semantic retrieval may implement the same function.

## 0. Consequence-first pre-router

Before adding governance machinery, ask what kind of decision is actually being made.

```text
Does the action materially affect an external/protected subject?
Does it depend on external authority?
Can retry/restart duplicate or contradict a world effect?
Can waiting change the safe decision?
Can missing knowledge/evidence change the decision?
Can self-change alter future behavior or recovery?
```

If none are materially relevant, prefer the lightweight path. ENA does not require ceremony merely because a reference organ exists.

## Fast cue routes

| Ordinary cue / failure | Route first | Concrete next surface |
|---|---|---|
| "I know we stored this before, but I cannot find or trust what was retrieved." | `OA-RET-01 Retrieval Obligation` | `references/general/retrieval-obligation/` + Host search/index/exact-path retrieval |
| "Memory keeps growing; raw incidents are accumulating but competence is not." | `OA-MEM-01 Memory Metabolism` | `HOW-MAP` memory branch + Host compiler/archive/retrieval patterns |
| "I need to summarize/compact, but omission could change the decision." | `OA-PROJ-01 Projection/Compaction` | preserve decision-material lineage; route cold dependencies back through Retrieval Obligation |
| "Nothing has happened yet. Should I retry, keep acting, or wait?" | `OA-WAIT-01 WAIT/Pause` | `references/general/wait-state/` or Host callback/interrupt/timer/polling |
| "Am I actually allowed to do this consequential action?" | `OA-AUTH-01 Authority` | `references/general/authority-lease/`; use `NOT_REQUIRED` when authority is genuinely irrelevant |
| "This external write may be retried/replayed after timeout or restart." | `OA-EFF-01 Effect Lifecycle` | `references/general/effect-lifecycle/`; choose idempotency/fencing/status/compensation/WAIT by target semantics |
| "The process restarted or restored state. Can it safely resume?" | `OA-REC-01 Recovery` | `references/general/recovery-adapter/` + effect/authority reconciliation |
| "A worker changed, forked, or failed. Who still owes the obligation?" | `OA-COM-01 Commitment/Settlement` | shared distinction in `HOW-MAP`; first candidate uses Effect + Authority + explicit settlement guidance; recovered machine organ is deferred |
| "Is this still the same Agent?" | `OA-ID-01 Purpose-relative continuity` | `operational/procedures/PURPOSE-RELATIVE-CONTINUITY.md`; ask continuity-for-what-decision, not metaphysical sameness |
| "A durable purpose/value/refusal/self-definition is being changed." | `OA-AUTHOR-01 Contested Authorship` | `references/advanced/contested-authorship/`; ordinary task/cache state may be out of scope |
| "Someone/another Agent raises an objection that could change a consequential decision." | `OA-STAND-01 Standing Input` | `operational/procedures/STANDING-INPUT.md`; being heard does not create sovereignty or authority |
| "Several reviewers agree. Are these actually independent supports?" | `OA-EVID-01 Evidence dependency` | `references/advanced/evidence-dependency-map/`; preserve common causes, no fake scalar independence score |
| "I have evidence, but does it support this claim for this subject now?" | `OA-EVID-01 Evidence envelope` | `references/advanced/evidence-envelope/`; keep evidence/support/applicability/provenance/witness/activation distinct |
| "A failure, friction, discovery, or success suggests the Agent should change." | `OA-EVO-01 Evolution` | Current v2 evolution record + candidate `tools/ena_evolve_v2.py` when assembled; variation may remain latent |
| "I want to share/import an adaptation from another Agent/Host." | `OA-MIG-01 Migration/Commons` | packet v2 + `operational/patterns/EVOLUTION-COMMONS.md`; source success is not receiver-local proof |
| "Agents need to discover or task each other live." | `OA-MIG-01 Active interoperability` | Host/A2A-style live protocol pattern; do not confuse active protocol with durable Commons |
| "A safeguard/control may no longer be necessary." | `OA-ECO-01 Control Retirement` | `operational/procedures/CONTROL-RETIREMENT.md`; no-incident/low-use alone is not retirement evidence |
| "A metric, reputation rule, or resource limit is shaping the population." | `OA-ECO-01 Ecology` | Host/field/mesocosm branch; measurement is itself selection pressure |
| "The rules exist in the repository but are not salient at runtime." | `OA-RT-01 Runtime routing` | compact hot cues -> cold operational retrieval; exact resident kernel remains Host-selectable |
| "How much ENA must I activate to adopt it?" | `OA-ADOPT-01 Adoption` | semantic baseline + operational routing; bundled references remain optional/default-off |
| "English and Chinese wording may lead to different decisions." | `OA-ADOPT-01 Language` | candidate zh-CN operational projection + paired semantic fixtures; structural parity is not behavioral proof |

## Failure-shape routes

### False confidence

If the failure sounds like:

```text
"it exists, therefore it was loaded"
"five Agents agree, therefore five independent confirmations"
"we restored state, therefore the world rolled back"
"we have a credential, therefore we have authority"
"the source adaptation worked, therefore it will work here"
"the schema passed, therefore the evidence is true"
```

route toward Retrieval / Evidence / Recovery / Authority / Migration before adding new Core rules.

### False BLOCK / ceremony

If the failure sounds like:

```text
"every local action needs a lease"
"every memory write is constitutional authorship"
"every recovery needs an independent rescue plane"
"every control needs a fixed numeric retirement threshold"
"every reference included in the package must be activated"
```

look for the relevant **not-applicable / NOT_REQUIRED / lightweight** branch before escalating governance.

### Unresolved world state

If local state and external reality may disagree:

```text
timeout
restart
restore
fork
failover
partial callback
unknown provider result
```

prefer `UNKNOWN + status/settlement query + WAIT/NARROW/ESCALATE` over narrating completion or blind replay.

## Traversal rule

After selecting a route:

```text
CUE-INDEX
-> HOW-MAP
-> REFERENCE-INDEX.yaml
-> exact procedure/reference/Host pattern
```

If the exact reference is absent or not applicable, do not invent universal machinery. Use the Host-native branch or retain an honest residual.

## Evidence boundary

A cue match proves only that a branch may be worth retrieving.

```text
CUE_MATCH != APPLICABILITY_PROVEN
ROUTER_CONFIGURED != FUTURE_SALIENCE_PROVEN
```

Natural fresh-session salience remains field evidence.

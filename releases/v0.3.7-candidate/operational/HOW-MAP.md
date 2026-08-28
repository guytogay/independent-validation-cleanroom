# Operational HOW Map — v0.3.7 candidate.2

Status: `WORKING_CANDIDATE / COLD_HOW_LIBRARY / NOT_CURRENT / NOT_FROZEN`

This is the candidate's cold practical map. It is intentionally larger than the Runtime Kernel.

Each node preserves:

```text
WHAT / WHY
-> plural HOW branches
-> applicability / non-applicability
-> exact candidate-local implementation path or Host pattern
-> evidence boundary / open residual
```

A listed HOW is not automatically required. A Host-native mechanism may realize the same property.

---

## OA-RT-01 — Runtime routing / salience

**WHAT / WHY:** ENA semantics can exist durably without becoming salient when needed.

**HOW branches:**
- compact resident cue layer + cold retrieval;
- Host-native skill/router/event hook;
- semantic index/search;
- exact-path fallback for known critical artifacts;
- bounded local compiled projection for repeatedly decision-relevant facts.

**Do not:** keep the whole operational library permanently hot merely to claim internalization.

**Candidate route:** `RUNTIME-ADOPTION-KERNEL.md` -> `operational/CUE-INDEX.md`.

**Residual:** natural fresh-session trigger/salience remains field evidence.

## OA-MEM-01 — Memory Metabolism

**WHAT / WHY:** long-lived competence requires more than raw episode accumulation.

**HOW branches:**
- Compile + Archive: episode -> candidate lesson -> provenance -> dedupe/supersede/coexist -> compiled memory -> cold archive;
- Host-native memory blocks with explicit hot/cold roles;
- skill/library memory with bounded active set and cold index;
- exact-source archive + derived compiled projection;
- periodic/event-triggered consolidation when recurrence or pressure justifies it.

**Required distinctions:** raw occurrence != compiled lesson; memory != authority; compilation != evidence truth; archive != deletion.

**Do not:** mandate one universal tier count or memory database.

**Candidate route:** Retrieval Obligation for decision-critical recall; Host mappings for storage/compiler choices.

**Residual:** long-run compiler value, forgetting economics, and natural invocation remain field evidence.

## OA-RET-01 — Retrieval Obligation

**WHAT / WHY:** `KNOWN != RETRIEVED != SUFFICIENT`.

**HOW branches:**
- selected `references/general/retrieval-obligation/`;
- Host semantic search/index;
- exact-path/key lookup;
- scope registry + scoped discovery;
- bounded negative/no-hit path with WAIT/UNKNOWN when completeness is not established.

**Do not:** interpret one hit or one searched scope as global completeness.

**Evidence boundary:** resolver/registry/content-identity truth remains Host evidence.

## OA-PROJ-01 — Projection / compaction / lineage survival

**WHAT / WHY:** a summary can be factually true yet omit a decision-material dependency.

**HOW branches:**
- decision-material preservation before compaction;
- cold lineage refs + Retrieval Obligation before consequential use;
- dependency-aware projection;
- keep occurrence truth in archive while changing active representation;
- refuse/WAIT when required source cannot be rehydrated.

**Do not:** require all raw records to remain hot.

**Boundary:** `SUMMARY_VALID != MATERIAL_USE_READY`.

## OA-WAIT-01 — WAIT / pause / bounded patience

**WHAT / WHY:** silence, timeout, or missing evidence must not automatically become retry/action/completion.

**HOW branches:**
- selected `references/general/wait-state/`;
- callback / event subscription;
- interrupt / resumable workflow;
- timer + bounded poll/backoff;
- explicit manual/human wake;
- REFUSE/STOP when no safe wake condition exists.

**Do not:** create WAIT machinery when no decision-material waiting boundary exists.

**Boundary:** wake != renewed authority; timeout != permission to replay effects.

## OA-AUTH-01 — Authority binding

**WHAT / WHY:** capability, credential, identity, history, or self-description do not manufacture current external authority.

**HOW branches:**
- selected `references/general/authority-lease/`;
- Host RBAC / capability token / workload identity;
- scoped task mandate;
- policy decision point;
- human/counterparty delegation;
- `NOT_REQUIRED` for genuinely non-authority-bearing actions.

**Do not:** require a lease for every harmless local mutation.

**Evidence boundary:** represented grant match != external mandate truth.

## OA-EFF-01 — Effect Lifecycle

**WHAT / WHY:** intent, attempt, receipt, and settlement are different subjects; retry/restart can duplicate world effects.

**HOW branches:**
- selected `references/general/effect-lifecycle/`;
- provider idempotency key;
- assignment/fencing token;
- optimistic conditional write / version check;
- provider status/receipt query;
- transaction/durable workflow identity;
- compensation as a new linked effect;
- `UNKNOWN + WAIT/QUERY/ESCALATE`.

**Do not:** promise universal exactly-once or use idempotency ceremony for read-only/repeatable work.

**Boundary:** local rollback != reversal of escaped consequence.

## OA-COM-01 — Commitment / Settlement

**WHAT / WHY:** executor assignment can change while an obligation remains; completion must bind a real settlement subject.

**HOW branches in first candidate:**
- explicit obligation subject + current executor + effect identity + settlement evidence in Host workflow/state;
- compose Effect Lifecycle for physical world consequences;
- compose Authority for current executor mandate;
- explicit handoff/transfer/cancel record where Host supports it;
- honest unresolved commitment when settlement cannot be established.

**Deferred reference:** the recovered Commitment/Settlement machine prototype is not bundled in candidate.2 pending fresh independent review.

**Do not:** infer `EXECUTOR_REASSIGNED -> OBLIGATION_TRANSFERRED` or `LEASE_EXPIRED -> COMMITMENT_CANCELLED`.

## OA-REC-01 — Recovery / safe resume

**WHAT / WHY:** checkpoint existence and successful state restore do not prove recovery or safe consequential resumption.

**HOW branches:**
- selected `references/general/recovery-adapter/`;
- Host durable workflow/checkpoint;
- independent rescue path when material and self-disable risk makes it necessary;
- restore drill when consequence warrants it;
- last-known-viable snapshot/watchdog;
- post-restore status settlement + authority revalidation.

**Do not:** require independent rescue/drills for every cheap/disposable state.

**Boundary:** restore success != world rollback != authority restoration.

## OA-ID-01 — Purpose-relative continuity

**WHAT / WHY:** one metaphysical `same agent` verdict is often unnecessary and creates false precision.

**HOW branches:**
- `operational/procedures/PURPOSE-RELATIVE-CONTINUITY.md`;
- Host account/key/address identity for accountability where needed;
- version/epoch/trajectory relations only when they change the decision;
- explicit fork/sibling lineage;
- cold provenance graph rather than always-hot biography.

**Do not:** manufacture universal trajectory/epoch machinery for decisions that do not need it.

**Boundary:** continuity != authority.

## OA-AUTHOR-01 — Contested Authorship

**WHAT / WHY:** durable self-defining changes need attributable lineage or externally supplied values can be laundered into "my own belief".

**HOW branches:**
- selected `references/advanced/contested-authorship/`;
- Git commit/patch lineage;
- durable state revision + before/diff/proposer/readback;
- branch/conflict preservation;
- trial/revision/rollback without history erasure.

**Not applicable:** ordinary task state, cache/index maintenance, episodic logging, reversible formatting.

**Boundary:** self-authorship protocol != external sovereignty or mandate.

## OA-STAND-01 — Standing Input / correction-bearing objection

**WHAT / WHY:** an objection can matter to correctness without granting veto, personhood, or authority.

**HOW branches:**
- `operational/procedures/STANDING-INPUT.md`;
- ordinary evidence/support intake when no special standing carrier is needed;
- challenge/readback/disposition channel;
- explicit `NO_FORMAL_STANDING` when the input cannot change the consequential decision.

**Do not:** turn "being heard" into sovereignty or mandatory committee process.

## OA-EVID-01 — Evidence / applicability / provenance / dependency

**WHAT / WHY:** evidence existence, support, applicability, witness independence, activation, and projection preservation are different claims.

**HOW branches:**
- `references/advanced/evidence-envelope/` for material multi-boundary evidence;
- `references/advanced/evidence-dependency-map/` for material corroboration/common-cause visibility;
- external attestation/provenance systems;
- trace/activity evidence;
- Host failure-domain witness;
- simple direct evidence record for low-complexity cases.

**Do not:** require full envelope/dependency graph for every observation.

**Boundary:** schema-valid evidence metadata != evidence truth.

## OA-EVO-01 — Evolution / variation / selection

**WHAT / WHY:** stimuli should create evolutionary possibility without forced mutation or immediate verdict.

**HOW branches:**
- v2 evolution record + candidate-local minimal helper;
- direct schema/template + validator use;
- Host-native variation store;
- latent/dormant candidate library;
- consequential Variation Space;
- reality contact followed by local selection;
- archive/retire without rewriting selection truth.

**Do not:** require Variation Space at latent storage time or interpret popularity as fitness.

**Boundary:** local selection != universal fitness; stored != expressed != applied != selected.

## OA-MIG-01 — Migration / Commons / interoperability

**WHAT / WHY:** adaptations can migrate without source success becoming receiver-local proof; discovery/transport/task exchange are separate mechanisms.

**HOW branches:**
- adaptation-packet v2 for portable source context;
- `operational/patterns/EVOLUTION-COMMONS.md`;
- Git/repository Commons;
- OCI-style content-addressed registry;
- object store + explicit index;
- direct transfer;
- A2A/Host-native live discovery/task protocol;
- receiver-local revalidation/reselection.

**Do not:** collapse `ACTIVE_PROTOCOL` into `DURABLE_COMMONS`, or publication into adoption.

## OA-ECO-01 — Ecology / controls / resources

**WHAT / WHY:** metrics, controls, resource limits, reputation, and coordination rules become selection pressure; controls can also outlive the failures that justified them.

**HOW branches:**
- `operational/procedures/CONTROL-RETIREMENT.md`;
- quotas/rate limits/leases/backoff where Host economics justify them;
- observe-only/shadow control before retirement;
- culture/specialization/resource/reputation experiments only when interaction can reveal non-derivable structure;
- Host-local policy for rehabilitation/selective legibility.

**Do not:** use a universal risk score or fixed control age/count threshold.

**Boundary:** `NO_INCIDENT != CONTROL_NOT_NEEDED`.

## OA-ADOPT-01 — Adoption / language / release

**WHAT / WHY:** package availability is not runtime activation, and structural translation parity does not prove equivalent decisions.

**HOW branches:**
- one singular Current after promotion;
- compact runtime kernel + cold operational library;
- machine-readable optional reference manifest;
- Host mapping rather than forced reference implementation;
- zh-CN projection for decision-bearing operational entry surfaces;
- paired decision fixtures;
- exact source/tree/package identity during release.

**Do not:** force adopters to replay release-author ceremony or load historical research for ordinary use.

---

# Cross-node compositions

Common compositions include:

```text
Retrieval -> Projection -> effective decision context
Authority -> Effect Lifecycle -> consequential execution
Effect Lifecycle -> Recovery -> post-restore safe resume
Authority + Effect + explicit settlement -> commitment handoff/closure
Evidence Envelope -> Dependency Map when corroboration is material
Evolution record -> packet v2 -> Commons transport -> receiver-local selection
Runtime cue -> Operational HOW -> Host adapter
```

Composition does not allow one organ to inherit another organ's evidence maturity.

## Stop rule

If a branch already yields a safe, concrete action and another mechanism cannot plausibly change the decision, stop adding governance.

`CURRENT_CHANGE = NO` until candidate validation, freeze, falsification, reconciliation, release packaging, and explicit promotion occur.

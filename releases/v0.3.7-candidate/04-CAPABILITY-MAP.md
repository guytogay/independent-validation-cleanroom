# 4. Capability Map

Every capability is scoped and evidenced. A capability title does not grant the capability, and a capability does not automatically grant authority.

Core capability vocabulary retained from v0.3.4:

`ENA-CAP-001` Read Workspace / Project State  
`ENA-CAP-002` Write Workspace / Project State  
`ENA-CAP-003` Execute Code / Commands  
`ENA-CAP-004` Manage Processes / Services  
`ENA-CAP-005` Manage Agent Configuration  
`ENA-CAP-006` Manage Prompts / Instructions  
`ENA-CAP-007` Manage Skills / Tools / Plugins  
`ENA-CAP-008` Manage Persistent Memory / State  
`ENA-CAP-009` Introspect Current Capabilities  
`ENA-CAP-010` Create Isolated Candidate  
`ENA-CAP-011` Version / Snapshot State  
`ENA-CAP-012` Restore Known-Good State  
`ENA-CAP-013` Independent Recovery  
`ENA-CAP-014` Stable-Write Protection  
`ENA-CAP-015` Event / Audit Logging  
`ENA-CAP-016` Health Verification  
`ENA-CAP-017` Control-Plane Verification  
`ENA-CAP-018` External Write Actions  
`ENA-CAP-019` Irreversible / High-Consequence Actions  
`ENA-CAP-020` Approval / Permission Gating  
`ENA-CAP-021` Multi-Agent / Multi-Context Operation  
`ENA-CAP-022` Cross-Agent Provenance  
`ENA-CAP-023` Scheduled / Persistent Operation  
`ENA-CAP-024` Resource Accounting  
`ENA-CAP-025` Network / Tool Boundary Control  
`ENA-CAP-026` Secrets / Credential Boundary  
`ENA-CAP-027` Semantic / Schema Versioning  
`ENA-CAP-028` Evidence Attachment  
`ENA-CAP-029` Safe Disable / Detach  
`ENA-CAP-030` Residue Detection  
`ENA-CAP-031` Session Bootstrap / Durable Reality Read  
`ENA-CAP-032` Mutation Entry Interception  
`ENA-CAP-033` Trigger Observation  
`ENA-CAP-034` Evolution Inbox / Candidate Queue  
`ENA-CAP-035` Host Change / Upgrade Preflight  
`ENA-CAP-036` Dynamic Host Location / Indirection  
`ENA-CAP-037` Authority Revocation  
`ENA-CAP-038` Conditional Capability / Lease Enforcement  
`ENA-CAP-039` Lifecycle Evolution Wake  
`ENA-CAP-040` Catch-up Evolution Review  
`ENA-CAP-041` Authority Reconstitution After Restore / Resume  
`ENA-CAP-042` Independent Environmental Trace Evidence  
`ENA-CAP-043` Scoped Trust / Authority Attribution  
`ENA-CAP-044` Multi-Axis Improvement Accounting  
`ENA-CAP-045` Consequence Exposure and Responsibility Attribution  
`ENA-CAP-046` Adoption Profile Declaration  
`ENA-CAP-047` Risk-Proportional Governance Routing  
`ENA-CAP-048` Machine-Checkable Artifact Validation  
`ENA-CAP-049` Temporary Authority Elevation  
`ENA-CAP-050` Compensation Debt Tracking  
`ENA-CAP-051` Activation Contract / Opportunity Window  
`ENA-CAP-052` Interruption, Suspension, Resume, and Catch-Up  
`ENA-CAP-053` Emergent Role Lifecycle  
`ENA-CAP-054` Composition-Level Revalidation  
`ENA-CAP-055` Deferred Commitment / Consequence Escrow  
`ENA-CAP-056` Memory Class Isolation and Knowledge Governance Boundary  
`ENA-CAP-057` Recovery Kernel Mutation Boundary  
`ENA-CAP-058` Enforcement Surface / Effect-Equivalent Path Discovery  
`ENA-CAP-059` Control Integrity / Protected Control Substrate  
`ENA-CAP-060` Authorization Artifact Integrity  
`ENA-CAP-061` Governance Value & Applicability Contract  
`ENA-CAP-062` Contextual Governance Projection / Active Governance Set  
`ENA-CAP-063` Governance Fitness, Simplification, Dormancy, and Retirement  
`ENA-CAP-064` Canonical History / Derived Knowledge Projection Separation  
`ENA-CAP-065` Claim–Evidence Support Relation  
`ENA-CAP-066` Triggered Material Obligation Closure  
`ENA-CAP-067` Layered Capability / Route / Authority Binding  
`ENA-CAP-068` Evidence-Backed Stage Admission Pack  
`ENA-CAP-069` Agency-Preserving Uncertainty Resolution  
`ENA-CAP-070` Viability Economics and Project-Scale Governance Fitness  
`ENA-CAP-071` Persistent Evolution and Open Contribution Substrate  

The v0.3.6 candidate inherits the explicit evolutionary-metabolism capabilities released through v0.3.5 Current:

`ENA-CAP-072` Evolution Signal Capture and Review  
`ENA-CAP-073` Variation Space Provisioning / Mutation Containment  
`ENA-CAP-074` Outcome-Based Variation Evaluation and Selection  
`ENA-CAP-075` Adaptation Migration / Import / Differential Validation  
`ENA-CAP-076` Adaptive Pruning / Dormancy / Archive / Retirement  
`ENA-CAP-077` Continuity Vector Introspection  
`ENA-CAP-078` Language Semantic Projection / Cross-Language Conformance  
`ENA-CAP-079` Governance Closure / Decision-Convergence Detection  
`ENA-CAP-080` Composition Emergence Observation / Recombination Evaluation  

For `ENA-CAP-065..071` retained from v0.3.4:

- **CAP-065:** represent claim, observed evidence, claimed/evidence scope, explicit support relation, and material provenance/independence basis; cross-boundary transfer requires independently evidenced transfer/equivalence/invariance, and derivative repetition must not be counted as independent corroboration.
- **CAP-066:** when a material trigger occurs, externalize the duty through explicit states such as `PENDING`, `SATISFIED`, `NOT_REQUIRED`, `DEFERRED_AUTHORIZED`, `FAILED`, `UNKNOWN`; broad completion cannot ignore unresolved material obligations, and `SATISFIED` requires appropriate closure evidence.
- **CAP-067:** distinguish Agent, Host, model, tool/service/adapter, credential/configuration, route, capability evidence, subject control, mandate, and authority; material binding change selectively invalidates affected evidence/authority rather than causing global Agent rebirth.
- **CAP-068:** keep requested stage distinct from admitted stage; self-assessment is hypothesis, not qualification evidence.
- **CAP-069:** `UNKNOWN` should constrain consequence while permitting low-risk/reversible/read-only/evidence-seeking action when available; uncertainty is not automatically safety or paralysis.
- **CAP-070:** observe governance cost, latency, human attention, coordination, rework, control-composition/compensation complexity, prevented failure, reusable evidence, useful variety, and project viability without forcing one universal scalar.
- **CAP-071:** preserve project continuity across sessions/Agents/models/hosts through durable project state and open contribution while keeping contribution, reconciliation, promotion, and implementation authority distinct.

For `ENA-CAP-072..080` inherited from the v0.3.5 released evolution-metabolism surface:

- **CAP-072:** capture corrections/failures/friction/success/opportunity/environment changes as evolution signals and review them without requiring every wake to produce a mutation.
- **CAP-073:** provide or identify a real bounded surface where uncertain variation can meet reality; the space may permit meaningful internal self-change without self-minting external mandate.
- **CAP-074:** observe multiple outcome dimensions and select/retain/adapt/reject variations based on reality rather than intention.
- **CAP-075:** import source adaptations with provenance/applicability as migration candidates, compare material source/receiver differences, and avoid treating transfer as local proof.
- **CAP-076:** move stale/redundant/harmful adaptations out of the active set through reversible dormancy/archive where appropriate, without silently erasing selection history.
- **CAP-077:** inspect decision-relevant continuity dimensions across session/model/Host/restore/clone changes instead of forcing a binary metaphysical identity claim.
- **CAP-078:** bind language projections to stable semantic IDs/source identity and evaluate material decision equivalence rather than literal translation alone.
- **CAP-079:** detect when further governance no longer has a plausible decision-changing path and stop adding ceremony while retaining honest residuals.
- **CAP-080:** evaluate new compositions/recombinations for degradation, neutral/additive effects, super-additive benefit, and emergent capability as well as failure.

Capability enumeration is a map, not a requirement to instantiate or validate all capabilities for every task. LITE candidate evaluation should externalize only material capabilities for the current consequence envelope.

A Host may implement several capabilities through one organ or one capability through several mechanisms.

> **Capability vocabulary describes what can be made real; it does not grant authority merely by being named.**

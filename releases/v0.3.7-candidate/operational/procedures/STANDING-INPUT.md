# Standing Input Procedure

Status: `v0.3.7 candidate.2 / BOUNDED_OPERATIONAL_PROCEDURE / OPTIONAL`

## Use when

An Agent, human, tool, subsystem, or affected counterparty raises an objection/correction that could materially change a consequential decision.

Do not invoke formal standing machinery when the input cannot change the decision. Ordinary feedback/evidence intake is enough.

```text
BEING_HEARD != BEING_SOVEREIGN
STANDING != AUTHORITY != PERSONHOOD
```

## Procedure

### 1. Bind the decision

Name the consequential decision the input could change.

If no decision is identifiable, route as ordinary feedback rather than manufacturing standing.

### 2. Capture the input without upgrading it

Record, in the Host's normal representation:

- source / speaker / affected subject when known;
- claim or objection;
- evidence/support refs when present;
- claimed consequence or error;
- scope and uncertainty.

The existence of a speaker does not prove the claim. The absence of credentials does not automatically make the factual content irrelevant.

### 3. Determine decision materiality

Use one bounded posture:

- `MATERIAL_TO_DECISION`
- `NOT_MATERIAL_TO_DECISION`
- `MATERIALITY_UNKNOWN`

Materiality is not a dignity/rank score. Ask only whether the input could change correctness, consequence ownership, authority, evidence, recovery, or another material decision boundary.

### 4. Route material/unknown input

If material or unresolved:

- inspect supporting evidence;
- route to the relevant ENA HOW (Authority, Effect, Recovery, Evidence, Continuity, etc.);
- expose the semantic interpretation back to the relevant decision-maker/Agent when feasible;
- preserve disagreement or uncertainty instead of silently dropping it.

### 5. Record disposition

Use a bounded outcome such as:

- `ACCEPTED_CHANGED_DECISION`
- `ACCEPTED_NO_DECISION_CHANGE`
- `REJECTED_WITH_BASIS`
- `DEFERRED_WAITING_FOR_EVIDENCE`
- `DISAGREEMENT_PRESERVED`
- `NO_FORMAL_STANDING`

The vocabulary is reference guidance, not a required Host enum.

### 6. Preserve authority boundaries

A material objection can cause a decision to be reconsidered without granting the objector authority to execute, approve, veto, or set policy.

If authority changes, that requires its own source/basis.

### 7. Close when further intake cannot change the decision

Do not turn standing into endless governance. If another bounded review cannot plausibly alter the decision and residuals are explicit, close the standing procedure while preserving the occurrence/disposition.

## False-BLOCK controls

Do not require:

- committee review for ordinary low-consequence feedback;
- legal/personhood classification before factual correction can be considered;
- veto power for every affected subject;
- formal Standing records when normal evidence intake already resolves the issue.

## Evidence boundary

This procedure proves neither the objection nor the legitimacy of the source. It prevents decision-relevant input from disappearing merely because it arrived outside the currently dominant execution path.

```text
INPUT_CONSIDERED != INPUT_TRUE
INPUT_CONSIDERED != AUTHORITY_GRANTED
```

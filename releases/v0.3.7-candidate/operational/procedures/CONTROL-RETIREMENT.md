# Control Retirement Procedure

Status: `v0.3.7 candidate.2 / BOUNDED_OPERATIONAL_PROCEDURE / OPTIONAL`

## Use when

A safeguard, gate, monitoring rule, approval, fallback, rate limit, feature/control flag, or other intervention may no longer be needed in its current form.

Do not retire a control merely because it has been quiet, old, low-use, or incident-free.

```text
NO_INCIDENT != CONTROL_NOT_NEEDED
LOW_USAGE != NO_PROTECTIVE_VALUE
AGE != RETIREMENT_THRESHOLD
```

## Reference outcomes

- `KEEP_ACTIVE`
- `NARROW_SCOPE`
- `SHADOW_OBSERVE`
- `DORMANT_ARCHIVE`
- `RETIRE_REMOVE`
- `REACTIVATE`
- `UNKNOWN_WAIT`

These are procedure outcomes, not mandatory Host enums.

## Procedure

### 1. Recover the original failure / purpose

Identify what decision-changing failure, risk, uncertainty, dependency, or temporary migration state justified the control.

If the original purpose cannot be reconstructed, do not silently delete. Use `UNKNOWN_WAIT` or bounded investigation.

### 2. Ask whether the original failure still exists

Possible answers:

- still present;
- structurally removed;
- materially reduced/narrowed;
- replaced by another mechanism;
- unknown.

Evidence may come from architecture changes, dependency removal, real field outcomes, audits, new provider guarantees, or another concrete mechanism.

No-incident history alone is ambiguous because the control itself may have prevented incidents.

### 3. Identify replacement / coverage

If another mechanism now carries the same protective property, verify the overlap explicitly.

Examples:

- provider idempotency replaces a local duplicate-write guard for one path;
- a migrated workflow removes a temporary compatibility gate;
- native RBAC replaces a provisional wrapper check;
- a new cue/router makes a manual reread gate unnecessary.

Do not infer complete replacement when effect-equivalent paths remain outside the new mechanism.

### 4. Check dependency and blast-radius effects

Before retirement ask whether anything still relies on the control for:

- safety/consequence ownership;
- observability;
- recovery;
- evidence/provenance;
- authority boundary;
- migration compatibility;
- fallback behavior.

A control may have acquired a secondary role even if its original trigger disappeared.

### 5. Prefer reversible reduction when uncertainty remains

Useful paths include:

- `NARROW_SCOPE` — keep only the contexts where the failure remains;
- `SHADOW_OBSERVE` — stop blocking but keep bounded observation;
- `DORMANT_ARCHIVE` — deactivate while retaining configuration/history for reactivation;
- staged exposure/limited cohort when Host supports it.

The purpose is not ritual de-escalation. Jump directly to removal when evidence makes intermediate stages pointless; keep the control active when consequence requires it.

### 6. Define reactivation evidence before removal

Specify what future observation would justify `REACTIVATE` or another control.

Examples:

- recurrence of the original failure;
- dependency rollback;
- provider guarantee withdrawn;
- new effect-equivalent path appears;
- language/Host/model change invalidates applicability.

### 7. Retire with lineage, not amnesia

A retirement record should preserve enough to answer:

- what problem the control addressed;
- why it is no longer needed or why scope changed;
- what replaced it, if anything;
- evidence used;
- where the old mechanism can be recovered;
- reactivation condition.

```text
REMOVE_FROM_ACTIVE_ARCHITECTURE != ERASE_FROM_LINEAGE
```

### 8. Close only when another check cannot change the retirement decision

Do not keep collecting evidence forever merely to make retirement look rigorous.

## False-BLOCK controls

Do not require:

- universal age thresholds;
- incident-count thresholds;
- one scalar control-value score;
- shadow periods when immediate retirement is obviously safe and reversible;
- permanent retention of every obsolete control in the active runtime.

## Evidence boundary

This procedure structures retirement reasoning. It does not prove counterfactual safety or guarantee that the failure will never recur.

`RETIRE_REMOVE` is a scoped decision under current evidence and environment, not universal proof that the mechanism was always unnecessary.

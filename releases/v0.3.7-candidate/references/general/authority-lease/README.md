# Authority Grant / Lease — Optional Reference

Status: `v0.3.7 candidate.2 / GENERAL_OPTIONAL_REFERENCE / DEFAULT_OFF / NOT_NORMATIVE_ONTOLOGY`

Use when a consequential action depends on represented external authority scope or validity.

Use the lightweight `NOT_REQUIRED` path for genuinely non-authority-bearing actions; do not create permission ceremony for harmless local work.

Bundled machine files reuse the selected research reference bytes. A Host may instead use RBAC, capability tokens, workload identity, policy decision points, or explicit task mandates.

Key boundaries:

```text
IDENTITY != AUTHORITY
CREDENTIAL_REF_MATCH != CREDENTIAL_EXTERNALLY_VALID
AUTHORIZED_BY_REPRESENTED_LEASE != WORLD_POLICY_CERTIFIED
EPOCH_BINDING_AVAILABLE != UNIVERSAL_EPOCH_REQUIREMENT
```

Machine PASS checks represented grant/query consistency only. It cannot establish that the authority source is authentic or still legitimate in the external world.

See `../../../operational/HOW-MAP.md` (`OA-AUTH-01`) for Host branches and composition with effects/recovery.

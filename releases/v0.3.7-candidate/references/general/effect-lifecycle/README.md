# Effect Lifecycle — Optional Reference

Status: `v0.3.7 candidate.2 / GENERAL_OPTIONAL_REFERENCE / DEFAULT_OFF / NOT_NORMATIVE_ONTOLOGY`

Use for consequential external effects where retry, timeout, restart, failover, settlement, compensation, or effect identity can change the decision.

Do not require effect/idempotency ceremony for read-only or intrinsically repeatable low-consequence operations.

Bundled contract, fixtures, and tools reuse the selected research reference bytes. Host-native alternatives include provider idempotency, fencing tokens, conditional writes, status queries, durable workflow identity, compensation, and WAIT.

Key boundary:

```text
INTENT != ATTEMPT != RECEIPT != SETTLEMENT
LOCAL_ROLLBACK != WORLD_ROLLBACK
RECEIPT_REPRESENTED != RECEIPT_EXTERNALLY_TRUE
EXACTLY_ONCE != UNIVERSAL_ENA_PROMISE
```

Machine PASS proves represented lifecycle consistency only.

See `../../../operational/HOW-MAP.md` (`OA-EFF-01`) for plural Host HOWs and `../recovery-adapter/` for safe-resume composition.

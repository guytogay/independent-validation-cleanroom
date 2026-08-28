# WAIT State — Optional Reference

Status: `v0.3.7 candidate.2 / GENERAL_OPTIONAL_REFERENCE / DEFAULT_OFF / NOT_NORMATIVE_ONTOLOGY`

Use when the safe next action is to pause for a represented wake condition rather than infer completion, retry blindly, or keep acting through uncertainty.

Do not manufacture WAIT state when no decision-material waiting boundary exists.

Bundled contract, fixtures, and tools reuse the selected research reference bytes. Host callbacks, interrupts, durable workflow waits, timers, or bounded polling/backoff may implement the same property without using this JSON vocabulary.

Key boundary:

```text
SILENCE != COMPLETION
TIMEOUT != RETRY_AUTHORITY
WAKE != RENEWED_AUTHORITY
WAIT != ABANDONMENT
```

Machine PASS proves represented state consistency, not that the wake condition will occur or that an external event is true.

See `../../../operational/HOW-MAP.md` (`OA-WAIT-01`) for Host alternatives and interaction with Effect Lifecycle.

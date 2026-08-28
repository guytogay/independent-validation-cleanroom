# Legacy evolution tooling — v1.2 compatibility

Status: `v0.3.7 candidate.1 / LEGACY_COMPATIBILITY / NOT_DEFAULT_V2_PATH`

`ena_evolve_v1_2.py` is the inherited v0.3.5-era state/schema 1.2 reference tool, preserved byte-for-byte for regression/history compatibility.

It is **not** the default v0.3.7 evolution path and does not fully implement v2 mutation-pressure, latent/expression, or adaptation-packet-v2 semantics. In particular, it retains the known `--variation-space` requirement on `propose` and `import`.

Use `../ena_evolve_v2.py` for candidate-local v2 latent record and packet-v2 orchestration.

The historical adversarial probes that specifically exercise this v1.2 tool are colocated here:

- `candidate1_adversarial_v1_2.py`;
- `candidate2_adversarial_v1_2.py`.

They remain executable regression history for the legacy tool. They are not candidate.1 semantic validators and do not establish v2 parity, external truth, or release readiness.

```text
LEGACY_TOOL_RETAINED != LEGACY_TOOL_IS_NORMATIVE_V2
LEGACY_REGRESSION_RETAINED != LEGACY_PATH_IS_DEFAULT
```

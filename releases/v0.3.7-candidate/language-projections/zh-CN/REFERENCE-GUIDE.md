# Candidate Optional References — 简体中文使用指南

状态：`v0.3.7 candidate.2 / ZH-CN_USAGE_GUIDE / MACHINE_ARTIFACTS_REMAIN_CANONICAL`

本候选包中的 reference 是**可选实现/机器参考**，不是 ENA 的强制器官清单。

```text
BUNDLED != REQUIRED
BUNDLED != DEFAULT_ACTIVE
REFERENCE_SCHEMA != ENA_ONTOLOGY
HOST_NATIVE_EQUIVALENT != NONCOMPLIANT
```

机器可读 optionality 以 `../../references/REFERENCE-MANIFEST.yaml` 为准。reference 内部 schema/fixture/tool 不逐文件翻译，以避免出现两套 machine canonical bytes。

## 一般 optional references

### Retrieval Obligation 0.5

用于：decision-material knowledge 依赖 retrieval scope、effective content identity、freshness 或 sufficiency closure。

不用于：只是“系统有长期存储”或 trivial task，并不存在 decision-material retrieval dependency。

路径：`../../references/general/retrieval-obligation/`

### WAIT

用于：应等待一个明确 wake condition，而不是把 silence/uncertainty 变成重复执行。

不用于：根本不存在 decision-material wait boundary。

路径：`../../references/general/wait-state/`

### Authority Lease

用于：consequential action 是否有当前外部 authority 会改变决策。

不用于：genuinely non-authority-bearing action；此时允许 `NOT_REQUIRED`。

路径：`../../references/general/authority-lease/`

### Effect Lifecycle

用于：retry、restart、settlement、compensation、effect identity 会影响 external-effect decision。

不用于：read-only 或 intrinsically repeatable low-consequence work。

路径：`../../references/general/effect-lifecycle/`

### Recovery Adapter

用于：recovery reachability、restore 后 world state 或 authority reconciliation 会改变 safe resume。

不用于：cheap/disposable state 不需要独立 rescue/drill 的场景。

路径：`../../references/general/recovery-adapter/`

## Advanced / specialized optional references

### Evidence Envelope

用于：material claim 需要显式区分 evidence、support、applicability、provenance、witness、activation、projection。

不用于：trivial observation 或简单直接 evidence 已足够的场景。

路径：`../../references/advanced/evidence-envelope/`

### Evidence Dependency Map

用于：多个 agreeing observation 之间的 common cause 会改变 corroboration 判断。

不用于：普通 recurrence/low-risk work，没有 dependency graph 的决策价值。

路径：`../../references/advanced/evidence-dependency-map/`

### Contested Authorship

用于：durable self-surface change 中 origin、endorsement、conflict、revision 或 authority laundering 会改变决策。

不用于：ordinary task state、cache/index maintenance、episodic logging、reversible formatting。

路径：`../../references/advanced/contested-authorship/`

## 本候选未 bundled，但没有被退休

Recovered Commitment/Settlement machine prototype 暂留 research lineage；candidate.2 没有把它打包，不等于它已被证伪或废弃。

```text
NOT_BUNDLED != RETIRED
SILENT_DISSOLUTION != EVIDENCE_BACKED_RETIREMENT
```

## Machine evidence 边界

Candidate Assembly Gate 已在 candidate-local path 上执行 bundled reference selftests。PASS 说明 exercised representation/consistency path 与当前 oracle/fixture 一致。

它不证明：external authority truth、receipt authenticity、recovery truth、evidence truth、universal Host applicability，或未来所有 case。

Observed fixture counts 只是 corpus fact，不是 architectural threshold。

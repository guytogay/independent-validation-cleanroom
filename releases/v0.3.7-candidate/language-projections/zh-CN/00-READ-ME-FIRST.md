# ENA v0.3.7 candidate.2 — 请先阅读

状态：**WORKING_CANDIDATE / NOT_CURRENT / NOT_FROZEN / NOT_RELEASED**

当前唯一面向采用者的 Current 仍然是 `releases/current/` 下的 v0.3.6。

本目录是 v0.3.7 candidate.2 的简体中文语义/运行投影，用来测试：在不增加无必要 Core 条文的情况下，ENA 能否通过具体 HOW 路由变得更可住、更可执行。

**ENA 的存在，是为了让持续的自我进化成为一种可行能力。**

## 建议先读

1. `../../CANDIDATE-BASELINE.yaml` — candidate 当前状态、谱系、机器证据、剩余 gate；
2. `RUNTIME-ADOPTION-KERNEL.md` — 中文 hot cue 语义面；
3. `operational/CUE-INDEX.md` — 从普通问题找到 HOW 家族；
4. `operational/HOW-MAP.md` — 中文 cold HOW map；
5. `operational/procedures/` — Purpose-Relative Continuity、Standing Input、Control Retirement；
6. `operational/patterns/` — Evolution Commons、Host Mappings；
7. `REFERENCE-GUIDE.md` — optional reference 的中文适用/不适用说明；
8. `01-CONSTITUTION.md` — 继承的 38 条稳定不变量；
9. `09-EVOLUTION-METABOLISM.md` — 进化生态语义与 candidate 工具/路由边界；
10. `projection-manifest.yaml` — 本投影与 candidate 身份、覆盖面和证据边界。

## Candidate.2 的实际变化

v0.3.6 的核心生态区分继续保持：

- `刺激 != 变异 != 改进`；
- 变异可以长期潜伏；
- `已保存 != 已表达 != 已应用 != 已选择`；
- 生命周期 / 表达 / 选择是不同轴；
- 局部成功不是普适适应度；
- 来源成功/流行度不是 receiver-local proof；
- 恢复本地状态不等于外部世界回滚，也不等于旧 authority 自动恢复。

v0.3.7 candidate.2 新增的是**怎么活出来**：

```text
HOT CUE
-> CUE-INDEX
-> HOW-MAP
-> procedure / optional reference / Host-native pattern
-> action / WAIT / UNKNOWN / NOT_APPLICABLE
```

完整 HOW 库不需要永久塞进热上下文。

## Reference 不是强制器官

candidate.2 打包了 Retrieval Obligation、WAIT、Authority Lease、Effect Lifecycle、Recovery Adapter、Evidence Envelope、Evidence Dependency Map、Contested Authorship 等 reference。

但：

```text
BUNDLED != REQUIRED
BUNDLED != DEFAULT_ACTIVE
REFERENCE_SCHEMA != ENA_ONTOLOGY
HOST_NATIVE_EQUIVALENT != NONCOMPLIANT
```

Recovered Commitment/Settlement machine prototype 本次没有 bundled，但仍保留在 research lineage：`NOT_BUNDLED != RETIRED`。

## 当前工具边界

candidate.2 的主要实用 v2 路径是：

`../../tools/ena_evolve_v2.py`

它可以创建不强制提前指定 Variation Space 的 latent v2 record，并提供 candidate-local record validation、packet-v2 export/import。

继承的 v1.2 工具保留在：

`../../tools/legacy/ena_evolve_v1_2.py`

它不再是 candidate 默认路径。

新的 v2 helper 仍然不是完整 evolution lifecycle engine，也不能证明外部 evidence/authority/recovery/receipt 本身是真的。

## 中文证据边界

`semantic-fixtures.v3.yaml` 定义了中英文 Operational Architecture 场景的预期 route/decision property；Stage-4 machine gate 已检查结构和 route parity。

这仍然不等于真实模型在 fresh session 中已经被证明中英文行为等价。

```text
TRANSLATED != BEHAVIORALLY_EQUIVALENT
FIXTURE_DEFINED != MODEL_PASS
```

## Candidate 边界

candidate.2 需要 targeted successor revalidation、exact pre-freeze validation、external freeze、reconciliation 与 explicit release decision；fresh Phase A 已作为 predecessor 的 sealed occurrence 保留，不由 author 重做。

当前不能因为文件已经很完整，就把它称为 Current。

> **内化 cue，按需寻找 HOW。**
>
> **压缩语义主干，让具体 HOW 分叉。**

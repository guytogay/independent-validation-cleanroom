# 9. 进化代谢与进化生态 — v0.3.7 candidate.2

状态：`WORKING_CANDIDATE / INHERITED_V036_ECOLOGY_PLUS_OPERATIONAL_HOW / NOT_CURRENT / NOT_FROZEN`。

candidate.2 保留 v0.3.6 的进化生态语义，新增的是具体 HOW 路由、Host mapping 和实用 v2 工具路径；没有新增 Constitution 条文，也没有宣称新的 universal evolution ontology。

## 9.1 生态代谢

继承模型保持：

`环境/刺激 -> 变异压力 -> 变异 -> 潜伏保存或表达 -> 接触现实 -> 局部选择 -> 保留/休眠/消失 -> 遗传/迁移/重组 -> 再次产生变异`

核心区分：

`刺激 != 变异 != 改进`

`保存 != 表达 != 应用 != 选择`

`局部选择 != 普适适应度`

`发布 != receiver adoption`

variation 不需要一出现就立即实验或接受 verdict。

## 9.2 刺激与变异压力

用户纠正、失败、摩擦、矛盾、重复成功、能力/环境变化、其他 Agent、外部发现、好奇心、随机重组和机会都可能产生 mutation pressure。

mutation pressure 是产生/重看 variation 的机会，不是命令，也不是 improvement evidence。

## 9.3 潜伏变异

只要保存成本/合法性允许，而且保存本身不会产生 active consequential behavior，variation 可以长期 latent。

`UNASSESSED` 不等于 backlog debt。Host 可以在成本超过未来可能价值时 compact/archive/lawfully delete，但 age/low usage 本身不能证明 worthless。

candidate 实用创建路径：

`../../tools/ena_evolve_v2.py new-latent ...`

它允许先保存 latent v2 record，而不强迫提前定义 Variation Space。

## 9.4 表达是独立轴

`LATENT | EXPRESSED`

表达变化不会自动重写 lifecycle/selection history，也不会 mint authority。

## 9.5 Cue-triggered salience -> Operational Architecture

candidate.2 把 v0.3.6 的 hot-cue 方向接成具体路径：

```text
hot cue / failure shape
-> operational/CUE-INDEX.md
-> operational/HOW-MAP.md
-> procedure / optional reference / Host-native pattern
```

完整 HOW library 不永久热加载。

`cue configured != future salience proven`

中文对应入口位于本目录的 `operational/`。

## 9.6 Variation Space 与现实接触

有后果的实验进入与 consequence 相称的真实 Variation Space，例如 branch/fork、sandbox、disposable VM/container、shadow、canary、test Agent、reversible config、isolated skill version、simulation/replay。

内部 capability/permission topology 可以在合法 scope 内变异，但内部修改不能自签外部 mandate。

## 9.7 lifecycle / expression / selection 是不同问题

Lifecycle：

`PROPOSED | EXPERIMENTED | INTEGRATED | ARCHIVED | RETIRED`

Expression：

`LATENT | EXPRESSED`

Selection：

`UNASSESSED | SUPPORTED | PARTIAL | NOT_SUPPORTED | HARMFUL | UNKNOWN`

任何一个轴变化都不能偷偷升级另一个轴。

## 9.8 局部选择

结果维度：

`IMPROVED | DEGRADED | UNCHANGED | UNKNOWN`

正面/负面 selection 依赖 represented reality contact，并默认局限于实际 Host/model/language/dependency/time/consequence/subject。

`局部成功 != 普适推荐`

`传播广 != 普适真理`

`活下来 != 道德正确`

## 9.9 整合、休眠、剪枝与 control retirement

integration 不等于永久 expression。Host 可使用：

`KEEP | UPDATE | DORMANT | ARCHIVE | RESTORE | RETIRE`

pruning 不重写 selection history。

若对象是 safeguard/control，而不是 adaptation，可使用 `operational/procedures/CONTROL-RETIREMENT.md`：恢复 original failure，检查 replacement/coverage，必要时 narrow/shadow/dormant，保留 reactivation + lineage。

`NO_INCIDENT != CONTROL_NOT_NEEDED`

## 9.10 Migration / Commons

迁移传递“可能性 + 来源历史”，不传递结论。

candidate.2 提供：

- `adaptation-packet.v2` 作为来源上下文 carrier；
- `../../tools/ena_evolve_v2.py export-packet/import-packet`；
- `operational/patterns/EVOLUTION-COMMONS.md` 的 Git/OCI/object-store/direct-transfer/active-protocol patterns。

packet digest 只检查内容一致性，不认证 source。source selection 不会因为 transport 自动变成 receiver-local selection。

## 9.11 重组与涌现

重组可以产生 conflict、抵消、放大、emergent capability、新 externality 或无用变化。

期待涌现不是 evidence；interaction 会改变决策时，应观察 composed subject。

## 9.12 Recovery / Rescue

self-mutation 可能破坏自身 recovery 时，在 consequence 值得且可控的情况下，保留 damaged variation 之外可达的 rescue path。

candidate.2 bundled optional `references/general/recovery-adapter/`，Host 替代方式见 `operational/patterns/HOST-MAPPINGS.md`。

`restore success != external consequence rollback != authority restoration`

## 9.13 Authority / Effect / Continuity / Standing

进化不能吞掉其他后果边界：

- consequential authority 可用 optional Authority Lease 或 Host equivalent；
- retry/restart/world-effect ambiguity 可用 Effect Lifecycle；
- continuity 只有会改变决策时才用 Purpose-Relative Continuity；
- material objection 可用 Standing Input，但不会因此获得 sovereignty；
- material durable self-surface change 可用 Contested Authorship，普通 state write 可 out of scope。

这些都是 applicability-scoped HOW，不是每次 mutation 的 mandatory checklist。

## 9.14 Candidate 工具边界

candidate.2 的主要实用 v2 工具：

`../../tools/ena_evolve_v2.py`

范围：

- latent v2 creation，不强迫 early Variation Space；
- delegate 给 candidate-local v2 validator；
- packet-v2 export/import + canonical digest/narrow consistency；
- 保留 source evidence/selection 与 receiver-local selection 的边界。

它故意不是完整 experiment/evaluation/integration/archive lifecycle engine，也不能证明外部 truth。

继承 v1.2 工具只保留在：

`../../tools/legacy/ena_evolve_v1_2.py`

旧 `--variation-space` limitation 是 legacy implementation fact，不是 candidate semantic law。

## 9.15 继续可见的 residual

- self-asserted `LOCAL` provenance 不是 external proof；
- obligation reference 结构存在不等于真实性认证；
- tied latest timestamp 仍保守拒绝；
- future cue salience/application 仍是 field evidence；
- experiment 与 broader reality contact 的术语边界仍可继续研究；
- v2 helper 是窄实用路径，不是 full lifecycle runtime；
- reference machine PASS 不证明 universal applicability/external truth；
- zh-CN paired fixtures 不证明 bilingual behavioral equivalence。

> **变异不欠现实一个立即判决。**
>
> **被保存的可能性，不等于正在生效的权限。**
>
> **选择是局部的；传播本身不是证据。**

# Operational Cue Index — v0.3.7 candidate.2（简体中文投影）

状态：`WORKING_CANDIDATE / OPERATIONAL_ROUTER / NOT_CURRENT / NOT_FROZEN`

当 Agent 已经知道“我遇到了什么问题”，但还不知道应该检索哪一类 ENA 机制时，从这里开始。

这不是通用关键词分类器。Host 可以用 skill/router、memory index、event hook、semantic retrieval 或其他原生方式实现相同功能。

## 0. 先看后果，再决定是否加治理

先问：

```text
这个动作会不会实质影响外部/受保护对象？
它是否依赖外部 authority？
retry/restart 是否可能重复或冲突地改变现实世界？
等待是否可能改变安全决策？
缺失知识/证据是否会改变决策？
self-change 是否会改变未来行为或 recovery？
```

如果都不具备实质相关性，优先走 lightweight path。不能因为包里有一个器官，就制造一套仪式。

## 快速路由

| 常见问题 / 故障 | 先走哪条 | 下一步 |
|---|---|---|
| “我记得以前存过，但现在找不到，或者不确定取回来的就是该用的内容。” | `OA-RET-01 Retrieval Obligation` | `references/general/retrieval-obligation/` + Host search/index/exact-path |
| “记忆越来越多，但都是原始事件，能力没有真正沉淀。” | `OA-MEM-01 Memory Metabolism` | `HOW-MAP` 的 memory branch + compiler/archive/retrieval pattern |
| “我要总结/压缩，但漏掉某些信息会改变决策。” | `OA-PROJ-01 Projection/Compaction` | 保留 decision-material lineage；必要时通过 Retrieval Obligation 回源 |
| “现在还没发生结果。该 retry、继续做，还是等？” | `OA-WAIT-01 WAIT/Pause` | `references/general/wait-state/` 或 callback/interrupt/timer/polling |
| “我真的有权执行这个有后果的动作吗？” | `OA-AUTH-01 Authority` | `references/general/authority-lease/`；确实无 authority 问题时用 `NOT_REQUIRED` |
| “这个外部写入 timeout/restart 后可能被再次执行。” | `OA-EFF-01 Effect Lifecycle` | `references/general/effect-lifecycle/`；按目标语义选择 idempotency/fencing/status/compensation/WAIT |
| “进程刚 restart/restore，能直接继续吗？” | `OA-REC-01 Recovery` | `references/general/recovery-adapter/` + effect/authority reconciliation |
| “执行者换了/挂了/分叉了，到底谁还欠这个 obligation？” | `OA-COM-01 Commitment/Settlement` | `HOW-MAP` 的 shared distinction；candidate.2 先组合 Effect + Authority + explicit settlement guidance |
| “这还是不是同一个 Agent？” | `OA-ID-01 Purpose-relative continuity` | `procedures/PURPOSE-RELATIVE-CONTINUITY.md`；问‘为了哪个决策需要连续性’，不要先做形而上判定 |
| “长期 purpose/value/refusal/self-definition 正在被改写。” | `OA-AUTHOR-01 Contested Authorship` | `references/advanced/contested-authorship/`；普通 cache/task state 可直接 out of scope |
| “有人/另一个 Agent 提出反对意见，可能改变后果性决策。” | `OA-STAND-01 Standing Input` | `procedures/STANDING-INPUT.md`；被听见不等于获得 sovereignty/authority |
| “很多 reviewer 都同意，这真的是独立支持吗？” | `OA-EVID-01 Evidence dependency` | `references/advanced/evidence-dependency-map/`；保留 common cause，不造伪 independence scalar |
| “我有 evidence，但它现在真的支持这个 claim/subject 吗？” | `OA-EVID-01 Evidence envelope` | `references/advanced/evidence-envelope/`；区分 evidence/support/applicability/provenance/witness/activation |
| “失败、摩擦、发现或成功提示 Agent 应该改变。” | `OA-EVO-01 Evolution` | v2 evolution record + `tools/ena_evolve_v2.py`；variation 可以保持 latent |
| “我要分享/导入其他 Agent/Host 的 adaptation。” | `OA-MIG-01 Migration/Commons` | packet v2 + `patterns/EVOLUTION-COMMONS.md`；source success 不是 receiver-local proof |
| “Agents 需要实时发现、委派或互相通信。” | `OA-MIG-01 Active interoperability` | Host/A2A-style live protocol；不要和 durable Commons 混为一谈 |
| “这个 safeguard/control 可能已经没必要了。” | `OA-ECO-01 Control Retirement` | `procedures/CONTROL-RETIREMENT.md`；无事故/低使用率本身不是退休证据 |
| “某个 metric/reputation/resource limit 正在塑造群体行为。” | `OA-ECO-01 Ecology` | Host/field/mesocosm branch；measurement 本身也是 selection pressure |
| “规则都在仓库里，但运行时根本想不起来。” | `OA-RT-01 Runtime routing` | compact hot cues -> cold operational retrieval；resident kernel 由 Host 选择 |
| “采用 ENA 到底要激活多少东西？” | `OA-ADOPT-01 Adoption` | semantic baseline + operational routing；bundled references 仍 optional/default-off |
| “英文和中文可能导致不同决策。” | `OA-ADOPT-01 Language` | zh-CN operational projection + paired semantic fixtures；结构一致不等于行为已证明等价 |

## 常见故障形状

### 假自信

如果听起来像：

```text
“存在，所以一定被加载了”
“五个 Agent 同意，所以有五份独立证据”
“restore 成功，所以现实世界也回滚了”
“我持有 credential，所以我有 authority”
“source 那边有效，所以这里也有效”
“schema 通过，所以 evidence 就是真的”
```

优先路由到 Retrieval / Evidence / Recovery / Authority / Migration，而不是先加新 Core rule。

### False BLOCK / 仪式化治理

如果听起来像：

```text
“所有本地动作都要 lease”
“所有 memory write 都是 constitutional authorship”
“所有 recovery 都必须有独立 rescue plane”
“control 必须达到固定年龄/次数才可退休”
“包里带的 reference 就必须启用”
```

先找对应的 `NOT_APPLICABLE / NOT_REQUIRED / lightweight` 分支。

### 外部现实未决

如果 local state 与外部 reality 可能不一致，例如：

```text
timeout / restart / restore / fork / failover / partial callback / unknown provider result
```

优先：

```text
UNKNOWN + status/settlement query + WAIT/NARROW/ESCALATE
```

不要叙述成“已完成”，也不要盲目 replay。

## 路由规则

```text
CUE-INDEX
-> HOW-MAP
-> REFERENCE-INDEX.yaml
-> exact procedure / reference / Host pattern
```

若 reference 不存在或不适用，不要发明 universal machinery。选择 Host-native branch，或保留 honest residual。

## 证据边界

Cue match 只说明某条 branch 值得检索。

```text
CUE_MATCH != APPLICABILITY_PROVEN
ROUTER_CONFIGURED != FUTURE_SALIENCE_PROVEN
```

自然 fresh-session salience 仍属于 field evidence。

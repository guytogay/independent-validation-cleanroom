# Purpose-Relative Continuity Procedure（简体中文投影）

状态：`v0.3.7 candidate.2 / BOUNDED_OPERATIONAL_PROCEDURE / OPTIONAL`

## 何时使用

当某个实际决策取决于：Agent/system/trajectory 在 restart、restore、migration、fork、model/Host change、identity rotation 或 handoff 后，是否保留了足够的连续关系。

不要因为有人问“它还是不是同一个 Agent？”就自动启动。若 continuity 不会改变任何决策，直接返回 `NOT_REQUIRED`。

## 目标

把一个 universal sameness verdict 换成：**这个具体决策真正需要哪些 continuity relation。**

```text
same_agent_for(purpose)
!= one global SAME_AGENT boolean
```

## 流程

### 1. 先写清楚要做什么决策

例如：restore 后能否继续 commitment？fork 是否继承 accountability history？credential/authority 能否继续用？旧 evidence 是否仍适用？某个 durable preference 是否仍属于 active self-surface？

若没有任何决策会变化，结束：`NOT_REQUIRED`。

### 2. 只识别相关 subject

按需识别 Evolutionary Subject、承担后果的 Protected Subject(s)、以及外部 counterparty/accountability subject。不要先建 universal identity ontology。

### 3. 选择会改变决策的 continuity dimensions

可包括：causal/state lineage、commitment/obligation、value/purpose/refusal、memory/compiled-learning、evidence/provenance、social/accountability identity、authority/mandate、resource/recovery、Host/model/tool/language projection 等。

列表开放；只选会改变当前决策的维度。

### 4. 对每个维度给 bounded posture

```text
CONTINUES
DOES_NOT_CONTINUE
UNKNOWN
NOT_APPLICABLE
```

Host 有真实 identifier/evidence 时就用，例如 commit/tree、account/key、checkpoint、obligation id、authority grant、evidence source、lineage edge。

缺证据就保持 `UNKNOWN`；名字没变不能证明所有 continuity 都没变。

### 5. 应用 non-transfer guards

不要自动推断：

```text
state continuity -> authority continuity
shared history -> shared post-fork authority
memory inheritance -> obligation ownership
same external account -> same internal trajectory
restore success -> current mandate
```

若当前决策依赖这些关系，继续路由到 Authority / Commitment / Recovery / Evidence HOW。

### 6. 只针对这个 purpose 给结论

返回：

- `CONTINUITY_SUFFICIENT_FOR_DECISION`
- `CONTINUITY_INSUFFICIENT_FOR_DECISION`
- `CONTINUITY_UNKNOWN_WAIT_OR_REVALIDATE`
- `NOT_REQUIRED`

不要把局部结论升级成 universal sameness。

### 7. 保留 fork/discontinuity truth

fork 时保留 shared-history lineage 和 fork 后 divergence。Sibling trajectories 可以共享 ancestry，但不共享后续 authority、obligation、evidence applicability 或 reputation。

continuity 断裂也不能擦掉旧 occurrence。Host 若需要，可创建 new epoch/trajectory id，但 ENA 不强制 universal identifier。

## 轻量例子

**本地 restart，没有外部 consequence：** 只决定一个 reversible formatting preference 是否继续。可能只需要 compiled preference continuity；authority/commitment/social identity 都 `NOT_APPLICABLE`。

**restore payment workflow：** state continuity 不够。必须组合 Effect Lifecycle + Recovery + Authority；即使 checkpoint 成功加载，仍可能是 `CONTINUITY_UNKNOWN_WAIT_OR_REVALIDATE`。

## 证据边界

这个流程只结构化 purpose-relative continuity decision，不认证 identity、personhood、legal succession、credential validity 或 mandate。

```text
CONTINUITY_SUFFICIENT_FOR_DECISION
!= UNIVERSAL_SAME_AGENT
!= AUTHORIZED
```

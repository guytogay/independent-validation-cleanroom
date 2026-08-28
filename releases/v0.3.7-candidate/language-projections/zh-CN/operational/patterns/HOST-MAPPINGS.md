# Host Mapping Patterns（简体中文投影）

状态：`v0.3.7 candidate.2 / HOST_ADAPTER_GUIDANCE / OPTIONAL`

ENA 标准化的是 decision property，不是某个固定实现。

```text
SHARED_PROPERTY
x HOST_CONDITIONS
-> FITTING_IMPLEMENTATION
```

Host-native implementation 不会因为没有使用 ENA reference schema 就变成“二等实现”。

## Runtime routing / salience

可用：persistent instruction/memory cue、skill/router dispatch、semantic retrieval/index、event hook、exact-path/key lookup、bounded compiled local projection。

**必须保留的属性：** relevant cold capability 能在需要时进入 salience，而不是把整个 library 永久热加载。

## Memory Metabolism

可用：native memory blocks；episodic archive + compiled memory；skill library + outcome-driven pruning；document/index + provenance；periodic/event consolidation；exact canonical files + derived compact projection。

**属性：** experience 能提高未来 competence，而不会导致 active memory 无限增长或 provenance laundering。

## WAIT / patience

可用：callback/webhook、message/event subscription、durable workflow wait、interrupt/resume、timer、bounded polling/backoff、human/counterparty wake。

**属性：** silence/uncertainty 不强迫 unsafe action 或 blind replay。

## Authority

可用：RBAC、capability token、scoped OAuth/service credential、workload identity、policy decision point、workflow mandate/task lease、explicit human/counterparty delegation。

**属性：** current consequential authority 绑定真实 source/scope，不能从 identity、possession、memory、reputation 或 self-description 合成。

## Effect Lifecycle

可用：provider idempotency key、fencing token/lease epoch、conditional write/CAS/version check、transactional/durable workflow ID、provider status/receipt query、saga/compensation、覆盖 effect-equivalent paths 的 gateway。

**属性：** retry/restart/failover 不会静默制造新的 intended effect，也不会把 unresolved external state 叙述成 settled。

## Recovery

可用：checkpoint/snapshot、last-known-viable version、watchdog/timer、independent startup path、external recovery controller、restore drill、state-store replay、human/peer handoff。

**属性：** recovery reachability 与 consequence class 相称；有后果 resume 前要把 restored local state 与 external world + current authority 对齐。

## Evidence / provenance

可用：signed attestation、supply-chain provenance、trace/activity links、append-only log、independent failure-domain witness、content-addressed artifact、explicit dependency graph。

**属性：** evidence/support/applicability/activation/dependency claim 保持 truthful strength；工具不能仅为 branding 而强制使用。

## Contested Authorship

可用：Git commit/patch lineage、versioned state document、proposal+diff+readback、branch/conflict record、trial/rollback/revision history。

**属性：** durable self-defining change 可追溯，不会 mint external authority，也不会擦除 competing material authorship。

## Commons / interoperability

可用：Git repo、OCI registry、object store + index、direct transfer、用于 discovery/task exchange 的 active Agent protocol。

**属性：** source context/lineage 在 transport 中存活；receiver 的 import/expression/selection 仍是 local decision。

## Control retirement

可用：feature/control flag lifecycle、policy shadow mode、monitor-only、narrowed scope/allowlist、dormant archived config、staged rollout/removal、explicit reactivation trigger。

**属性：** retirement 要绑定 original failure/replacement/current evidence，而不是 age、quietness 或 arbitrary universal threshold。

## Language portability

可用：canonical semantic IDs + translated projection、paired decision fixtures、bilingual glossary、language-specific runtime cue surface、跨语言共享 machine artifact + translated usage guide。

**属性：** supported-language adopter 不依赖隐藏 English-only HOW；structural parity 不被冒充为 behavioral equivalence。

## Host 选择纪律

选择 mechanism 时问：

1. 它是否真的实现目标 decision property？
2. 会不会制造新的 false-BLOCK / ceremony burden？
3. 是否保留必要的 evidence/authority/effect boundary？
4. 在这个 Host 上是否可 recovery / maintain？
5. Host 已有原生机制是否更经济地实现同一 property？
6. 什么 evidence 会说明 mapping 失败？

不要因为一个 mechanism 出现在这份文件里就选它；**因为它适合当前 Host 和问题才选。**

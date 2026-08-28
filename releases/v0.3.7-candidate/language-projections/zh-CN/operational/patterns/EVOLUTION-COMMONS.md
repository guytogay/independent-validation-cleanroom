# Evolution Commons Patterns（简体中文投影）

状态：`v0.3.7 candidate.2 / OPERATIONAL_PATTERN_LIBRARY / OPTIONAL`

Evolution Commons 是可发现的 possibility pool，不是指定某一个 registry 产品，也不是自动更新通道。

```text
PUBLISH != DISCOVER != IMPORT != EXPRESS != EXPERIMENT != LOCALLY_SELECT
```

每一步都分别受 authority 和 local evaluation 约束。

## Pattern A — Git / repository Commons

适合：需要 human/Agent review；artifact 适合 Git；pull/review/fork lineage 有价值。

```text
content-addressed commit/tree
+ discoverable index/catalog
+ source evidence/context
+ receiver clone/fetch
+ receiver-local review/reselection
```

branch 新、star 多、下载多都不等于 fitness。

## Pattern B — OCI-style content-addressed registry

适合 packaged artifact，尤其当 immutable digest、manifest、provenance、promotion channel、cache 有价值。

```text
artifact digest
+ metadata/index
+ optional attestation
+ receiver pull
+ receiver verify identity/context
+ receiver local selection
```

signature/attestation 可加强 origin/integrity，但不证明 local usefulness，也不授权 apply。

## Pattern C — object store + explicit index

适合大 artifact 或不适合 Git/OCI 的内容。

```text
object identity/digest
+ index entry
+ source/context/evidence refs
+ access policy
+ receiver-local validation
```

不要把 bucket listing order 当 semantic ranking。

## Pattern D — direct transfer

适合 bounded P2P/counterparty exchange，无需 global registry。仍要保留足够 source identity/context/negative lineage，避免收到的对象变成 context-free truth。

## Pattern E — active Agent protocol / A2A-style exchange

适合实时 discovery、task delegation、messaging、capability negotiation、active collaboration。

它解决的是另一类问题：

```text
ACTIVE_PROTOCOL != DURABLE_COMMONS
DISCOVER_AGENT != DISCOVER_DURABLE_ADAPTATION
TASK_RESULT != INDEPENDENT_EVIDENCE
```

Host 可以把 active protocol 与 Git/OCI/object-store Commons 组合，但不能说其中一个自动实现另一个。

## Portable adaptation 最小形态

按实际 adaptation，可保留：immutable content identity/digest、source candidate/adaptation id、hypothesis/change、source environment/context、experiments/evaluations、selection posture、expression/dormancy context、negative evidence/lineage、dependencies/unknowns、provenance/authentication claim、protected-subject/authority limitation。

`adaptation-packet.v2` 只承载其中一个 bounded subset，不是完整 Commons registry protocol。

## Receiver 流程

```text
DISCOVER
-> 按需验证 source/content identity
-> 查看 source context + negative lineage
-> 判断 import 是否 authorized/useful
-> import，但不升级 source proof
-> 选择 local expression/experiment surface
-> 声称 selection 前做 local reality contact
-> 记录 receiver-local result
```

source success 是关于 source environment 的 evidence，不自动变成 receiver applicability。

## Publisher / Receiver autonomy

publisher 在真正有 authority 且合法时可 publish；receiver 可以忽略/拒绝，而不是因为“不采用”就否决 publication。

receiver 也可在环境不同的时候重新测试 elsewhere-failed adaptation。local positive evidence 不能擦掉 source negative lineage。

## Security / evidence boundary

Commons 不能静默升级：

```text
digest -> authentication
signature -> authorization
popularity -> fitness
source selection -> receiver selection
transport success -> semantic compatibility
```

Host-specific access control、provenance、scanning、sandboxing、supply-chain verification 可以很重要，但 ENA 不绑定一个 vendor stack。

## 选择原则

按 artifact type、collaboration model、trust/evidence need、latency、scale 和 Host economics 选择 substrate。

任何 substrate 都不会因为“现在最方便”就成为唯一的 **the ENA Commons**。

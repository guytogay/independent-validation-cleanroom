# Standing Input Procedure（简体中文投影）

状态：`v0.3.7 candidate.2 / BOUNDED_OPERATIONAL_PROCEDURE / OPTIONAL`

## 何时使用

当 Agent、human、tool、subsystem 或 affected counterparty 提出 objection/correction，并且它可能实质改变一个 consequential decision。

如果这个 input 根本不会改变决策，不要制造 formal standing machinery；普通 feedback/evidence intake 就够了。

```text
BEING_HEARD != BEING_SOVEREIGN
STANDING != AUTHORITY != PERSONHOOD
```

## 流程

### 1. 绑定具体 decision

写清楚这个 input 可能改变哪个 consequential decision。若找不到具体 decision，就按普通 feedback 处理。

### 2. 接收 input，但不要自动升级它

按 Host 正常表示方式记录：source/speaker/affected subject（已知时）、claim/objection、evidence/support refs、声称的 consequence/error、scope 和 uncertainty。

有 speaker 不等于 claim 为真；没有 credential 也不等于事实内容无关。

### 3. 判断 decision materiality

使用 bounded posture：

- `MATERIAL_TO_DECISION`
- `NOT_MATERIAL_TO_DECISION`
- `MATERIALITY_UNKNOWN`

这不是 dignity/rank score。只问：它是否可能改变 correctness、consequence ownership、authority、evidence、recovery 或其他实质决策边界？

### 4. 对 material / unknown input 做路由

- 检查 supporting evidence；
- 路由到相关 ENA HOW（Authority、Effect、Recovery、Evidence、Continuity 等）；
- 可行时把 semantic interpretation 回显给实际 decision-maker/Agent；
- disagreement/uncertainty 不要静默丢掉。

### 5. 记录 disposition

可使用：

- `ACCEPTED_CHANGED_DECISION`
- `ACCEPTED_NO_DECISION_CHANGE`
- `REJECTED_WITH_BASIS`
- `DEFERRED_WAITING_FOR_EVIDENCE`
- `DISAGREEMENT_PRESERVED`
- `NO_FORMAL_STANDING`

这是 reference guidance，不是强制 Host enum。

### 6. 保持 authority boundary

一个 material objection 可以促使重新决策，但不会因此自动获得 execute/approve/veto/set-policy authority。若 authority 真正发生变化，必须有独立来源和 basis。

### 7. 当继续 intake 已不可能改变决策时结束

不要把 standing 变成无限治理。只要新的 bounded review 已不可能改变决策，并且 residual 已显式，就结束流程，同时保留 occurrence/disposition。

## False-BLOCK controls

不要要求：

- ordinary low-consequence feedback 也走 committee review；
- 先判定 legal/personhood 才允许事实纠错；
- 每个 affected subject 都必须有 veto；
- 普通 evidence intake 已能解决时仍造 formal Standing record。

## 证据边界

这个流程既不证明 objection 为真，也不证明 source 的 legitimacy。它的目的只是防止 decision-relevant input 因为不在当前主执行路径上而消失。

```text
INPUT_CONSIDERED != INPUT_TRUE
INPUT_CONSIDERED != AUTHORITY_GRANTED
```

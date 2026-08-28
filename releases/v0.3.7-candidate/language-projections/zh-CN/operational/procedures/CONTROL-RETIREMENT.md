# Control Retirement Procedure（简体中文投影）

状态：`v0.3.7 candidate.2 / BOUNDED_OPERATIONAL_PROCEDURE / OPTIONAL`

## 何时使用

当 safeguard、gate、monitoring rule、approval、fallback、rate limit、feature/control flag 或其他 intervention 可能已经不需要保持当前形态。

不要仅仅因为它安静、很老、使用率低或最近没事故就退休。

```text
NO_INCIDENT != CONTROL_NOT_NEEDED
LOW_USAGE != NO_PROTECTIVE_VALUE
AGE != RETIREMENT_THRESHOLD
```

## Reference outcomes

`KEEP_ACTIVE / NARROW_SCOPE / SHADOW_OBSERVE / DORMANT_ARCHIVE / RETIRE_REMOVE / REACTIVATE / UNKNOWN_WAIT`

这些是流程结果，不是强制 Host enum。

## 流程

### 1. 找回原始 failure / purpose

识别当初是什么 decision-changing failure、risk、uncertainty、dependency 或 temporary migration state 让这个 control 出现。

如果原始 purpose 已无法重建，不要静默删除；用 `UNKNOWN_WAIT` 或 bounded investigation。

### 2. 原 failure 现在还存在吗？

可能是：仍存在；结构性消失；范围/严重性已缩小；被其他机制替代；未知。

证据可以来自 architecture change、dependency removal、真实 field outcome、audit、新 provider guarantee 或其他 concrete mechanism。

单纯“没事故”是含糊证据，因为 control 本身可能正是事故没发生的原因。

### 3. 明确 replacement / coverage

若另一个机制接管了同一 protective property，显式验证 overlap。

例如 provider idempotency 替代某一路径 local duplicate-write guard；native RBAC 替代 provisional wrapper；新 cue/router 让 manual reread gate 不再需要。

不要因为主路径被覆盖，就假设所有 effect-equivalent path 都被覆盖。

### 4. 检查 secondary dependency / blast radius

退休前确认是否仍有人依赖它提供：safety/consequence ownership、observability、recovery、evidence/provenance、authority boundary、migration compatibility、fallback behavior。

control 可能在服役过程中获得了新的 secondary role。

### 5. 不确定时优先可逆收缩

可以选择：`NARROW_SCOPE`、`SHADOW_OBSERVE`、`DORMANT_ARCHIVE`、staged exposure/limited cohort。

这不是仪式化 de-escalation。证据足够时可以直接 remove；consequence 仍需要它时就继续 active。

### 6. 移除前先定义 reactivation evidence

例如：原 failure 再现、dependency rollback、provider guarantee 被撤回、新 effect-equivalent path 出现、Host/model/language change 让旧 applicability 失效。

### 7. 退休要保留 lineage，不能失忆

至少保留：原问题；为什么现在不再需要/缩小范围；replacement；使用的 evidence；旧机制在哪里可找回；reactivation condition。

```text
REMOVE_FROM_ACTIVE_ARCHITECTURE != ERASE_FROM_LINEAGE
```

### 8. 当下一次检查不再可能改变 retirement decision 时停止

不要为了“看起来严谨”永久收集 evidence。

## False-BLOCK controls

不要强制：universal age threshold、incident-count threshold、single scalar control-value score、明明可直接安全移除却必须经历 shadow period、所有 obsolete control 永久留在 active runtime。

## 证据边界

这个流程结构化 retirement reasoning，但不证明 counterfactual safety，也不保证 failure 永不复发。

`RETIRE_REMOVE` 只是当前 evidence/environment 下的 scoped decision，不是“这个 mechanism 从来就没必要”的 universal proof。

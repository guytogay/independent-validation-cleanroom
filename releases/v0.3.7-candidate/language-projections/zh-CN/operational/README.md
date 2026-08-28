# Operational Architecture — v0.3.7 candidate.2（简体中文投影）

状态：`WORKING_CANDIDATE / OPERATIONAL_HOW_PROJECTION / NOT_CURRENT / NOT_FROZEN`

本目录是候选版本面向实际运行的 HOW 层中文语义投影。它不是对 Constitution 的重复翻译，也不是新的规范权威；英文候选语义树和机器文件仍是 canonical source。

它的目标很简单：让采用者在不阅读 `research/` 的情况下，从一个真实问题走到可执行的机制分支。

## 建议路径

```text
普通问题 / 故障 / 决策
-> 先看后果类型
-> CUE-INDEX
-> HOW-MAP
-> REFERENCE-INDEX
-> 有界流程 / 可选 reference / Host 原生模式
-> 具体行动、WAIT、UNKNOWN、REFUSE 或 NOT_APPLICABLE
```

## 核心结构

压缩边界放在 HOW 之前：

```text
WHAT / WHY
-> 可以收敛、抽象、去重

HOW
-> 可以分叉、专门化、并存、Host-specific
```

`HOW_VARIATION != SEMANTIC_DUPLICATION`

同一个属性可以有多个合理机制。例如外部副作用控制，在不同 Host 中可以采用 provider idempotency、fencing、conditional write、status query、compensation 或 WAIT。

## Hot / Cold 边界

完整 HOW 库是 cold capability，不应被强制永久塞入 Agent 的热上下文。

```text
HOT_KERNEL
-> 识别当前问题
-> 找到需要的 operational branch
-> 按 applicability / Host 条件过滤
-> 行动

HOT_KERNEL != HOW_LIBRARY
```

## Reference 边界

候选包中的 reference 是可复用实现和机器表面，不是 ENA 必须安装的器官清单。

```text
REFERENCE_EXISTS != UNIVERSAL_APPLICABILITY
PACKAGE_INCLUDED != DEFAULT_ACTIVE
HOST_NATIVE_IMPLEMENTATION != NONCOMPLIANT
```

机器可读的角色和 optionality 见 `../../../references/REFERENCE-MANIFEST.yaml`。中文使用指南见 `../REFERENCE-GUIDE.md`。

## 一个好的 HOW 应该做到什么

HOW 的价值在于改变 Agent 实际能做什么。视机制而定，它可以包含：

- 适用/触发条件；
- 有序动作或状态转换；
- tool / schema / template / resolver；
- Host 能力依赖；
- effect / authority 边界；
- 失败症状；
- fallback / WAIT / REFUSE / recovery；
- 证据成熟度；
- 明确的“不适用”路径。

这不是固定检查表。若一个 HOW 只是把原则换句话说，它仍然是 operational debt。

## 证据规则

证据必须落到具体分支，而不只停在父层原则：

```text
WHAT_WHY_SUPPORTED
!= HOW_A_SUPPORTED
!= HOW_B_SUPPORTED
!= HOW_A_SUPPORTED_ON_HOST_X
```

某个 Host 上成功，不会自动产生 universal fitness。

## 反消融规则

没有进入 candidate.2 的机制，不等于被证伪或退休。替代、休眠、研究中的 HOW 仍保留在项目 lineage 中；release packaging 不能因为“这次没装进包”就让它从 ENA 历史中消失。

> **压缩语义主干，让具体 HOW 自由分叉。**

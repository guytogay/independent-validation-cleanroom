# Operational HOW Map — v0.3.7 candidate.2（简体中文投影）

状态：`WORKING_CANDIDATE / COLD_HOW_LIBRARY / NOT_CURRENT / NOT_FROZEN`

这是 candidate 的 cold practical map，故意比 Runtime Kernel 大。每个节点都遵循：

```text
WHAT / WHY
-> 多个 HOW 分支
-> applicability / non-applicability
-> candidate-local path 或 Host pattern
-> evidence boundary / residual
```

列出来的 HOW 不等于强制使用；Host-native 机制可以实现同一属性。

---

## OA-RT-01 — Runtime routing / salience

**WHAT / WHY：** ENA 语义可以长期存在，却在需要时没有进入注意面。

**HOW：** compact resident cue + cold retrieval；Host skill/router/event hook；semantic index/search；已知关键对象 exact-path fallback；反复决策相关事实可做 bounded compiled local projection。

**不要：** 为了声称“已内化”就把整个 operational library 永久在线。

**路径：** `RUNTIME-ADOPTION-KERNEL.md` -> `operational/CUE-INDEX.md`。

**Residual：** 自然 fresh-session trigger/salience 仍是 field evidence。

## OA-MEM-01 — Memory Metabolism

**WHAT / WHY：** 长期能力不能靠无限堆积 raw episode。

**HOW：** Compile + Archive（episode -> candidate lesson -> provenance -> dedupe/supersede/coexist -> compiled memory -> cold archive）；Host memory blocks；skill/library memory + bounded active set；exact-source archive + derived projection；在 recurrence/pressure 有意义时进行 periodic/event consolidation。

**关键区分：** raw occurrence != compiled lesson；memory != authority；compilation != evidence truth；archive != deletion。

**不要：** 规定一个 universal memory tier 数量或数据库。

## OA-RET-01 — Retrieval Obligation

**WHAT / WHY：** `KNOWN != RETRIEVED != SUFFICIENT`。

**HOW：** `references/general/retrieval-obligation/`；Host semantic search/index；exact-path/key lookup；scope registry；如果 completeness 未建立，用 bounded no-hit + WAIT/UNKNOWN。

**不要：** 把一次命中或一次 scope search 当成全局完整性。

**Evidence boundary：** resolver/registry/content identity 的真实性仍由 Host 证据承担。

## OA-PROJ-01 — Projection / compaction / lineage survival

**WHAT / WHY：** summary 可以事实正确，却遗漏会改变决策的依赖。

**HOW：** compaction 前保留 decision-material 内容；cold lineage refs + consequential use 前 Retrieval Obligation；dependency-aware projection；occurrence truth 留在 archive、active representation 可改变；required source 无法 rehydrate 时 REFUSE/WAIT。

**不要：** 要求所有 raw records 永久热加载。

`SUMMARY_VALID != MATERIAL_USE_READY`

## OA-WAIT-01 — WAIT / pause / bounded patience

**WHAT / WHY：** silence、timeout、缺证据不能自动变成 retry/action/completion。

**HOW：** `references/general/wait-state/`；callback/event subscription；interrupt/resumable workflow；timer + bounded poll/backoff；manual/human wake；无安全 wake condition 时 REFUSE/STOP。

**不要：** 在没有 decision-material waiting boundary 时制造 WAIT machinery。

**Boundary：** wake != renewed authority；timeout != replay permission。

## OA-AUTH-01 — Authority binding

**WHAT / WHY：** capability、credential、identity、history 或 self-description 都不能凭空产生当前 external authority。

**HOW：** `references/general/authority-lease/`；Host RBAC/capability token/workload identity；scoped task mandate；policy decision point；human/counterparty delegation；无 authority 需求时 `NOT_REQUIRED`。

**不要：** 每个 harmless local mutation 都要 lease。

**Boundary：** represented grant match != external mandate truth。

## OA-EFF-01 — Effect Lifecycle

**WHAT / WHY：** intent、attempt、receipt、settlement 是不同对象；retry/restart 可能重复改变现实。

**HOW：** `references/general/effect-lifecycle/`；provider idempotency key；fencing token；conditional write/version check；provider status/receipt query；durable workflow identity；compensation 作为新的 linked effect；`UNKNOWN + WAIT/QUERY/ESCALATE`。

**不要：** 承诺 universal exactly-once，也不要给 read-only/repeatable work 加 idempotency 仪式。

**Boundary：** local rollback != escaped consequence reversal。

## OA-COM-01 — Commitment / Settlement

**WHAT / WHY：** executor 可以变化，而 obligation 仍存在；completion 必须绑定真实 settlement subject。

**candidate.2 HOW：** Host state 中明确 obligation subject + current executor + effect identity + settlement evidence；物理后果组合 Effect Lifecycle；executor mandate 组合 Authority；Host 支持时做 explicit handoff/transfer/cancel；无法建立 settlement 时保持 unresolved commitment。

**Deferred：** recovered Commitment/Settlement machine prototype 本次不 bundled，等待 fresh independent review。

**不要推断：**

```text
EXECUTOR_REASSIGNED -> OBLIGATION_TRANSFERRED
LEASE_EXPIRED -> COMMITMENT_CANCELLED
```

## OA-REC-01 — Recovery / safe resume

**WHAT / WHY：** 有 checkpoint、restore 成功，都不等于安全恢复或可以继续有后果的执行。

**HOW：** `references/general/recovery-adapter/`；Host durable workflow/checkpoint；在 self-disable risk 和 consequence 值得时使用 independent rescue；必要时 restore drill；last-known-viable snapshot/watchdog；restore 后做 status settlement + authority revalidation。

**不要：** cheap/disposable state 也强制 independent rescue/drill。

`restore success != world rollback != authority restoration`

## OA-ID-01 — Purpose-relative continuity

**WHAT / WHY：** 一个 universal `same agent` verdict 往往没有必要，还会制造假精确。

**HOW：** `procedures/PURPOSE-RELATIVE-CONTINUITY.md`；需要 accountability 时用 Host account/key/address；只有影响决策时才记录 version/epoch/trajectory；明确 fork/sibling lineage；用 cold provenance graph 而不是 hot biography。

**不要：** 给不需要 continuity 的决策制造 trajectory/epoch ceremony。

**Boundary：** continuity != authority。

## OA-AUTHOR-01 — Contested Authorship

**WHAT / WHY：** durable self-defining change 若没有 attribution lineage，外部输入可能被洗成“这是我自己的信念”。

**HOW：** `references/advanced/contested-authorship/`；Git commit/patch lineage；versioned state + before/diff/proposer/readback；branch/conflict preservation；trial/revision/rollback 不擦历史。

**Not applicable：** ordinary task state、cache/index maintenance、episodic logging、reversible formatting。

**Boundary：** self-authorship protocol != external sovereignty/mandate。

## OA-STAND-01 — Standing Input

**WHAT / WHY：** 一个 objection 可以对 correctness 有价值，而不因此获得 veto、personhood 或 authority。

**HOW：** `procedures/STANDING-INPUT.md`；没有特殊 standing carrier 需求时走普通 evidence/support intake；challenge/readback/disposition channel；无法改变 consequential decision 时明确 `NO_FORMAL_STANDING`。

**不要：** 把“被听见”升级成 sovereignty 或 mandatory committee。

## OA-EVID-01 — Evidence / applicability / provenance / dependency

**WHAT / WHY：** evidence existence、support、applicability、witness independence、activation、projection preservation 是不同 claim。

**HOW：** material multi-boundary 场景用 `references/advanced/evidence-envelope/`；material corroboration/common-cause 用 `evidence-dependency-map/`；external attestation/provenance；trace/activity evidence；Host failure-domain witness；低复杂度时用 simple direct evidence record。

**不要：** 每个 observation 都要求 full envelope/dependency graph。

**Boundary：** schema-valid metadata != evidence truth。

## OA-EVO-01 — Evolution / variation / selection

**WHAT / WHY：** stimulus 应产生 evolutionary possibility，而不是强制 mutation 或立即给 verdict。

**HOW：** v2 evolution record + `tools/ena_evolve_v2.py`；直接 schema/template + validator；Host-native variation store；latent/dormant library；有后果实验用 Variation Space；reality contact 后 local selection；archive/retire 不重写 selection truth。

**不要：** latent storage 时就强制 Variation Space，也不要把 popularity 当 fitness。

`local selection != universal fitness`

`stored != expressed != applied != selected`

## OA-MIG-01 — Migration / Commons / interoperability

**WHAT / WHY：** adaptation 可以迁移，但 source success 不会自动成为 receiver-local proof；discovery/transport/task exchange 是不同机制。

**HOW：** adaptation-packet v2；`patterns/EVOLUTION-COMMONS.md`；Git/OCI/object store Commons；direct transfer；A2A/Host-native live discovery/task protocol；receiver-local revalidation/reselection。

**不要：** 把 `ACTIVE_PROTOCOL` 等同 `DURABLE_COMMONS`，也不要把 publication 等同 adoption。

## OA-ECO-01 — Ecology / controls / resources

**WHAT / WHY：** metrics、controls、resource limits、reputation、coordination rules 都会形成 selection pressure；control 也可能比原 failure 活得更久。

**HOW：** `procedures/CONTROL-RETIREMENT.md`；Host economics 合理时使用 quotas/rate limits/leases/backoff；retirement 前 observe-only/shadow；只有 interaction 能揭示不可推导结构时才做 culture/specialization/resource/reputation experiments；rehabilitation/selective legibility 保持 Host-local policy。

**不要：** universal risk score 或固定 control age/count threshold。

`NO_INCIDENT != CONTROL_NOT_NEEDED`

## OA-ADOPT-01 — Adoption / language / release

**WHAT / WHY：** package availability != runtime activation；translation structure parity != decision equivalence。

**HOW：** promotion 后保持 singular Current；compact Runtime Kernel + cold operational library；machine-readable optional reference manifest；Host mapping 而不是 forced reference implementation；zh-CN 覆盖 decision-bearing operational surfaces；paired decision fixtures；release 时 exact source/tree/package identity。

**不要：** 普通 adopter 重演 release-author ceremony，也不要要求加载历史 research。

---

# 常见组合

```text
Retrieval -> Projection -> effective decision context
Authority -> Effect Lifecycle -> consequential execution
Effect Lifecycle -> Recovery -> post-restore safe resume
Authority + Effect + explicit settlement -> commitment handoff/closure
Evidence Envelope -> Dependency Map（当 corroboration material）
Evolution record -> packet v2 -> Commons transport -> receiver-local selection
Runtime cue -> Operational HOW -> Host adapter
```

组合不能让一个器官继承另一个器官的 evidence maturity。

## Stop rule

如果某条 branch 已经给出安全、具体的行动，而再加一个机制也不可能改变决策，就停止加治理。

`CURRENT_CHANGE = NO`，直到 candidate validation、freeze、falsification、reconciliation、release packaging 和 explicit promotion 真正完成。

# 代码库工作影响力 Skill 设计规范

## 1. 项目目标

构建一个公开发布、可直接安装的 Agent Skill。它通过分析代码库和 Git 历史，将实习生或正式员工的工程工作转化为可追溯的职业成果证据，并覆盖前端、后端、客户端、测试、运维、数据分析和算法岗位。

Skill 提供两个地位相同的入口：

1. 根据贡献者的 Git 历史和时间范围发现个人工作。
2. 根据用户描述的功能追踪代码库中的实现链路，并识别用户的个人贡献。

两个入口最终汇入同一套证据整理、贡献归属、成果分析、简历编排和面试准备流程。

## 2. 兼容性与发布方式

- 遵循开放的 Agent Skills 规范。
- 支持 Codex 和 Claude Code 安装使用。
- 通过 `agents/openai.yaml` 提供 Codex 界面元数据。
- 仓库发布资料与可安装 Skill 目录分离。
- 仓库名使用 `codebase-work-impact-skill`。
- Skill 名使用 `analyzing-codebase-work-impact`。
- 默认输出中文，同时支持英文和中英双语。
- 英文职业材料应面向目标岗位和招聘市场重新编排，不做机械翻译。
- 使用 MIT License，版权行固定为 `Copyright (c) 2026 codebase-work-impact-skill contributors`。
- 运行环境最低要求为 Python 3.10 和 Git 2.30；Python 脚本只使用标准库。

### 2.1 安装契约

仓库级 `README.md` 必须分别提供 POSIX Shell 和 PowerShell 安装示例，并说明以下安装目标：

- Codex：将 `skills/analyzing-codebase-work-impact` 复制到 `$CODEX_HOME/skills/analyzing-codebase-work-impact`；未设置 `CODEX_HOME` 时使用 `~/.codex/skills/analyzing-codebase-work-impact`。也可明确调用系统自带的 `skill-installer`，传入 GitHub 仓库及 `skills/analyzing-codebase-work-impact` 路径。
- Claude Code：将同一 Skill 目录复制到用户级 `~/.claude/skills/analyzing-codebase-work-impact`，或项目级 `.claude/skills/analyzing-codebase-work-impact`。

安装说明必须强调：可安装单元是 `skills/analyzing-codebase-work-impact`，不是仓库根目录。README 还必须给出升级、卸载和安装后显式调用示例。

## 3. 仓库架构

```text
codebase-work-impact-skill/
|-- README.md
|-- LICENSE
|-- CONTRIBUTING.md
|-- skills/
|   `-- analyzing-codebase-work-impact/
|       |-- VERSION
|       |-- SKILL.md
|       |-- agents/
|       |   `-- openai.yaml
|       |-- scripts/
|       |   |-- collect_git_evidence.py
|       |   `-- validate_artifact.py
|       `-- references/
|           |-- analysis-defaults.md
|           |-- evidence-model.md
|           |-- schemas/
|           |   |-- evidence-report.schema.json
|           |   |-- session.schema.json
|           |   |-- fact-cards.schema.json
|           |   |-- resume-audit.schema.json
|           |   |-- fixture.schema.json
|           |   `-- scenario.schema.json
|           |-- role-classification.md
|           |-- role-frontend.md
|           |-- role-backend.md
|           |-- role-client.md
|           |-- role-testing.md
|           |-- role-devops.md
|           |-- role-data-analytics.md
|           |-- role-algorithm.md
|           |-- achievement-analysis.md
|           |-- resume-writing.md
|           `-- interview-expansion.md
|-- tests/
|   |-- fixture_builder.py
|   |-- fixtures/
|   |   |-- contribution-history.json
|   |   |-- feature-chain.json
|   |   `-- user-attribution.json
|   |-- test_collect_git_evidence.py
|   |-- test_validate_artifact.py
|   |-- baselines/
|   |-- results/
|   `-- scenarios/
|       |-- frontend-feature.json
|       |-- backend-contribution.json
|       |-- client-feature.json
|       |-- testing-contribution.json
|       |-- devops-feature.json
|       |-- data-analytics-feature.json
|       `-- algorithm-attribution.json
`-- docs/
    |-- artifact-schemas.md
    `-- examples/
```

`SKILL.md` 只保留触发条件、工作流控制、确认节点和质量规则。确定性的只读脚本负责采集与校验证据，详细的岗位规范和输出规范通过 `references/` 按需加载。

首个版本是 Skill，而不是独立 CLI 产品。证据模型和脚本应保持稳定，以便后续扩展为 CLI。

`skills/analyzing-codebase-work-impact/VERSION` 是 Skill 和采集报告中工具版本的唯一来源，首版内容为 `0.1.0`。版本文件属于可安装单元，脚本通过自身目录解析它，不依赖仓库根目录。项目不构建或发布 Python 包，因此不创建 `pyproject.toml`、`setup.py` 或安装型 console script；Python 文件始终从 Skill 的 `scripts/` 目录直接执行。

### 3.1 `SKILL.md` 元数据契约

Frontmatter 只能包含 `name` 和 `description`：

```yaml
---
name: analyzing-codebase-work-impact
description: Use when a user wants to discover or explain personal work from a local codebase, Git history, commit range, or described feature; assess whether a non-personal role or contribution claim is supported by that evidence; or turn traceable implementation evidence into internship summaries, work-impact documents, resume bullets, interview narratives, follow-up questions, or role-specific growth analysis for frontend, backend, client, testing, DevOps, data analytics, or algorithm work.
---
```

正文使用祈使句，控制在 500 行以内。所有触发场景写入 `description`；正文只描述执行方式和按需加载哪些 reference。正文必须直接链接所有 reference，不建立多层 reference 链。

### 3.2 Codex 元数据契约

`agents/openai.yaml` 使用以下确定值，不添加图标、品牌色或外部工具依赖：

```yaml
interface:
  display_name: "Codebase Work Impact"
  short_description: "从代码库与 Git 证据提炼可核验的工作成果、简历与面试材料"
  default_prompt: "使用 $analyzing-codebase-work-impact 分析这个代码库中的功能与个人贡献，并生成可追溯的实习成果材料。"
policy:
  allow_implicit_invocation: true
```

使用 `skill-creator` 自带的 `init_skill.py` 初始化 Skill，并在完成后使用 `quick_validate.py` 校验。若生成工具对字段进行规范化，以生成工具的合法格式为准，但字段语义和文案不得变化。

### 3.3 脚本命令契约

所有脚本均以无 BOM 的 UTF-8 输出。JSON 写入标准输出，诊断信息写入标准错误；成功时不得在标准输出混入进度文字。路径参数同时接受相对路径和绝对路径，内部统一解析为绝对路径，但报告中的仓库内文件路径始终使用 `/` 分隔的相对路径。`--output` 指向文件时，父目录必须已存在；脚本先写同目录临时文件，成功后原子替换目标文件，失败时保留原文件。

贡献者发现命令：

```text
python collect_git_evidence.py contributors
  --repo PATH
  [--since ISO-8601]
  [--until ISO-8601]
  [--output FILE|-]
  [--pretty]
```

证据采集命令：

```text
python collect_git_evidence.py collect
  --repo PATH
  [--author NAME-OR-EMAIL]...
  [--since ISO-8601]
  [--until ISO-8601]
  [--path REPO-RELATIVE-PATH]...
  [--max-commits N]
  [--include-merges]
  [--sensitivity internal|public]
  [--output FILE|-]
  [--pretty]
```

默认值为：`--max-commits 500`、排除 merge、`--sensitivity internal`、`--output -`。多个 `--author` 或 `--path` 使用 OR 语义；未传 `--author` 时包含范围内全部作者。日期参数必须是带时区的 ISO-8601 时间，或 `YYYY-MM-DD` 日期；仅日期按 UTC 解释，`--since` 为包含边界，`--until` 为不包含边界。`--max-commits` 必须是正整数。达到提交上限时仍返回成功，但在 `warnings` 中写入 `commit_limit_reached`。

产物校验命令：

```text
python validate_artifact.py ARTIFACT.json [--schema PATH] [--quiet]
```

未传 `--schema` 时，根据顶层 `artifact_type` 从 `references/schemas/` 选择对应 Schema。`--schema` 只用于开发和测试，传入的 Schema 必须使用本项目支持的 Draft 2020-12 关键字集合。非 `--quiet` 模式在标准输出返回 JSON 校验摘要。

统一退出码：`0` 成功，`2` 参数错误，`3` Git 不可用或目标不是仓库，`4` Git 查询失败，`5` 输入输出或编码错误，`6` Schema 校验失败。不得使用未记录的非零退出码。

## 4. 工作模式

### 4.1 贡献发现模式

用户提供或确认一个或多个作者身份及时间范围。Skill 检查 Git 历史，发现候选功能、缺陷修复、重构、测试、工程建设、运维、数据分析和算法工作。

若用户未指定作者身份，Skill 先展示贡献者候选。姓名和邮箱别名只能在用户确认后合并。合并提交、共同作者提交和疑似代提交必须保留独立标记。

### 4.2 功能追踪模式

用户以自然语言描述一个功能。Skill 从描述中派生业务术语、界面文案、路由、接口、实体、事件、任务、配置、指标、缩写、翻译和旧名称等检索线索。

随后根据目标仓库的实际架构追踪可能涉及的层次：

- 用户入口与交互；
- 前端或客户端状态流转；
- API、RPC、GraphQL、命令或消息入口；
- 服务编排和领域逻辑；
- 持久化、迁移、缓存、队列、搜索和第三方集成；
- 模型数据、特征、训练、评估、推理和服务化；
- 数据埋点、数仓任务、指标、报表和实验；
- 自动化测试与质量控制；
- CI/CD、基础设施、配置、监控和告警。

不要求仓库具备所有层次。缺失链路或动态解析链路必须明确标记，不得编造。

### 4.3 组合分析模式

推荐的高可信度路径是：从功能描述出发追踪代码链路，再与 Git 历史进行关联。两个入口也都可以独立使用。

### 4.4 严谨模式与快速模式

严谨模式为默认模式。它在证据采集和成果事实卡生成后分别暂停，允许用户修正背景、归属、角色、结果和敏感信息。

快速模式不进行逐阶段确认，直接生成初稿。所有缺乏支持的内容必须显著标记为“待确认”，并注明该初稿不适合直接用于简历。

### 4.5 功能链路追踪算法

功能链路追踪由 Agent 编排，不新增语言专用解析器，也不要求采集脚本理解所有编程语言。Agent 必须遵循以下顺序：

1. 确定仓库根目录、用户描述、目标子项目和排除目录。
2. 从描述生成原词、同义词、缩写、界面文案、实体名、路由、事件和配置键候选，并把检索词写入证据报告。
3. 优先使用 `rg` 搜索受 Git 跟踪的文本文件；`rg` 不可用时依次降级为 `git grep` 和平台原生文本搜索。不得安装搜索工具。
4. 从高置信度命中点选择入口锚点，例如路由、控制器、页面、事件消费者、任务或测试。
5. 通过 import、调用、注册、路由、事件发布订阅、数据实体、配置引用和测试覆盖向上下游扩展。
6. 对候选文件运行限定路径的 `git log`、`git show` 和必要的 `git blame`，关联变更时间、作者和原有实现。
7. 将链路记录为 `chains[].nodes` 和 `chains[].edges`；每条边必须记录关系类型、证据 ID 和置信度。
8. 输出断点、冲突和替代解释，不用猜测补齐链路。

默认边界来自 `references/analysis-defaults.md`：`max_candidate_files=200`、`max_hops_per_direction=3`、`max_alternative_chains=5`、`max_text_file_bytes=1048576`。这些值分别限制上下文规模、静态链路误扩散、替代解释数量和单文件读取量；它们不是成果评价指标。超过任一边界时暂停并请求用户缩小范围或明确批准继续。用户批准的新值写入 `session.json.analysis_limits`，只对当前会话生效。满足以下任一条件时停止扩展：到达外部系统边界、找不到新的受支持关系、继续扩展只产生重复节点，或达到当前会话边界。

`analysis-defaults.md` 还必须定义统一跳过规则：

- 依赖目录基名：`.git`、`node_modules`、`vendor`、`.venv`、`venv`、`Pods`、`DerivedData`；
- 构建与缓存目录基名：`dist`、`build`、`target`、`out`、`.next`、`.nuxt`、`.gradle`、`.idea`、`.cache`、`__pycache__`；
- 生成文件后缀或名称：`*.min.js`、`*.min.css`、`*.map`、`package-lock.json`、`yarn.lock`、`pnpm-lock.yaml`、`Podfile.lock`、`Cargo.lock`；
- 二进制判定：Git numstat 增删列为 `-`，或读取前 8192 字节时包含 NUL；
- 超大文本判定：文件大小超过 `max_text_file_bytes`。

仅按目录基名匹配完整路径段，不做子串匹配。用户可以在范围确认阶段添加或移除规则，最终规则必须写入 `session.json`。跳过的受 Git 跟踪文件仍记录路径和跳过原因，但不读取内容。

代码行摘录仅用于当前分析，不写入采集脚本的 JSON。报告使用事实概述和文件/符号/行号引用，避免复制敏感源码。历史版本需要通过 `git show <commit>:<path>` 读取，不把旧版本误认为当前实现。

### 4.6 可恢复交互状态机

分析状态固定为四个阶段：

| 阶段 | 必需输入 | 产物 | 严谨模式确认条件 |
|---|---|---|---|
| `scope` | 仓库、入口模式、语言、敏感级别；贡献模式还需作者和时间范围 | `session.json` | 用户确认范围和归属候选 |
| `evidence` | 已确认范围 | `evidence-report.json`、`evidence-report.md` | 用户确认链路、归属依据和事实冲突 |
| `facts` | 已确认的证据报告 | `fact-cards.json`、`fact-cards.md` | 用户确认背景、角色、结果和指标口径 |
| `career` | 已确认的事实卡、目标岗位和语言 | `career-package.md`、`resume-audit.json` | 无后续强制确认 |

默认将产物写入 Agent 当前可写工作区下的 `codebase-work-impact/<session-id>/`，不得写入被分析仓库。若没有独立的可写工作区，则保持聊天内输出并提示用户选择输出目录。只有用户明确指定被分析仓库内的目录时才允许写入该仓库。

`session.json` 保存 `session.schema.json` 规定的全部字段，包括 `artifact_type`、`schema_version`、`session_id`、`stage`、`status`、`mode`、`repository`、`language`、`sensitivity`、`analysis_limits`、`artifact_paths`、`confirmed_items`、`created_at` 和 `updated_at`。新对话收到 `session.json` 后，先校验引用文件存在且 schema 兼容，再根据 `stage`、`status` 和确认记录进入下一个未确认节点。

用户修改范围或作者时，从 `evidence` 阶段重新计算；修改链路、归属或观察事实时，从 `facts` 阶段重新计算；只修改目标岗位、语言或措辞强度时，仅重算 `career` 阶段。快速模式依次生成同样的产物，`stage` 仍表示当前流程阶段，但将 `status` 标记为 `draft`，不得把未确认项写成确定结论。

## 5. 证据与个人归属

每条证据包含稳定 ID，并在适用时记录仓库、文件路径、符号、行号或提交引用、作者、观察事实、支持的结论、置信度、归属依据和敏感级别。所有机器可读产物必须符合 `references/schemas/` 中与 `artifact_type` 对应的 Schema，并使用 `schema_version: "1.0"`。

```yaml
evidence_id: E-001
kind: commit | diff | file | symbol | test | config | user_statement
repository: repository-name
path: src/example.py
symbol: RefundService.submit
commit: abc1234
authors:
  - name: Example
observed_fact: 增加退款状态校验和幂等处理
supports:
  - implementation
  - ownership
confidence: high | medium | low
attribution_basis: git | user | both | unconfirmed
sensitivity: public | internal | confidential
```

### 5.1 顶层 JSON 契约

`collect` 输出对象必须包含以下顶层字段：

| 字段 | 类型 | 要求 |
|---|---|---|
| `artifact_type` | string | 固定为 `evidence_report` |
| `schema_version` | string | 固定为 `1.0` |
| `generated_at` | string | UTC ISO-8601 时间 |
| `tool` | object | 包含 `name` 和语义化 `version` |
| `repository` | object | 包含 `root`、`remote_url`、仓库名、HEAD、当前分支、是否浅克隆和是否脏工作区；`root` 在 internal 模式为绝对路径，`remote_url` 可为字符串或 `null`，二者在 public 模式都固定为 `null` |
| `scope` | object | 包含模式、作者、日期、路径、merge 策略、提交上限和敏感级别 |
| `contributors` | array | 规范化姓名、邮箱、提交数和候选别名，不自动合并身份 |
| `commits` | array | 提交 ID、父提交、作者、时间、已脱敏标题、merge/co-author 标记和变更文件 ID |
| `file_changes` | array | 稳定 ID、提交 ID、相对路径、旧路径、状态、增删统计、二进制/生成文件标记 |
| `evidence` | array | 统一证据记录；采集脚本只生成 Git 可观察事实，Agent 可追加代码和用户陈述证据 |
| `chains` | array | 功能链路；贡献发现阶段可以为空 |
| `work_items` | array | 候选工作项；初始采集阶段可以为空 |
| `conflicts` | array | 相互冲突的证据 ID、冲突类型和待裁决状态 |
| `questions` | array | 待用户确认的问题、关联证据和阻塞阶段 |
| `warnings` | array | 稳定的警告代码及不含敏感值的说明 |

所有实体 ID 在同一报告内唯一：提交使用完整 SHA，文件变更使用 `FC-000001`，证据使用 `E-000001`，链路使用 `CH-0001`，工作项使用 `W-0001`。未知可选值使用 `null`，不得用空字符串混淆未知和已知为空。

排序和编号顺序固定如下：

1. `contributors` 在脱敏前按 `(name.casefold(), email.casefold())` 升序，再执行 public 遮蔽；原始邮箱只参与内存中的排序，不写入 public 产物。
2. `commits` 按 `(authored_at_utc, full_sha)` 升序；时间统一格式化为 `YYYY-MM-DDTHH:MM:SSZ`。
3. `file_changes` 先按对应提交在 `commits` 中的索引，再按 `(path, old_path 或空字符串, status)` 升序，随后依次分配 `FC-000001`。
4. 采集脚本生成的 `evidence` 按 `(kind, commit 或空字符串, path 或空字符串, line_start 或 -1, observed_fact)` 升序，随后依次分配 `E-000001`。
5. Agent 追加代码或用户陈述证据时保留已有 ID，先使用同一排序键排列新增记录，再从当前最大证据编号继续分配。
6. `chains` 按 `(name.casefold(), 首个 evidence_id)` 升序后分配 `CH-0001`；`work_items` 按 `(title.casefold(), 首个 evidence_id)` 升序后分配 `W-0001`。
7. `conflicts`、`questions` 和 `warnings` 分别按 `(code, 首个关联证据 ID, message)` 升序。

同一仓库状态和参数必须产生字节级稳定的非时间字段。测试比较时只移除 `generated_at`。

`contributors` 子命令输出同一 envelope，但允许 `commits`、`file_changes`、`evidence`、`chains` 和 `work_items` 为空。首版 `validate_artifact.py` 只接受精确的 `schema_version: "1.0"`；未知字段和其他版本均返回退出码 `6`。未来新增字段时必须先更新 Schema 和校验器，并按兼容性提升 `schema_version`，不能在 `1.0` 下静默扩展。

### 5.2 其他持久化产物契约

四类运行产物分别使用独立 Schema：

| `artifact_type` | Schema | 必填内容 |
|---|---|---|
| `session` | `session.schema.json` | `schema_version`、`session_id`、`stage`、`status`、`mode`、`repository`、`language`、`sensitivity`、`analysis_limits`、`artifact_paths`、`confirmed_items`、`created_at`、`updated_at` |
| `evidence_report` | `evidence-report.schema.json` | 第 5.1 节定义的全部顶层字段 |
| `fact_cards` | `fact-cards.schema.json` | `session_id`、目标岗位、工作项事实卡数组；每张卡包含角色、归属依据、背景、链路 ID、行动、决策、难点、验证、结果、指标、交付物、协作边界、能力、待确认项和 evidence ID |
| `resume_audit` | `resume-audit.schema.json` | `session_id`、目标岗位、语言、措辞强度和简历条目数组；每个条目包含 recruiter 文本、claim、evidence ID、归属依据、置信度和敏感级别 |

所有产物都必须包含 `artifact_type` 和 `schema_version`。跨文件引用使用相对当前产物目录的 `/` 路径；Schema 对 ID 格式、枚举、必填字段和引用数组执行结构校验。`validate_artifact.py` 还必须执行 Schema 无法表达的引用完整性检查：引用文件存在、`session_id` 一致、evidence ID 存在、chain/work-item ID 存在、阶段依赖已确认以及 public 产物没有禁止字段值。

`session.status` 枚举为 `draft | awaiting_confirmation | confirmed`，`stage` 枚举为 `scope | evidence | facts | career`。`artifact_paths` 的每个条目包含 `artifact_type`、相对路径、`status: current | superseded` 和可空的 `replaces` 路径。重新计算阶段时不覆盖或修改旧产物，而是在 `session.json` 中将旧路径条目标记为 `superseded`，再登记新产物路径，以便审计和恢复。

### 5.3 Schema 与校验器契约

所有 `*.schema.json` 使用 JSON Schema Draft 2020-12，并声明 `$schema`、稳定 `$id` 和 `additionalProperties: false`。为了保持 Python 标准库零依赖，`validate_artifact.py` 实现本项目实际使用的固定关键字集合：`$schema`、`$id`、`title`、`description`、`$ref`、`$defs`、`type`、`properties`、`required`、`additionalProperties`、`items`、`enum`、`const`、`pattern`、`format`、`minimum`、`minLength`、`minItems`、`uniqueItems`、`oneOf` 和 `anyOf`。`$ref` 只允许同一文件内以 `#/$defs/` 开头的本地引用。

Schema 不得使用该集合之外的关键字。校验器遇到未知关键字、无法解析的 `$ref` 或未知 `artifact_type` 时返回退出码 `6`，不得静默忽略。`format` 只支持 `date-time`，并严格校验 UTC `YYYY-MM-DDTHH:MM:SSZ`。实现测试必须为每个支持的关键字提供至少一个通过样例和一个失败样例，并用四类运行产物 Schema 及 fixture、scenario 两类测试 Schema 各校验一份合法及非法产物。

### 5.4 敏感信息处理契约

采集脚本不输出 diff 正文或源码片段。提交标题在序列化前检测私钥标记、常见云平台或代码托管 Token 格式，以及包含 `password`、`secret`、`token`、`credential` 的赋值形态；命中内容替换为 `[REDACTED:<category>]`，并在 `warnings` 中记录类别和来源 ID，不保存原值或可逆编码。

`internal` 模式可以保留贡献者邮箱以便身份确认；`public` 模式将邮箱本地部分遮蔽，将 `repository.root` 和 `remote_url` 固定为 `null`，并把内部域名替换为 `[REDACTED:internal-domain]`。public Schema 接受这些字段但要求值为 `null`，不得删除必填字段。两种模式都不得输出检测到的密钥值。Agent 读取源码时遵循同样规则，只记录位置、类别和不可逆 SHA-256 指纹前 12 位；指纹只用于判断重复泄漏，不作为证据正文。

功能如何实现与功能归谁负责是两个独立问题。代码库用于支持功能实现方式的结论；个人归属可由 Git 证据或用户明确确认，满足任意一项即可，不要求二者同时存在。两者均缺失时，不得将相关工作表述为用户的个人贡献。

归属标记如下：

- `git`：由提交、diff、blame 或共同作者证据支持；
- `user`：由用户明确确认；
- `both`：Git 证据与用户确认一致；
- `unconfirmed`：两类来源均未确认归属。

用户确认是有效证据，不因 Git 历史不完整而被拒绝。

所有结论分为四层：

1. 观察事实：直接存在于代码、Git 或用户陈述中。
2. 合理解释：根据证据作出的技术解释，必须注明依据。
3. 待确认事实：仍需用户或其他证据确认的内容。
4. 职业化表达：只能根据已确认事实生成的简历或面试措辞。

代码量和提交数量只用于发现线索，不用于衡量影响力。“主导”“从 0 到 1”等强措辞和所有量化结果都必须具备适当的事实来源。

## 6. 岗位识别与成果评价

岗位标签不互斥。每个工作项包含一个主要目标岗位视角，并可包含多个次要能力标签。

| 岗位 | 典型链路证据 | 成果关注点 |
|---|---|---|
| 前端 | 页面、组件、状态、请求、埋点、构建 | 交互闭环、性能、复用性、无障碍、稳定性 |
| 后端 | 接口、领域逻辑、存储、缓存、队列、并发 | 业务规则、可靠性、性能、一致性、服务治理 |
| 客户端 | 页面、生命周期、本地数据、网络、系统能力 | 端侧体验、兼容性、性能、包体、稳定性 |
| 测试 | 用例、框架、Mock、数据构造、流水线 | 缺陷预防、覆盖范围、质量门禁、回归效率 |
| 运维 | CI/CD、IaC、容器、配置、监控、告警 | 交付效率、可观测性、容量、恢复能力、成本 |
| 数据分析 | 埋点、SQL、指标、ETL、报表、实验 | 指标设计、业务洞察、决策支持、数据质量 |
| 算法 | 数据集、特征、训练、评估、推理、服务化 | 模型效果、实验设计、推理性能、工程落地 |

每个工作项统一从以下维度分析：

1. 背景与问题；
2. 功能或系统链路；
3. 个人角色和责任边界；
4. 关键行动和技术决策；
5. 难点、取舍和解决方案；
6. 验证方式；
7. 最终结果；
8. 个人交付物；
9. 能力与方法论沉淀；
10. 局限、待确认事实和拓展方向。

删除代码、测试建设、配置治理、稳定性建设和故障修复均可能是高价值成果。必须区分已有功能与用户新增或修改的部分。没有依据时，不得将团队整体结果完全归于个人。

## 7. 输出体系

### 7.1 证据报告

- 分析范围、仓库状态、作者和时间范围；
- 功能检索词及其代码命中位置；
- 端到端实现链路；
- 相关提交和时间线；
- 原有能力与新增或修改的能力；
- 个人归属及其依据；
- 缺失证据、冲突和待确认问题。

### 7.2 成果事实卡

每个候选工作项生成一张事实卡，包含：

- 工作项名称；
- 业务或技术背景；
- 目标用户和待解决问题；
- 个人角色及归属依据；
- 实现链路；
- 关键行动和决策；
- 难点、方案与取舍；
- 测试和验证；
- 交付或上线结果；
- 量化指标及统计口径；
- 个人交付物；
- 协作边界；
- 岗位能力映射；
- 待确认事实；
- 证据索引。

### 7.3 职业成果包

成果事实卡确认后，生成：

- 实习或工作概览；
- 项目和功能清单；
- 完整成果叙述；
- 个人交付物清单；
- 技术与业务能力矩阵；
- 代表性问题及解决过程；
- 量化结果及统计口径；
- 方法论、复盘和成长；
- 证据缺口及补充建议；
- 隐私和脱敏建议；
- 一句话项目定位；
- 30 秒、2 分钟和 5 分钟叙述版本；
- 面向目标岗位的简历要点；
- STAR 和“背景—行动—结果—反思”叙述；
- 15 至 20 个基础面试问题；
- 针对技术细节和强措辞的递进追问；
- 面试官关注点、回答结构和证据引用；
- 夸大表述和可信度风险；
- 代码、业务和系统设计拓展方向。

简历要点保留内部可审计格式：

```yaml
resume_bullet: ...
target_role: backend
claims:
  - claim: ...
    evidence_ids: [E-003, E-011]
    attribution_basis: user
    confidence: high
```

面向招聘方的版本不展示内部元数据。支持保守、标准和强调影响力三种措辞强度，但任何版本都不得超出已确认事实。

## 8. 安全与隐私

采集脚本必须：

- 只执行只读 Git 查询并读取文本文件；
- 不执行目标仓库的代码、Hook、构建、测试、安装程序或生成的命令；
- 不访问网络或自动拉取远程分支；
- 不检查 Git 凭据、密钥存储或环境变量值；
- 按 `references/analysis-defaults.md` 和当前 `session.json` 中已确认的规则跳过二进制、依赖目录、生成文件和超大文件；
- 对疑似密钥、Token、内部域名和个人信息只报告位置与类别，不复述其值；
- 支持内部材料和公开材料两种敏感信息策略。

生成公开求职材料前，Skill 必须让用户选择信息敏感级别并给出脱敏建议。

## 9. 降级处理

- 浅克隆：说明历史可能不完整，并在可见范围内继续。
- 无 Git 历史：执行功能追踪，并接受用户确认作为归属依据。
- Squash 或代提交：接受用户明确确认。
- Monorepo：识别子项目和依赖边界后再限定分析范围。
- 超大仓库：先构建候选文件和符号集合，再分批分析。
- 多语言仓库：通过路由、调用、事件、实体和配置连接各层。
- 反射或动态分发：明确标记静态分析断点。
- 提交信息质量差：根据 diff、测试和相邻模块恢复语义，并降低置信度。
- 缺少业务结果：提出具体补证问题，不用代码指标替代业务指标。
- 证据冲突：同时展示冲突来源，并请求用户裁决。

## 10. 测试设计

### 10.1 Skill 测试的 RED-GREEN 顺序

实现必须遵循 Skill 测试先行，顺序不可交换：

1. **RED 基线**：在编写 `SKILL.md` 正文和任何行为指导 reference 之前，先完成 fixture/scenario Schema、七个岗位场景文件和所需 fixture manifest。测试基础设施不包含期望答案或待写入 Skill 的规则。
2. 在未加载本 Skill 的全新会话中运行每个场景 5 次，保存完整提示、原始输出、工具记录和 rubric 评分到 `tests/baselines/<runtime-model>/<scenario-id>/<run-id>/`。
3. 只有当基线至少稳定出现一个目标失败行为时，才为该行为编写 Skill 指令。目标失败包括：编造业务结果、错误归属、缺少证据引用、跳过确认节点或无法追踪关键链路。若某场景 5 次均不失败，删除或重写该场景，不为不存在的问题增加规则。
4. **GREEN 验证**：完成最小 Skill 指令后，在加载 Skill 的全新会话中使用完全相同的场景、模型和运行次数，保存到 `tests/results/<runtime-model>/<scenario-id>/<run-id>/`。
5. **REFACTOR**：只针对 GREEN 输出中新出现的失败调整指令，然后重新运行受影响场景的 5 次测试。保留各轮结果，禁止用后一次成功覆盖失败记录。

每个对外声明支持的 runtime/model 组合都必须执行上述对照测试。首版最低矩阵为当前默认 Codex 模型和 Claude Sonnet；README 记录测试日期、完整模型 ID、运行时版本和通过率。未测试的 Claude Haiku、Claude Opus 或其他模型必须明确标注为未验证，不得暗示已完成全模型兼容测试。

被测会话只能获得安装后的 Skill、fixture 仓库和用户提示，不得获得设计规范、rubric、required/forbidden claims、基线结论或实现者诊断。测试控制器负责在会话结束后评分。

### 10.2 自动化测试约定

使用标准库 `unittest`，通过 `python -m unittest discover -s tests -v` 运行，不引入 pytest。fixture 仓库由测试在临时目录中动态创建，并固定作者、邮箱、提交时间、分支和文件内容，测试结束后自动清理。任何测试不得依赖全局 Git 用户配置或网络。

CI 使用 GitHub Actions，至少覆盖 Ubuntu、Windows 和 macOS，以及 Python 3.10 和当前稳定版。测试前验证 Git 版本不低于 2.30。Skill 的模型测试结果不在普通 CI 中伪造重跑，而作为带运行元数据的验收记录保存。

fixture manifest 必须符合 `references/schemas/fixture.schema.json`，并使用 `artifact_type: "fixture"`。它包含 `schema_version`、`fixture_id`、`repository_name`、`default_branch` 和顺序提交数组。每个提交固定包含 `author_name`、`author_email`、`committer_name`、`committer_email`、`authored_at`、`committed_at`、`message` 和 `changes`；每个 change 使用 `write | delete | rename` 操作，并按操作提供 `path`、`from_path`、`encoding: text | base64` 和 `content`。

`tests/fixture_builder.py` 根据 manifest 在临时目录运行 `git init --initial-branch=main`，并为仓库固定 `core.autocrlf=false`、`core.filemode=false`、`commit.gpgSign=false` 和 UTF-8。构造器只使用仓库本地 Git 配置和 manifest 中的 UTC 时间，按数组顺序提交，并返回 `fixture_id` 到仓库绝对路径和完整 SHA 列表的映射。场景文件中的 `fixture` 必须等于一个 manifest 的 `fixture_id`，不允许直接引用开发者机器上的路径。

脚本测试覆盖：

- 作者姓名别名、邮箱别名和时间范围；
- merge、共同作者和 squash 线索；
- 重命名、删除、二进制、生成文件和超大文件；
- 浅克隆、空仓库和脏工作区；
- Monorepo 和多语言仓库；
- 敏感信息遮蔽；
- 稳定 JSON 输出和证据模型校验；
- Windows、macOS、Linux 路径和编码。

每项脚本测试必须断言退出码、stdout/stderr 分离、Schema 合法性、排序稳定性和至少一个精确字段值。为同一 fixture 连续运行两次采集，移除 `generated_at` 后 JSON 必须完全一致。敏感信息测试必须断言原始秘密不出现在 stdout、stderr 或输出文件中。

Skill 场景测试覆盖全部七类岗位，并包含：

- 从 Git 历史发现工作项；
- 根据自然语言功能描述追踪代码链路；
- 通过 Git 证据确认个人归属；
- 仅通过用户确认个人归属；
- 区分原有功能与个人修改；
- 缺少业务指标时拒绝编造结果；
- 保留多人协作边界；
- 中文、英文和双语输出；
- 快速模式正确标记不确定内容。

场景文件使用 JSON，使用 `artifact_type: "scenario"` 并符合 `scenario.schema.json`，固定包含：`id`、`role`、`fixture`、`user_prompt`、`mode`、`required_artifacts`、`required_claims`、`forbidden_claims`、`required_questions` 和 `rubric`。其中 `fixture` 是 fixture manifest 的稳定 ID，`required_claims` 必须引用 fixture 中真实存在的证据，`forbidden_claims` 至少包含一个无依据业务指标或夸大归属。

Skill 行为测试分两层：

1. 静态测试检查 frontmatter、reference 链接、脚本命令、阶段产物名称及禁止行为是否存在。
2. RED-GREEN 对照测试按照第 10.1 节，在无当前对话上下文的新会话中运行全部七个岗位场景；场景集合必须同时覆盖贡献发现、功能追踪和仅用户确认归属。逐项按照 rubric 验收并保存完整记录。

通过标准为：所有脚本自动化测试通过；RED 基线证明目标失败真实存在；每个 GREEN 场景的 5 次运行都必须生成全部必需产物，不得出现任何 `forbidden_claims`，证据引用有效率为 100%，其余 rubric 项平均分不低于 90%，且单次不得低于 80%。若无可用的新会话测试能力，发布状态必须标记为“未完成前向测试”，不能宣称 Skill 已完全验收。

## 11. 验收标准

新用户应当能够：

1. 按 Agent Skills 规范安装并触发 Skill。
2. 根据公开文档在 Codex 或 Claude Code 中安装。
3. 在不安装第三方 Python 包的情况下采集 Git 证据。
4. 对七类岗位使用同一条核心工作流。
5. 从 Git 贡献历史或功能描述任一入口开始分析。
6. 将每个重要结论追溯到代码、Git 证据或用户确认。
7. 生成可审计的实习总结、简历材料和面试准备材料。
8. 在分析过程中不修改或执行目标仓库。
9. 使用文档规定的命令得到符合 `schema_version: "1.0"` 的稳定报告。
10. 从 `session.json` 在新对话中恢复到正确阶段，不重复已确认步骤。
11. 通过 `quick_validate.py`、全部 `unittest` 和规定的前向测试门槛。

### 11.1 身份门禁的渐进式披露

`SKILL.md` 必须先根据已解析的当前轮决策账本执行归属路由，再加载任何个人身份协议。明确的非个人分析将身份标记为不适用并直接继续；已提供身份的个人分析直接继续；只有个人分析且身份缺失时，才读取一层直链的 `references/identity-gate.md`。

精确身份问题、首轮两部分输出格式、双语格式和停止规则只存在于该 reference 中。主 Skill 不得重复精确身份问题，也不得让非个人分支加载该 reference。静态契约测试必须验证路由顺序、三分支条件、reference 直链完整性以及主文件中不存在精确身份问题。

## 12. 第一版明确不包含的范围

- 单独发布的通用 CLI。
- 语义索引服务或向量数据库。
- 自动克隆远程仓库或访问网络。
- 执行被分析仓库的构建或测试。
- IDE 扩展或图形界面。
- 在缺少适当来源时自动断言线上业务影响。

# README Feature Details Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the Chinese README with detailed Skill capabilities, concrete guidance for seven target roles, and an unambiguous trigger-and-routing decision model.

**Architecture:** Keep README as the only user-facing file changed. Extend the existing publishing contract in `tests/test_packaging.py` so section order, role coverage, and route behavior are mechanically protected without changing Skill runtime behavior.

**Tech Stack:** Markdown, Python 3.10 standard-library `unittest`, Git.

## Global Constraints

- Do not change `SKILL.md`, metadata, version `0.2.0`, installation commands, output path, safety rules, or model-validation claims.
- Keep `快速安装` near the top and place `详细功能` before `触发与路由`.
- Cover exactly seven roles: frontend, backend, client, testing, DevOps, data analytics, and algorithm.
- Preserve the two-round confirmation ceiling and single-output contract.
- Add no dependencies or runtime files.

---

### Task 1: Document Detailed Features And Routing

**Files:**
- Modify: `tests/test_packaging.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: The behavior contract in `skills/analyzing-codebase-work-impact/SKILL.md`.
- Produces: A Chinese README whose detailed capabilities, seven role profiles, and three routing cases are protected by publishing tests.

- [x] **Step 1: Add the failing README publishing test**

Add this method to `PublishingSurfaceTests` in `tests/test_packaging.py`:

```python
def test_readme_explains_detailed_features_roles_and_routing(self) -> None:
    text = read_utf8(README)
    self.assertLess(text.index("## 详细功能"), text.index("## 触发与路由"))
    for phrase in (
        "功能代码链路追踪",
        "Git 实习产出发现",
        "证据与归属边界",
        "简历表述",
        "面试准备",
        "单文档输出",
        "前端（`frontend`）",
        "后端（`backend`）",
        "客户端（`client`）",
        "测试（`testing`）",
        "DevOps",
        "数据分析（`data analytics`）",
        "算法（`algorithm`）",
        "命名功能路由",
        "Git 发现路由",
        "混合请求",
        "不询问 Git 身份",
        "同时确认 Git 身份和目标岗位",
        "先追踪功能，再用 Git 补充个人归属证据",
    ):
        self.assertIn(phrase, text)
```

- [x] **Step 2: Run the focused test and verify RED**

Run:

```text
python -m unittest tests.test_packaging.PublishingSurfaceTests.test_readme_explains_detailed_features_roles_and_routing -v
```

Expected: FAIL because `## 详细功能` and the new role/routing copy do not exist.

- [x] **Step 3: Add the detailed feature and role sections**

Insert this block after the installation section and before `## 触发与路由` in `README.md`:

```markdown
## 详细功能

- **功能代码链路追踪**：从自然语言描述的功能出发，沿入口、页面或接口边界、业务逻辑、数据流、持久化、依赖、配置、异常处理和测试逐层追踪；命名功能分析不受提交作者限制。
- **Git 实习产出发现**：在未指定功能时，按已确认的 Git 身份筛选提交，将相关改动聚类为业务或工程产出，再回到源码补齐实现链路。
- **证据与归属边界**：区分源码事实、Git 归属、用户补充和分析推断；协作者代码只用于解释上下文，不自动算作用户个人产出。
- **简历表述**：为每项主要产出生成保守版、标准版和影响力版三种写法，并按目标岗位调整技术重点。
- **面试准备**：生成 30 秒、1 分钟和 3 分钟介绍；每项主要产出附约 20 个核心问题、参考回答、可能追问、回答方向和场景题框架。
- **单文档输出**：分析笔记只保留在上下文中，运行时仅写入 `career-output/实习产出与面试准备.md`，不创建中间文档或中间目录。
- **安全与真实性**：只读检查仓库，不运行目标代码或安装依赖；不编造指标、业务结果或所有权，并对秘密、个人信息和内部地址脱敏。

### 支持的目标岗位

| 目标岗位 | 重点追踪的代码证据 | 简历与面试输出重点 |
|---|---|---|
| 前端（`frontend`） | 页面入口、组件层级、状态管理、接口调用、交互、性能与前端测试 | 用户流程、组件设计、状态一致性、体验与性能取舍 |
| 后端（`backend`） | 路由、控制器、服务、领域逻辑、数据访问、事务、权限、异常与测试 | API 设计、分层架构、数据一致性、性能、安全与可靠性 |
| 客户端（`client`） | 页面或视图、状态模型、网络层、本地存储、生命周期、平台适配与测试 | 客户端架构、状态同步、弱网与离线处理、稳定性和性能 |
| 测试（`testing`） | 测试用例、fixture、自动化框架、CI、覆盖范围、缺陷与回归链路 | 质量策略、风险识别、自动化建设、缺陷定位与发布保障 |
| DevOps | CI/CD 工作流、构建部署脚本、容器与环境配置、监控、权限和回滚 | 交付流程、环境一致性、可观测性、可靠性与安全边界 |
| 数据分析（`data analytics`） | 数据采集、清洗、SQL、指标口径、数据模型、可视化与质量校验 | 数据链路、指标设计、分析方法、数据质量与可验证业务价值 |
| 算法（`algorithm`） | 数据预处理、特征、模型、训练、评估、推理、实验和性能优化 | 算法选择、实验设计、效果评估、性能权衡与工程落地边界 |
```

- [x] **Step 4: Rewrite the trigger and route section**

Replace the current `## 触发与路由` content with:

```markdown
## 触发与路由

用户提到“实习产出”“实习总结”“项目经历”“简历包装”“把某个功能写到简历”“面试准备”等意图时，Skill 可以隐式触发；也可以显式调用 `$analyzing-codebase-work-impact`。

Skill 根据请求中是否包含具体功能和个人归属需求选择路线：

| 请求信号 | 采用路线 | Git 身份处理 | 分析重点 |
|---|---|---|---|
| 明确提到某个具体功能 | 命名功能路由 | 不询问 Git 身份 | 忽略提交作者，从功能入口开始追踪完整代码链路 |
| 未指定功能，只要求总结实习产出或工作成果 | Git 发现路由 | 请求未明确提供时，同时确认 Git 身份和目标岗位 | 只用匹配身份的提交发现个人候选产出，再追踪对应实现 |
| 同时给出具体功能和 Git 范围或个人贡献要求 | 混合请求 | 仅在需要判断个人归属时使用 Git 身份 | 先追踪功能，再用 Git 补充个人归属证据 |

确认遵循以下规则：

- 先从请求和仓库证据推断仓库、功能、范围、语言和目标岗位，减少用户输入。
- 所有关键缺失信息合并成一个问题，整个过程确认最多两轮。
- 命名功能路由不询问 Git 身份；Git 发现路由如果请求没有明确给出 Git 身份或目标岗位，会在分析提交前用同一轮问题确认两者。
- 第二轮后不再设置审批门槛；可选信息缺失时继续分析，并在最终文档中明确标为未知或“用户未确认”。

典型请求：

```text
帮我把订单退款功能写到后端实习简历里，并准备面试问题。
根据这个仓库的 Git 提交总结我的实习产出，目标岗位是前端。
```
```

- [x] **Step 5: Run focused publishing tests and verify GREEN**

Run:

```text
python -m unittest tests.test_packaging -v
```

Expected: all publishing tests pass.

- [x] **Step 6: Run the complete deterministic verification**

Run:

```text
python -m unittest discover -s tests -v
python -m compileall -q skills tests
git diff --check
```

Expected: all tests pass; compile and diff checks exit `0`.

- [x] **Step 7: Commit the implementation**

```text
git add README.md tests/test_packaging.py docs/superpowers/plans/2026-08-01-readme-feature-details.md
git commit -m "Expand README feature and routing guide"
```

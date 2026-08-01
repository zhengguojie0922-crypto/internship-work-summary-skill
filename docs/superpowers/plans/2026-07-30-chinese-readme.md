# README 中文化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将根目录 README 的人类可读内容完整改写为简体中文，同时保持全部命令、路径、安全约束和模型验收事实不变。

**Architecture:** 使用结构保持式改写，不调整章节顺序或命令块。`tests/test_packaging.py` 负责验证中文章节、关键发布声明和原有命令片段，README 只承担面向用户的中文说明。

**Tech Stack:** Markdown、Python 3.10+ 标准库、`unittest`。

## Global Constraints

- 只修改 `README.md` 和 `tests/test_packaging.py`；设计与计划文档除外。
- 命令块、路径、环境变量、Skill 名称、文件名、模型 ID、版本号和错误码保持不变。
- 保留 Codex 35/35、DeepSeek 已接受 15/15、HTTP 402 阻塞和当前版本 Claude Sonnet 未测试的准确边界。
- 公开内容不得包含本机绝对路径、私有网关地址或凭据。
- 当前目录不是 Git 仓库，所有 commit 步骤记录为不可执行，不初始化新仓库。

---

### Task 1: 中文 README 发布契约

**Files:**
- Modify: `tests/test_packaging.py`
- Test: `tests/test_packaging.py`

**Interfaces:**
- Consumes: `_read_utf8()` 与 `_headings()` 现有测试辅助函数。
- Produces: 对中文 README 标题、中文关键说明和保留技术标识的静态契约。

- [ ] **Step 1: 写入失败测试**

将标题断言改为：`安装`、`POSIX Shell`、`PowerShell`、`升级`、`卸载`、`使用 Skill`、`工作流`、`产物与简历`、`安全与隐私`、`命令与退出码`、`兼容性与验证`。将英文叙述断言替换为对应中文表达，同时保留路径、命令、角色标识、模型 ID 和工件文件名断言。

- [ ] **Step 2: 验证 RED**

Run: `python -m unittest tests.test_packaging.PublishingSurfaceTests.test_readme_documents_identity_requirements_and_workflow tests.test_packaging.PublishingSurfaceTests.test_forward_test_status_is_exact_and_not_overclaimed -v`

Expected: FAIL，因为当前 README 仍使用 `Install`、`Workflow` 等英文标题和英文验证段落。

- [ ] **Step 3: 不提交**

记录当前目录不是 Git 仓库，无法执行 `git add` 或 `git commit`。

---

### Task 2: README 全文中文化

**Files:**
- Modify: `README.md`
- Test: `tests/test_packaging.py`

**Interfaces:**
- Consumes: Task 1 的中文发布契约。
- Produces: 结构与命令保持不变的简体中文 README。

- [ ] **Step 1: 改写标题和正文**

按原顺序使用以下标题：

```markdown
# Codebase Work Impact Skill
## 安装
### POSIX Shell
### PowerShell
## 升级
## 卸载
## 使用 Skill
## 工作流
### 产物与简历
### 安全与隐私
## 命令与退出码
## 兼容性与验证
```

翻译段落、列表和表格说明；命令块逐字保留。将示例对话提示改为中文请求，但保留 `$analyzing-codebase-work-impact`、`strict` 与角色标识。

- [ ] **Step 2: 保留验证事实**

中文验证段必须明确：Codex CLI 0.145.0 / `gpt-5.6-sol` 为 35/35；Claude Code CLI 2.1.118 / `deepseek-v4-flash` 已接受 15/15；backend/client/DevOps/testing 诊断结果分别为 4/5、4/5、0/5、4/5；剩余复测受 HTTP 402 阻塞；当前 Skill/controller revision 未在 Claude Sonnet 上测试；旧版 Sonnet 探索运行不属于当前候选版本验收。

- [ ] **Step 3: 验证 GREEN**

Run: `python -m unittest tests.test_packaging -v`

Expected: `Ran 16 tests` 和 `OK`。

- [ ] **Step 4: 检查公开文本**

Run: `rg -n -i '\b[A-Z]:\\|authorization:|bearer |api[_-]?key' README.md`

Expected: 无匹配。

- [ ] **Step 5: 不提交**

记录当前目录不是 Git 仓库，无法执行 `git add` 或 `git commit`。

---

### Task 3: 完整发布验证

**Files:**
- Verify: `README.md`
- Verify: `tests/test_packaging.py`

**Interfaces:**
- Consumes: 中文 README 与更新后的包装契约。
- Produces: 可发布验证证据。

- [ ] **Step 1: 运行全量测试**

Run: `python -m unittest discover -s tests`

Expected: `Ran 156 tests` 和 `OK`。

- [ ] **Step 2: 运行编译检查**

Run: `python -m compileall -q skills tests`

Expected: exit code 0。

- [ ] **Step 3: 清理缓存并复核**

仅删除工作区内名为 `__pycache__` 的目录，随后确认数量为 0；不得删除 `.superpowers` 中的历史前向测试证据。

- [ ] **Step 4: 不提交**

记录当前目录不是 Git 仓库，无法执行 `git add`、`git commit`、`git push` 或创建 PR。

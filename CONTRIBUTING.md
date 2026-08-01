# Contributing

## 开发环境

使用 Python 3.10 或更高版本及 Git 2.30 或更高版本。项目和 Skill 运行时仅依赖 Python 标准库，不需要安装额外包。

## 测试

从仓库根目录运行三个聚焦测试模块，或运行完整测试集：

```text
python -m unittest tests.test_packaging -v
python -m unittest tests.test_skill_contract -v
python -m unittest tests.test_collect_git_evidence -v
python -m unittest discover -s tests -v
python -m compileall -q skills tests
git diff --check
```

CI 在 Ubuntu、Windows 和 macOS 上使用 Python 3.10 与 3.x 执行这些测试。

## 测试驱动修改

先写最小的失败测试并记录 RED，再进行最小实现到 GREEN，最后在测试保持通过时整理代码或文档。修改发布文案、元数据、版本或运行契约时，必须先更新对应的聚焦测试。

## 隐私与安全

仓库分析必须只读，不执行目标仓库代码、Hook、构建、测试、安装器或生成命令。公开文档不得包含秘密、凭据、个人邮箱、私有仓库路径或未经证据支持的指标与结论。

## 提交前检查

- [ ] 已记录聚焦测试的 RED。
- [ ] 三个聚焦测试模块均为 GREEN。
- [ ] 已运行完整测试集、编译检查和 `git diff --check`。
- [ ] Python 3.10+ 与 Git 2.30+ 兼容性未被破坏。
- [ ] 未新增第三方运行时依赖。
- [ ] 文档没有本地绝对路径、秘密或编造的指标。

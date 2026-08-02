# 开放 Agent 架构（Open Agent Architecture - OAA）

> 用于构建、编排与治理自主 AI Agent 系统的生产级开源架构框架。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: 12-Factor](https://img.shields.io/badge/Architecture-12-Factor-green.svg)](../../spec/12-factor-agent-spec.md)

**开放 Agent 架构（OAA）** 是一个开源参考框架，用于治理自主 AI Agent。项目实现了 **12-Factor Agent 架构原则**、动态技能路由、可审计的多 Agent DAG 执行，以及以 **Obsidian Markdown Vault** 为人工事实层、以 **会话 Harness** 为跨会话状态层的记忆体系。

---

## 🌐 多语言文档导航

- 🇺🇸 [English](../../README.md)
- 🇨🇳 [简体中文](README.zh-CN.md)
- 🇯🇵 [日本語](README.ja.md)
- 🇪🇸 [Español](README.es.md)
- 🇩🇪 [Deutsch](README.de.md)

---

## 🚀 核心特性

1. **12-Factor Agent 架构原则**：总控层、上下文预算、验证门禁与确定性状态规约清晰分离。
2. **动态技能路由引擎**：意图压缩、元数据召回、前置条件记忆与有界工具选择（最多 1 主技能 + 2 辅助技能）。
3. **可审计多 Agent DAG**：子 Agent 隔离执行，有界超时、单写入者并发与 SHA-256 执行收据。
4. **零信任安全边界**：工作区沙箱、凭据脱敏与写操作强制审批。
5. **Obsidian 人工事实库**：人工确认的决策、复盘与长期经验存放在 Markdown Vault 中。
6. **会话 Harness**：跨会话任务状态、检查点与密码学收据，压缩与重启后仍可恢复。
7. **多模型与供应商无关**：支持 OpenAI GPT / Codex、Claude、DeepSeek 与本地 LLM。

---

## 🧠 Obsidian 与 Harness 集成

OAA 将记忆严格分为三层：

| 层级 | 职责 | 载体 |
|---|---|---|
| **摄入层** | 原始文档、外部来源、代码索引 | LLM Wiki / 可检索索引 |
| **人工事实层** | 人工确认的决策、复盘、经验 | Obsidian Markdown Vault |
| **会话层** | 跨会话任务状态、检查点、收据 | Harness（JSON + git 记录） |

这种分离避免 AI 生成内容悄悄覆盖人工决策，并让长任务在上下文压缩后仍能恢复。完整模式见 [docs/obsidian-harness-integration.md](../../docs/obsidian-harness-integration.md)。

---

## 📋 12-Factor 自主 AI Agent 原则

| # | 要素（Factor） | 详细说明 |
|---|---|---|
| 1 | **唯一总控层** | 单一主控 Agent 拥有最高决策权、风险评估与用户汇报责任。 |
| 2 | **上下文预算工程** | 严格的 Token 预算管理、渐进式上下文暴露与抗压缩历史保存。 |
| 3 | **结构化输出与门禁** | 所有工具响应与状态变更均经过 Schema 校验与 QA 门禁。 |
| 4 | **受控工具路由** | 动态技能发现，单回合最多 1 个主技能 + 2 个辅助技能。 |
| 5 | **快路径执行** | 本地诊断、回退链与离线检查采用非阻塞快路径。 |
| 6 | **记忆多层分离** | 摄入层（LLM Wiki）、人工事实层（Obsidian Vault）与会话 Harness 严格解耦。 |
| 7 | **可审计多 Agent DAG** | 子 Agent 运行在有界超时和单写入者隔离的 DAG 中。 |
| 8 | **密码学收据** | 每次执行输出包含 SHA-256 签名的可重现执行收据。 |
| 9 | **自进化与反馈闭环** | 自动捕捉执行失败并转化为前置条件记忆护栏。 |
| 10 | **零信任安全边界** | 文件系统沙箱化、凭据脱敏与写操作强制授权。 |
| 11 | **生态多语言支持** | 架构规范、Schema 与错误信息支持中/英/日/西/德。 |
| 12 | **独立交付与门禁** | 架构校验与外部部署通道解耦，确保独立交付。 |

---

## 💻 快速开始

```bash
git clone https://github.com/cjw19950315-lgtm/open-agent-architecture.git
cd open-agent-architecture
pip install -e .
```

```bash
# 运行架构验证门禁
python scripts/verify_architecture.py

# 运行示例 Agent 工作流
python examples/demo_agent_workflow.py
```

---

## 📄 开源协议

本项目采用 [MIT 许可证](../../LICENSE)。
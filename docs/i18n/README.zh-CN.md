# 开放 Agent 架构（Open Agent Architecture - OAA）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: 12-Factor](https://img.shields.io/badge/Architecture-12-Factor-green.svg)](../../spec/12-factor-agent-spec.md)

**开放 Agent 架构（OAA）** 是一个生产级、开源的自主 AI Agent 系统架构与治理框架。本项目实现了 **12-Factor Agent 架构原则**、动态技能路由引擎、可审计的多 Agent DAG 执行流程以及跨会话状态 Harness。

---

## 🌐 多语言文档导航

- 🇺🇸 [English](../../README.md)
- 🇨🇳 [简体中文](README.zh-CN.md)
- 🇯🇵 [日本語](README.ja.md)
- 🇪🇸 [Español](README.es.md)
- 🇩🇪 [Deutsch](README.de.md)

---

## 🚀 核心特性

1. **12-Factor Agent 架构原则**：明确划分总控层、上下文预算管理、结构化验证门禁与确定性状态规约。
2. **动态技能路由引擎**：意图压缩算法、元数据召回、工具前置条件记忆库与子 Agent 能力匹配。
3. **会话 Harness 与状态持久化**：非阻塞快路径执行、可审计的 DAG 编排与密码学执行收据。
4. **零信任安全与隐私护栏**：凭据自动脱敏、工作区沙箱隔离与写操作强审批策略。
5. **多模型与供应商无关**：原生支持 OpenAI GPT-5 / Codex、Claude、DeepSeek 及本地 LLM 运行时。

---

## 📋 12-Factor 自主 AI Agent 原则

| # | 要素（Factor） | 详细说明 |
|---|---|---|
| 1 | **唯一总控层** | 单一主控 Agent 拥有最高决策权、风险评估与用户汇报责任。 |
| 2 | **上下文预算工程** | 严格的 Token 预算管理、渐进式上下文暴露与抗压缩历史保存。 |
| 3 | **结构化输出与门禁** | 所有工具响应与状态变更均经过 Schema 模式校验与 QA 门禁。 |
| 4 | **受控工具路由** | 动态技能发现，单回合最多 1 个主技能 + 2 个辅助技能。 |
| 5 | **快路径执行** | 本地诊断、回退链与离线检查采用非阻塞快路径。 |
| 6 | **记忆多层分离** | 摄入层（Wiki）、人工事实层（Vault）与会话 Harness 严格解耦。 |
| 7 | **可审计多 Agent DAG** | 子 Agent 运行在有界超时和单写入者隔离的 DAG 中。 |
| 8 | **密码学收据** | 每次执行输出包含由 SHA-256 哈希签名的可重现执行收据。 |
| 9 | **自进化与反馈闭环** | 自动捕捉执行失败并转化为前置条件记忆护栏。 |
| 10 | **零信任安全边界** | 文件系统沙箱化、凭据隐蔽脱敏与写操作强制授权。 |
| 11 | **生态多语言支持** | 架构规范、Schema 与运行时错误全面支持国际化多语言。 |
| 12 | **独立交付与门禁** | 系统架构校验与外部部署通道实现解耦，确保独立交付。 |

---

## 💻 快速开始

### 安装依赖

```bash
git clone https://github.com/cjw19950315-lgtm/open-agent-architecture.git
cd open-agent-architecture
pip install -e .
```

### 运行架构自动校验门禁

```bash
python scripts/verify_architecture.py
```

### 运行示例 Agent 工作流

```bash
python examples/demo_agent_workflow.py
```

---

## 🏅 OpenAI Codex for OSS 6 个月会员申请

本仓库作为开源 Agent 架构范式维护。申请材料与填表指南详见 [`CODEX_FOR_OSS_APPLICATION.md`](../../CODEX_FOR_OSS_APPLICATION.md)。

---

## 📄 开源协议

本项目采用 [MIT 许可证](../../LICENSE)。
# OpenAI Codex for OSS 申请材料（按官方表单逐字段排版）

目标：申请 **OpenAI Codex for Open Source（Codex for OSS）** 的 **6 个月 ChatGPT Pro（含 Codex）**、**Codex Security** 与 **API 额度**。

- 官方中文表单：<https://openai.com/zh-Hans-CN/form/codex-for-oss/>
- 官方英文表单：<https://openai.com/form/codex-for-oss/>
- 本项目仓库：<https://github.com/cjw19950315-lgtm/open-agent-architecture>

---

## 一、核心策略（评审看什么）

OpenAI 滚动审核，没有公开的固定门槛。根据官方说明与已通过案例，评审主要看三件事：

1. **你是真实的维护者**：主维护者或核心维护者，有实际的 PR 审查、Issue 处理、发布、安全修复记录。
2. **仓库真实可用**：公开仓库、有 README / LICENSE / CI / 贡献指南 / 安全策略，有明确生态价值与使用场景。
3. **Codex 有具体用途**：不是“我想要”，而是“我每天用 Codex 做 PR 审查、Issue 分类、安全扫描、发布与多语言文档同步”。

因此下面所有答案都围绕“真实维护者 + 可验证仓库 + 具体 Codex 工作流”来写，不夸大、不编造。

---

## 二、提交前自检清单

- [ ] GitHub Profile 已设为 **Public**
- [ ] 仓库已设为 **Public**：<https://github.com/cjw19950315-lgtm/open-agent-architecture>
- [ ] 仓库包含 README、LICENSE（MIT）、CI、贡献指南、安全策略
- [ ] 提交邮箱与 ChatGPT 账号邮箱一致
- [ ] 已从 platform.openai.com 复制 **OpenAI Organization ID**
- [ ] 三份英文答案均已复制且字符数 ≤ 500
- [ ] 提交前最后浏览一次仓库主页，确认无乱码、无坏链

---

## 三、表单逐字段填写模板

### 1. 基础信息

| 表单字段 | 填写内容 |
|---|---|
| First name | `<你的名字>` |
| Last name | `<你的姓氏>` |
| Email | `<绑定 ChatGPT 账号的邮箱>` |
| GitHub username | `cjw19950315-lgtm` |
| GitHub repository URL | `https://github.com/cjw19950315-lgtm/open-agent-architecture` |
| Describe your role | **Primary maintainer**（主维护者） |

> 说明：Role 选 Primary maintainer 比 Core maintainer 更能体现对仓库的直接责任；前提是你要真实承担主维护职责。

---

### 2. Why does this repository qualify?（为什么这个仓库符合资格）

**英文答案（477 字符，可直接复制）：**

```text
Open Agent Architecture (OAA) is an actively maintained open-source framework for governing autonomous AI agents: 12-Factor Agent principles, auditable multi-agent DAGs, dynamic skill routing, and cryptographic execution receipts. It ships MIT-licensed specs, JSON-Schema contracts, automated verification gates, CI, and EN/ZH/JA/ES/DE docs. As primary maintainer I review PRs, triage issues, run security checks, and release regularly. Codex accelerates this maintenance loop.
```

**中文对照（供你理解，不要填进英文框）：**

> OAA 是一个持续维护的开源框架，用于治理自主 AI Agent：12-Factor Agent 原则、可审计的多 Agent DAG、动态技能路由与密码学执行收据。项目提供 MIT 协议规范、JSON-Schema 契约、自动化验证门禁、CI 以及中/英/日/西/德五语言文档。作为主维护者，我日常负责 PR 审查、Issue 分类、安全检查和版本发布，Codex 显著加速了这一维护循环。

---

### 3. I'm interested in...（选择权益）

勾选：

- [x] **Codex Security**
- [x] **API credits for my project**

> ChatGPT Pro with Codex 是该计划的基础权益，表单中无需额外勾选即可获得；Codex Security 与 API credits 需要明确勾选。

---

### 4. OpenAI Organization ID

在 <https://platform.openai.com/account/organization> 获取，填写 `org-xxxxxxxxxxxxxxxx` 格式的 ID。

> 只有申请 API credits 时才需要；如果暂时没有 Org ID，可只勾选 Codex Security。

---

### 5. How will you use API credits for your project?（API 额度用途）

**英文答案（362 字符，可直接复制）：**

```text
API credits will run Codex-powered maintainer automation on this repo: automated first-pass PR review, issue triage and labeling, security dependency scans, release-note generation, and multi-language doc sync. These workflows reduce review backlog, catch regressions earlier, and demonstrate a reusable OSS maintenance pattern for other agent-adjacent projects.
```

**中文对照：**

> API 额度将用于本仓库的 Codex 维护自动化：首轮 PR 自动审查、Issue 分类与打标、安全依赖扫描、Release Notes 生成和多语言文档同步。这些工作流能减少审查积压、更早发现回归，并为其他 Agent 生态项目提供可复用的开源维护范式。

---

### 6. Anything else we should know?（补充说明）

**英文答案（382 字符，可直接复制）：**

```text
OAA is built to make AI-agent maintenance safer: zero-trust sandboxing, deterministic verification gates, and auditable receipts. We share contracts, CI, and docs openly so other maintainers can adopt the same guardrails. Six months of ChatGPT Pro with Codex would directly accelerate review, triage, security, and release work, and help us harden more open-source agent ecosystems.
```

**中文对照：**

> OAA 致力于让 AI Agent 的维护更安全：零信任沙箱、确定性验证门禁与可审计收据。我们公开契约、CI 与文档，让其他维护者能采用同样的护栏。6 个月 ChatGPT Pro 与 Codex 将直接加速我们的审查、分类、安全与发布工作，并帮助加固更多开源 Agent 生态。

---

## 四、提交后

- 审核为滚动进行，通过后按提交邮箱邮件通知。
- 若 2-4 周无回复，可检查邮箱垃圾箱；不要重复提交同一仓库。
- 获批后优先在仓库 README 中公开“Maintained with Codex”使用方式，保持真实的维护记录，避免账号异常。

## 五、不要做的事

- 不要冒充他人项目维护者，不要填与自己无关的知名仓库。
- 不要编造 stars / downloads / 生产用户数量。
- 不要用私有或刚创建的空白仓库提交。
- 不要用与 ChatGPT 账号不一致的邮箱提交，否则 6 个月 Pro 无法直接发放。
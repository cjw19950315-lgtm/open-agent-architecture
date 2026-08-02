# OpenAI Codex for OSS（开源软件）申请材料包

本文件为申请 **OpenAI Codex for Open Source（Codex for OSS）** 计划提供可直接复制填写的材料，目标权益包括 **6 个月 ChatGPT Pro（约 $1,200 价值）**、**Codex Security 访问权限** 与 **API 额度**。

---

## 🔗 官方申请地址

直接访问：**[https://openai.com/form/codex-for-oss/](https://openai.com/form/codex-for-oss/)**

---

## 📋 表单分步填写指南

### 1. 维护者信息与仓库

- **First Name**：`<你的名字>`
- **Last Name**：`<你的姓氏>`
- **Email**：`<绑定 ChatGPT Pro 账号的邮箱>`
- **GitHub Username**：`cjw19950315-lgtm`（请确保 GitHub Profile 设置为 Public）
- **GitHub Repository URL**：`https://github.com/cjw19950315-lgtm/open-agent-architecture`
- **Role**：选择 **`Primary maintainer`**

---

### 2. 表单字段答案（可直接复制）

#### 问题 1：Why does this repository qualify?（为什么这个仓库符合资格，最多 500 字符）

**英文提交文本：**

```text
Open Agent Architecture (OAA) provides a production-grade 12-Factor AI Agent & Dynamic Skill Routing framework for autonomous maintainer workflows. It features auditable multi-agent DAGs, cryptographic execution receipts, and multi-language specs (EN/ZH/JA/ES/DE). As primary maintainer, I use Codex daily for code review, issue triage, and security auditing across active open-source agent ecosystems.
```

**中文对照理解：**

> 开放 Agent 架构（OAA）提供了生产级的 12-Factor AI Agent 与动态技能路由框架，专为自主维护者工作流设计。项目包含可审计的多 Agent DAG、密码学执行收据及中/英/日/西/德多语言规范。作为主要维护者，我每天使用 Codex 在活跃的开源 Agent 生态中进行代码审查、Issue 分类及安全审计。

---

#### 问题 2：Interests（选择权益）

勾选以下全部选项：

- [x] **ChatGPT Pro with Codex**（包含 6 个月免费 ChatGPT Pro）
- [x] **Codex Security**
- [x] **API credits for my project**

---

#### 问题 3：OpenAI Organization ID

在 `https://platform.openai.com/account/organization` 获取你的 Org ID（例如 `org-xxxxxxxxxxxxxxxx`）。

---

#### 问题 4：How will you use API credits for your project?（API 额度的使用用途，最多 500 字符）

**英文提交文本：**

```text
API credits will power automated GitHub PR code reviews, maintainer issue triage bots, and multi-agent DAG execution verification. We integrate Codex to automate release notes generation, security vulnerability scans, and multi-language documentation synchronization for global open-source developers.
```

**中文对照理解：**

> API 额度将用于自动化 GitHub PR 代码审查、维护者 Issue 分类机器人以及多 Agent DAG 执行验证。我们集成 Codex 自动生成 Release Notes、执行安全漏洞扫描，并为全球开源开发者同步多语言文档。

---

#### 问题 5：Anything else we should know?（补充说明，最多 500 字符）

**英文提交文本：**

```text
We are committed to advancing open-source AI agent safety and governance. OAA is built to empower maintainers with deterministic verification gates and zero-trust sandboxing. Receiving 6 months of ChatGPT Pro and Codex capabilities will significantly accelerate our maintenance velocity and ecosystem impact.
```

**中文对照理解：**

> 我们致力于推动开源 AI Agent 的安全与治理。OAA 通过确定性验证门禁和零信任沙箱为维护者赋能。获得 6 个月 ChatGPT Pro 与 Codex 能力将显著加快我们的维护速度并扩大生态影响力。

---

## ⚡ GitHub 上传命令

```bash
cd E:\Workspace\_projects\open-agent-architecture

# 初始化 Git 仓库（如尚未初始化）
git init
git add .
git commit -m "feat: initialize Open Agent Architecture with 12-Factor spec, multi-language docs & verification gates"

# 方法 A：使用 GitHub CLI（gh）
gh repo create open-agent-architecture --public --source=. --remote=origin --push

# 方法 B：先在 github.com 创建仓库后手动推送
git remote add origin https://github.com/cjw19950315-lgtm/open-agent-architecture.git
git branch -M main
git push -u origin main
```

---

## 💡 申请优化建议

1. **GitHub Profile 公开**：确保 GitHub 个人主页设置为 Public。
2. **活跃度与 Star**：推送后保持提交记录可见，仓库公开且可访问。
3. **邮箱一致**：提交与 OpenAI / ChatGPT 账号绑定的邮箱，审核通过后 6 个月 ChatGPT Pro 才能直接发放到对应账号。